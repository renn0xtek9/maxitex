#!/usr/bin/env python3
import unittest
import os
import sys
from maxitexparser import maxitexparser


class TestMaxitexParser(unittest.TestCase):
    def setUp(self):
        self.projectdirectory = os.path.join(os.getcwd(), "../maxitex_text/")
        self.buildirectory = os.path.join(self.projectdirectory, "build")
        #self.p = maxitexparser(self.projectdirectory, self.buildirectory)
        self.p = maxitexparser(self.projectdirectory)
        pass

    def test_detectauthor(self):
        self.p._parsemaximafile('maxitex_test/default.mac')
        self.assertTrue(self.p.author)

    def test_detectnomenclature(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/default.mac')
        self.assertTrue(self.p.nomenclature)

    def test_detecttitle(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/default.mac')
        self.assertTrue(self.p.title)

    def test_detectabstract(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/default.mac')
        self.assertTrue(self.p.abstract)

    def test_falsepositive_title(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/notitle.mac')
        self.assertFalse(self.p.title)

    def test_falsepositive_author(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/noauthor.mac')
        self.assertFalse(self.p.author)

    def test_falsepositive_abstract(self):
        p = maxitexparser()
        self.p._parsemaximafile('maxitex_test/noabstract.mac')
        self.assertFalse(self.p.abstract)

    def test_proceed_default_create_tex(self):
        import os
        if (os.path.isfile("maxitex_test/default.tex")):
            os.remove("maxitex_test/default.tex")
        p = maxitexparser()
        self.p.GenerateTexFile(
            "maxitex_test/default.mac", "maxitex_test/default")
        import os.path
        assert (os.path.isfile("maxitex_test/default.tex") == True)


if __name__ == '__main__':
    unittest.main()
