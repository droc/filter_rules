import unittest

from filter_rules import ConditionOnCollectionAttribute, ConditionOnAttribute
from typing import List


class Example(object):
    def __init__(self, something, smth_else, a_collection):
        # type: (str, int, List[int]) -> None
        self.something = something
        self.smth_else = smth_else
        self.a_collection = a_collection


class ExampleCond(object):
    SOMETHING = ConditionOnAttribute("something")
    SMTH_ELSE = ConditionOnAttribute("smth_else")
    A_COLLECTION = ConditionOnCollectionAttribute("a_collection")


class ConditionOnAttributeTest(unittest.TestCase):
    def test_equals(self):
        e = Example("a", 1, [])
        cond_something_ = (ExampleCond.SOMETHING == "a")
        self.assertTrue(cond_something_.accepts(e))


class ConditionOnCollectionTest(unittest.TestCase):
    def test_length(self):
        e = Example("a", 1, [1])
        self.assertFalse((ExampleCond.A_COLLECTION.length() > 1).accepts(e))
        self.assertTrue((ExampleCond.A_COLLECTION.length() == 1).accepts(e))
        self.assertFalse((ExampleCond.A_COLLECTION.length() < 1).accepts(e))
        self.assertTrue((ExampleCond.A_COLLECTION == [1]).accepts(e))
