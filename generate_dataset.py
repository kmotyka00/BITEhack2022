#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
from schedule import Client

import xlwt
MAX_AVAIBLE_HOURS = 20
MAX_DAY_HOURS_AVAILABLE = 7


def generate_data(n_of_people: int=30, n_of_classes: int=10, n_of_time: int=18):
    people_ids = range(1, n_of_people+1)
    people_class_preferences = [None for _ in range(n_of_people)]
    for i in range(n_of_people):
        r = random.randint(1, int(n_of_classes//3))
        CLASSES_RANGE = [str(i) for i in range(n_of_classes)]
        random.shuffle(CLASSES_RANGE)
        client_pref = CLASSES_RANGE[:r]
        people_class_preferences[i] = client_pref

    people_time_preferences = [[] for _ in range(n_of_people)]
    for i in range(n_of_people):
        day_n = random.randint(1, 7)
        DAY_RANGE = list(range(7))
        random.shuffle(DAY_RANGE)
        DAY_RANGE = DAY_RANGE[:day_n]
        # w ile dni pasują mu treningi
        needed_hours = len(people_class_preferences[i])
        random_expected_hours = random.randint(needed_hours, MAX_AVAIBLE_HOURS)
        for day in DAY_RANGE:
            r = random.randint(1, MAX_DAY_HOURS_AVAILABLE)
            if random_expected_hours == 0:
                pass
            else:
                if r > random_expected_hours:
                    r = random_expected_hours
                    random_expected_hours = 0
                    # przypisz random_expecteD_hours
                else:
                    random_expected_hours -= r
                DAY_HOURS_RANGE = [str(i) for i in range(n_of_time)]
                random.shuffle(DAY_HOURS_RANGE)
                DAY_HOURS_RANGE = DAY_HOURS_RANGE[:r]
                people_time_preferences[i].append([day, DAY_HOURS_RANGE])
    return [Client(people_ids[i], people_class_preferences[i], people_time_preferences[i]) for i in range(n_of_people)]


def write_data_csv(Client_list: list, name: str="Dataset_TEST.xls"):
    WorkBook = xlwt.Workbook(encoding="utf-8")
    sheet = WorkBook.add_sheet("Sheet1")
    Letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']
    Names = ["ID", "Lesson Types", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    for i, letter in enumerate(Letters):
        sheet.write(0, i, Names[i])

    for i, client in enumerate(Client_list):
        sheet.write(i+1, 0, str(client.id))
        sheet.write(i+1, 1, str(" ".join(list(client.selected_training.tolist()))))
        for day in client.selected_availability:
            if day[0] == 0:
                sheet.write(i+1, 2, str(" ".join(day[1])))
            elif day[0] == 1:
                sheet.write(i+1, 3, str(" ".join(day[1])))
            elif day[0] == 2:
                sheet.write(i+1, 4, str(" ".join(day[1])))
            elif day[0] == 3:
                sheet.write(i+1, 5, str(" ".join(day[1])))
            elif day[0] == 4:
                sheet.write(i+1, 6, str(" ".join(day[1])))
            elif day[0] == 5:
                sheet.write(i+1, 7, str(" ".join(day[1])))
            elif day[0] == 6:
                sheet.write(i+1, 8, str(" ".join(day[1])))
    WorkBook.save("client_data/" + name)
    print("-----WRITING TO EXCEL DONE-----")

clients = generate_data(30, 10, 18)
write_data_csv(clients)
x = [32, 24, 5]
random.shuffle(x)
print(x)
print(random.shuffle(list(range(10))))