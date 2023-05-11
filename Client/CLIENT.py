import socket
from inputimeout import inputimeout
import mediapipe as mp
import cv2
import numpy as np
import copy
import itertools
from collections import deque, Counter
import tensorflow as tf
import threading

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

actions = ['stop', 'goLeft', 'goRight', 'modeDiaPo', 'modeNormal']
poses = ['left-right', 'up-down', 'stop']
message = ['lwlhada']

def mediapipe_detection(image, model):
    image = cv2.flip(image, 1)
    debug_image = copy.deepcopy(image)
    # COLOR CONVERSION BGR 2 RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = model.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image, results, debug_image


def pre_process_landmark(landmark_list):
    temporarly_landmark_list = copy.deepcopy(landmark_list)

    # Convert to relative coordinates
    base_x, base_y = 0, 0
    for index, landmark_point in enumerate(temporarly_landmark_list):
        if index == 0:
            base_x, base_y = landmark_point[0], landmark_point[1]

        temporarly_landmark_list[index][0] = temporarly_landmark_list[index][0] - base_x
        temporarly_landmark_list[index][1] = temporarly_landmark_list[index][1] - base_y

    temporarly_landmark_list = list(
        itertools.chain.from_iterable(temporarly_landmark_list))
    max_value = max(list(map(abs, temporarly_landmark_list)))

    def normalize_(n):
        return n / max_value
    temporarly_landmark_list = list(map(normalize_, temporarly_landmark_list))
    return temporarly_landmark_list


def calc_landmark_list(image, landmarks):
    image_width, image_height = image.shape[1], image.shape[0]

    landmark_point = []

    # キーポイント
    for _, landmark in enumerate(landmarks.landmark):
        landmark_x = min(int(landmark.x * image_width), image_width - 1)
        landmark_y = min(int(landmark.y * image_height), image_height - 1)
        # landmark_z = landmark.z

        landmark_point.append([landmark_x, landmark_y])

    return landmark_point


def pre_process_Keypoint_history(image, point_history):
    image_width, image_height = image.shape[1], image.shape[0]

    temp_point_history = copy.deepcopy(point_history)

    base_x, base_y = 0, 0
    for index, point in enumerate(temp_point_history):
        if index == 0:
            base_x, base_y = point[0], point[1]

        temp_point_history[index][0] = (temp_point_history[index][0] -
                                        base_x) / image_width
        temp_point_history[index][1] = (temp_point_history[index][1] -
                                        base_y) / image_height

    temp_point_history = list(
        itertools.chain.from_iterable(temp_point_history))

    return temp_point_history

##################################################################


class PoseClassifier(object):
    def __init__(
        self,
        model_path='Model/Sign_classifier_MetaData.tflite',
        num_threads=1,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def __call__(
        self,
        landmark_list,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([landmark_list], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        return result_index


class Classifier(object):
    def __init__(
        self,
        model_path='Model/Gestures_classifier_MetaData.tflite',
        score_th=0.8,
        invalid_value=0,
        num_threads=1,
    ):
        self.interpreter = tf.lite.Interpreter(model_path=model_path,
                                               num_threads=num_threads)

        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.score_th = score_th
        self.invalid_value = invalid_value

    def __call__(
        self,
        point_history,
    ):
        input_details_tensor_index = self.input_details[0]['index']
        self.interpreter.set_tensor(
            input_details_tensor_index,
            np.array([point_history], dtype=np.float32))
        self.interpreter.invoke()

        output_details_tensor_index = self.output_details[0]['index']

        result = self.interpreter.get_tensor(output_details_tensor_index)

        result_index = np.argmax(np.squeeze(result))

        if np.squeeze(result)[result_index] < self.score_th:
            result_index = self.invalid_value

        return result_index


Pose_classifier = PoseClassifier()
keypoint_classifier = Classifier()

##################################################################
history_length = 16  # lenght of list that takes max indexes of predections
Keypoints_history = deque(maxlen=history_length)
Argmax_list = deque(maxlen=history_length)
use_boundary_recttangle = True

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 540)
most_common_fg_id = None
ActionDetected = 0
class Client:
    def __init__(self):
        self.chivariable = False
        self.addr = ""
        self.thread1 = threading.Thread(target=self.Ai)
        self.thread2 = None
        self.message = ""

    def tcpp(self, addr):
        while True:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                clientSocket.connect((addr[0], 9090))
                while True:
                    try:
                        data = self.message
                        clientSocket.send(data.encode())
                    except:
                        rp, addr = clientSocket.recvfrom(1024)

                        break
            except:
                break
            break
        return 0

    def Ai(self):
        # code for the Ai() function goes here
        with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5, max_num_hands=1) as hands:

            while cap.isOpened():
                key = cv2.waitKey(10)
                if key == 27:
                    break

                ret, frame = cap.read()
                if not ret:
                    break

                # Make detections
                image, results, debug_image = mediapipe_detection(frame, hands)
                if results.multi_hand_landmarks:
                    for hand_landmarks, handedness in zip(results.multi_hand_landmarks,
                                                          results.multi_handedness):

                        # Landmark calculation
                        landmark_list = calc_landmark_list(
                            debug_image, hand_landmarks)

                        # Conversion to relative coordinates / normalized coordinates
                        pre_processed_landmark_list = pre_process_landmark(
                            landmark_list)
                        pre_processed_Keypoints_list = pre_process_Keypoint_history(
                            debug_image, Keypoints_history)

                        hand_id = Pose_classifier(pre_processed_landmark_list)

                        hand_sign_id = 0
                        hand_sign_len = len(pre_processed_Keypoints_list)
                        
                        if hand_id in (0, 1):
                            landmark_index = 8 if hand_id == 0 else 12
                            Keypoints_history.append(
                                landmark_list[landmark_index])
                        else:
                            Keypoints_history.append([0, 0])

                        if hand_sign_len == (history_length * 2):
                            hand_sign_id = keypoint_classifier(
                                pre_processed_Keypoints_list)

                        action_detected = [
                            1, 2,0] if hand_id == 0 else [3, 4,0]
                        Argmax_list.append(hand_sign_id)
                        most_common_fg_id = Counter(
                            Argmax_list).most_common()
                        ActionDetected = most_common_fg_id[0][0] if most_common_fg_id[0][0] in action_detected else 0
                        if (message[-1] != actions[ActionDetected]):
                            print(message[-1])
                            message.append(actions[ActionDetected])
                            message.append(actions[ActionDetected])
                            if message[-1] == "goLeft":
                                self.message = actions[ActionDetected]
                            elif message[-1] == "goRight":
                                self.message = actions[ActionDetected]
                            elif message[-1] == "modeDiaPo":
                                self.message = actions[ActionDetected]
                            elif message[-1] == "modeNormal":
                                self.message = actions[ActionDetected]
                            elif message[-1] == "stop":
                                self.message = actions[ActionDetected]

                     

                    cv2.imshow('Hand Gesture Recognition', debug_image)

        cap.release()

        cv2.destroyAllWindows()
        pass

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("0.0.0.0", 5005))
        while True:
            data, self.addr = sock.recvfrom(1024)
            resp = b'response'
            if (data == resp):
                if not self.chivariable:
                    self.thread2 = threading.Thread(
                        target=self.tcpp, args=(self.addr,))
                    self.thread2.start()
                    # self.thread2.start()
                    self.thread1.start()
                    self.chivariable = True


client = Client()
client.start()
