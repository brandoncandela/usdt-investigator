"""Build the public workspace from verified saved evidence."""
import json,shutil
from investigator import ROOT,load_case
from verify import verify
verify()
out=ROOT/'dist';out.mkdir(exist_ok=True)
for p in (ROOT/'static').iterdir():
 if p.is_file():shutil.copy2(p,out/p.name)
case=load_case();(out/'case.json').write_text(json.dumps(case,indent=2)+'\n')
assert json.loads((out/'case.json').read_text())==case
print('Built workspace with verified saved case and bounded live collection.')
