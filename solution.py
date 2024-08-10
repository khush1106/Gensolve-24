import numpy as np
import cv2
import os
import cairosvg

def load_and_process_csv(file_path):
    try:
        # Load CSV data into a NumPy array
        data_array = np.genfromtxt(file_path, delimiter=',')
        print("CSV data loaded successfully:")
        print(data_array)
        
        organized_data = []
        unique_paths = np.unique(data_array[:, 0])
        
        for path_id in unique_paths:
            path_data = data_array[data_array[:, 0] == path_id][:, 1:]
            print(f"Data for path {path_id}:")
            print(path_data)
            
            xy_groups = []
            for group_id in np.unique(path_data[:, 0]):
                group_data = path_data[path_data[:, 0] == group_id][:, 1:]
                print(f"Group {group_id} data:")
                print(group_data)
                xy_groups.append(group_data)
            organized_data.append(xy_groups)
        
        return organized_data
    
    except Exception as e:
        print(f"Error loading or processing CSV file: {e}")

def convert_svg_to_png(input_svg_path, output_png_path):
    try:
        cairosvg.svg2png(url=input_svg_path, write_to=output_png_path)
        print(f"SVG successfully converted to PNG and saved at {output_png_path}.")
    except Exception as e:
        print(f"Error during SVG to PNG conversion: {e}")

def identify_shape(contour):
    tolerance = 0.04 * cv2.arcLength(contour, True)
    approx_contour = cv2.approxPolyDP(contour, tolerance, True)
    vertex_count = len(approx_contour)

    if vertex_count == 2:
        return "Line"
    elif vertex_count == 3:
        return "Triangle"
    elif vertex_count == 4:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        return "Square" if 0.95 < aspect_ratio < 1.05 else "Rectangle"
    elif vertex_count == 5:
        return "Pentagon"
    elif vertex_count > 6:
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if circularity > 0.8:
            return "Circle"
        elif vertex_count > 10:
            return "Star"
        else:
            return "Polygon"
    return "Unidentified Shape"

def analyze_image_shapes(image_file_path):
    try:
        image = cv2.imread(image_file_path)
        if image is None:
            raise ValueError("Error: Unable to load image.")
        
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
        edge_image = cv2.Canny(blurred_image, 50, 150)
        contours, _ = cv2.findContours(edge_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            shape = identify_shape(contour)
            print(f"Identified shape: {shape}")

    except Exception as e:
        print(f"Error analyzing image shapes: {e}")

if __name__ == "__main__":
    main()
