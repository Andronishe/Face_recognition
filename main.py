import os
import pickle
import sys
import face_recognition
from PIL import Image
import cv2
import numpy
from read import Select


def compare(img1, img2):
    face = face_recognition.load_image_file(img1)
    face_enc = face_recognition.face_encodings(face)[0]

    face1 = face_recognition.load_image_file(f"images/{img2}")
    face_enc1 = face_recognition.face_encodings(face1)[0]
    print(face_recognition.compare_faces([face_enc], face_enc1))


def train_model_by_img(folder_name):
    if not os.path.exists(folder_name):
        print("there is no directory 'images'")
        sys.exit()

    images_encodings = {}
    images = os.listdir(folder_name)

    for image in images:

        face_img = face_recognition.load_image_file(f"images/{image}")
        face_enc = face_recognition.face_encodings(face_img)[0]
        images_encodings[image.split('.')[0]] = face_enc

    return images_encodings


def detect_person_in_video(path_video, db_encoding: dict):
    video = cv2.VideoCapture(path_video)
    result = []
    while True:
        ret, image = video.read()
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        for face_encodings, face_locations in zip(encodings, locations):
            for name, enc in db_encoding.items():
                if face_recognition.compare_faces(enc, face_encodings):
                    result.append(name)
                    # db_encoding.pop(name)

    return result


if __name__ == "__main__":
    train_model_by_img("andrey")
    # db_enc = train_model_by_img("images")
    # extracting_faces("images/Jmishenko.jpg")
    # print(detect_person_in_video("video2.mp4", db_enc))

