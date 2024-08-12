# Importing Liabrary for Iris detection


import cv2 as cv
import numpy as np
import mediapipe as mp
import math
import tkinter as tk
from tkinter import messagebox

L_eye = [362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398]
R_eye = [33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 246]
right_iris = [474, 475, 476, 477]
left_iris = [469, 470, 471, 472]
L_leftmost = [33]  # right eye right most landmark
L_rightmost = [133]  # right eye left most landmark
R_leftmost = [362]  # left eye right most landmark
R_rightmost = [263]  # left eye left most landmark
look_center_time = 0

def euclidian_distance(point_1, point_2):
    x1, y1 = point_1.ravel()  # Return contineous 1D array
    x2, y2 = point_2.ravel()
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# Create a Tkinter window for the pop-up message
root = tk.Tk()
root.withdraw()
def eye_ratio(center, right_pos, left_pos):
    global look_center_time
    center_to_right_dist = euclidian_distance(center, right_pos)
    Total_dis = euclidian_distance(right_pos, left_pos)
    ratio = center_to_right_dist / Total_dis
    iris_position = ""
    if ratio <= 0.42:
        iris_position = "right"
        look_center_time = 0
    elif ratio > 0.42 and ratio <= 0.57 :
        iris_position = "center"
        look_center_time += 1
        if look_center_time == 100 :
            # Show a pop-up message if the user has been looking at the center for 5 minutes
            message = "Warning: You have been looking at the center for 30 sce Please Take Break !"
            messagebox.showwarning("Warning", "You have been looking at the center for 30 sec Please Take Break !")

    else:
        iris_position = "left"
        look_center_time = 0


    return iris_position, ratio
def timer_thread():
    global look_center_time
    while True:
        time.sleep(1)
        if look_center_time > 0:
            print(f"Time spent looking at center: {look_center_time} seconds")



mp_face_mesh = mp.solutions.face_mesh
cap = cv.VideoCapture(0)
with mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                           min_tracking_confidence=0.5) as face_mesh:
    while True:
        ret, frame = cap.read()  # ret is for camera avilibility
        if not ret:
            break
        frame = cv.flip(frame, 1)
        rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            # print(results.multi_face_landmarks[0].landmark)
            mesh_points = np.array(
                [np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])
            # print(mesh_points.shape)
            (l_cx, l_cy), l_radius = cv.minEnclosingCircle(mesh_points[left_iris])
            (r_cx, r_cy), r_radius = cv.minEnclosingCircle(mesh_points[right_iris])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)
            cv.circle(frame, center_left, int(l_radius), (0, 0, 255), 1, cv.LINE_AA)
            cv.circle(frame, center_right, int(r_radius), (0, 0, 255), 1, cv.LINE_AA)
            cv.circle(frame, mesh_points[L_leftmost][0], 2, (255, 0, 255), -1, cv.LINE_AA)
            cv.circle(frame, mesh_points[L_rightmost][0], 2, (0, 255, 255), -1, cv.LINE_AA)

            iris_posi, ratio = eye_ratio(center_right, mesh_points[R_rightmost], mesh_points[R_leftmost][0])

            print(iris_posi)
        cv.imshow('img', frame)
        key = cv.waitKey(1)
        _, frame = cap.read()
        frame_h, frame_w, _ = frame.shape
        output = face_mesh.process(rgb_frame)
        landmark_points = output.multi_face_landmarks
        landmarks = landmark_points[0].landmark
        left = [landmarks[145], landmarks[159]]

        if (left[0].y - left[1].y) < 0.004:
            look_center_time=0

        if key == ord('e') == ord('e'):  # this method is for making waitkey in Unicode
            break
cap.release()
cv.destroyAllWindows()