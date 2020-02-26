import face_recognition
import os
import numpy as np
from encoding_operation import Encoding
from collections import defaultdict
import shutil


class FaceRecognition:
    def __init__(self, pic_name):
        self.all_face_encodings = defaultdict(lambda: [0])

        # Encoding.__init__(self, self.local_faces)
        self.local_faces = '/Users/apple/Face Recognition/localfaces/'
        self.encoding = Encoding(self.local_faces)
        # self.encoding.output_encodings()
        # self.update_face('ziming', '/Users/apple/Face Recognition/unknown/ziming1.jpg')

        self.cal_face_distance(pic_name)

    def cal_encoding(self, face):
        unknown_image = face_recognition.load_image_file(face)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        # print(unknown_encoding)
        return unknown_encoding

    def cal_face_distance(self, pic_name):
        # 代码待优化
        unknown_path = pic_name
        unknown_encoding = self.cal_encoding(unknown_path)
        self.all_face_encodings = self.encoding.import_encodings()
        keys = sorted(self.all_face_encodings.keys())
        print(keys)
        # print(self.all_face_encodings)
        name_sim = defaultdict(lambda: [0])
        result_name = ''
        for key_name in keys:
            results = face_recognition.face_distance(self.all_face_encodings[key_name], unknown_encoding)
            # print(self.all_face_encodings['ziming'])
            # mul = 1
            # for distance in results:
            #     mul *= distance
            # print("name: " + key + "\ndistances: " + str(results) + '\nsimilarity: ' + str(1-mul))
            sim = 1 - results.mean()
            print("\nname: " + key_name + "\ndistances: " + str(results) + '\nsimilarity: ' + str(sim))
            name_sim[key_name] = sim
            result_name = max(name_sim, key=name_sim.get)

        if self.check_result(result_name) == 'Yes':
            print("\nOkay! start updating...")
            self.encoding.update_encodings(unknown_encoding, result_name)
            self.update_face(result_name, unknown_path)
        else:
            new_name = self.get_new_name()
            encoding_filepath = self.local_faces + new_name + '/' + new_name + '_encodings.txt'
            new_encoding = []
            new_encoding.append(unknown_encoding.tolist())
            self.create_new_person(new_name)
            self.update_face(new_name, unknown_path)
            self.encoding.write_encodings(encoding_filepath, new_encoding)

    def check_result(self, result_name):
        print('\nPredicted name:' + str(result_name))
        query = input('Is this prediction correct? > Yes/No \n')
        return query

    def update_face(self, result_name, unknown_path):
        old_name = os.path.basename(unknown_path)
        order = 0
        new_path = self.local_faces + result_name + '/'
        # print(new_path)
    # transfer to local faces
        shutil.move(unknown_path, new_path)
    # get number of existing pictures
        list_filename = os.listdir(new_path)
        # print(list_filename)
        for name in list_filename:
            if name == result_name + '_encodings.txt' or name == '.DS_Store':
                continue
            else:
                order = order + 1
    # rename
        new_name = new_path + result_name + str(order) + '.png'
        old_name = new_path + old_name
        os.rename(old_name, new_name)
        print(os.listdir(new_path))
        print("\n...local databases successfully updated.")

    def get_new_name(self):
        new_name = input('\nPlease input your name: > ')
        return new_name

    def create_new_person(self, new_name):
        new_path = self.local_faces + new_name
        os.mkdir(new_path)

# rec_test = FaceRecognition('pass')
