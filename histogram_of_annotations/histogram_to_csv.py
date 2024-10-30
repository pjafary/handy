import os
import glob
import numpy as np
import csv

# Function to write data to CSV file where each class gets its own column
def write_to_csv_multicolumn(file_name, data_dict, header):
    max_length = max(len(values) for values in data_dict.values())  # Find the longest list
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)

        # Write data row by row
        for i in range(max_length):
            row = []
            for class_id in header:
                row.append(data_dict[class_id][i] if i < len(data_dict[class_id]) else '')  # Handle unequal lengths
            writer.writerow(row)

# Function to write annotation count to a CSV file
def write_annotation_count_to_csv(file_name, annotations_count):
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Annotation Count"])  # Header
        for count in annotations_count:
            writer.writerow([count])  # Write each count in a new row

# function for reading annotations
def read_annotations(annotation_dir, image_width, image_height):
    class_heights = {i: [] for i in range(8)}  # Initialize empty lists for each class
    class_widths = {i: [] for i in range(8)}
    annotations_count = []

    if not os.path.exists(annotation_dir):
        print(f"Directory '{annotation_dir}' does not exist.")
        return class_heights, class_widths, annotations_count

    annotation_files = glob.glob(os.path.join(annotation_dir, "*.txt"))

    if not annotation_files:
        print(f"No annotation files found in '{annotation_dir}'.")
        return class_heights, class_widths, annotations_count

    for annotation_file in annotation_files:
        with open(annotation_file, 'r') as file:
            lines = file.readlines()
            annotations_count.append(len(lines))
            for line in lines:
                elements = line.strip().split()
                if len(elements) != 5:
                    print(f"Invalid annotation line: {line}")
                    continue

                class_id = int(elements[0])
                _, _, _, width, height = map(float, elements)
                bbox_height = height * image_height
                bbox_width = width * image_width

                class_heights[class_id].append(bbox_height)
                class_widths[class_id].append(bbox_width)

    return class_heights, class_widths, annotations_count

# function for saving data to files with each class in a separate column
def save_data_multicolumn(class_heights, class_widths, annotations_count):
    # We now use numeric class IDs in the header for the CSV file
    height_header = sorted(class_heights.keys())  # Using numeric IDs (0, 1, 2, ...)
    width_header = sorted(class_widths.keys())

    # Save heights and widths to CSV files
    write_to_csv_multicolumn("heights_multicolumn.csv", class_heights, height_header)
    write_to_csv_multicolumn("widths_multicolumn.csv", class_widths, width_header)

    # Save annotations count to a CSV file
    write_annotation_count_to_csv("annotations_count.csv", annotations_count)

# usage
annotation_dir = '/home/parham/datasets/igrow/labels/all'  # absolute path to annotations directory
image_width = 5184  # image width
image_height = 3456  # image height

class_heights, class_widths, annotations_count = read_annotations(annotation_dir, image_width, image_height)
if class_heights and class_widths and annotations_count:
    save_data_multicolumn(class_heights, class_widths, annotations_count)
else:
    print("No valid data to save.")
