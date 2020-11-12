import pre_processing as pp
files = pp.get_files("/Users/evan/Documents/uni/pdiot/coursework/coursework_3/gitrepo/pdiot/pdiot-data/2020/")
data = pp.get_data("Chest_Left", files)
clean_data, targets, students = pp.get_data_by_datapoints(data, points_wanted = 25)
cleaned_data, targets, student_data, student_targets = pp.leave_one_out(clean_data, targets, students)

print(len(cleaned_data))
converted_targets = pp.convert_targets(targets)
print(len(converted_targets) == len(targets))
