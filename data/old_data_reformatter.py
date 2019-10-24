# data_manipulation.py
import json # javascript object notation library for converting json to dictonaries

flight_file = open("old_irec2019.json")  # Open up the file
lines = flight_file.readlines()  # Read it as a list of strings
list_of_dicts = [json.loads(line) for line in lines]
# This basically says that the list_of_dicts variable is equal to the
# json.loads(line) (a dictionary made from a json string) for each line
# in the list (fancy array) of lines. The variable name line is arbitrary. 


# What if the data isn't in order? We can sort by time.
time_dict = {} # Empty dictionary 
for data_set in list_of_dicts:
    # Set the value at the key of time to the original dictionary
    time_dict[data_set['time']] = data_set  
list_of_times = list(time_dict.keys()) # A list of the keys of the dictionary
list_of_times.sort() # Sorted in-place, so we don't need to set it to anything

# A list of data_point dictionaries in order
sorted_list = [time_dict[time] for time in list_of_times]

# Print out the top three to test order
for i in range(3):
    print(f"{sorted_list[i]}\n")
print("\n\n\n")


# Now we can remove data we don't want (the data I remove is semi-arbitrary)
for data_set in sorted_list:
    data_set.pop('type')
        
    for item in ["hour", "min", "sec", "day", "mon", "year"]:
        data_set["sensors"]['gps'].pop(item)
    data_set["sensors"]["lat"] = data_set["sensors"]["gps"]["lat"]
    data_set["sensors"]["lon"] = data_set["sensors"]["gps"]["lon"]
    data_set["sensors"].pop("gps")

    data_set["sensors"]["pitch"] = data_set["sensors"]["att"]["p"]
    data_set["sensors"]["yaw"] = data_set["sensors"]["att"]["y"]
    data_set["sensors"]["roll"] = data_set["sensors"]["att"]["r"]
    data_set["sensors"].pop("att")
    
    data_set["sensors"]["alt"] = data_set["sensors"]["bar"]["alt"]
    data_set["sensors"]["pres"] = data_set["sensors"]["bar"]["p"]
    data_set["sensors"]["hum"] = data_set["sensors"]["bar"]["hum"]
    data_set["sensors"]["temp"] = data_set["sensors"]["bar"]["temp"]
    data_set["sensors"].pop("bar")
    data_set.pop("state")
    
print(sorted_list[0],"\n")

print(sorted_list[0])

# If it looks good, we can write it to a new file via json.dump
open("manipulated_data.json","w").close()  # Hacky erase file
new_file = open("manipulated_data.json", "a")  # Open file to append to
for data_set in sorted_list:
    json.dump(data_set, new_file)
    new_file.write("\n")
new_file.close()  # Done, check out the new data!
