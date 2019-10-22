from src.data_processment.stop_region_thierry import MovingCentroidStopRegionFinder
import pandas as pd
import os


def find_clusters(user_data):
    r = 50
    delta_t = 300

    user_data = local_time(user_data)

    if len(user_data) == 0:
        print("User data is empty")
        return

    print("FINDING STOP REGIONS")
    stop_region_finder = MovingCentroidStopRegionFinder(region_radius=r, delta_time=delta_t)

    clusters = stop_region_finder.find_clusters(user_data, verbose=False)
    print(len(clusters), "found")

    return clusters


def load_user_gps_csv(userid, from_day_n=None, to_day_n=None, fill=False):
    try:
        user_data = pd.read_csv("outputs/user_gps/" + str(userid) + '_gps.csv')
    except pd.errors.EmptyDataError:
        return pd.DataFrame()

    user_data = local_time(user_data)
    if len(user_data) > 0:
        user_data = user_data.drop_duplicates().sort_values(by="local_time")

    min_time = user_data["local_time"].min()

    if from_day_n is None:
        use_data_from_time = min_time
    else:
        use_data_from_time = min_time + 86400 * from_day_n

    if to_day_n is None:
        use_data_to_time = user_data["local_time"].max()
    else:
        use_data_to_time = use_data_from_time + to_day_n * 86400

    user_data = user_data[(user_data["local_time"] >= use_data_from_time) & (user_data["local_time"] <= use_data_to_time)]

    if fill:
        pass

    return user_data

def local_time(data, time_col="time", tz_col="tz"):
    data["local_" + time_col] = data[time_col] + data[tz_col]
    return data