# Import the necessary Packages for this software to run
import mediapipe 
import cv2 
from collections import Counter

# pip install mediapipe opencv-python


# Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands
mod = handsModule.Hands()

# Use CV2 Functionality to create a Video stream and add some values
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

tip = [8, 12, 16, 20]
fingers = []
finger = []

h = 720
w = 1080


def findpostion(frame1):
    list = []
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:
            drawingModule.draw_landmarks(
                frame1, handLandmarks, handsModule.HAND_CONNECTIONS)
            list = []
            for id, pt in enumerate(handLandmarks.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                list.append([id, x, y])

    return list


def findnameoflandmark(frame1):
    list = []
    results = mod.process(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks != None:
        for handLandmarks in results.multi_hand_landmarks:

            for point in handsModule.HandLandmark:
                list.append(str(point).replace("< ", "").replace(
                    "HandLandmark.", "").replace("_", " ").replace("[]", ""))
    return list


# Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
# image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
# More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2) as hands:

    # Create an infinite loop which will produce the live feed to our desktop and that will search for hands
    while True:
        ret, frame = cap.read()
        # Unedit the below line if your live feed is produced upsidedown
        # flipped = cv2.flip(frame, flipCode = -1)

        # Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
        frame1 = cv2.resize(frame, (640, 480))

        a = findpostion(frame1)
        b = findnameoflandmark(frame1)

        if len(b and a) != 0:
            finger = []
            if a[0][1:] < a[4][1:]:
                finger.append(1)
                print(b[4])
            else:
                finger.append(0)

            fingers = []
            for id in range(0, 4):
                if a[tip[id]][2:] < a[tip[id]-2][2:]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        x = fingers + finger
        c = Counter(x)
        up = c[1]
        down = c[0]
        if (up > 0):
            print(up)

        # Below shows the current frame to the desktop
        cv2.imshow("Frame", frame1)
        key = cv2.waitKey(1) & 0xFF

        # Below states that if the |q| is press on the keyboard it will stop the system
        if key == ord("q"):
            break
