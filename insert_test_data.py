import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
from sklearn.cluster import KMeans
from skimage import io
import os
from random import randint, uniform
import psycopg2
import calendar

conn = psycopg2.connect(database="vino", user="postgres", password="root", host="51.250.23.5", port="9003")

cursor = conn.cursor()
cursor.execute('Select * from params;')
record = cursor.fetchall()

TYPE_SOIL = [
    'Clay', 'SiltyClay', 'SiltyClayLoam', 'SandyClay', 'SandyClayLoam', 'ClayLoam', 'Silt', 'SiltLoam', 'Loam', 'Sand',
    'LoamySand', 'SandyLoam'
]


TYPE_FLOODED = [
    'No',
    'From0To1',
    'From1To3',
    'From3To6'
]
MONTH = [
    calendar.month_name[0],
    calendar.month_name[1],
    calendar.month_name[2],
    calendar.month_name[3],
    calendar.month_name[4],
    calendar.month_name[5],
    calendar.month_name[6],
    calendar.month_name[7],
    calendar.month_name[8],
    calendar.month_name[9],
    calendar.month_name[10],
    calendar.month_name[11],
]


def insert_regions():
    query = "insert into regions (name, bounds, center) values (%s, %s, %s);"
    data1 = ['Краснодар', '{{1000, 1000}, {99999, 99999}}', '{44.929065, 39.046412}']
    data2 = ['region2', '{{1, 1}, {2, 2}}', '{54.929065, 39.046412}']
    data3 = ['region3', '{{500, 99999}, {500, 99999}}', '{34.929065, 39.046412}']
    cursor.execute(query, data1)
    cursor.execute(query, data2)
    cursor.execute(query, data3)
    conn.commit()


def insert_polygon():
    query = "insert into polygon(scoring, bounds, center, geo, area, free_area, param_id, region_id) values ( %s, %s, %s, %s, %s, %s, %s, %s);"

    global score1
    score1 = randint(1, 10)
    data1 = [
        score1, '{{45.081619, 38.631342}, {45.280263, 38.752630}}', '{45.157698, 38.750502}',
        '{{45.240440, 38.639854}, {45.081619, 38.631342}, {45.183286, 38.949457}, {45.280263, 38.752630}}',
        randint(1, 10), randint(1, 10), 1, 1
    ]

    global score2
    score2 = randint(1, 10)
    data2 = [
        score2, '{{45.062770, 38.374473}, {45.241216, 38.711720}}', '{45.111397, 38.507283}',
        '{{45.062770, 38.374473}, {45.220128, 38.378950}, {45.241216, 38.711720}, {45.241216, 38.711720}}',
        randint(1, 10), randint(1, 10), 2, 2
    ]

    global score3
    score3 = randint(1, 10)
    data3 = [
        score3, '{{500, 99999}, {500, 99999}}', '{44.929065, 39.046412}',
        '{{44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}}',
        randint(1, 10), randint(1, 10), 3, 3
    ]

    global score4
    score4 = randint(1, 10)
    data4 = [
        score4, None, '{44.929065, 39.046412}',
        '{{44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}}',
        randint(1, 10), randint(1, 10), 1, 3
    ]

    global score5
    score5 = randint(1, 10)
    data5 = [
        score5, None, '{44.929065, 39.046412}',
        '{{44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}, {44.74564075, 39.5214215}}',
        randint(1, 10), randint(1, 10), 2, 1
    ]

    global score6
    score6 = randint(1, 10)
    data6 = [
        score6, '{{500, 99999}, {500, 99999}}',
        '{54.931849, 39.043582}',
        '{{54.932151, 39.035563}, {54.931819, 39.041957}, {54.935621, 39.043634}, {54.932151, 39.035563}}',
        randint(1, 10), randint(1, 10), 3, 1
    ]

    data7 = [
        None, '{{1, 1}, {2, 2}}',
        '{33.804073, 38.511625}',
        '{{33.631501, 38.333460}, {34.074067, 37.896146}, {34.474080, 38.519723}, {33.976294, 39.025873}}',
        randint(1, 10), randint(1, 10), None, None
    ]


    color_data1 = [
        color_score1, '{{45.166996, 39.233192}, {45.287697, 39.438593}}',
        '{45.209042, 39.301299}',
        '{{45.171585, 39.233192},{45.281592, 39.236435}, {45.287697, 39.438593}, {45.166996, 39.422377}}',
        randint(1, 10), randint(1, 10), 1, 1

    ]

    global score8
    score8 = 50
    color_data2 = [
        color_score2, '{{44.796333, 39.267786}, {44.804030, 39.518592}}',
        '{44.845575, 39.347784}',
        '{{44.796333, 39.267786},{44.978471, 39.409405}, {44.804030, 39.518592}}',
        randint(1, 10), randint(1, 10), 1, 1

    ]

    global score9
    score9 = 88
    color_data3 = [
        color_score3, '{{44.733682, 38.614013}, {44.930612, 38.872386}}',
        '{44.786058, 38.759956}',
        '{{44.733682, 38.614013},{44.930612, 38.702659}, {44.741387, 38.872386}}',
        randint(1, 10), randint(1, 10), 1, 1

    ]


    cursor.execute(query, data1)
    cursor.execute(query, data2)
    cursor.execute(query, data3)
    cursor.execute(query, data4)
    cursor.execute(query, data5)
    cursor.execute(query, data6)
    cursor.execute(query, data7)
    cursor.execute(query, color_data1)
    cursor.execute(query, color_data2)
    cursor.execute(query, color_data3)
    conn.commit()


def insert_detail():
    query = "insert into details (month, tavg, tmax, tmin, pavg, pmax, pmin, param_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    data1_month = 1
    data1 = [data1_month, uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), 1]

    data2 = [data1_month, uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), 1]

    data3 = [randint(0, 11), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), 2]

    data4 = [randint(0, 11), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), 3]

    data5 = [randint(0, 11), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), 4]

    cursor.execute(query, data1)
    cursor.execute(query, data2)
    cursor.execute(query, data3)
    cursor.execute(query, data4)
    cursor.execute(query, data5)
    conn.commit()


def insert_params():
    query = "insert into params (min_relief_aspect, max_relief_aspect, avg_relief_aspect, min_relief_height, max_relief_height, avg_relief_height, max_relief_slope, min_relief_slope, avg_relief_slope, avg_sunny_days, max_sunny_days, min_sunny_days, water_seasonlyty, flooded, soil, scoring, forest) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data1 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             None, randint(0, 11), True]

    data2 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), False]

    data3 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), True]

    data4 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), True]

    data5 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), False]

    data6 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), None]

    data7 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], randint(0, 11), None]

    global color_score1
    color_score1 = 32
    color_data1 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
             randint(0, 11), TYPE_FLOODED[randint(0, 3)],
             TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], color_score1, None]

    global color_score2
    color_score2 = 50
    color_data2 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
                   uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
                   randint(0, 11), TYPE_FLOODED[randint(0, 3)],
                   TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], color_score2, None]

    global color_score3
    color_score3 = 77
    color_data3 = [uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
                   uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10), uniform(1, 10),
                   randint(0, 11), TYPE_FLOODED[randint(0, 3)],
                   TYPE_SOIL[randint(0, len(TYPE_SOIL) - 1)], color_score3, None]

    cursor.execute(query, data1)
    cursor.execute(query, data2)
    cursor.execute(query, data3)
    cursor.execute(query, data4)
    cursor.execute(query, data5)
    cursor.execute(query, data6)
    cursor.execute(query, data7)
    cursor.execute(query, color_data1)
    cursor.execute(query, color_data2)
    cursor.execute(query, color_data3)
    conn.commit()


def insert_marker():
    query = "insert into markers (center, scoring, bounds, param_id, region_id) values ( %s, %s, %s, %s, %s)"
    data1 = ['{45.164517, 38.982895}', score1, '{{10, 10}, {100, 100}}', 1, 1]

    data2 = ['{54.929065, 39.046412}', score2, '{{1, 1}, {2, 2}}', 2, 2]

    data3 = ['{34.929065, 39.046412}', score3, '{{0, 99999}, {500, 99999}}', 3, 3]

    cursor.execute(query, data1)
    cursor.execute(query, data2)
    cursor.execute(query, data3)

    conn.commit()


insert_regions()
insert_params()
insert_polygon()
insert_detail()
insert_marker()
