import subprocess
import cv2 as cv
import numpy as np
import mediapipe as mp
import math
import tkinter as tk

from tkinter import messagebox

# Define the commands to execute the Python scripts
cmd_abv = ['python', 'EyestressFinal.py']
cmd_xyz = ['python', 'heartrate.py']
cmd_test = ['python', 'posturefinal.py']

# Start the subprocesses to run the scripts in parallel
proc_abv = subprocess.Popen(cmd_abv)
proc_xyz = subprocess.Popen(cmd_xyz)
proc_test = subprocess.Popen(cmd_test)

# Wait for all subprocesses to finish
proc_abv.wait()
proc_xyz.wait()
proc_test.wait()

# Print a message indicating that all scripts have finished
print('All scripts have finished running.')
