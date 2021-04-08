# -*- coding: utf-8 -*-
# @Time     : 2021/3/31 10:13
# Author    : YangLiu
# @Site     : 
# @File     : extra_tree_test.py
# @Software :
import numpy as np
import pandas as pd
import openpyxl as op
import tqdm as tqdm
from sklearn.tree import DecisionTreeClassifier
from sklearn import model_selection
import matplotlib.pyplot as plt
import csv
import pandas as pd
import os


class Fame2(object):

    def __init__(self, file_path):
        self.file_path = file_path

    @staticmethod
    def descriptor():
        """
        挑出有用的数据
        """
        Atom_type = ['Br', 'C.1', 'C.2', 'C.3', 'C.ar', 'Cl', 'F', 'I', 'N.1', 'N.2', 'N.3',
                     'N.4', 'N.am', 'N.ar', 'N.pl3', 'O.2', 'O.3', 'P.3', 'S.2', 'S.3', 'S.O2', 'S.O']
        QC = ['piS(r)', 'De(r)', 'Dn(r)', 's-Pop', 'p-Pop', 'NumOfElecs', 'NetCharge',
              'valence', 'mull_charge', 'mull_pop']
        CDK = ['effectiveAtomPolarizability', 'stabilizationPlusCharge', 'sigmaElectronegativity',
               'piElectronegativity', 'partialSigmaCharge', 'partialTChargeMMFF94',
               'atomDegree', 'atomValence', 'atomHybridizationVSEPR', 'atomHybridization',
               'longestMaxTopDistInMolecule', 'highestMaxTopDistInMatrixRow', 'diffSPAN', 'relSPAN']
        CYP = ['1A2', '1A2_1', '1A2_2', '1A2_3', '2A6', '2A6_1', '2A6_2', '2A6_3',
               '2B6', '2B6_1', '2B6_2', '2B6_3', '2C19', '2C19_1', '2C19_2', '2C19_3',
               '2C8', '2C8_1', '2C8_2', '2C8_3', '2C9',	'2C9_1', '2C9_2', '2C9_3',
               '2D6', '2D_1', '2D6_2', '2D6_3',	'2E1',	'2E1_1', '2E1_2', '2E1_3',
               '3A4', '3A4_1', '3A4_2', '3A4_3', 'HLM']
        cir_QC = {'xuhao': 0}
        header = ['xuhao']
        descriptors = [{}]
        for qc in QC:
            for at in Atom_type:
                cir_QC[qc+'_'+at+'_3'] = 0
                header.append(qc+'_'+at+'_3')
        for cdk in CDK:
            cir_QC[cdk] = 0
            header.append(cdk)
        cir_QC['1A2'] = 0
        header.append('1A2')

        file_location = 'D:/dmpk/FMAE/fame2data/dataset_concatenated_flipper_1conf_mldata_unique.csv'
        new_file_location = ('D:/dmpk/FMAE/fame2data/'+'CDK+cirQC3+'+'1A2'+'.csv')

        with open(file_location, 'r', encoding='utf-8') as csv_file:
            csv_file = csv.DictReader(csv_file)
            for row in csv_file:
                for key in cir_QC.keys():
                    cir_QC[key] = row[key]
                descriptors.append(cir_QC.copy())
        del descriptors[0]
        with open(new_file_location, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=header)  # 提前预览列名，当下面代码写入数据时，会将其一一对应。
            writer.writeheader()  # 写入列名
            writer.writerows(descriptors)  # 写入数据

    def x_csv(self):
        """
        从一个csv获取x,并用0填充空白格
        """
        x = np.loadtxt(self.file_path, dtype=np.str0, delimiter=',', skiprows=1,
                       usecols=range(1, 235), encoding='utf-8')
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                if x[i, j] == '':
                    x[i, j] = 0
        print(x, x.shape)
        return x

    def x_csvs(self):
        """
        从不同csv分别获取x
        """
        x_sum = np.empty([22, 757])
        m = 0
        for dirpath, dirnames, filenames in os.walk(self.file_path):
            for file in filenames:
                m += 1
                x = np.loadtxt(os.path.join(file_path, file), dtype=np.str0, delimiter=',',
                               skiprows=1, usecols=range(1, 757), encoding='utf-8')  # 22行，7列
                if m == 1:
                    x_sum = x
                elif m > 1:
                    x_sum = np.concatenate((x_sum, x), axis=0)
                    # x_sum = np.array([x_sum, x])
                    # for i in range(x.shape[0]):
                    #     for j in range(x.shape[1]):
                    #         if x[m, i, j] == '':
                    #             x[m, i, j] = 0
            print(x_sum, x_sum.shape)
        return x_sum
    def y_csv(self):
        """
        获取y，并转换成0/1
        """
        y = np.loadtxt(self.file_path, dtype=np.str0, delimiter=',', skiprows=1,
                       usecols=235, encoding='utf-8')
        for i in range(len(y)):
            if y[i] == 'unknown':
                y[i] = 0
            elif y[i] == 'true':
                y[i] = 1
            elif y[i] == 'TRUE':
                y[i] = 1
        y = y.astype(np.float32)
        print(y, type(y[0]))
        return y

    def y_sdf(self):
        """
        从sdf中读反应位点
        """
        y = 0
        return y
    def load_data(self):
        """
        加载数据集
        """
        X_train = self.x_csvs()
        y_train = self.y_sdf()
        print('X_train:', X_train)
        print('y_train:', y_train)
        return X_train, y_train
        # return model_selection.train_test_split(X_train, y_train, test_size=0.2, random_state=0, stratify=y_train)

    def run(self):
        """
        测试 DecisionTreeClassifier
        :return:  None
        """
        # X_train, X_test, y_train, y_test = self.load_data()
        X_train, y_train = self.load_data()
        clf = DecisionTreeClassifier()
        clf.fit(X_train, y_train)
        print("Training score:%f" % (clf.score(X_train, y_train)))
        # print("Testing score:%f" % (clf.score(X_test, y_test)))


if __name__ == "__main__":
    # file_path = "/data/yangliu/fame2/dataset_concatenated_flipper_1conf_mldata_unique.csv"
    # file_path = 'D:/dmpk/FMAE/fame2data/'+'CDK+cirQC3+'+'1A2'+'.csv'
    file_path = r"D:\dmpk\FMAE\fame3\fame3-0.1.0\res\cir_CDK\6_cirCDK"
    fame = Fame2(file_path)
    # fame.load_data()
    # range(3, 4922)
    fame.x_csvs()
    # fame.y()
    # fame.run()
    # fame.descriptor()