# -*- coding:utf-8 -*-
'''
@author: xinquan
@file: set_config.py
@time: 2021/10/22 10:10
@desc: 
'''
import os
import warnings
import sys
import pickle as pkl
import json
import pandas as pd

warnings.filterwarnings('ignore')  # 忽略一些警告,可以删除
root_path = os.path.split(os.path.realpath(__file__))[0]  # 获取该脚本的地址,有效避免Linux和Windows文件路径格式不一致等问题,可以删除


class Config(object):
    def __init__(self):
        # 配置数据路径
        self.base_path = r"D:\python_program\reverse_2"
        self.data_warehouse = os.path.join(self.base_path, "src/data")


        # self.code2label_path = os.path.join(self.data_witsky_path, "data_conf", "map_code.pkl")

        """各类模型地址"""
        # if sys.platform == 'darwin':
        #     self.model_path = r'/Users/zhuxinquan/Desktop/data/model'
        # elif self.is_exist(r'/data/nlp/data_origin/model'):
        #     self.model_path = r'/data/nlp/data_origin/model'
        # else:
        #     self.model_path = r'/0324/nlp/data_origin/model'
        # self.pretrain_path = os.path.join(self.model_path, 'pretraining_model')
        # self.model_hubert = os.path.join(self.pretrain_path, "audio_model", "chinese-hubert-base")
        # self.model_path_ft = os.path.join(self.model_path, 'project_model', "audio")
        # self.model_path_thq_ft = os.path.join('/data/thq/ring_tone/audioclassification-hubert-main/model', 'project_model', "audio")

    @staticmethod
    def is_exist(path, mkdir=False):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            if mkdir:
                os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
            # print("该路径不存在")
            return False
        else:
            # print("该路径存在")
            return True

    @staticmethod
    def load_data_pkl(data_path: str):
        fopen_pkl = open(data_path, 'rb')
        target_data = pkl.load(fopen_pkl)
        return target_data

    @staticmethod
    def dump_data_pkl(target_data, data_path):
        fopen = open(data_path, 'wb')
        pkl.dump(target_data, fopen)

    def read_data(self, file_path: str):
        if file_path.endswith("xlsx"):
            task_data = pd.read_excel(file_path, keep_default_na=False)
            return task_data
        elif file_path.endswith("csv"):
            task_data = pd.read_csv(file_path, keep_default_na=False)
            return task_data

        elif file_path.endswith("pkl"):
            task_data = self.load_data_pkl(file_path)
            return task_data
        elif file_path.endswith("json"):
            fopen_json = open(file_path, 'r')
            json_data = json.load(fopen_json)
            return json_data

        else:
            return "数据格式不支持"

    def dumps_data(self, input_data, file_path: str):
        if file_path.endswith("xlsx"):
            task_data = input_data.to_excel(file_path, index=False)
            return task_data
        elif file_path.endswith("csv"):
            task_data = input_data.to_csv(file_path, index=False)
            # print("完成:{}".format(file_path))
            return task_data

        elif file_path.endswith("pkl"):
            self.dump_data_pkl(input_data, file_path)
            return
        elif file_path.endswith("json"):
            fopen = open(file_path, 'w')
            json.dump(input_data, fopen, indent=-1)
        else:
            return "数据格式不支持"

    def merge_pd(self, find_path, output_path):
        from tqdm import tqdm
        import glob
        print("find_path:", find_path)
        all_path = glob.glob(find_path + '/*.csv')
        print(len(all_path))
        result_list = []
        for iter_index in tqdm(range(len(all_path))):
            one_path = all_path[iter_index]
            tmp_pd = self.read_data(one_path)
            result_list.append(tmp_pd)
        result_pd = pd.concat(result_list)
        print(len(result_pd))
        self.dumps_data(result_pd, output_path)

    @staticmethod
    def cut_pd(list_temp, n):
        result_list = []
        for i in range(0, len(list_temp), n):
            result_list.append(list_temp[i:i + n])
        return result_list

    def func_read(self, task_id: int, input_path: str):
        task_file = self.read_data(input_path)
        print("完成:{}/{}".format(task_id, input_path))
        return task_file


Config_base = Config()
if __name__ == '__main__':
    Config_base.merge_pd(r"/Users/zhuxinquan/Desktop/project_witsky/AudioClassification-Hubert/data_witsky/result_0607",
                         r"/Users/zhuxinquan/Desktop/project_witsky/AudioClassification-Hubert/data_witsky/data_val/val_result_0607_1.csv")



"""
/Users/zhuxinquan/Desktop/data/model/project_model/audio/hubert_c1_0527_1
/Users/zhuxinquan/Desktop/data/model/project_model/audio/hubert_c1_0527_1

"""