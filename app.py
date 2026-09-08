"""Run: python3 app.py. Bound to loopback; no third-party dependencies."""
import json, argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from investigator import ROOT, load_case

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        route=self.path.split('?')[0]
        if route in ('/api/case','/case.json'):
            body=json.dumps(load_case()).encode(); mime='application/json'
        elif route in ('/core.mjs','/live.mjs','/ui.mjs'):
            body=(ROOT/'static'/route[1:]).read_bytes(); mime='text/javascript; charset=utf-8'
        elif route in ('/','/index.html'):
            body=(ROOT/'static/index.html').read_bytes(); mime='text/html; charset=utf-8'
        else:
            self.send_error(404); return
        self.send_response(200)
        self.send_header('Content-Type',mime)
        self.send_header('Content-Length',str(len(body)))
        self.send_header('X-Content-Type-Options','nosniff')
        self.end_headers(); self.wfile.write(body)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args(); load_case()
    print(f'Open http://127.0.0.1:{args.port} — Ctrl+C stops the dashboard.',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
