# gve_devnet_webex_common_calling_and_contact_center_reporting

This sample code shows a Webex Call Flow Dashboard, which allows you to view different call flows and their associated data within a pre-defined time range (max last 31 days). Additionally, the calling and called numbers of each entry, are categorized as Webex Call Queue, WxCC Dial Number, WxCC Agent User, WxCC User, Webex User, Webex number or other.


## Contacts
* Ramona Renner


## Solution Components
* Webex Control Hub (with Pro Pack subscription, Admin User Account)
* Webex Contact Center (with Contact Center Administrator User Account)
* Webex Calling


## Prerequisites

- **Webex API Personal Token**:
1. To use the Webex REST API in this demo, you need a Webex admin account backed by Cisco Webex Common Identity (CI) with a Pro Pack subscription.
2. When making a request to the Webex REST API, the request must contain a header that includes the access token. A personal access token can be obtained [here](https://developer.webex.com/docs/getting-started).

    > Note: This token has a short lifetime - only 12 hours after logging into this site - so it shouldn't be used outside of app development. For a production environment use a [oAuth integration](https://developer.webex.com/docs/integrations)).


- **Webex Contact Center API Personal Token and Organization ID**:
1. To use the Webex Contact Center REST API, you need a Webex Contact Center Administrator account. 
2. When making a request to the API, the request must contain a header that includes the access token. A personal access token can be obtained via the following steps:
* Go to: https://developer.webex-cx.com/documentation/dial-number/v1/list-dial-numbers and sign in as a Webex Contact Center Administrator. 
* Click the **Try Out** tab on the right side of the page
* Click the **Copy Icon** next to the **Authorization** text field to copy and save the token
* Copy and save the **orgid** from the **Parameters** section


    > Note: This token has a short lifetime - so it shouldn't be used outside of app development. For a production environment use a [oAuth integration](https://developer.webex-cx.com/documentation/authentication).

## Installation and Running

There are several options for running this demo:

* Option 1: Run Sample Code in a Docker Container - Requires to [install Docker](https://docs.docker.com/get-docker/).
* Option 2: Install and Run Sample Code Locally - Requires to [install Python 3.8](https://www.python.org/downloads/)


### Option 1: Run Sample Code in a Docker Container

1. Make sure Docker is installed in your environment, and if not, you may [install Docker](https://docs.docker.com/get-docker/).

2. Clone this Github repository:
    ```git clone [add github link here]```
    * For Github link: In Github, click on the clone or download button in the upper part of the page > click the copy icon
    * Or simply download the repository as a zip file using the 'Download ZIP' button and extract it

3. Access the downloaded folder:

    ```cd gve_devnet_webex_common_calling_and_contact_center_reporting```   

4. Create an .env file with the following variables:

```
WEBEX_TOKEN=<Personal Token for Webex API (see Prerequisites section)>
WEBEX_CC_TOKEN=<Personal Token for Webex Contact Center API (see Prerequisites section)>
REPORT_START_DATE=<Format YYYY-MM-DD, max 31 days ago>
REPORT_END_DATE=<Format YYYY-MM-DD, min 1 day ago>
TEMPLATE_ID=<Report template ID of the Call History Report, e.g. 500. (see hint)>
WXCC_ORG_ID=<ID of the WxCC organization (see Prerequisites section)>"
LOCAL_TIME_ZONE="<Local Time zone, e.g. Europe/Berlin (see hint)>"
TIME_ZONE_DIFF="<Negative hour difference between local time and WxC, WxCC lab time>" 
```   

> Hint: Get a list of all available templates and their associated IDs by accessing `localhost:5000/templates` via the browser after starting the application without a set template id environment variable.   

> Hint: [Full list of available time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)


5.1 To run the code via Docker compose, using the command:

    ```docker compose up```

5.2  **OR** use the following command to build a new image and run the docker container.

    ```docker build .```

    ```docker run -p 5000:5000 -e TZ=<Fill in your time zone (see hint)> <Fill in the image id (see output of last command "writing image sha256:<image_id>")>```         

> Hint: [Full list of available time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)


### Option 2: Install and Run Sample Code Locally

1. Make sure Python 3.8 is installed in your environment, and if not, you may download Python 3.8 [here](https://www.python.org/downloads/).

2. (Optional) Create and activate a virtual environment for the project ([Instructions](https://docs.python.org/3/tutorial/venv.html)).

3. (Optional) Access the created virtual environment folder   

    ```cd [add name of virtual environment here]``` 

4. Clone this Github repository:
    ```git clone [add github link here]```
    * For Github link: In Github, click on the clone or download button in the upper part of the page > click the copy icon
    * Or simply download the repository as a zip file using the 'Download ZIP' button and extract it

5. Access the downloaded folder:

    ```cd gve_devnet_webex_common_calling_and_contact_center_reporting```   

6. Create an .env file with the following variables:

```
WEBEX_TOKEN=<Personal Token for Webex API (see Prerequisites section)>
WEBEX_CC_TOKEN=<Personal Token for Webex Contact Center API (see Prerequisites section)>
REPORT_START_DATE=<Format YYYY-MM-DD, max 31 days ago>
REPORT_END_DATE=<Format YYYY-MM-DD, min 1 day ago>
TEMPLATE_ID=<Report template ID of the Call History Report, e.g. 500. (see hint)>
WXCC_ORG_ID=<ID of the WxCC organization (see Prerequisites section)>"
LOCAL_TIME_ZONE="<Local Time zone, e.g. Europe/Berlin (see hint)>"
TIME_ZONE_DIFF="<Negative hour difference between local time and WxC lab time>"
```   

> Hint: Get a list of all available templates and their associated IDs by accessing `localhost:5000/templates` via the browser after starting the application without a set template id environment variable.   

> Hint: [Full list of available time zones](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List)

7. Install all dependencies:

    ```pip3 install -r requirements.txt```  


8. To run the code, using the command:
    
    ```$ python3 app.py```

## Usage

![/IMAGES/0image.png](/IMAGES/screenshot1.png)

* Access the Call Flow Dashboard for historic call details via **localhost:5000/history**.
**Please be aware that the creation and download of a new report take a few minutes. During this time, the page stays in loading mode.**

    > Hint: In case a report was downloaded via the script before and is available as a file in the report folder. It is possible to use the mentioned file instead of downloading a new one. Therefore, comment line 50 in the app.py file, fill in the name of the file (without .csv) in line 51 and uncomment line 51. Only supported with local installation or Docker build and run command.

* Access the Call Flow Dashboard for current call details via **localhost:5000/latest**

* Access a list of all templates and associated IDs via **localhost:5000/templates**


### Limitations

* The sample code only uses temporary personal access tokens for authentication. These tokens are only meant for app development purposes. In production, the use of OAuth integrations is recommended.
* The report functionality was only tested for the Webex Control Hub report **Detailed Call History**.
* The demo implements only limited error handling.
* The retrieval of the call history entries (see localhost:5000/latest) of the last 48 hours is currently limited to 500 entries. For more entries, the implementation of pagination logic is required.

### Reference

* This sample code uses some of the code from https://github.com/justinhaef/py_webex_report_downloader.

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.