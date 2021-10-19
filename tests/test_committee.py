import unittest
from open_fec import OpenFEC


class TestCommittee(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpenFEC("DEMO_KEY")


class TestCommittees(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpenFEC("DEMO_KEY")
