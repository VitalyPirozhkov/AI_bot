import cv2
import math

face_prototype = "./data/opencv_face_detector.pbtxt"
face_model = "./data/opencv_face_detector_uint8.pb"
gender_prototype = "./data/gender_deploy.prototxt"
gender_model = "./data/gender_net.caffemodel"

gender_list = ["Сушество мужского пола", "Сушество женского пола"]

face_net = cv2.dnn.readNet(face_model, face_prototype)
gender_net = cv2.dnn.readNet(gender_model, gender_prototype)

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)


def highlight_face(net, frame, threshold=0.7):
    frame_opencv_dnn = frame.copy()
    height = frame_opencv_dnn.shape[0]
    width = frame_opencv_dnn.shape[1]
    blob = cv2.dnn.blobFromImage(frame_opencv_dnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    face_boxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > threshold:
            x1 = int(detections[0, 0, i, 3] * width)
            y1 = int(detections[0, 0, i, 4] * height)
            x2 = int(detections[0, 0, i, 5] * width)
            y2 = int(detections[0, 0, i, 6] * height)
            face_boxes.append([x1, y1, x2, y2])
    return frame_opencv_dnn, face_boxes


def resolve(image):
    video = cv2.VideoCapture(image if image else 0)
    padding = 20

    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()

        if not hasFrame:
            cv2.waitKey()
            break

        result_img, face_boxes = highlight_face(face_net, frame)
        if not face_boxes:
            print("no face detected")

        genders = []
        for facebox in face_boxes:
            face = frame[max(0, facebox[1] - padding): min(facebox[3] + padding, frame.shape[0] - 1),
                   max(0, facebox[0] - padding): min(facebox[2] + padding, frame.shape[1] - 1)]

            blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
            gender_net.setInput(blob)
            gender_predictions = gender_net.forward()

            gender = gender_list[gender_predictions[0].argmax()]
            genders.append(gender)
        return genders
