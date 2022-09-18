from prepare_for_bd import PrepareData
import psycopg2
import calendar
preparedata = PrepareData()
conn = psycopg2.connect(database="vino", user="postgres", password="root", host="51.250.23.5", port="9003")

cursor = conn.cursor()

def filter(data):
    if -5000 > data or data > 5000:
        return None
    else:
        return data

def get_bounds(data):
    x_min = min([el[0] for el in data])
    x_max = max([el[0] for el in data])
    y_min = min([el[1] for el in data])
    y_max = max([el[1] for el in data])
    return [[x_min, y_min],[x_max, y_max]]

def get_center(geo):
    max_y = max(geo)
    min_y = min(geo)
    max_x = max()

TYPE_SOIL = [
'Loam',
'Sand',
]


TYPE_FLOODED = [
    'From3To6',
    'No',
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
    data1 = ['Краснодар', '{{44.161484, 38.190585}, {45.579993, 39.397642}}', '{44.929065, 39.046412}']
    cursor.execute(query, data1)
    conn.commit()


def insert_polygon():
    query = "insert into polygon(scoring, bounds, center, geo, area, free_area, param_id, region_id) values ( %s, %s, %s, %s, %s, %s, %s, %s);"
    score_data = preparedata.add_scoring()
    geo_data = preparedata.add_geo_data()
    area_data = preparedata.get_area()
    for id in score_data:
        scoring = score_data[id]['score']
        geo = geo_data[id]['geo']
        center = geo_data[id]['center']
        area = area_data[id]['bad_arrea']
        free_area = area_data[id]['good_arrea']
        region_id = 1
        param_id = id + 1
        bounds = get_bounds(geo)

        data = [scoring, bounds, center, geo, area, free_area, param_id, region_id]


        cursor.execute(query, data)
        conn.commit()


def insert_detail():
    query = "insert into details (month, tavg, tmax, tmin, pavg, pmax, pmin, param_id) values (%s, %s, %s, %s, %s, %s, %s, %s)"
    data1, data2 = preparedata.add_feature('data/freadom.csv')

    for id in data1:
        pass

    # cursor.execute(query, data)
    conn.commit()


def insert_params():
    query = "insert into params (min_relief_aspect, max_relief_aspect, avg_relief_aspect, min_relief_height, max_relief_height, avg_relief_height, min_relief_slope, max_relief_slope, avg_relief_slope, min_sunny_days, max_sunny_days, avg_sunny_days, flooded, soil, scoring, forest) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    data1, data2 = preparedata.add_feature('data/freadom.csv')
    data5 = preparedata.add_is_warning()
    score_data = preparedata.add_scoring()
    for id, el2, el3 in zip(data1, data5, score_data):
        min_relief_aspect = filter(data1[id]['min_value_KRA_RELIEF_ASPECT_100m'])
        max_relief_aspect = filter(data1[id]['max_value_KRA_RELIEF_ASPECT_100m'])
        avg_relief_aspect = filter(data1[id]['mean_value_KRA_RELIEF_ASPECT_100m'])
        min_relief_height = filter(data1[id]['min_value_KRA_RELIEF_HEIGHT_100m'])
        max_relief_height = filter(data1[id]['max_value_KRA_RELIEF_HEIGHT_100m'])
        avg_relief_height = filter(data1[id]['mean_value_KRA_RELIEF_HEIGHT_100m'])
        min_relief_slope = filter(data1[id]['min_value_KRA_RELIEF_SLOPE_100m'])
        max_relief_slope = filter(data1[id]['max_value_KRA_RELIEF_SLOPE_100m'])
        avg_relief_slope = filter(data1[id]['mean_value_KRA_RELIEF_SLOPE_100m'])
        min_sunny_days = filter(data1[id]['min_value_KRA_SUNNY_DAYS_APR_OCT_100m'])
        max_sunny_days = filter(data1[id]['max_value_KRA_SUNNY_DAYS_APR_OCT_100m'])
        avg_sunny_days = filter(data1[id]['mean_value_KRA_SUNNY_DAYS_APR_OCT_100m'])
        flooded = el2.get(id)
        if flooded:
            flooded = flooded['flood']

        soil = el2.get(id)
        if soil:
            soil = soil['loan']

        scoring = score_data[0]['score']

        forest = el2.get(id)
        if forest:
            forest = forest['les']







        result_data = [min_relief_aspect, max_relief_aspect, avg_relief_aspect, min_relief_height, max_relief_height,
                       avg_relief_height, min_relief_slope, max_relief_slope, avg_relief_slope, min_sunny_days, max_sunny_days,
                       avg_sunny_days, flooded, soil, scoring, forest
                       ]
        cursor.execute(query, result_data)
        conn.commit()


def insert_marker():
    query = "insert into markers (center, scoring, bounds, param_id, region_id) values ( %s, %s, %s, %s, %s)"
    data = []
    cursor.execute(query, data)

    conn.commit()


# insert_regions()
# insert_params()
# insert_polygon()
insert_detail()
# insert_marker()
