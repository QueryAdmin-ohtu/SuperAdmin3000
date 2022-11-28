*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Resource  resource_survey_status.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page
Library  src/tests/robot_tests/utils.py


*** Test Cases ***
Survey Status Is Red After Creating New Survey
    Go To Backdoor Login Page
    Login With Correct Credentials
    Click Link  New survey
    Create Survey With Details   Status  Status Survey  A survey about Status
    Survey Status Is Red
    ${SURVEY_URL}=  Get Location
    Set Global Variable  ${CURRENT_URL}

Survey Status is Green After Fixing
    Log Variables
    Go To  ${SURVEY_URL}
    Create New Category  Niceness  Very nice