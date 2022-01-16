#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
from schedule import Client




def Read_from_json():
    clients_alg = list()
    clients_email = list()
    for file in os.listdir('client_data/json_files/'):
        f = open(f'client_data/json_files/{file}') # 'client_data/json_files/'
        data = json.load(f)
        clients_alg.append(Client(data['id'], data['classes'], data['availability']))
        clients_email.append(ClientEmail(data['name'], data['surname'], data['id'], data['email'], None))
    return clients_alg, clients_email

    #ID, TRENINGI

def actual_emails(client_lst: list):
    pass

if __name__ == "__main__":
    _, cl_email = Read_from_json()
    print(cl_email)