import unittest
from fec_api_wrapper import FECAPIWrapper


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = FECAPIWrapper(api_key="DEMO_KEY")

    def test_candidate(self):
        res = self.api_wrapper.search("Richard Blumenthal", "candidates")
        self.assertIsInstance(res, list, "Search did not return list")
        self.assertGreaterEqual(len(res), 1, "Search results does not contain anything")
        self.assertIsInstance(res[0], dict, "Search result list does not contain dicts")
        self.assertEqual(
            set(res[0].keys()),
            {"id", "name", "office_sought"},
            "Search results element keys not as expected",
        )

    def test_candidates(self):
        res = self.api_wrapper.search(
            ["Richard Blumenthal", "Chris Murphy"], "candidates"
        )
        self.assertIsInstance(res, list, "Search did not return list")
        self.assertGreaterEqual(
            len(res), 2, "Search results does not contain at least 2 results"
        )
        self.assertIsInstance(res[0], dict, "Search result list does not contain dicts")
        self.assertEqual(
            set(res[0].keys()),
            {"id", "name", "office_sought"},
            "Search results element keys not as expected",
        )

    def test_committee(self):
        res = self.api_wrapper.search("justice", "committees")
        self.assertIsInstance(res, list, "Search did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Search results does not contain at least 1 results"
        )
        self.assertIsInstance(res[0], dict, "Search result list does not contain dicts")
        self.assertEqual(
            set(res[0].keys()),
            {"id", "name", "is_active"},
            "Search results element keys not as expected",
        )

    def test_committees(self):
        res = self.api_wrapper.search(["justice", "peace"], "committees")
        self.assertIsInstance(res, list, "Search did not return list")
        self.assertGreaterEqual(
            len(res), 2, "Search results does not contain at least 2 results"
        )
        self.assertIsInstance(res[0], dict, "Search result list does not contain dicts")
        self.assertEqual(
            set(res[0].keys()),
            {"id", "name", "is_active"},
            "Search results element keys not as expected",
        )


class TestCandidate(unittest.TestCase):
    def setUp(self) -> None:
        # self.api_wrapper = FECAPIWrapper(api_key="DEMO_KEY")
        self.api_wrapper = FECAPIWrapper(api_key=API_KEY)

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
