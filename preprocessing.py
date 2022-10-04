import pandas as pd
import numpy as np
import requests

MAPS_API_KEY = ''

def isnan(string):
    if string != string or string == 'nan':
        return True
    else:
        return False

# Given:
#   st_num  - Property Street Number
#   direc   - Property Direction (N/S/E/W)
#   st_name - Property Street Name
#   city    - Property City
#   state   - Propert State
# Return:
#   []      - Array with Property Latitude, Longitude
def get_lat_lng_from_addr(st_num, direc, st_name, city, state):
    # Request LAT/LNG data from Google Maps API
    response = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address='+st_num+'+'+direc+'+'+st_name+',+'+city+',+'+state+'&key='+MAPS_API_KEY)
    # Retrieve LAT/LNG from Google Maps API
    resp_json_payload = response.json()
    # Set LAT/LNG values from response JSON
    try:
        lat = resp_json_payload['results'][0]['geometry']['location']['lat']
        lng = resp_json_payload['results'][0]['geometry']['location']['lng']
        # Return array containing LAT/LNG values
        return [lat, lng]
    except IndexError:
        response2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json?address=' + st_num + '+' + st_name + ',+' + city + ',+' + state + '&key=' + MAPS_API_KEY)
        resp_json_payload2 = response2.json()
        try:
            lat2 = resp_json_payload2['results'][0]['geometry']['location']['lat']
            lng2 = resp_json_payload2['results'][0]['geometry']['location']['lng']
            # Return array containing LAT/LNG values
            return [lat2, lng2]
        except IndexError:
            print("Uh Oh! Failed to get some data. Info below.")
            print("-----> Street Number: " + st_num)
            print("-----> Direction: " + direc)
            print("-----> Street Name: " + st_name)
            print("-----> City: " + city)
            print("-----> State: " + state)


def add_lat_lng_data(csv_file):
    # Read Property Address values from provided file
    df = pd.read_csv(csv_file, dtype=str)
    # Save column names, add LAT/LNG columns
    column_names = list(df.columns)
    column_names.append("Lat")
    column_names.append("Lng")
    # Convert DF to NP Array for simpler iteration
    np_arr = df.to_numpy()
    # Add LAT/LNG columns to NP Array
    np_arr = np.hstack([np_arr, np.zeros([len(np_arr), 2])])
    i = 0
    for property in np_arr:
        try:
            geo_coord = get_lat_lng_from_addr(str(property[13]), str(property[14]), str(property[15]),
                                              str(property[17]), str(property[18]))
            property[83] = geo_coord[0]
            property[84] = geo_coord[1]
            np_arr[i] = property
        except TypeError:
            print("Could not fetch from Google Maps API. Continuing...")
        i = i+1

    return [np_arr, column_names, csv_file]

def np_tocsv(info_arr):
    to_remove = [0, 1, 2, 3, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 60, 65, 66, 70, 74, 75, 76, 77, 81, 82]

    np_arr = np.delete(info_arr[0], to_remove, 1)
    np_columns = np.delete(info_arr[1].to_numpy(), to_remove, 1)
    df2 = pd.DataFrame(np_arr, columns=np_columns)

    # Writes LAT/LNG to provided file
    df2.to_csv("Clean_CLS5Mi/"+info_arr[2], index=False)