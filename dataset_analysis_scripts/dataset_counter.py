from utils.dataset_metadata import DatasetMetadata 
from utils.read_files import read_from_json  
import os
from os.path import join   
from static_variables.dataset_variables import CholecInstanceSegVariables
import argparse


class DatasetCounter:
    def __init__(self, 
                path_to_dataset:str, 
                dataset_name: str = 'cholec_instance_seg', 
                dataset_style: str = 'split_seq_img_dir-ann_dir',
                class_names = ['grasper','hook','irrigator','clipper','bipolar','scissors','snare']
                ):
        self.path_to_dataset = path_to_dataset
        self.dataset_name = dataset_name
        self.dataset_style = dataset_style
        self.dataset = DatasetMetadata(path_to_dataset=path_to_dataset,
                                          dataset_name=dataset_name,
                                          dataset_style=dataset_style)
        self.dataset_metadata = self.dataset.get_dataset_metadata()
        self.class_names = class_names
        self.class_frequency_dict_dataset = self.generate_class_frequency_dict_dataset()
        

    ## We want to have a count per image and annotation of the values, 
    ## We want to have a way to go through and sum these up. 
    
    ## step 1.
    ## so we get an instance
    ## we get the instruments in the instance for each class. store this as a dict. we could use list but we choose dict because it is easier to debug dicts and we can convert.
            ##performance is not an issue.  
    
    ## step 2, 
    ## we perform this for every instance and produce a new dict from the dataset metadata called, class frequency dict
    ## we essentailly repeat step 1 for every metadata instance and store somethng that is like
        # train - seq - image - name  - dict. dict should have keys as instrument names and values as frequency. 
    ## We store this value. 
    
    ## sum over various settings. 
    ## we want to know this values for the dataset, we want to know these values for each split, and each sequence.     
    
    
    def generate_class_frequency_dict_image(self, ann_path):
        
        class_frequency_dict_image = {class_name: 0   for class_name in self.class_names}
        
        ann = read_from_json(ann_path)
        for shape in ann['shapes']:
            assert shape['group_id'] != 0, f"there is an error in {ann_path}, there is a group id that is 0 for {shape['label']}"
            if shape['group_id'] > class_frequency_dict_image[shape['label']]: #handle multiple shapes with the same group_id 
                class_frequency_dict_image[shape['label']] += 1 
        
        return class_frequency_dict_image
    
    def generate_class_frequency_dict_dataset(self):
        # we need to walk through the dict and get the result. 
        # for each ann_path give me a frequency is what I want to do. So keep going in till you find a variable.
        
        class_frequency_dict_dataset = {}
        for split, seq_data in self.dataset_metadata.items():
            class_frequency_dict_split = {}
            for seq, annotations in seq_data.items():
                class_frequency_dict_seq = {}
                for annotation in annotations:
                    ann_path = annotation['ann_path']
                    ann_name = ann_path.split('/')[-1]
                    class_frequency_dict_image = self.generate_class_frequency_dict_image(ann_path)
                    class_frequency_dict_seq[ann_name] = class_frequency_dict_image
                class_frequency_dict_split[seq] = class_frequency_dict_seq
            class_frequency_dict_dataset[split] = class_frequency_dict_split
        return class_frequency_dict_dataset
    
    
    def count_class_frequency(self, aggregation_level='dataset'):
        target_dict = {}
        for split, split_data in self.class_frequency_dict_dataset.items():       
            for seq_name, seq_data in split_data.items():
                for ann_name, annotation in seq_data.items():                
                    for instrument, frequency in annotation.items():
                        if aggregation_level == 'dataset':
                            target_dict.setdefault(instrument, 0)
                            target_dict[instrument] += frequency
                        elif aggregation_level == 'split':
                            target_dict.setdefault(split, {}).setdefault(instrument, 0)
                            target_dict[split][instrument] += frequency
                        elif aggregation_level == 'sequence':
                            target_dict.setdefault(seq_name, {}).setdefault(instrument, 0)
                            target_dict[seq_name][instrument] += frequency
                            
        return target_dict
    
    def count_instance_frequency(self, aggregation_level='dataset'):
        target_dict = {}
        for split, split_data in self.class_frequency_dict_dataset.items():            
            for seq_name, seq_data in split_data.items():
                for ann_name, annotation in seq_data.items():                    
                    for instrument, frequency in annotation.items():
                        if aggregation_level == 'dataset':
                            target_dict.setdefault('total_instances', 0)
                            target_dict['total_instances'] += frequency
                        elif aggregation_level == 'split':
                            target_dict.setdefault(split, 0)
                            target_dict[split] += frequency
                        elif aggregation_level == 'sequence':
                            target_dict.setdefault(seq_name, 0)
                            target_dict[seq_name] += frequency
                        elif aggregation_level == 'image':
                            target_dict.setdefault(ann_name, 0)
                            target_dict[ann_name] += frequency
                        elif aggregation_level == 'sequence_and_image':
                            target_dict.setdefault(seq_name, {}).setdefault(ann_name, 0)
                            target_dict[seq_name][ann_name] += frequency        
                            
        return target_dict

            
        
            
    
    

def main():
    parser = argparse.ArgumentParser(description='Compute class frequency for a dataset')
    parser.add_argument('--path_to_dataset', type=str, default='C:/Users/tal22/Documents/repositories/generate_binary_and_instance_masks_for_cholecseg8k/datasets/instance_cholec_v1_during_quality_control', help='Path to the dataset')
    parser.add_argument('--dataset_name', type=str, default='cholec_instance_seg', help='Name of the dataset')
    parser.add_argument('--dataset_style', type=str, default='split_seq_img_dir-ann_dir', help='Dataset style')
    parser.add_argument('--aggregation_level', type=str, default='dataset', choices=['dataset', 'split', 'sequence'], help='Aggregation level')

    args = parser.parse_args()

    instrument_id_to_instrument_class_dict = CholecInstanceSegVariables.instrument_id_to_instrument_class_dict
    class_names = list(instrument_id_to_instrument_class_dict.values())

    frequency_of_classes_counter = FrequencyOfClassesDatasetCounter(
        path_to_dataset=args.path_to_dataset,
        dataset_name=args.dataset_name,
        dataset_style=args.dataset_style,
        class_names=class_names,
    )

    class_frequency = frequency_of_classes_counter.get_class_frequency(aggregation_level=args.aggregation_level)
    print(f"Class Frequency for {args.aggregation_level}:")
    print(class_frequency)

    

if __name__ == "__main__":
    main()