"""
Copyright (c) 2024 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

import csv

class CSVReader():

    '''
    Converts a csv file to a Python dictionary.
    '''
    @staticmethod
    def csv_to_dict(filename):

        with open(f'{filename}', 'r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)
            data = [row for row in csv_reader]
                
        return data
