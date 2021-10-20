import unittest
from opynfec import OpynFEC


class TestCommittee(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpynFEC("DEMO_KEY")


class TestCommittees(unittest.TestCase):
    def setUp(self) -> None:
        self.api_wrapper = OpynFEC("DEMO_KEY")
