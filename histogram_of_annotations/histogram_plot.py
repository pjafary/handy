import os
import glob
import matplotlib.pyplot as plt
import numpy as np

# function for reading annotations
def read_annotations(annotation_dir, image_width, image_height):
    class_heights = {}
    class_widths = {}
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

                if class_id not in class_heights:
                    class_heights[class_id] = []
                
                if class_id not in class_widths:
                    class_widths[class_id] = []

                class_heights[class_id].append(bbox_height)
                class_widths[class_id].append(bbox_width)

    return class_heights, class_widths, annotations_count

# function for plotting histograms
def plot_histograms(class_heights, class_widths, annotations_count):
 # mapping class IDs to stage names
    class_to_stage = {0: 'Stage A', 1: 'Stage B', 2: 'Stage C', 3: 'Stage D', 4: 'Stage E', 5: 'Stage F', 6: 'Stage G', 7: 'Stage H'}

    plt.figure(figsize=(18, 6))

    # Function to calculate density
    def calculate_density(data):
        density, _ = np.histogram(data, bins=30, density=True)
        return density.mean()

    # Calculate densities for heights
    heights_densities = {class_id: calculate_density(heights) for class_id, heights in class_heights.items()}
    sorted_heights = sorted(class_heights.items(), key=lambda item: heights_densities[item[0]], reverse=True)

    # Plot Density vs Pixel Height for each class
    plt.subplot(1, 3, 1)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(class_heights)))
    for class_id, heights in sorted_heights:
        stage_name = class_to_stage.get(class_id, f'Class {class_id}')
        plt.hist(heights, bins=20, density=True, alpha=1, label=f'{stage_name}')
    plt.xlabel('Pixel Height')
    plt.ylabel('Density')
    plt.title('a')
    plt.legend()
    
    # Calculate densities for widths
    widths_densities = {class_id: calculate_density(widths) for class_id, widths in class_widths.items()}
    sorted_widths = sorted(class_widths.items(), key=lambda item: widths_densities[item[0]], reverse=True)

    # Plot Density vs Pixel Width for each class
    plt.subplot(1, 3, 2)
    for class_id, widths in sorted_widths:
        stage_name = class_to_stage.get(class_id, f'Class {class_id}')
        plt.hist(widths, bins=20, density=True, alpha=1, label=f'{stage_name}')
    plt.xlabel('Pixel Width')
    plt.ylabel('Density')
    plt.title('b')
    plt.legend()

    # Plot Density vs Number of Annotations
    plt.subplot(1, 3, 3)
    plt.hist(annotations_count, bins=20, density=True, alpha=1, color='g')
    plt.xlabel('Number of Annotations')
    plt.ylabel('Density')
    plt.title('c')

    plt.tight_layout()
    plt.show()

# usage
annotation_dir = '/home/parham/datasets/igrow/labels/all'  # absolute path to annotations directory
image_width = 5184  #  image width
image_height = 3456  #  image height

class_heights, class_widths, annotations_count = read_annotations(annotation_dir, image_width, image_height)
if class_heights and class_widths and annotations_count:
    plot_histograms(class_heights, class_widths, annotations_count)
else:
    print("No valid data to plot.")
