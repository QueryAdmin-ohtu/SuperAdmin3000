*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_survey_status.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page


*** Test Cases ***
Survey Status Is Red After Creating New Survey
    Go To Backdoor Login Page
    Login With Correct Credentials
    Click Link  New survey
    Create Survey With Details   Status  Status Survey  A survey about Status
    Survey Status Is Red
    ${SURVEY_URL}=  Get Location
    Set Global Variable  ${SURVEY_URL}

Survey Status is Green After Adding Category Question And Answer
    Go To  ${SURVEY_URL}
    Create New Category  Alertness  How alerted are you
    Add New Question  When?  1
    Add New Answer  Now  1
    Click Link  Back to survey
    Survey Status Is Green