''' this file is mainly for CLI (without Front end)'''

import multiprocessing
import os.path
import threading
import cv2
import hubconfCustom
import time
import validators
from hubconfCustom import video_detection

frames_buffer = []


def generate_raw_frames(ip_cam):
    global frames_buffer

    video_frames = cv2.VideoCapture(ip_cam)
    frame_count = 0
    start_time = time.time()

    while True:
        success, frame = video_frames.read()

        if success:
            frame_copy = frame.copy()
            frames_buffer.append(frame_copy)

        frame_count += 1
        elapsed_time = time.time() - start_time
        fps = frame_count / elapsed_time
        fps = int(fps)
        print(f"Raw FPS: {fps}")


def live_inference(ip_cam):
    global frames_buffer

    if validators.url(ip_cam):
        ip_cam = ip_cam.strip()
        video_frames = cv2.VideoCapture(ip_cam)

        if not video_frames.isOpened():
            print("Cannot connect to livestream!")
            return

        while video_frames.isOpened():
            success, frame = video_frames.read()

            if success:
                yolo_output = video_detection(0.75, frames_buffer)

                for processed_frame, total_detections in yolo_output:
                    print(f"Total number of persons detected in current frame is {total_detections}")


if __name__ == "__main__":
    ip_cam_address = "http://192.168.15.27:4747"  # input("Enter the address of the IP Camera: ")
    alert_recipient = "prakharsingh2018@gmail.com"  # input("Enter email address of alert recipient: ")
    hubconfCustom.is_email_allowed = True
    hubconfCustom.send_next_email = True
    hubconfCustom.email_recipient = alert_recipient

    thread_1 = threading.Thread(target=generate_raw_frames, args=(ip_cam_address,))
    thread_2 = threading.Thread(target=live_inference, args=(ip_cam_address,))

    thread_1.start()
    thread_2.start()

