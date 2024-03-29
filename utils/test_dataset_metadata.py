import unittest
import os
from dataset_metadata import DatasetMetadata
import pprint

class TestDatasetMetadata(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.dataset_paths_properly_structured = {
            "img_annotation_just_2_files": {
                'path': "test_assets/test_dataset_metadata/img_annotation_just_2_files",
                'metadata': {
                    'train': {
                        'seq1' : [
                            {
                                'img_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/train/seq1/img_dir/test - Copy.png',
                                'ann_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/train/seq1/ann_dir/test - Copy.json'
                            },
                            {
                                'img_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/train/seq1/img_dir/test.png',
                                'ann_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/train/seq1/ann_dir/test.json'
                            }
                            
                        ]
                        },
                    'val': {
                        'seq2' : [],
                        'seq3': [
                            {
                                'img_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/val/seq3/img_dir/test_3.png',
                                'ann_path': 'test_assets/test_dataset_metadata/img_annotation_just_2_files/val/seq3/ann_dir/test_3.json'
                            },
                        ]
                        
                    }
                }
                },
            
            "no_img_no_annotation": {
                    'path': "test_assets/test_dataset_metadata/no_img_no_annotation",
                    'metadata': {'train': {'seq1': []},
                                 'val': {'seq2': [],
                                         'seq3': []}
                    }
                } 
        }
        
        self.dataset_path_for_missing_annotation_dataset = "test_assets/test_dataset_metadata/img_annotation_just_2_files_err_ann"

    def test_split_seq_img_dir_ann_dir(self):
        for dataset_name, dataset_info in self.dataset_paths_properly_structured.items():
            with self.subTest(dataset_name=dataset_name):
                dataset = DatasetMetadata(path_to_dataset=dataset_info['path'],
                                          dataset_name=dataset_name,
                                          dataset_style="split_seq_img_dir-ann_dir")
                dataset_metadata = dataset.get_dataset_metadata()
                # pprint.pprint(dataset_metadata)
                self.assertIsNotNone(dataset_metadata)
                self.assertIsInstance(dataset_metadata, dict)
                self.assertDictEqual(dataset_metadata, dataset_info['metadata'])


    def test_invalid_dataset_style(self):
        with self.assertRaises(ValueError):
            dataset = DatasetMetadata(path_to_dataset="path/to/dataset",
                                      dataset_name="invalid_dataset",
                                      dataset_style="invalid_style")

    def test_missing_annotation(self):
        with self.assertRaises(AssertionError):
            dataset = DatasetMetadata(path_to_dataset=self.dataset_path_for_missing_annotation_dataset,
                                      dataset_name="missing_annotation",
                                      dataset_style="split_seq_img_dir-ann_dir")

if __name__ == "__main__":
    unittest.main()
