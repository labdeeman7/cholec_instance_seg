import os
import json

def change_class_names_suture_passer_with_snare(file_paths_of_ann,
                                                word_to_replace = "suture_passer",
                                                replacement_word = "snare",
                                                ):

    # Iterate over each file in the file[atjs]
    for file_path in file_paths_of_ann :
        if file_path.endswith('.json'):
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Loop through each shape object in the "shapes" array
            for shape in data['shapes']:
                # Check if the "label" field contains the word to replace
                if shape['label'] == word_to_replace:
                    # Replace the word in the "label" field
                    shape['label'] = replacement_word
            
            # Write the modified data back to the same file
            with open(file_path, 'w') as f:
                json.dump(data, f)

    print("class changed successfully.")
