import tkinter as tk
import subprocess
from tkinter import filedialog
import cv2


def run_main_file():
    output_text.delete(1.0, tk.END)
    output = subprocess.check_output(['python', 'priya.py'])
    output_text.insert(tk.END, output)

def run_other_file():
    video_path = r"C:\Users\Abc\PycharmProjects\pythonProject\rice.mp4"

    # Open video file
    cap = cv2.VideoCapture(video_path)

    # Loop over frames in video
    while True:
        # Read frame
        ret, frame = cap.read()
        if not ret:
            break

        # Display frame
        cv2.imshow("Video", frame)
        if cv2.waitKey(1) == ord('q'):
            break

def run_third_file():
    output_text.delete(1.0, tk.END)
    output = subprocess.check_output(['python', 'main.py'])
    output_text.insert(tk.END, output)

def run_fourth_file():
    output_text.delete(1.0, tk.END)
    output = subprocess.check_output(['python', 'heart.py'])
    output_text.insert(tk.END, output)

def run_fifth_file():
    output_text.delete(1.0, tk.END)
    output = subprocess.check_output(['python', 'new.py'])
    output_text.insert(tk.END, output)

def run_six_file():
    output_text.delete(1.0, tk.END)
    output = subprocess.check_output(['python', 'heart.py'])
    output_text.insert(tk.END, output)


# create the main window
root = tk.Tk()
# set window size
root.geometry("700x400")
# create the label widget
label = tk.Label(root, text="Rice Grains Analysis", font=("Helvetica", 20))

# # arrange the label widget in a grid
# label.grid(row=0, column=0, columnspan=2)

# create the buttons
button1 = tk.Button(root, text="Detecting type of rice grains", command=run_main_file, width=20, height=5)
button2 = tk.Button(root, text="Detect rice grains using AI", command=run_other_file, width=20, height=5)
button3 = tk.Button(root, text="Total count of rice grains", command=run_third_file, width=20, height=5)
button4 = tk.Button(root, text="Count of rice grains using AI", command=run_fourth_file, width=20, height=5)
button5 = tk.Button(root, text="Measurements of the rice",command=run_fifth_file, width=20, height=5)
button6 = tk.Button(root, text="Measurements using AI",command=run_six_file, width=20, height=5)
button7 = tk.Button(root, text="Button 7", width=20, height=5)
button8 = tk.Button(root, text="Button 8", width=20, height=5)

# create the output text widget
output_text = tk.Text(root, height=10)

# arrange the label widget in a grid
label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# arrange the buttons and output text widget in a grid
button1.grid(row=1, column=0, padx=10, pady=10)
button2.grid(row=1, column=1, padx=10, pady=10)
button3.grid(row=1, column=2, padx=10, pady=10)
button4.grid(row=1, column=3, padx=10, pady=10)
button5.grid(row=2, column=0, padx=10, pady=10)
button6.grid(row=2, column=1, padx=10, pady=10)
button7.grid(row=2, column=2, padx=10, pady=10)
button8.grid(row=2, column=3, padx=10, pady=10)
# output_text.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

# output_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

# run the main loop
root.mainloop()
