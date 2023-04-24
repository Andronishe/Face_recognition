import os
import pickle
import sys
import face_recognition
from PIL import Image
import cv2
import numpy
from read import Select

known_names = []


def train_model_by_img():
    if not os.path.exists("images"):
        print("there is no directory 'images'")
        sys.exit()

    known_face_encodings = []
    images = os.listdir("images")

    for image in images:
        face_img = face_recognition.load_image_file(f"images/{image}")
        face_enc = face_recognition.face_encodings(face_img)[0]
        known_names.append(image.split('.')[0])
        known_face_encodings.append(face_enc)

    return known_face_encodings


def detect_person_in_video(path_video, db_encoding):
    video = cv2.VideoCapture(path_video)
    result = []
    while True:
        ret, image = video.read()
        locations = face_recognition.face_locations(image)
        encodings = face_recognition.face_encodings(image, locations)
        for face_encodings in encodings:
            result = face_recognition.compare_faces(db_encoding, face_encodings)

        names_list = []

        if True in result:
            match_indexes = [i for i in range(len(result)) if result[i]]
            for ind in match_indexes:
                if known_names[ind] not in names_list:
                    names_list.append(known_names[ind])
                else:
                    continue
        else:
            names_list.append("there are no names")

        return names_list


def compare(known_encodings, img2):
    try:
        face1 = face_recognition.load_image_file(img2)
        face_enc1 = face_recognition.face_encodings(face1)[0]
        result = face_recognition.compare_faces(known_encodings, face_enc1)

        names_list = []

        if True in result:
            match_indexes = [i for i in range(len(result)) if result[i]]
            for ind in match_indexes:
                names_list.append(known_names[ind])
        else:
            names_list.append("there are no names")
    except Exception:
        return ["No faces detected on the image"]
    return names_list


# detect_person_in_video("video2.mp4", train_model_by_img("images"))
print("\n".join(compare(train_model_by_img(), "Valakas2.jpg")))