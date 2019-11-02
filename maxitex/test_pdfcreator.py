#!/usr/bin/env python3
import unittest
from pdfcreator import PdfCreator

class TestPdfCreator(unittest.TestCase):
    def setUp(self):
        pass
    
    def CreateCreatorOnTestRessources(self):
        pass
        
    
    
    def test_builddirectory(self):
        pdc=PdfCreator("/home/foo/bar")
        self.assertEqual(pdc.BuildDirectory(),"/home/foo/bar/build")
        
    
        
        
if __name__ == '__main__':
    unittest.main()
            
            
            
