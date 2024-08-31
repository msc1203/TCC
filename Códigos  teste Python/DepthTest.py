import freenect
import cv2
import numpy as np

def get_depth():
    """
    Fetch depth data from Kinect sensor.
    """
    depth, _ = freenect.sync_get_depth()
    return depth

def convert_depth_to_meters(depth):
    """
    Convert raw Kinect depth data to meters.
    """
    return depth * 0.001  # Assuming depth is in millimeters

def display_depth_image():
    """
    Display depth data as an image and print distance of the object
    at the center of the frame.
    """
    while True:
        depth = get_depth()
        print("Depth is: ", depth)
        print("Depth length is: ", len(depth))
        for i in range(120):
            depth[i] = 0
        for i in range(360, 480):
            depth[i] = 0
        depth_in_meters = convert_depth_to_meters(depth)
        
        # Scale depth values for visualization
        depth_scaled = np.uint8(depth / 2048 * 255)
        print(type(depth_scaled))
        print("Depth scaled is: ", depth_scaled)
        print("Deth Length is: ", len(depth_scaled[0]))
        print("Deth Length is: ", len(depth_scaled))
        print("Depth meters is: ", depth_in_meters)
        for i in range(120):
            depth_scaled[i] = 0
        for i in range(360, 480):
            depth_scaled[i] = 0

        print("Depth scaled is: ", depth_scaled)
        # Apply a colormap to the depth image
        depth_colored = cv2.applyColorMap(depth_scaled, cv2.COLORMAP_JET)
        
        # Get the distance of the object in the center
        center_distance = depth_in_meters[depth.shape[0] // 2, depth.shape[1] // 2]
        
        # Display the depth image
        cv2.imshow('Depth Image', depth_scaled)
        # cv2.imshow('Depth Image', depth_colored)
        
        # Print distance at the center
        print(f'Distance at center: {center_distance:.2f} meters')
        
        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    display_depth_image()
