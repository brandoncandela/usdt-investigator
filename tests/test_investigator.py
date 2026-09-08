import copy, json, unittest
from decimal import Decimal
from investigator import CONTRACT, TRANSFER, ROOT, decode, explore, load_case

class EvidenceTests(unittest.TestCase):
    def setUp(self):
        record=json.loads(next((ROOT/'data/raw').glob('logs-*')).read_text())
        self.log=record['response']['result'][0]
    def test_exact_large_amount(self):
        log=copy.deepcopy(self.log);units=2**200+123456
        log['data']='0x'+format(units,'064x')
        self.assertEqual(decode(log)['units'],str(units))
        whole, fraction = divmod(units, 10**6)
        self.assertEqual(decode(log)['amount'], f'{whole}.{fraction:06d}')
    def test_reject_wrong_contract(self):
        log=copy.deepcopy(self.log);log['address']='0x'+'1'*40
        with self.assertRaises(ValueError):decode(log)
    def test_reject_removed(self):
        log=copy.deepcopy(self.log);log['removed']=True
        with self.assertRaises(ValueError):decode(log)
    def test_bad_padding(self):
        log=copy.deepcopy(self.log);log['topics'][1]='0x1'+log['topics'][1][3:]
        with self.assertRaises(ValueError):decode(log)
    def test_case_integrity_and_unique_ids(self):
        case=load_case()
        self.assertEqual(case['window_event_count'],7640)
        self.assertEqual(len(case['nodes']),15)
        self.assertEqual(len(case['events']),len({e['id'] for e in case['events']}))
    def test_bounded_graph_and_zero_filter(self):
        events=[dict(source=a,target=b,units=u) for a,b,u in [('a','b','1'),('b','c','1'),('c','d','1'),('a','z','0')]]
        nodes,edges,omitted=explore(events,'a',hops=2,max_addresses=3)
        self.assertEqual(nodes,{'a':0,'b':1,'c':2});self.assertEqual(len(edges),2)
        nodes,edges,omitted=explore(events,'a',hops=2,max_addresses=2)
        self.assertEqual(omitted,['c'])
    def test_chronological_order(self):
        events=load_case()['events']
        keys=[(e['block'],e['tx_index'],e['log_index']) for e in events]
        self.assertEqual(keys,sorted(keys))
    def test_same_amount_candidate_has_two_distinct_transactions(self):
        es=[e for e in load_case()['events'] if e['amount']=='353.912839']
        self.assertEqual(len(es),2);self.assertEqual(es[0]['target'],es[1]['source'])
        self.assertLess(es[0]['block'],es[1]['block']);self.assertNotEqual(es[0]['tx'],es[1]['tx'])

if __name__=='__main__':unittest.main()
