# -*- coding: utf-8 -*-

import csv
import os

def descriptor(file_location, new_file_location):
    """
    挑出有用的数据
    """
    Atom_type = ['Br', 'C.1', 'C.2', 'C.3', 'C.ar', 'Cl', 'F', 'I', 'N.1', 'N.2', 'N.3',
                 'N.4', 'N.am', 'N.ar', 'N.pl3', 'O.2', 'O.3', 'P.3', 'S.2', 'S.3', 'S.O2',
                 'S.O', 'Zn','Se', 'Na', 'Si', 'Sn', 'Mg', 'Ca', 'Cu', 'Du', 'LP', 'Li', 'H',
                 'F', 'Fe', 'Du.C', 'Hal', 'K', 'Mn', 'Mo', 'Het', 'Hev', 'H.spc', 'H.t3p',
                 'C.cat', 'O.t3p', 'O.co2', 'O.spc', 'Co.oh', 'Cr.oh', 'Cr.th', 'Al', 'Any']
    QC = ['piS(r)', 'De(r)', 'Dn(r)', 's-Pop', 'p-Pop', 'NumOfElecs', 'NetCharge',
          'valence', 'mull_charge', 'mull_pop']
    CDK = ['effectiveAtomPolarizability', 'stabilizationPlusCharge', 'sigmaElectronegativity',
           'piElectronegativity', 'partialSigmaCharge', 'partialTChargeMMFF94',
           'atomDegree', 'atomValence', 'atomHybridizationVSEPR', 'atomHybridization',
           'longestMaxTopDistInMolecule', 'highestMaxTopDistInMatrixRow', 'diffSPAN', 'relSPAN']

    # CYP = ['1A2', '1A2_1', '1A2_2', '1A2_3', '2A6', '2A6_1', '2A6_2', '2A6_3',
    #        '2B6', '2B6_1', '2B6_2', '2B6_3', '2C19', '2C19_1', '2C19_2', '2C19_3',
    #        '2C8', '2C8_1', '2C8_2', '2C8_3', '2C9', '2C9_1', '2C9_2', '2C9_3',
    #        '2D6', '2D_1', '2D6_2', '2D6_3', '2E1', '2E1_1', '2E1_2', '2E1_3',
    #        '3A4', '3A4_1', '3A4_2', '3A4_3', 'HLM']
    
    print(file_location)
    print(os.listdir(file_location))
    for dirpath, dirnames, filenames in os.walk(file_location):
        print(1)
        for file in filenames:
            
            descriptors = [{}]
            cir_QC = {}
            header = []
            file_name = str(file).split('.')[0]
            # print(file_name)
            cir_QC['Atom_'+str(file_name)] = 0
            header.append('Atom_' + str(file_name))


            # for qc in QC:
            #     for at in Atom_type:
            #         cir_QC[qc + '_' + at + '_3' + '_' + file_name] = 0
            #         header.append(qc + '_' + at + '_3' + '_' + file_name)


            for cdk in CDK:
                for at in Atom_type:
                    cir_QC[cdk + '_' + at + '_3' + '_' + file_name] = 0
                    header.append(cdk + '_' + at + '_3' + '_' + file_name)


            # for at in Atom_type:
            #     cir_QC['AtomType_' + at + '_10_' + file_name] = 0
            #     header.append('AtomType_' + at + '_10_' + file_name)
            cir_QC['isSoM' + '_' + file_name] = 0
            header.append('isSoM' + '_' + file_name)


            # print(cir_QC, header)
            # with open(file_location+'\\'+file, 'r', encoding='utf-8') as csv_file:
            with open(os.path.join(file_location,file), 'r', encoding='utf-8') as csv_file:
                csv_file = csv.DictReader(csv_file)
                for row in csv_file:
                    for key in cir_QC.keys():
                        cir_QC[key] = row[key]
                    descriptors.append(cir_QC.copy())
            del descriptors[0]


            # with open(new_file_location+'\\'+file, 'w', newline='', encoding='utf-8') as f:
            with open(os.path.join(new_file_location,file), 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                writer.writerows(descriptors)
            del descriptors


if __name__ == '__main__':
    # file_location = 'D:/dmpk/FMAE/fame2data/dataset_concatenated_flipper_1conf_mldata_unique.csv'
    #     # new_file_location = ('D:/dmpk/FMAE/fame2data/' + 'CDK+cirQC3+' + '1A2' + '.csv')
    # file_location = r'D:\dmpk\FMAE\fame3\fame3-0.1.0\res\4'
    # file_location =  r'fame3\fame3-0.1.0\4Glory_res'
    # file_location = 'fame3-0.1.0\\4Glory_res'
    file_location = os.path.join('fame3','fame3-0.1.0','2Smartcyp_res')
    # new_file_location = r'D:\dmpk\FMAE\fame3\fame3-0.1.0\res\4Glory_res'
    # new_file_location = os.path.join('fame3-0.1.0','res','4Glory_res')
    new_file_location = os.path.join('fame3','fame3-0.1.0','res','2Smartcyp_res')
    # new_file_location =  r'fame3\fame3-0.1.0\res\4Glory_res'
    # print(211111111)
    descriptor(file_location, new_file_location)
    
