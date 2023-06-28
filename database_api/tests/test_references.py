import unittest

from database_api.code_verse import reference
from database_api.errors import BookNotFoundError


class ReferenceTest(unittest.TestCase):
    def test_correct_references(self):
        self.assertEqual(("ecclesiastes", 3000001, 3000001), reference("Ecclesiastes 3:1"))
        self.assertEqual(("genesis", 1000001, 1000001), reference("Genesis 1:1"))
        self.assertEqual(("songofsolomon", 1000001, 1000001), reference("Song of Solomon 1:1"))

    def test_incorrect_book_names(self):
        self.assertRaises(BookNotFoundError, reference, "Jon 1")
        self.assertRaises(BookNotFoundError, reference, "Jack 3:16")
        self.assertRaises(BookNotFoundError, reference, "Test 3:1-16")
        self.assertRaises(BookNotFoundError, reference, "Not 1:1-2:16")

    def test_correct_abbreviations(self):
        self.assertEqual(("mark", 3000016, 3000016), reference("Mk 3:16"))
        self.assertEqual(("matthew", 3000016, 3000017), reference("Mt 3:16-17"))

    def test_correct_alternatives(self):
        self.assertEqual(("songofsolomon", 1000001, 1000001), reference("Song of Songs 1:1"))
        self.assertEqual(("ecclesiastes", 3000001, 3000001), reference("Qoheleth 3:1"))
        self.assertEqual(("revelation", 3000001, 3000001), reference("Apocalypse 3:1"))
        self.assertEqual(("3john", 1000001, 1000001), reference("III John 1:1"))

    def test_lowercase_names(self):
        self.assertEqual(("mark", 3000016, 3000016), reference("mark 3:16"))

    def test_with_range_references(self):
        self.assertEqual(("mark", 3000016, 3000017), reference("Mark 3:16-17"))
        self.assertEqual(("mark", 3000016, 14000017), reference("Mark 3:16-14:17"))
        self.assertEqual(("mark", 3000016, 3000017), reference("Mark 3:16-17"))

    def test_with_incorrect_range(self):
        # corrects the bigger item
        self.assertEqual(("mark", 3000014, 3000016), reference("Mark 3:16-14"))

    def test_with_grammatically_correct(self):
        # Despite these not being in the bible, the logic still work the same
        self.assertEqual(("mark", 900000009321, 900000009321), reference("Mark 900000:9321"))


if __name__ == '__main__':
    unittest.main()
