import unittest
from ChomskyNormalForm import Grammar, ChomskyForm  # Assuming both classes are in the same module

class TestChomskyForm(unittest.TestCase):
    def setUp(self):
        VN = {"S", "A", "B", "C", "E"}
        VT = {"a", "b"}
        start = "S"
        P = {
            "S": ["bA", "B"],
            "A": ["a", "aS", "bAaAb"],
            "B": ["AC", "bS", "aAa"],
            "C": ["", "AB"],  # Epsilon is presented as ''
            "E": ["BA"]
        }
        self.chomsky = ChomskyForm(VN, VT, P, start)

    def test_remove_duplicates(self):
        test_list = ["a", "b", "a", "c", "b"]
        expected_list = ["a", "b", "c"]
        result = self.chomsky.remove_duplicates(test_list)
        self.assertEqual(set(result), set(expected_list), "Duplicates are not properly removed.")

    def generate_strings_with_letter_removed(self, s, letter):
        strings = set()
        pos = s.find(letter)
        while pos != -1:
            new_string = s[:pos] + s[pos + 1:]
            strings.add(new_string)
            pos = s.find(letter, pos + 1)
        return list(strings)

    def test_removeEmptyString(self):
        self.chomsky.P['C'] = ["", "AB"]
        self.chomsky.removeEmptyString()
        self.assertNotIn("", self.chomsky.P['C'], "Empty strings were not removed.")
        self.assertIn("AB", self.chomsky.P['C'], "Valid productions are lost.")

    def test_removeInaccessible(self):
        self.chomsky.removeInaccessible()
        self.assertNotIn("E", self.chomsky.P, "Inaccessible symbols were not removed.")

    def test_unitProduction(self):
        self.chomsky.P['A'] = ["B"]
        self.chomsky.P['B'] = ["a"]
        self.chomsky.unitProduction()
        self.assertIn("a", self.chomsky.P['A'], "Unit productions were not replaced correctly.")

    def test_chomsky(self):
        self.chomsky.transformInChomsky()
        print("After conversion to Chomsky Normal Form:", self.chomsky.P)
        for key, productions in self.chomsky.P.items():
            for production in productions:
                if not production:
                    continue
                elif len(production) == 2:
                    self.assertTrue(all(ch in self.chomsky.VN for ch in production),
                                    f"Production '{production}' should be two non-terminals but is not: {key} -> {production}")



if __name__ == '__main__':
    unittest.main()
