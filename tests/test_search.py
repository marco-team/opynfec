import unittest
from opyn_fec import OpynFEC


class TestSearch(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpynFEC(api_key="DEMO_KEY")

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
