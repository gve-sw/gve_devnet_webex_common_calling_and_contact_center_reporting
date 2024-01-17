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

from flask import Flask, render_template
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os

from webex import WebexAPI
from webex_reports import Webex_Reports
from csv_reader import CSVReader
from webex_contact_center import WebexContactCenterAPI
from report_processing import ReportProcessing

load_dotenv()

app = Flask(__name__)


def retrieve_categorization_data():
    '''
    Requests all information required for categoriation.
    '''

    wxcc_dial_numbers = webex_cc_api.list_dial_numbers()
    w_queue_numbers = webex_api.get_call_queues()
    wxcc_user = webex_cc_api.list_users()
    w_phone_numbers = webex_api.get_phone_numbers()

    return wxcc_dial_numbers, w_queue_numbers, wxcc_user, w_phone_numbers


@app.route('/history')
def history():
    '''
    Route to view the historic call flows (Max 31 days and latest end_date yesterday)
    '''
    try:
        
        report_id = wbx_report.report_workflow()
        #report_id = "<Fill in name of report file to use (without .csv)>"
        call_history = CSVReader.csv_to_dict(f'./reports/{report_id}.csv')
        
        wxcc_dial_numbers, w_queue_numbers, wxcc_user, w_phone_numbers = retrieve_categorization_data()
        
        report_processor = ReportProcessing(call_history, wxcc_dial_numbers, wxcc_user, w_queue_numbers, w_phone_numbers)
        final_report_data = report_processor.process_report_data()
        
        return render_template('table.html', hiddenLinks=False, call_history=final_report_data)
    except Exception as e: 
        print(f"Error: {e}")  
        return render_template('table.html', error=True, errormessage=e, call_history=[])


@app.route('/latest')
def latest():
    '''
    Route to view historic call flow data of last 48 h
    '''
    try:

        time_zone_difference = int(os.getenv("TIME_ZONE_DIFF")) 
        end_date = datetime.now() - timedelta(hours=time_zone_difference, minutes=5)
        start_date = datetime.now() - timedelta(hours=47+time_zone_difference, minutes=55) 
        start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        end_date = end_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")

        call_history = webex_api.get_detailed_call_history(start_date, end_date)

        wxcc_dial_numbers, w_queue_numbers, wxcc_user, w_phone_numbers = retrieve_categorization_data()

        report_processor = ReportProcessing(call_history, wxcc_dial_numbers, wxcc_user, w_queue_numbers, w_phone_numbers)
        final_report_data = report_processor.process_report_data()

        return render_template('table.html', hiddenLinks=False, call_history=final_report_data)
    except Exception as e: 
        print(f"Error: {e}")  
        return render_template('table.html', error=True, errormessage=e, call_history=[])


@app.route('/templates')
def templates():
    try:
        templates = wbx_report._get_templates()

        return render_template('templates.html', hiddenLinks=False, templates=templates)

    except Exception as e: 
        print(f"Error: {e}")  
        return render_template('templates.html', error=True, errormessage=e)


if __name__ == "__main__":
    webex_api = WebexAPI()
    wbx_report = Webex_Reports(webex_api)
    webex_cc_api = WebexContactCenterAPI()
    app.run(host='0.0.0.0', port=5000, debug=True)