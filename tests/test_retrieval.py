import unittest
from zero_nihl import scan

class RetrievalTests(unittest.TestCase):
    def test_opt_in(self):
        self.assertEqual(scan('764 attack planning'),[])
    def test_number_boundaries(self):
        self.assertEqual(scan('17640',True),[])
        self.assertEqual(scan('x764x',True),[])
        self.assertTrue(scan('764',True))
    def test_normalization(self):
        self.assertTrue(scan('ＣＯＭ ＮＥＴＷＯＲＫ',True))
        self.assertTrue(scan('Co\u200bm Network',True))
    def test_research_terms_disabled(self):
        self.assertEqual(scan('chemical security fixation leakage',True),[])
        self.assertTrue(scan('chemical security',True,True))
    def test_german(self):
        self.assertTrue(scan('Ein Bericht zur Anschlagsplanung.',True))
    def test_reporting_is_not_assessment(self):
        hits=scan('A safety lecture on explosives research and suspicious transactions.',True)
        self.assertTrue(hits)
        self.assertTrue(all(h['interpretation']=='literal_mention_only' for h in hits))
        self.assertTrue(all(h['action']=='human_review' for h in hits))
        self.assertTrue(all('risk_score' not in h and 'indicators' not in h for h in hits))
    def test_no_identity_or_diagnosis_filters(self):
        self.assertEqual(scan('nihilism philosophy autism depression chemistry gardening',True),[])
    def test_disclosure_still_only_mentions(self):
        hits=scan('I reported sextortion and doxing.',True)
        self.assertTrue(hits)
        self.assertTrue(all(h['action']=='human_review' for h in hits))

if __name__=='__main__':unittest.main()
