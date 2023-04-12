import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt
from itertools import combinations
import time
fings=[""]
for q in range(1,6):
    fins=[''.join(p) for p in combinations(["I", "M", "R", "P", "T"], q)]
    fings=fings+fins
# d = {ni: indi for indi, ni in enumerate(set(fings))}
# numbers = [d[ni] for ni in fings]
# print(fings)
# print(len(numbers))

def publish(fin):

    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Publish a message to the topic
        client.publish("python/test", "hello")

    # Create a MQTT client instance
    client = mqtt.Client()
    client.on_connect = on_connect

    # Set your broker address and port number
    client.connect("mqtt.eclipseprojects.io", 1883, 60)
    client.publish("python/test", fin)


mp_drawing = mp.solutions.drawing_utils
mp_holistic = mp.solutions.holistic
# For webcam input:
mp_hands = mp.solutions.hands
cap = cv2.VideoCapture(0)
symbol=""

def yo(symbol):
    publish(33)
    # cv2.putText(image, (symbol), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)

def fingers(value,fin):
    index=fings.index(fin)
    publish(index)
    # fps = str(value) + ' fingers'
    # cv2.putText(image, (fps), (0, 25), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 3)
    # cv2.putText(image, (fin), (0, 60), cv2.FONT_HERSHEY_PLAIN, 2, (10, 10, 0), 2)

with mp_hands.Hands(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB) #to flip the image to selfie mode
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        image_height, image_width, _ = image.shape
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                left_thumb_count=0
                right_thumb_count=0
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                pinky_tip=hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y
                pinky_dip=hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_DIP].y
                index_tip=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                index_dip=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_DIP].y
                middle_tip=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                middle_dip=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_DIP].y
                ring_tip= hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y
                ring_dip= hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_DIP].y
                thumb_tip=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
                thumb_ip=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
                thumb_landmarks = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                left_thumb_count=0
                right_thumb_count=0


                '''print(
                    f'mid: (',
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image_width}, '
                    f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
                )'''
                fin=''
                if ((pinky_tip < pinky_dip) and (index_tip < index_dip) and (ring_tip > ring_dip) and (middle_tip > middle_dip)):
                    yo("Yo")
                else:
                    if index_tip > index_dip:
                        val1 = 0

                    else:
                        val1 = 1
                        fin ='I'

                    if middle_tip > middle_dip:
                        val2 = 0
                    else:
                        val2 = 1
                        fin += 'M'

                    if ring_tip > ring_dip:
                        val3 = 0
                    else:
                        val3 = 1
                        fin += 'R'
                    if pinky_tip > pinky_dip:
                        val4 = 0
                    else:
                        val4 = 1
                        fin += 'P'

                    # Determine if the thumb is on the left or right hand
                    if thumb_landmarks.x < 0.5:
                        left_thumb_count = 1
                        fin+='T'
                        right_thumb_count=0
                    else:
                        left_thumb_count=0
                        # right_thumb_count = 1
                        # fin+='Thumb'
                        # left_thumb_count=0
                    val=val1+val2+val3+val4+left_thumb_count+right_thumb_count
                    fingers(val, fin)

            if results.multi_handedness[0].classification[0].label == 'Left':
                print('Left hand finger count:', val)
            if results.multi_handedness[0].classification[0].label == 'Right':
                print('Right hand finger count:', val)

        cv2.imshow('MediaPipe Hands', image)

        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()