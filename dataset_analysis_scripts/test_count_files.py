import unittest
from dataset_analysis_scripts.count_files import count_sizes_in_my_dataset

class TestCountSizesInADict(unittest.TestCase):
    def test_count_sizes_in_my_dataset(self):
        my_dict = {
            'a': [1, 2, 3],
            'b': {
                'c': [4, 5],
                'd': {
                    'e': [6, 7, 8],
                    'f': [9, 10]
                },
                'g': {
                    'h': [11]
                }
            },
            'i': [12, 13]
        }
        print('\n--- Test 1 ---')
        self.assertEqual(count_sizes_in_my_dataset(my_dict, 1), 13)

    def test_empty_dict(self):
        print('\n--- Test 2 ---')
        self.assertEqual(count_sizes_in_my_dataset({}, 1), 0)

    def test_dict_with_empty_lists(self):
        my_dict = {
            'a': [],
            'b': {
                'c': [],
                'd': {}
            }
        }
        print('\n--- Test 3 ---')
        self.assertEqual(count_sizes_in_my_dataset(my_dict, 1), 0)

    def test_dict_with_no_lists(self):
        my_dict = {
            'a': 1,
            'b': {
                'c': {},
                'd': {
                    'e': 'string'
                }
            }
        }
        print('\n--- Test 4 ---')
        self.assertEqual(count_sizes_in_my_dataset(my_dict, 1), 0)

if __name__ == '__main__':
    unittest.main()