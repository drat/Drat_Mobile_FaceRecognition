import face_recognition
import os
import numpy as np
from collections import defaultdict

class FaceRecognition:
    def __init__(self):
        self.all_face_encodings = defaultdict(lambda: [0])
        self.face_encodings = []
        self.path_faces = '/Users/apple/Face Recognition/examples/'
        self.file_process(self.path_faces)
        self.open_file()

        self.cal_face_distance()

    def file_process(self, path_faces):
        name_faces = os.listdir(path_faces)  # files of all faces
        for name_face in name_faces:
            self.face_encodings = []
            # if name_face != 'ziming' :
            #     continue
            if name_face == '.DS_Store' :
                continue
            name = name_face
            print(name_face)
            path_name_faces = path_faces + name_face + '/'
            faces  = os.listdir(path_name_faces)    # get all faces of a single person
            print(faces)
            test = name_face + '_encodings.txt'
            print(test)
            if test in faces:
                continue
            for face in faces:    # every single face
                if face == '.DS_Store':
                    continue
                # print(face)
                if face == name_face + '_encodings.txt':
                    continue
                face_image = path_name_faces + face
                print(face_image)
                known_image = face_recognition.load_image_file(face_image)
                face_encoding = face_recognition.face_encodings(known_image)[0]
                # print(type(face_encoding))
                self.face_encodings.append(face_encoding.tolist())    # the first face

            # print(self.face_encodings)
            # self.all_face_encodings[name] = self.face_encodings
            # print(self.all_face_encodings)

            filename = path_name_faces + name + '_encodings.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.face_encodings))

    def open_file(self):
        name_faces = os.listdir(self.path_faces)  # files of all faces
        for name_face in name_faces:
            if name_face == '.DS_Store':
                continue
            path = '/Users/apple/Face Recognition/examples/' + name_face + '/' + name_face + '_encodings.txt'
            file_object = open(path)  # 文件夹目录

            for line in file_object:
                # print(line)
                self.all_face_encodings[name_face] = eval(line)    # string list to list
            # print(type(self.face_encodings))

        # self.all_face_encodings[name] = file_object.
        # print(self.all_face_encodings[name])

    def cal_face_distance(self):
        unknown_image = face_recognition.load_image_file('/Users/apple/Face Recognition/unknown/unknown-cherry.jpg')
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        keys = sorted(self.all_face_encodings.keys())
        # print(keys)
        # print(self.all_face_encodings)
        for key in keys:
            results = face_recognition.face_distance(self.all_face_encodings[key], unknown_encoding)
        # print(self.all_face_encodings['ziming'])
            mul = 1
            for distance in results:
                mul *= distance
            print("name: " + key + "\ndistances: " + str(results) + '\nsimilarity: ' + str(1-mul))



test = FaceRecognition()