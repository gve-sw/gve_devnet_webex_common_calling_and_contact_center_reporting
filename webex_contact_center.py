
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

class WebexContactCenterAPI():
    '''
    Class for communication with Webex Contact Center API:
    https://developer.webex-cx.com/documentation/getting-started
    '''
    
    def __init__(self):
        self.access_token=os.getenv("WEBEX_CC_TOKEN")
        self.headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {self.access_token}', 'Accept': 'application/json'}
        self.base_url = 'https://api.wxcc-us1.cisco.com'
        self.organization_id = os.getenv("WXCC_ORG_ID")

    
    def execute_rest_call(self, method, url, payload):
        '''
        Execute and check a REST call based on the provided data.
        '''

        response = requests.request(method, url, headers=self.headers, json=payload)
        
        if response.status_code == 200 or response.status_code == 201:
            print(f'Successful Webex CC API call: {url}')
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

    
    def list_dial_numbers(self):
        '''
        List WxCC dial numbers
        (see also: https://developer.webex-cx.com/documentation/dial-number/v1/list-dial-numbers)
        '''

        method = "GET"
        url = f"{self.base_url}/organization/{self.organization_id}/dial-number"
        payload = {}

        response = self.execute_rest_call(method, url, payload)

        return response


    def list_users(self):
        '''
        List WxCC users
        (see also: https://developer.webex-cx.com/documentation/users/v2/list-users)
        '''

        method = "GET"
        url = f"{self.base_url}/organization/{self.organization_id}/v2/user"
        payload = {}

        response = self.execute_rest_call(method, url, payload)

        return response['data']
