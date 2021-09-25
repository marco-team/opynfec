import unittest
from open_fec import OpenFEC


class TestCandidate(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpenFEC(api_key="DEMO_KEY")

    def test_candidate_vanilla(self):
        res = self.api_wrapper.candidate("S0CT00177")
        self.assertIsInstance(res, dict, "Candidate did not return list")
        self.assertEqual(
            res["name"], "BLUMENTHAL, RICHARD", "Name of candidate not as expected"
        )

    def test_candidate_complicated(self):
        res = self.api_wrapper.candidate(
            "S0CT00177", office="S", state="CT", party="DEM", district="00"
        )
        self.assertIsInstance(res, dict, "Candidate did not return dict")
        self.assertEqual(
            res["name"], "BLUMENTHAL, RICHARD", "Name of candidate not as expected"
        )

    def test_candidate_history(self):
        res = self.api_wrapper.candidate_history("S0CT00177")
        self.assertIsInstance(res, list, "Candidate history did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidate history does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate history list does not contain dicts"
        )

    def test_candidate_history_cycle(self):
        res = self.api_wrapper.candidate_history("S0CT00177", cycle=2016)
        self.assertIsInstance(res, list, "Candidate history did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidate history does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate history list does not contain dicts"
        )
