import csv
import json
import pickle
import pandas as pd
from collections import defaultdict


def add_geo_data(geo_data):
    arr = []
    for key, value in geo_data.items():
        arr.append({int(key): {'geo': value}})

    return arr


def add_scoring():
    with open("data/score_data.csv", 'r') as f:
        reader = csv.reader(f, delimiter=',')
        score_data = [{row[1]: row[2]} for row in reader][1:]
    arr = {}
    for el in score_data:
        for key, value in el.items():
            arr[key] = value

    arr = [{int(key): {'score': value}} for key, value in arr.items()]
    return arr




def add_feature(path):
    arr = {}
    i = 0
    df = pd.read_csv(path)

    need_colomns = [x for x in df.columns if ('chanel' not in x) & ('value' in x)]
    index_col = 'index_cluster'
    all_dict_1 = {}
    for ind, row in df.iterrows():
        index = row[index_col]
        dict_res = {i: v for i, v in row[need_colomns].items()}
        all_dict_1[int(index)] = dict_res

    all_dict_2 = {}
    need_colomns = [x for x in df.columns if ('chanel' in x) & ('mean' in x)]
    month_dict_name = defaultdict(list)
    name_need_col = ['min_value_KRA_PREC_100m_chanel_',
                     'max_value_KRA_PREC_100m_chanel_',
                     'mean_value_KRA_PREC_100m_chanel_',
                     'mean_value_KRA_TAVG_100m_chanel_',
                     'mean_value_KRA_TMIN_100m_chanel_',
                     'mean_value_KRA_TMAX_100m_chanel_']

    for _, row in df.iterrows():
        index = int(row[index_col])
        tmp_dict = {}
        for k in range(0, 12):
            dict_res = {}
            for c in name_need_col:
                dict_res[c] = row[c + str(k)]

            tmp_dict[k] = dict_res
        all_dict_2[index] = tmp_dict

    return all_dict_1, all_dict_2


class PrepareData():

    def add_geo_data(self):
        with open('data/geo.json') as f:
            geo_data = json.load(f)
        arr = {}
        for key, value in geo_data.items():
            arr[int(key)] = {'geo': value['coords'], 'center': value['center']}
        # arr = {{int(key): {'geo': value['coords']}, 'center': value['center']} for key, value in geo_data.items()}

        return arr

    def add_scoring(self):
        with open("data/score_data.csv", 'r') as f:
            reader = csv.reader(f, delimiter=',')
            score_data = [{row[1]: row[2]} for row in reader][1:]
        arr = {}
        for el in score_data:
            for key, value in el.items():
                arr[key] = value

        arr = {int(key): {'score': value} for key, value in arr.items()}
        return arr

    def add_is_warning(self):
        with open('data/is_warning_ter.json', 'r') as f:
            data = json.load(f)

        arr = [{int(key): value} for key, value in data.items()]
        return arr

    def add_feature(self, path):
        arr = {}
        i = 0
        df = pd.read_csv(path)

        need_colomns = [x for x in df.columns if ('chanel' not in x) & ('value' in x)]
        index_col = 'index_cluster'
        all_dict_1 = {}
        for ind, row in df.iterrows():
            index = row[index_col]
            dict_res = {i: v for i, v in row[need_colomns].items()}
            all_dict_1[int(index)] = dict_res

        all_dict_2 = {}
        need_colomns = [x for x in df.columns if ('chanel' in x) & ('mean' in x)]
        month_dict_name = defaultdict(list)
        name_need_col = ['min_value_KRA_PREC_100m_chanel_',
                         'max_value_KRA_PREC_100m_chanel_',
                         'mean_value_KRA_PREC_100m_chanel_',
                         'mean_value_KRA_TAVG_100m_chanel_',
                         'mean_value_KRA_TMIN_100m_chanel_',
                         'mean_value_KRA_TMAX_100m_chanel_']

        for _, row in df.iterrows():
            index = int(row[index_col])
            tmp_dict = {}
            for k in range(0, 12):
                dict_res = {}
                for c in name_need_col:
                    dict_res[c] = row[c + str(k)]

                tmp_dict[k] = dict_res
            all_dict_2[index] = tmp_dict

        return all_dict_1, all_dict_2

    def get_area(self):
        with open('data/arrea.json') as f:
            area_data = json.load(f)
            arr = {}
            for key, value in area_data.items():
                arr[int(key)] = value

            return arr


if __name__ == '__main__':
    pd = PrepareData()
    pd.add_geo_data()
