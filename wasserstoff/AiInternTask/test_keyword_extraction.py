# tests/test_summarization.py
import unittest
from src.summarization import generate_summary  # Ensure this path is correct

class TestSummarization(unittest.TestCase):
    def test_generate_summary(self):
        text = "This is a long document that needs summarization."
        num_pages = 1  # Set the number of pages as needed
        summary = generate_summary(text, num_pages)  # Pass both arguments
        self.assertTrue(len(summary) > 0)  # Replace with your actual assertions

if __name__ == '__main__':
    unittest.main()  # This will run the tests when the script is executed
