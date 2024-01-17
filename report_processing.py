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

import copy

class ReportProcessing:
    '''
    Class for report processing - sorts, orders, filters and categorizes the report entries.
    '''

    def __init__(self, call_history, wxcc_dial_numbers, wxcc_user, w_queue_numbers, w_phone_numbers):
        self.call_history = call_history
        self.wxcc_dial_numbers = wxcc_dial_numbers
        self.wxcc_user = wxcc_user
        self.w_phone_numbers = w_phone_numbers
        self.w_queue_numbers = w_queue_numbers


    def entry_is_no_notification_entry(self, call_entry):
        '''
        Checks if an call history entry is a PushNotificationRetrieval entry.
        '''
        
        return call_entry['Related reason'] != "PushNotificationRetrieval"


    def sort_based_on_correlation_id(self, call_history):
        '''
        Sorts the call history in groups based on the correlation ID of each entry.
        '''

        sorted_history = {}

        for call_entry in call_history:
            
            if self.entry_is_no_notification_entry(call_entry): 
                
                correlation_id = call_entry['Correlation ID']
                if correlation_id in sorted_history:
                    sorted_history[correlation_id].append(call_entry)
                else:
                    sorted_history[correlation_id] = [call_entry]


        return sorted_history


    def entries_of_same_bidirectional_connection(self, compare_call_entry, call_entry):
        '''
        Checks if two entries are part of the same connection. Each covering one of the directions. 
        '''
        
        return compare_call_entry["Start time"] == call_entry["Start time"] and compare_call_entry["Called number"] == call_entry["Called number"] and compare_call_entry['Direction'] == "TERMINATING" and call_entry['Direction'] == "ORIGINATING"


    def remove_origination_entries_for_two_way_entries(self, call_history):
        '''
        Removes the ORIGINATING entries in case an associated TERMINATING entry for the same connection is additionally available in the call history.
        '''
        
        filtered_call_history = {}

        for call_entry_group_key, call_entry_group in call_history.items():
            filtered_call_history[call_entry_group_key] = []

            for call_entry in call_entry_group: 

                mark_for_delete = False

                for compare_call_entry in call_entry_group: 

                    if self.entries_of_same_bidirectional_connection(compare_call_entry, call_entry):

                        mark_for_delete = True
                        break

                if not mark_for_delete:
                    filtered_call_history[call_entry_group_key].append(call_entry)
        
        return filtered_call_history


    def sort_by_start_time(self, call_history):
        '''
        Sorts the call history entries by start time. 
        '''

        ordered_call_history = copy.deepcopy(call_history)

        for call_entry_group_key, call_entry_group in call_history.items():
            ordered_call_history[call_entry_group_key] = []

            ordered_call_history[call_entry_group_key] = sorted(call_entry_group, key=lambda x: x['Start time'])

        return ordered_call_history


    def already_categorized_number(self, number_string):
        '''
        Checks if a number string was already tagged.
        '''

        if "(" in number_string:
            return False
        return True


    def tag_calling_string(self, call_entry, calling_number, tag):
        '''
        Tags calling number string and returns new calling_number value.
        '''

        call_entry['Calling number'] = f"{calling_number} {tag}"
        calling_number = call_entry['Calling number']
        return call_entry, calling_number


    def tag_called_string(self, call_entry, called_number, tag):
        '''
        Tags called number string and returns new called_number value.
        '''

        call_entry['Called number'] = f"{called_number} {tag}"
        called_number = call_entry['Called number']
        return call_entry, called_number


    def compare_and_tag_number_on_match(self, call_entry, identifier_number, calling_number, called_number, tag):
        '''
        Compares the calling and called number with the identifier number. 
        If equal and number wasn't categorized before, it is tagged.
        '''
        
        if calling_number == identifier_number and self.already_categorized_number(calling_number):
            call_entry, calling_number = self.tag_calling_string(call_entry, calling_number, tag)
        if called_number == identifier_number and self.already_categorized_number(called_number):
            call_entry, called_number = self.tag_called_string(call_entry, called_number, tag)

        return call_entry, calling_number, called_number


    def map_and_tag_numbers(self, call_entry, identifiers_numbers, identifier_key, tag, calling_number, called_number):
        '''
        Maps the calling and called numbers to a identifiers_number (in identifiers_numbers list with identifier_key).
        On successful mapping the number is tagged with a provided tag string.
        '''

        for identifier_number_entry in identifiers_numbers:
            if identifier_key in identifier_number_entry:
                identifier_number= identifier_number_entry[identifier_key]

                call_entry, calling_number, called_number = self.compare_and_tag_number_on_match(call_entry, identifier_number, calling_number, called_number, tag) 

        return call_entry, calling_number, called_number


    def map_and_tag_wxcc_users(self, call_entry, wxcc_users, calling_number, called_number):
        '''
        Maps the user uuid to WxCC users. Furthermore, it checks if the mapped user has a agend profil ID.
        On successful mapping the calling or called number is tagged with (WxCC Agent User) or (WxCC User).
        '''

        report_user_uuid = call_entry['User UUID']
        direction = call_entry['Direction']

        for user in wxcc_users:
            user_uuid = user['ciUserId']

            if report_user_uuid == user_uuid:
                if self.already_categorized_number(called_number):
                    if "agentProfileId" in user:
                        if direction == "ORIGINATING":
                            call_entry, calling_number = self.tag_calling_string(call_entry, calling_number, "(WxCC Agent User)")
                        if direction == "TERMINATING":
                            call_entry, called_number = self.tag_called_string(call_entry, called_number, "(WxCC Agent User)")
                    else:
                        if direction == "ORIGINATING":
                            call_entry, calling_number = self.tag_calling_string(call_entry, calling_number, "(WxCC User)")
                        if direction == "TERMINATING":
                            call_entry, called_number = self.tag_called_string(call_entry, called_number, "(WxCC User)")

        return call_entry, calling_number, called_number


    def map_and_tag_webex_numbers(self, call_entry, w_phone_numbers, calling_number, called_number):
        '''
        Maps the calling and called numbers to Webex numbers and their owner type.
        On successful mapping the number is tagged with (Webex User) or (Webex Number).
        '''

        for number in w_phone_numbers:

            if "phoneNumber" in number:
                phone_number = number['phoneNumber']
                owner_type = number['owner']['type']

                if owner_type == "PEOPLE":
                    call_entry, calling_number, called_number = self.compare_and_tag_number_on_match(call_entry, phone_number, calling_number, called_number, "(Webex User)") 
                else: 
                    call_entry, calling_number, called_number = self.compare_and_tag_number_on_match(call_entry, phone_number, calling_number, called_number, "(Webex Number)") 

        return call_entry, calling_number, called_number


    def categorize_entries(self, call_history):
        '''
        Categorizes the calling number, called number or user uuid of all report entries based on information
        about the WxCC dial numbers, Webex queue numbers, Webex overall numbers or WxCC users. 
        '''

        categorized_call_history = copy.deepcopy(call_history)
        
        for key, call_entry_group in categorized_call_history.items():

            for call_entry in call_entry_group:
                calling_number = call_entry['Calling number']
                called_number = call_entry['Called number']
                
                call_entry, calling_number, called_number = self.map_and_tag_numbers(call_entry, self.wxcc_dial_numbers, "dialledNumber", "(WxCC Dial Number)", calling_number, called_number)
                call_entry, calling_number, called_number = self.map_and_tag_wxcc_users(call_entry, self.wxcc_user, calling_number, called_number)
                call_entry, calling_number, called_number = self.map_and_tag_numbers(call_entry, self.w_queue_numbers, "phoneNumber", "(Webex Call Queue)", calling_number, called_number)
                call_entry, calling_number, called_number = self.map_and_tag_webex_numbers(call_entry, self.w_phone_numbers, calling_number, called_number)

        return categorized_call_history


    def process_report_data(self):
        '''
        Takes the call history report and sorts, orders, filters and categorizes the content.
        '''

        call_history = self.sort_based_on_correlation_id(self.call_history)
        call_history = self.remove_origination_entries_for_two_way_entries(call_history)
        call_history = self.sort_by_start_time(call_history)
        call_history = self.categorize_entries(call_history)

        return call_history
        



