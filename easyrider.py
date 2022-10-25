# Write your code here
import json
import re
import sys

json_list = json.loads(input())


def check_data_types():
    bus_id = 0
    stop_id = 0
    stop_name = 0
    next_stop = 0
    stop_type = 0
    a_time = 0

    for i in range(len(json_list)):
        json_dict = dict(json_list[i])
        if not isinstance(json_dict["bus_id"], int):
            bus_id += 1
        if not isinstance(json_dict["stop_id"], int):
            stop_id += 1
        if not (isinstance(json_dict["stop_name"], str) and json_dict["stop_name"] != ""):
            stop_name += 1
        if not isinstance(json_dict["next_stop"], int):
            next_stop += 1
        if not (isinstance(json_dict["stop_type"], str) and (json_dict["stop_type"] == "S" or json_dict["stop_type"] == "O"
                or json_dict["stop_type"] == "F" or json_dict["stop_type"] == "")):
            stop_type += 1
        if not (isinstance(json_dict["a_time"], str) and json_dict["a_time"] != ""):
            a_time += 1
    errors = stop_name + bus_id + stop_id + stop_type + a_time + next_stop
    print("Type and required field validation: " + str(errors) + " errors")
    print("bus_id: " + str(bus_id))
    print("stop_id: " + str(stop_id))
    print("stop_name: " + str(stop_name))
    print("next_stop: " + str(next_stop))
    print("stop_type: " + str(stop_type))
    print("a_time: " + str(a_time))


def check_syntax():
    stop_name = 0
    a_time = 0
    stop_type = 0

    for i in range(len(json_list)):
        json_dict = dict(json_list[i])
        if not re.match('[A-Z].* (Road|Avenue|Boulevard|Street)$', json_dict["stop_name"]):
            stop_name += 1
        if not re.match('[SOF]$|$', json_dict["stop_type"]):
            stop_type += 1
        if not re.match('2[0-3]:[0-5][0-9]$|[0-1][0-9]:[0-5][0-9]$', json_dict["a_time"]):
            a_time += 1
    errors = stop_name + stop_type + a_time
    print("Format validation: " + str(errors) + " errors")
    print("stop_name: " + str(stop_name))
    print("stop_type: " + str(stop_type))
    print("a_time: " + str(a_time))

    d = {}
    for i in range(len(json_list)):
        json_dict = json_list[i]
        if json_dict["bus_id"] in d:
            d[json_dict["bus_id"]] += 1
        else:
            d.update({json_dict["bus_id"]: 1})

    print("Line names and number of stops:")
    for i in d:
        print("bus_id: " + str(i) + ", stops: " + str(d[i]))


def check_stop_types():
    d = {}
    start_stops = []
    transfer_stops = []
    finish_stops = []
    stops = {}

    for i in range(len(json_list)):
        json_dict = json_list[i]
        if json_dict["bus_id"] not in d:
            d.update({json_dict["bus_id"]: [1, 0, 0]})
        if json_dict["stop_type"] == "S":
            d[json_dict["bus_id"]][1] += 1
            if d[json_dict["bus_id"]][1] >= 2:
                print("There is no start or end stop for the line: " + str(json_dict["bus_id"]))
                sys.exit()
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            if json_dict["stop_type"] not in start_stops:
                start_stops.append(json_dict["stop_name"])
        elif json_dict["stop_type"] == "F":
            d[json_dict["bus_id"]][2] += 1
            if d[json_dict["bus_id"]][2] >= 2:
                print("There is no start or end stop for the line: " + str(json_dict["bus_id"]))
                sys.exit()
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            if json_dict["stop_name"] not in finish_stops:
                finish_stops.append(json_dict["stop_name"])
        elif json_dict["stop_type"] == "" or json_dict["stop_type"] == "O":
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
    for i in d:
        if d[i][1] == 0 or d[i][2] == 0:
            print("There is no start or end stop for the line: " + str(i))
            sys.exit()
    print("start stops: " + str(len(start_stops)) + " " + str(sorted(start_stops)))
    print("transfer stops: " + str(len(transfer_stops)) + " " + str(sorted(transfer_stops)))
    print("finish stops: " + str(len(finish_stops)) + " " + str(sorted(finish_stops)))


def check_times():
    incorrect = {}
    prev_a_time = {}
    for i in range(len(json_list)):
        json_dict = json_list[i]
        if json_dict["bus_id"] not in incorrect:
            if json_dict["bus_id"] not in prev_a_time:
                prev_a_time.update({json_dict["bus_id"]: json_dict["a_time"]})
            else:
                if prev_a_time[json_dict["bus_id"]] >= json_dict["a_time"]:
                    incorrect.update({json_dict["bus_id"]: json_dict["stop_name"]})
                else:
                    prev_a_time.update({json_dict["bus_id"]: json_dict["a_time"]})

    print("Arrival time test:")
    if not incorrect:
        print("OK")
    else:
        for i in incorrect:
            print("bus_id line " + str(i) + ": wrong time on station " + incorrect[i])


def check_on_demand():
    start_stops = []
    transfer_stops = []
    finish_stops = []
    stops = {}

    for i in range(len(json_list)):
        json_dict = json_list[i]
        if json_dict["stop_type"] == "S":
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            if json_dict["stop_type"] not in start_stops:
                start_stops.append(json_dict["stop_name"])
        elif json_dict["stop_type"] == "F":
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])
            if json_dict["stop_name"] not in finish_stops:
                finish_stops.append(json_dict["stop_name"])
        elif json_dict["stop_type"] == "O":
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
        elif json_dict["stop_type"] == "":
            if json_dict["stop_name"] not in stops:
                stops.update({json_dict["stop_name"]: [json_dict["bus_id"]]})
            elif json_dict["bus_id"] not in stops[json_dict["stop_name"]]:
                stops[json_dict["stop_name"]].append(json_dict["bus_id"])
                if len(stops[json_dict["stop_name"]]) > 1 and json_dict["stop_name"] not in transfer_stops:
                    transfer_stops.append(json_dict["stop_name"])

    ok = 1
    wrong = []
    for i in range(len(json_list)):
        json_dict = json_list[i]
        if json_dict["stop_type"] == "O":
            if json_dict["stop_name"] in transfer_stops or json_dict["stop_name"] in start_stops or json_dict["stop_name"] in finish_stops:
                wrong.append(json_dict["stop_name"])
                ok = 0

    print("On demand stops test:")
    if ok == 1:
        print("OK")
    else:
        print("Wrong stop type: " + str(sorted(wrong)))

check_on_demand()
