import cv2
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
def get_rice_size(video_path):
    # Open the video file
    video = cv2.VideoCapture('charran.avi')
# Define the antecedents and consequent
size_input = ctrl.Antecedent(np.arange(0, 101, 1), 'size_input')
weight = ctrl.Antecedent(np.arange(0, 101, 1), 'weight')
rice_quality = ctrl.Consequent(np.arange(0, 9, 1), 'rice_quality')

# Auto-membership function population is possible with .automf(2, 4, or 6)
size_input.automf(3, names=['small', 'medium', 'large'])
weight.automf(3, names=['light', 'average', 'heavy'])

# Custom membership functions can be built interactively with a familiar,
# Pythonic API
rice_quality['poor'] = fuzz.trimf(rice_quality.universe, [0, 0, 4])
rice_quality['good'] = fuzz.trimf(rice_quality.universe, [0, 4, 14])
rice_quality['excellent'] = fuzz.trimf(rice_quality.universe, [4, 12, 12])

# Define the rules
ruleA = ctrl.Rule(size_input['small'] & weight['light'], rice_quality['poor'])
ruleB = ctrl.Rule(size_input['small'] & weight['average'], rice_quality['poor'])
ruleC = ctrl.Rule(size_input['small'] & weight['heavy'], rice_quality['good'])
ruleD = ctrl.Rule(size_input['medium'] & weight['light'], rice_quality['poor'])
ruleE = ctrl.Rule(size_input['medium'] & weight['average'], rice_quality['good'])
ruleF = ctrl.Rule(size_input['medium'] & weight['heavy'], rice_quality['good'])
ruleG = ctrl.Rule(size_input['large'] & weight['light'], rice_quality['good'])
ruleH = ctrl.Rule(size_input['large'] & weight['average'], rice_quality['good'])
ruleI = ctrl.Rule(size_input['large'] & weight['heavy'], rice_quality['excellent'])
# View a single rule
ruleA.view()
# You can see how these look with .view()

size_input.view()
plt.show()
weight.view()
plt.show()
rice_quality.view()
plt.show()

# Create the control system
rice_quality_ctrl = ctrl.ControlSystem([ruleA, ruleB, ruleC, ruleD, ruleE, ruleF, ruleG, ruleH, ruleI])

# Create the simulation and store the rice quality
rice_quality_sim = ctrl.ControlSystemSimulation(rice_quality_ctrl)

# Initialize the video file and create a window
video = cv2.VideoCapture('Vi1.avi')
cv2.namedWindow('Rice Quality', cv2.WINDOW_NORMAL)


def get_rice_size(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    while True:

        # Read a frame from the video
        ret, frame = video.read()
        # Calibration factor (pixels per millimeter)
        calibration_factor = 0.1
        # Stop if the video has ended
        if not ret:
            break

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
            x, y, w, h = cv2.boundingRect(contour)
            rice_quality_sim.input['size_input'] = w
            rice_quality_sim.input['weight'] = h
            rice_quality_sim.compute()
            rice_quality_value = rice_quality_sim.output['rice_quality']
            # Filter out small contours (adjust the threshold as needed)
            if area > 100:
                # Compute the perimeter of the contour
                perimeter = cv2.arcLength(contour, True)

                # Approximate the contour as a polygon
                approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

                # Compute the bounding box of the contour
                x, y, w, h = cv2.boundingRect(approx)

                # Calculate width, length, and area in millimeters using the calibration factor
                width_mm = w * calibration_factor
                length_mm = h * calibration_factor
                area_mm2 = area * (calibration_factor ** 2)

                # Set the color of the bounding box and text based on the area
                if area < 6000:
                    color = (0, 0, 255)  # red for small rice
                elif area < 7000:
                    color = (255, 0, 0)  # blue for medium rice
                else:
                    color = (0, 255, 0)  # green for large rice

                # Draw the bounding box on the frame
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                # Display the width, length, and area on the frame
                text = f" Area: {area_mm2:.2f} mm^2"
                cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        # Display the frame
        cv2.imshow('Rice Sizes', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object
    video.release()

    # Destroy all windows
    cv2.destroyAllWindows()
rice_quality.view(sim=rice_quality_sim)
plt.show()
# Path to the input video
video_path = 'charran.avi'
# Process the video and display rice sizes
get_rice_size(video_path)
video.release()
cv2.destroyAllWindows()





