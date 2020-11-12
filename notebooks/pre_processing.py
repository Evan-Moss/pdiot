import os
from pathlib import Path
import re
import pandas as pd
import numpy as np

activity_dict = {
    0: "Sitting",
    4: "Sitting bent forward",
    5: "Sitting bent backward",
    1: "Walking at normal speed",
    100: "Standing",
    2: "Lying down on back",
    7: "Lying down left",
    6: "Lying down right",
    8: "Lying down on stomach",
    9: "Movement",
    11: "Running",
    12: "Climbing stairs",
    13: "Descending stairs",
    31: "Desk work"}

new_activity_dict = {
    0: "Sitting",
    1: "Sitting bent forward",
    2: "Sitting bent backward",
    3: "Walking at normal speed",
    4: "Standing",
    5: "Lying down on back",
    6: "Lying down left",
    7: "Lying down right",
    8: "Lying down on stomach",
    9: "Movement",
    10: "Running",
    11: "Climbing stairs",
    12: "Descending stairs",
    13: "Desk work"
    }
coversion = {
    0:0,
    4:1,
    5:2,
    1:3,
    100:4,
    2:5,
    7:6,
    6:7,
    8:8,
    9:9,
    11:10,
    12:11,
    13:12,
    31:13
}

# From Joao Maio on Piazza
def get_files(path):
    target_folder = path

    student_pattern = "s\d{7}"

    files = {}
    for (dirpath, dirnames, filenames) in os.walk(target_folder):
      s_match = re.search(student_pattern, dirpath)
      # if regex matches, and files exist
      if s_match and filenames:
        s = s_match.group()
        #print(f"adding files for {s} (in {dirpath})")
        dir = Path(dirpath)
        try: files[s]
        except KeyError: files[s] = []
        # only accept .csv files
        files[s].extend([dir/f for f in filenames if f[-4:] == '.csv'])

    #print("File count:")
    #print({k: len(v) for (k, v) in files.items()})
    return files

# From Teodora Georgescu on Piazza
def read_old_file_format(file_path):
    """
    Reads the recording files that do not contain headers.
    """
    pdiot_data = pd.read_csv(file_path)

    ACTIVITY_CODE_TO_NAME_MAPPING = {
        0: "Sitting",
        4: "Sitting bent forward",
        5: "Sitting bent backward",
        1: "Walking at normal speed",
        100: "Standing",
        2: "Lying down on back",
        7: "Lying down left",
        6: "Lying down right",
        8: "Lying down on stomach",
        9: "Movement",
        11: "Running",
        12: "Climbing stairs",
        13: "Descending stairs",
        31: "Desk work"}

    pdiot_header_information = dict()
    pdiot_header_information["Sensor position"] = pdiot_data['sensor_position'].values[0]
    pdiot_header_information["Sensor side"] = pdiot_data['sensor_side'].values[0]
    pdiot_header_information["Activity type"] = ACTIVITY_CODE_TO_NAME_MAPPING[pdiot_data['activity_type'].values[0]]
    pdiot_header_information["Activity code"] = pdiot_data['activity_type'].values[0]
    pdiot_header_information["Subject id"] = pdiot_data['subject_id'].values[0]

    pdiot_data.drop(columns=['sensor_position','sensor_side', 'subject_id', 'activity_type', 'recording_id'], inplace=True)

    return pdiot_data, pdiot_header_information

# Change depending on what sensor position you want.
def get_data(desired_position, files):
    desired = []
    for student in files:
        desired = desired + ([f for f in files[student] if desired_position in str(f)])
    len(desired)

    header_size = 5
    data = []
    for d in desired:
        read = pd.read_csv(d, skiprows=5)
        if 'timestamp' not in read.columns:
            read, head = read_old_file_format(d)
        else:
            with open(d) as f:
                head = [next(f).rstrip().split('# ')[1] for x in range(header_size)]
        data.append((head,read))
    return data

def get_data_by_datapoints(data, points_wanted=50, overlap=0.5):
    new_data = []
    new_targets = []
    students = []
    for d in data:
        main = d[1].reset_index(drop=True)
        if len(d[1]) == 0:
            continue
        if type(d[0]) != dict:
            target = int(d[0][3].split(':')[1])
            student = d[0][4].split(':')[1].strip()
        else:
            target = d[0]["Activity code"]
            student = d[0]["Subject id"]
        # Shave of first and last second
        start = 13
        end = len(main) - 1 - 13
        main = main[start:end].reset_index(drop=True)
        iters = main.shape[0] / points_wanted
        start = 0
        end = points_wanted
        for i in range(int(iters/overlap)-1):
            s_data = main[start:end].filter(['accel_x','accel_y','accel_z']).reset_index(drop=True)
            s_data = np.append( np.append(np.array(s_data['accel_x']).flatten(), np.array(s_data['accel_y']).flatten()), np.array(s_data['accel_z']).flatten() )

            new_data.append(s_data)

            new_targets.append(target)
            students.append(student.lower())
            start += int(points_wanted * overlap)
            end = int(start + points_wanted)

    return np.array(new_data), np.array(new_targets), np.array(students)

def convert_targets(targets):
    keys, inv = np.unique(targets, return_inverse=True)
    vals = np.array([coversion[key] for key in keys])
    result = vals[inv]
    return result 

def get_random_student(students):
    return np.random.choice(students)

def leave_one_out(cleaned_data, targets, students, no_students = 1):
    un = np.unique(students)
    un = un[un != ""]
    random_student = get_random_student(un)

    student_data = cleaned_data[students == random_student]
    student_targets = targets[students == random_student]

    cleaned_data = cleaned_data[students != random_student]
    targets = targets[students != random_student]

    return cleaned_data, targets, student_data, student_targets
