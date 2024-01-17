""" Copyright (c) 2024 Cisco and/or its affiliates.
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

from dotenv import load_dotenv
import os
import requests
import time
import logging
log = logging.getLogger(__name__)

load_dotenv()

class WebexAPI():
    '''
    Class for communication with Webex API:
    https://developer.webex.com/docs/getting-started
    '''

    def __init__(self):
        self.access_token=os.getenv("WEBEX_TOKEN")
        self.headers = {'Authorization': f'Bearer {self.access_token}'}
        self.base_url = 'https://webexapis.com/v1'


    def execute_rest_call(self, method, url, payload):
        '''
        Execute and check a REST call based on the provided data.
        '''

        response = requests.request(method, url, headers=self.headers, json=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f'Successful Webex API call: {url} ({method})')
            #print(response.json())
            return response.json()

        elif response.status_code == 204:
            print(f'Successful Webex API call: {url} ({method})')
            return

        elif response.status_code == 429:
            print(f'''-----Error 429 (Too Many Requests). Retry in {response.headers["Retry-After"]} seconds -----''')
            time.sleep(int(response.headers["Retry-After"]))
            response = self.execute_rest_call(method, url, payload)
            return response
        
        else:
            raise Exception(response.json())


    def get_detailed_call_history(self, start_time, end_time):
        '''
        Retrieve detailed call history of the last 48 hours as json.
        start_time and end_time need to use the following format: YYYY-MM-DDTHH:MM:SS.mmmZ
        Max 500 entries supported per call. No pagination implemented so far.
        (see also: https://developer.webex.com/docs/api/v1/reports-detailed-call-history/get-detailed-call-history)
        '''

        method = "GET"
        max = 500
        url = f"https://analytics.webexapis.com/v1/cdr_feed?startTime={start_time}&endTime={end_time}&max={max}"
        payload = {}
        
        
        response = self.execute_rest_call(method, url, payload)

        return response['items']


    def get_report_templates(self):
        ''' 
        Get all the report templates:
        (see also: https://developer.webex.com/docs/api/v1/report-templates/list-report-templates)
        '''

        method = "GET"
        url = f'{self.base_url}/report/templates'
        payload = {}

        response = self.execute_rest_call(method, url, payload)

        return response['items']


    def create_report(self, template_id, start_date, end_date):
        ''' 
        Creates a report. 
        endDate - latest possible end date is yesterday for detailed call history report.
        startDate - max 31 days ago
        (see also https://developer.webex.com/docs/api/v1/reports/create-a-report) 
        '''

        method = "POST"
        url = f'{self.base_url}/reports'
        payload = {
            "templateId": int(template_id),
            "startDate": start_date,
            "endDate": end_date
        }

        response = self.execute_rest_call(method, url, payload)

        return response['items']


    def get_report(self, id):
        ''' 
        Check status of a created report based on its ID.
        (see also: https://developer.webex.com/docs/api/v1/reports/get-report-details)
        '''
        method = "GET"
        url = f'{self.base_url}/reports/{id}'
        payload = {}

        response = self.execute_rest_call(method, url, payload)

        return response['items'] 


    def download_report(self, url):
        ''' 
        Download the report data of a created report.
        '''
        method = "GET"
        payload = {}

        response = requests.request(method, url, headers=self.headers, data=payload)
        return response.content


    def delete_report(self, id):
        ''' 
        Delete a report based on its id
        (see also https://developer.webex.com/docs/api/v1/reports/delete-a-report)
        '''
        method = "DELETE"
        url = f'{self.base_url}/reports/{id}'
        payload = {}

        response = self.execute_rest_call(method, url, payload)

        
    def get_call_queues(self):
        '''
        Get Webex call queues.
        (see also https://developer.webex.com/docs/api/v1/features-call-queue/read-the-list-of-call-queues)
        '''
        method = "GET"
        url = f"{self.base_url}/telephony/config/queues"
        payload = {}
        
        response = self.execute_rest_call(method, url, payload)

        return response['queues']


    def get_phone_numbers(self):
        '''
        Get Webex phone numbers of an organization.
        (see also https://developer.webex.com/docs/api/v1/numbers/get-phone-numbers-for-an-organization-with-given-criterias)
        '''

        method = "GET"
        url = f"{self.base_url}/telephony/config/numbers"
        payload = {}
        
        response = self.execute_rest_call(method, url, payload)

        return response['phoneNumbers']

