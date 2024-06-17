import argparse
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.dataset_metadata import DatasetMetadata

#pass datasetmetadata to count. 
def count_sizes_in_my_dataset(d, current_level=1, hspace=3):
        if current_level == 1:
            print('Entering base data structure')
        if isinstance(d, dict):
            total_count = 0
            for key, value in d.items():
                if isinstance(value, list):
                    print(f"{' '*hspace*current_level}size of seq '{key}': {len(value)}")
                    total_count += len(value)
                elif isinstance(value, dict):
                    print(f"{' '*hspace*current_level}Entering {'sub-'*current_level}dictionary key '{key}'")
                    current_level += 1
                    sub_count = count_sizes_in_my_dataset(value, current_level)
                    current_level -= 1
                    print(f"{' '*hspace*current_level}Total count in sub-dictionary at key '{key}': {sub_count}")
                    total_count += sub_count
            return total_count
        else:
            print('data structure is not a dict')
            return 0


def main(path_to_dataset, dataset_name, dataset_style):
    dataset = DatasetMetadata(path_to_dataset=path_to_dataset,
                              dataset_name=dataset_name,
                              dataset_style=dataset_style)
    dataset_metadata = dataset.get_dataset_metadata()
    total_count = count_sizes_in_my_dataset(dataset_metadata)
    print(f"Total count of all images annotated in the dataset: {total_count}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to count files in a dataset")
    parser.add_argument("path_to_dataset", type=str, nargs='?', default='C:/Users/tal22/Documents/repositories/generate_binary_and_instance_masks_for_cholecseg8k/datasets/instance_cholec_v1_before_quality_control', help="Path to the dataset")
    parser.add_argument("dataset_name", type=str, nargs='?', default='instance_cholec_v1_before_quality_control', help="Name of the dataset")
    parser.add_argument("dataset_style", type=str, nargs='?', default='split_seq_img_dir-ann_dir', help="Style of the dataset")
    args = parser.parse_args()

    main(args.path_to_dataset, args.dataset_name, args.dataset_style)
    