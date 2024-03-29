import unittest
import numpy as np
import json
import os
from utils.save_files import save_image, save_to_json, save_npy, save_text  # Replace 'your_module' with the actual name

class TestSaveFiles(unittest.TestCase):

    def setUp(self):
        # Setup: Temporary paths for saving files
        self.temp_image_path = 'temp_image.png'
        self.temp_json_path = 'temp_data.json'
        self.temp_npy_path = 'temp_data.npy'
        self.temp_txt_path = 'temp_file.txt'
        # Example data to save
        self.image_data = np.zeros((100, 100, 3), dtype=np.uint8)  # Example black square image
        self.json_data = {"key": "value"}
        self.npy_data = np.array([1, 2, 3])
        self.text_data = "Hello, world!"

    def test_save_image(self):
        # Test save_image
        save_image(self.image_data, self.temp_image_path)
        self.assertTrue(os.path.exists(self.temp_image_path))
        # Additional checks can be added for image content if necessary

    def test_save_to_json(self):
        # Test save_to_json
        save_to_json(self.json_data, self.temp_json_path)
        self.assertTrue(os.path.exists(self.temp_json_path))
        with open(self.temp_json_path, 'r') as f:
            data_loaded = json.load(f)
        self.assertEqual(self.json_data, data_loaded)

    def test_save_npy(self):
        # Test save_npy
        save_npy(self.npy_data, self.temp_npy_path)
        self.assertTrue(os.path.exists(self.temp_npy_path))
        data_loaded = np.load(self.temp_npy_path)
        np.testing.assert_array_equal(self.npy_data, data_loaded)

    def test_save_text(self):
        # Test save_text
        save_text(self.text_data, self.temp_txt_path)
        self.assertTrue(os.path.exists(self.temp_txt_path))
        with open(self.temp_txt_path, 'r') as file:
            data_loaded = file.read()
        self.assertEqual(self.text_data, data_loaded)

    def tearDown(self):
        # Clean up: Remove temporary files created during tests
        for path in [self.temp_image_path, self.temp_json_path, self.temp_npy_path, self.temp_txt_path]:
            if os.path.exists(path):
                os.remove(path)

if __name__ == '__main__':
    unittest.main()
