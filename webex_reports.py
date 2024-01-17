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
import time
from pathlib import Path

load_dotenv()

class Webex_Reports():
    ''' 
        Class to create, check download and delete a report.
        Build based on the sample code at: https://github.com/justinhaef/py_webex_report_downloader 
    '''

    def __init__(self, webex_api):
        self.webex_api = webex_api
        self.template_id =  os.getenv("TEMPLATE_ID")   
        self.start_date = os.getenv("REPORT_START_DATE")  
        self.end_date = os.getenv("REPORT_END_DATE") 


    def _get_templates(self):
        ''' Gets and returns all report templates
        '''

        templates = self.webex_api.get_report_templates()
            
        for template in templates:
            print(f"Template Title: {template['title']}, Template ID: {template['Id']}")

        return templates


    def _report_creation(self):
        ''' Creates the needed report.
        '''

        report = self.webex_api.create_report(self.template_id, self.start_date , self.end_date)

        print(f"Created Report ID: {report['Id']}")
        return report['Id']


    def _check_on_report(self, id):
        ''' Loop on a 30 second interval checking if the newly created
            report is done and ready to be downloaded.
        '''
        
        report_status = 'not done'
        download_url = ""
        
        while report_status != 'done':
            
            report = self.webex_api.get_report(id)

            download_url = report[0]['downloadURL']
            report_status = report[0]['status']
            print(f"Report status: {report[0]['status']}, checking in 30 seconds...")
            time.sleep(30)

        print(f'Report Download URL: {download_url}')

        return download_url


    def _download_report(self, url: str, id: str):
        ''' Downloads the report to a new CSV file in the reports folder with the report id 
            as name.
        '''
        try:
            download_content = self.webex_api.download_report(url)
            with open(Path(f'./reports/{id}.csv'), 'wb') as writefile:
                writefile.write(download_content)
            print(f'Downloaded Report... See file reports/{id}.csv')
            return True
        except Exception as e:
            print(f'Error: {e}')


    def _delete_report(self, id):
        ''' Delete the downloaded report.
        '''

        self.webex_api.delete_report(id)

        print(f'Deleted Report with ID: {id}')


    def report_workflow(self):
        '''
        Creates, checks, downloads and deletes a report.
        '''
        
        report_id = self._report_creation()

        report_created = self._check_on_report(id=report_id)
        report_downloaded = self._download_report(url=report_created, id=report_id)
        if report_downloaded:
            self._delete_report(id=report_id)
            return report_id
        else:
            print(f'Unable to download Report ID: {report_id} from URL: {report_created}')