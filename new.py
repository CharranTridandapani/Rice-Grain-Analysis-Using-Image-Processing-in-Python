import cv2
import numpy as np

def get_rice_size(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Calibration factor (pixels per millimeter)
    calibration_factor = 0.1

    while True:
        # Read a frame from the video
        ret, frame = video.read()

        # Stop if the video has ended
        if not ret:
            break

        # Resize the frame
        frame = cv2.resize(frame, (800, 700))

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Perform edge detection
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the frame
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Iterate over the contours
        for contour in contours:
            # Compute the area of the contour
            area = cv2.contourArea(contour)

            # Filter out small contours (adjust the threshold as needed)
            if area > 100:
                # Compute the perimeter of the contour
                perimeter = cv2.arcLength(contour, True)

                # Approximate the contour as a polygon
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                # Compute the bounding box of the contour
                x, y, w, h = cv2.boundingRect(approx)

                # Calculate width and length in millimeters using the calibration factor
                width_mm = w * calibration_factor
                length_mm = h * calibration_factor

                # Draw the bounding box on the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Display the width and length on the frame
                text = f"Width: {width_mm:.2f} mm, Length: {length_mm:.2f} mm"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Rice Sizes', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    video.release()

    # Destroy all windows
    cv2.destroyAllWindows()

# Path to the input video
video_path = 'charran.avi'

# Process the video and display rice sizes
get_rice_size(video_path)
