*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_delete_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Delete An Existing Survey
    Go To Backdoor Login Page
    Login With Correct Credentials
    Make A Survey To Delete
    Delete The Survey
    Page Should Not Contain  Poistuisikohan