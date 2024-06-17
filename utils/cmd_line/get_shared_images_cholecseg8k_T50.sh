#!/bin/bash

# Define the directories containing the images
cd C:/Users/tal22/Documents/repositories/generate_binary_and_instance_masks_for_cholecseg8k/datasets

dir1="instance_cholec_v6_during_quality_control/train/VID12_seg8k/img_dir"
dir2="instance_cholec_v6_during_quality_control/train/VID12_t50_full/img_dir"

# Define the similarity threshold
threshold=0.2

# Output file for similar images
output_file="compare_images/similar_images.csv"

# Initialize CSV file with a header
echo "Image1,Image2,PhashDifference" > "$output_file"

# Loop through each image in the first directory
for img1 in "$dir1"/*; do
    # Loop through each image in the second directory
    for img2 in "$dir2"/*; do
        # Perform the comparison and capture the output
        # Redirect stderr to stdout to capture the phash metric
        diff=$(magick compare -metric phash "$img1" "$img2" null: 2>&1)
        # Check if the comparison resulted in an error
        if [[ $? -eq 0 ]]; then
            result=$(python -c "print(int($diff < $threshold))")
            # If no error and difference is less than the threshold, save to CSV
            if [ "$result" -eq 1 ]; then
                echo "$img1,$img2,$diff"
                echo "$img1,$img2,$diff" >> "$output_file"
            fi
        fi
    done
done

# Inform the user
echo "Comparison complete. Results saved to $output_file"










# #!/bin/bash

# shared_seq_ids=('12' '01' '18' '25' '26' '27' '35' '43' '48' '52')

# cd C:/Users/tal22/Documents/repositories/generate_binary_and_instance_masks_for_cholecseg8k/datasets/instance_cholec_v6_during_quality_control/train

# for seq_id in "${shared_seq_ids[@]}"
# do
#   t50_seq_name=VID${seq_id}_t50_full
#   seg8k_seq_name=VID${seq_id}_seg8k

#   #seg8k
#   # Navigate to the image directory
#   cd ${seg8k_seq_name}/img_dir

#   # Ensure the output directory exists
#   mkdir -p ../../../../compare_images

#   # Prepare the output file, clear it if it exists
#   > ../../../../compare_images/${seg8k_seq_name}.csv

#   # Process each PNG file
#   for img_file in *.png
#   do
#     # Use ImageMagick's magick command to get the hash of each image
#     magick identify -quiet -moments -format "%f, %#\n" "${img_file}" >> ../../../../compare_images/${seg8k_seq_name}.csv
#   done

#   # Return to the initial directory to start the next sequence
#   cd ../..  

#   #t50  
#   # Navigate to the image directory
#   cd ${t50_seq_name}/img_dir

#   # Ensure the output directory exists
#   mkdir -p ../../../../compare_images

#   # Prepare the output file, clear it if it exists
#   > ../../../../compare_images/${t50_seq_name}.csv

#   # Process each PNG file
#   for img_file in *.png
#   do
#     # Use ImageMagick's magick command to get the hash of each image
#     magick identify -quiet -moments -format "%f, %#\n" "${img_file}" >> ../../../../compare_images/${t50_seq_name}.csv
#   done

#   # Return to the initial directory to start the next sequence
#   cd ../..
# done

# echo "All sequences processed."


