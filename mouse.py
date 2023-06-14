import cv2
import mediapipe as mp
import pyautogui
import numpy as np

cap = cv2.VideoCapture(0)

hand_detector = mp.solutions.hands.Hands()

drawing_utils = mp.solutions.drawing_utils

screen_width, screen_height = pyautogui.size()

index_y = 0

green_lower = np.array([40, 40, 40])
green_upper = np.array([70, 255, 255])


while True:
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame_height, frame_width, _ = frame.shape

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    output = hand_detector.process(rgb_frame)


    ####
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, green_lower, green_upper)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        area = cv2.contourArea(c)
        if area > 300:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            pyautogui.moveTo((screen_width/frame_width*x), (screen_width/frame_width*y))

    ####

    # Hand detect
    
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                
                if id == 0:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    wrist_x = screen_width/frame_width*x
                    wrist_y = screen_height/frame_height*y
                    # pyautogui.moveTo(wrist_x, wrist_y)

                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y

                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    print('outside', abs(index_y - thumb_y))
                    if abs(index_y - thumb_y) < 15:
                        pyautogui.mouseDown()
                    elif abs(index_y - thumb_y) > 30:
                        pyautogui.mouseUp()
                        

                # # if id == 8:
                # #     break
    
    # No more hand detect
    
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)