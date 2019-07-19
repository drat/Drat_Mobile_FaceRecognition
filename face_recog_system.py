import face_recognition
import os
import numpy as np
from encoding_operation import EncodingOperation
from collections import defaultdict
import shutil


class FaceRecognition:
    def __init__(self):
        self.all_face_encodings = defaultdict(lambda: [0])
        # Encoding.__init__(self, self.local_faces)
        self.local_faces = '/Users/apple/Face Recognition/localfaces/'
        self.encoding = EncodingOperation(self.local_faces)
        self.unknown_encoding = []
        self.unknown_path = ''
        self.result_name = ''
        # self.system_test()

    def face_feature_extraction(self, face):
        unknown_image = face_recognition.load_image_file(face)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
        # print(unknown_encoding)
        return unknown_encoding

    def face_classification(self, pic_name):
        self.unknown_path = pic_name
        self.unknown_encoding = self.face_feature_extraction(self.unknown_path)
        self.all_face_encodings = self.encoding.import_encodings()
        keys = sorted(self.all_face_encodings.keys())
        print(keys)
        name_sim = defaultdict(lambda: 0)
        for key_name in keys:
            results = face_recognition.face_distance(self.all_face_encodings[key_name], self.unknown_encoding)
            avg_sim = 1 - results.mean()
            print("\nname: " + key_name + "\ndistances: " + str(results) + '\naverage similarity: ' + str(avg_sim))
            name_sim[key_name] = avg_sim

        self.result_name = max(name_sim, key=name_sim.get)
        num = name_sim[self.result_name]
        if num < 0.6:
            max_name_sim = 'new_user'
        else:
            max_name_sim = self.result_name + "_" + str(round(num, 4))

        return max_name_sim

    def update_system(self, feedback, unknown_encoding, result_name, unknown_path):
        if feedback == 'confirm':
            print("\nOkay! start updating...")
            self.encoding.update_encodings(unknown_encoding, result_name)
            self.update_face(result_name, unknown_path)
        else:
            new_name = feedback
            encoding_file_path = self.local_faces + new_name + '/' + new_name + '_encodings.txt'
            new_encoding = []
            new_encoding.append(unknown_encoding.tolist())
            if new_name not in os.listdir(self.local_faces):
                self.create_new_person(new_name)
            self.update_face(new_name, unknown_path)
            self.encoding.write_encodings(encoding_file_path, new_encoding)

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
        # print(os.listdir(new_path))
        print("\n...local databases successfully updated.")

    def create_new_person(self, new_name):
        new_path = self.local_faces + new_name
        os.mkdir(new_path)

    def system_test(self):
        # print(rec_test.face_classification('/Users/apple/Face Recognition/unknown/unknown_linlin.png'))
        # print(self.face_classification('/Users/apple/Face Recognition/ziming6.png'))
        self.encoding.output_encodings()

# rec_test = FaceRecognition()