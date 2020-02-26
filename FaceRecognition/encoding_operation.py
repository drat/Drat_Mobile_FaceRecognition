import face_recognition
import os
import numpy as np
from collections import defaultdict


class Encoding:
    # this class includes methods related to encoding operations
    def __init__(self, path_faces):
        self.all_face_encodings = defaultdict(lambda: [0])
        self.face_encodings = []
        self.local_faces = path_faces
        # self.output_encodings(self.path_faces)
        # self.import_encodings()
        # self.cal_face_distance()

    def import_encodings(self):
        name_faces = os.listdir(self.local_faces)  # files of all faces
        for name_face in name_faces:
            if name_face == '.DS_Store':
                continue
            path = self.local_faces + name_face + '/' + name_face + '_encodings.txt'
            file_object = open(path)  # 文件夹目录

            for line in file_object:
                # print(line)
                self.all_face_encodings[name_face] = eval(line)    # string list to list
            # print(type(self.face_encodings))
        return self.all_face_encodings

    def update_encodings(self, unknown_encoding, update_person):
        # name_faces = os.listdir(path_faces)  # files of all faces
        self.face_encodings = []
        path = self.local_faces + update_person + '/' + update_person + '_encodings.txt'
        file_object = open(path)  # 文件夹目录

        for line in file_object:
            # print(line)
            self.face_encodings = eval(line)    # string list to list

        self.face_encodings.append(unknown_encoding.tolist())
        self.write_encodings(path, self.face_encodings)

    def write_encodings(self, path, face_encodings):
        with open(path, 'w') as file_object:
            file_object.write(str(face_encodings))
        file_object.close()
        print("\n...encodings successfully updated.")

    def output_encodings(self):
        # update all encoding files
        name_faces = os.listdir(self.local_faces)  # files of all faces
        print(name_faces)
        for name_face in name_faces:
            self.face_encodings = []
            if name_face != 'ziming' and name_face != 'fanyu':
                continue
            if name_face == '.DS_Store' :
                continue
            name = name_face
            print(name_face)
            path_name_faces = self.local_faces + name_face + '/'
            faces = os.listdir(path_name_faces)    # get all faces of a single person
            print(faces)

            # if self.check_encoding_file(name_face, faces):
            #     continue

            for face in faces:    # every single face
                if face == '.DS_Store':
                    continue
                if face == name_face + '_encodings.txt':
                    continue
                face_image = path_name_faces + face
                print(face_image)
                known_image = face_recognition.load_image_file(face_image)
                face_encoding = face_recognition.face_encodings(known_image)[0]
                # face_encoding = self.cal_encoding(face_image)
                # print(type(face_encoding))
                self.face_encodings.append(face_encoding.tolist())    # default setting is the first face

            filename = path_name_faces + name + '_encodings.txt'
            with open(filename, 'w') as file_object:
                file_object.write(str(self.face_encodings))
            file_object.close()

    def check_encoding_file(self, name_face, faces):
        test = name_face + '_encodings.txt'  # check if the encoding file exists
        # print(test)
        if test in faces:
            return True