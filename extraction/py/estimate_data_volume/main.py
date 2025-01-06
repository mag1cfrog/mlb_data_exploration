import base64
import json
import os

import numpy as np
import cv2


def calculate_frame_size_mb(high_fps, high_cam_count, standard_fps, standard_cam_count, game_duration_seconds, total_data_tb):
    # Calculate total frames captured by high-frame-rate cameras
    total_high_frames = high_fps * high_cam_count * game_duration_seconds
    
    # Calculate total frames captured by standard cameras
    total_standard_frames = standard_fps * standard_cam_count * game_duration_seconds
    
    # Calculate total frames
    total_frames = total_high_frames + total_standard_frames
    
    # Convert total data storage from TB to bytes
    total_data_bytes = total_data_tb * 10**12
    
    # Calculate frame size in bytes
    frame_size_bytes = total_data_bytes / total_frames
    
    # Convert frame size from bytes to MB
    frame_size_mb = frame_size_bytes / 10**6
    
    return frame_size_mb


def find_optimal_image_settings(target_size_mb, output_dir, trials=5):
    # Define a set of potential dimensions (width x height) and JPEG qualities to test
    dimensions = [(640, 480), (800, 600), (1024, 768)]  # Common video resolutions
    qualities = range(80, 100, 5)  # High-quality range for JPEG
    
    best_match = None
    min_diff = float('inf')
    
    # Test combinations of dimensions and qualities
    for width, height in dimensions:
        for quality in qualities:
            # Create a random image
            image_data = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
            
            # Temporarily save the image to disk
            test_filename = os.path.join(output_dir, "test_frame.jpg")
            cv2.imwrite(test_filename, image_data, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
            
            # Check the file size
            current_size_mb = os.path.getsize(test_filename) / (1024 * 1024)
            
            # Calculate how close we are to the target size
            diff = abs(current_size_mb - target_size_mb)
            
            if diff < min_diff:
                min_diff = diff
                best_match = (width, height, quality, current_size_mb)
            
            # Clean up test file
            os.remove(test_filename)
    
    return best_match

def generate_fake_frame_data(output_dir, image_width, image_height, jpeg_quality):
    # Create a random image
    image_data = np.random.randint(0, 256, (image_height, image_width, 3), dtype=np.uint8)

    # Generate metadata
    metadata = {
        "timestamp": "2023-10-01T12:00:00Z",
        "camera_id": 1,
        "frame_id": 12345,
        "tracking_info": {
            "object_coordinates": [100, 200],
            "velocity": [5, -3]
        }
    }
    metadata_json = json.dumps(metadata)

    # Save image to a file as JPEG
    image_filename = os.path.join(output_dir, "frame.jpg")
    cv2.imwrite(image_filename, image_data, [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality])

    # Calculate file size in MB
    image_file_size = os.path.getsize(image_filename) / (1024 * 1024)

    # Save metadata to a file
    metadata_filename = os.path.join(output_dir, "metadata.json")
    with open(metadata_filename, 'w') as f:
        f.write(metadata_json)
    
    # Calculate metadata file size in MB
    metadata_file_size = os.path.getsize(metadata_filename) / (1024 * 1024)

    return image_file_size, metadata_file_size


def encode_image_to_base64(image_path):
    """Encode image to Base64 string and calculate the size of the Base64 string."""
    with open(image_path, "rb") as image_file:
        # Read the image as binary data
        binary_data = image_file.read()
        # Convert binary data to Base64 encoded string
        base64_encoded_data = base64.b64encode(binary_data)
        # Convert bytes to string for JSON serialization
        base64_string = base64_encoded_data.decode('utf-8')
        return base64_string


def calculate_base64_size(base64_string):
    """Calculate the size of the Base64 string in bytes."""
    base64_size = len(base64_string.encode('utf-8'))  # Get the number of bytes
    return base64_size / (1024 * 1024)  # Convert bytes to megabytes


def main():
    # Constants
    HIGH_FPS = 300
    HIGH_CAM_COUNT = 5
    STANDARD_FPS = 100
    STANDARD_CAM_COUNT = 7
    GAME_DURATION_SECONDS = 3 * 60 * 60  # 3 hours
    TOTAL_DATA_TB = 7  # Known total data storage

    # Calculate frame size in MB
    target_frame_size_mb = calculate_frame_size_mb(HIGH_FPS, HIGH_CAM_COUNT, STANDARD_FPS, STANDARD_CAM_COUNT, GAME_DURATION_SECONDS, TOTAL_DATA_TB)
    print(f"Estimated frame size: {target_frame_size_mb:.2f} MB")

    output_dir = '/home/hanbow/repositories/mlb_data_exploration/data'  # Adjust this to your actual output directory
    # Find optimal image settings
    optimal_settings = find_optimal_image_settings(target_frame_size_mb, output_dir)
    if optimal_settings:
        width, height, quality, achieved_size = optimal_settings
        print(f"Optimal settings: {width}x{height} at quality {quality}, achieved size: {achieved_size:.2f} MB")
        image_size, metadata_size = generate_fake_frame_data(output_dir, width, height, quality)
        print(f"Generated image size: {image_size:.2f} MB, Metadata size: {metadata_size:.2f} MB")

        # Encode image to Base64
        image_path = os.path.join(output_dir, "frame.jpg")
        base64_string = encode_image_to_base64(image_path)
        base64_size = calculate_base64_size(base64_string)
        print(f"Base64 size: {base64_size:.2f} MB")
        
if __name__ == "__main__":
    main()
