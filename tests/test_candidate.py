import unittest
from open_fec import OpenFEC


class TestCandidate(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpenFEC(api_key="DEMO_KEY")

    def test_candidate_vanilla(self):
        res = self.api_wrapper.candidate("S0CT00177")
        self.assertIsInstance(res, list, "Candidate did not return list")
        self.assertEqual(len(res), 1, "Candidate does not contain exactly 1 results")
        self.assertEqual(
            res[0]["name"], "BLUMENTHAL, RICHARD", "Name of candidate not as expected"
        )

    def test_candidate_complicated(self):
        res = self.api_wrapper.candidate(
            "S0CT00177", office="S", state="CT", party="DEM", district="00"
        )
        self.assertIsInstance(res, list, "Candidate did not return dict")
        self.assertEqual(len(res), 1, "Candidate does not contain exactly 1 results")
        self.assertEqual(
            res[0]["name"], "BLUMENTHAL, RICHARD", "Name of candidate not as expected"
        )

    def test_candidate_history(self):
        res = self.api_wrapper.candidate("S0CT00177", history=True)
        self.assertIsInstance(res, list, "Candidate history did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidate history does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate history list does not contain dicts"
        )

    def test_candidate_history_cycle(self):
        res = self.api_wrapper.candidate("S0CT00177", history=True, cycle=2016)
        self.assertIsInstance(res, list, "Candidate history did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidate history does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate history list does not contain dicts"
        )

    def test_candidate_totals(self):
        res = self.api_wrapper.candidate("S0CT00177", totals=True)
        self.assertIsInstance(res, list, "Candidate totals did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidate totals does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate totals list does not contain dicts"
        )


class TestCandidates(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpenFEC(api_key="DEMO_KEY")

    def test_candidates(self):
        res = self.api_wrapper.candidates(
            office="P", name="Biden", election_year=2020, party="DEM"
        )
        self.assertIsInstance(res, list, "Candidates did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidates does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate totals list does not contain dicts"
        )
        self.assertEqual(res[0]["name"], "BIDEN, JOSEPH R JR", "Name not as expected")

    def test_candidates_search(self):
        res = self.api_wrapper.candidates(
            search=True, office="P", name="Biden", election_year=2020, party="DEM"
        )
        self.assertIsInstance(res, list, "Candidates did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidates searcg does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidates search list does not contain dicts"
        )
        self.assertEqual(res[0]["name"], "BIDEN, JOSEPH R JR", "Name not as expected")

    def test_candidates_totals(self):
        res = self.api_wrapper.candidates(totals=True, candidate_id="P80000722")
        self.assertIsInstance(res, list, "Candidates total did not return list")
        self.assertGreaterEqual(
            len(res), 1, "Candidates does not contain at least 1 results"
        )
        self.assertIsInstance(
            res[0], dict, "Candidate totals list does not contain dicts"
        )
        self.assertEqual(res[0]["name"], "BIDEN, JOSEPH R JR", "Name not as expected")

    def test_candidates_totals_by_office(self):
        res = self.api_wrapper.candidates(
            totals=True, by_office=True, election_year=2020
        )
        self.assertIsInstance(
            res, list, "Candidates totals by office did not return list"
        )
        self.assertEqual(
            len(res), 3, "Candidates totals by office did not return 3 results"
        )
        for element in res:
            self.assertIsInstance(
                element, dict, "Candidate totals by office does not contain dicts"
            )
            self.assertEqual(
                set(element.keys()),
                {"office", "total_disbursements", "total_receipts", "election_year"},
                "Candidate totals by office keys not as expected",
            )

    def test_candidates_totals_by_office_by_party(self):
        res = self.api_wrapper.candidates(
            totals=True, by_office=True, by_party=True, election_year=2020
        )
        self.assertIsInstance(
            res, list, "Candidates totals by office by party did not return list"
        )
        self.assertEqual(
            len(res), 9, "Candidates totals by office by party did not return 3 results"
        )
        for element in res:
            self.assertIsInstance(
                element,
                dict,
                "Candidate totals by office by party does not contain dicts",
            )
            self.assertEqual(
                set(element.keys()),
                {
                    "office",
                    "total_disbursements",
                    "total_receipts",
                    "election_year",
                    "party",
                },
                "Candidate totals by office by party keys not as expected",
            )
