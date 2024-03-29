import unittest
from utils.read_files import read_from_json, read_image, read_npy, read_text
import numpy as np
import json
import os

class TestReadFiles(unittest.TestCase):

    def setUp(self):
        # Initialize paths to your test files
        self.image_path = 'tests/assets/baboon.tif'
        self.json_path = 'tests/assets/test.json'
        self.npy_path = 'tests/assets/test.npy'
        self.txt_path = 'tests/assets/test.txt'
    
    def test_read_image(self):
        # Test read_image
        result = read_image(self.image_path, 'RGB')
        self.assertIsInstance(result, np.ndarray)  # Check if it is numpy array
        self.assertEqual(result.shape[2], 3)  # Check if image is in RGB mode
    
    def test_read_image_gray(self):
        # Test read_image in grayscale
        result = read_image(self.image_path, 'GRAY')
        self.assertIsInstance(result, np.ndarray)  # Check if it is numpy array
        self.assertEqual(len(result.shape), 2)  # Check if image is in grayscale
    
    def test_read_from_json(self):
        # Test read_from_json
        expected_result = {'version': 'test'}  # Update with expected result from your json file
        result = read_from_json(self.json_path)
        self.assertEqual(result, expected_result)
    
    def test_read_npy(self):
        # Test read_npy
        expected_result = np.array([1, 2, 3])  # Update with expected array from your npy file
        result = read_npy(self.npy_path)
        np.testing.assert_array_equal(result, expected_result)
    
    def test_read_text(self):
        # Test read_text
        expected_result = 'Hello World!'  # Update with expected content of your txt file
        result = read_text(self.txt_path)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
