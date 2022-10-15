*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Logged In User Can View Audit Logs
    Login Through Backdoor
    Click link  Logs
    Page Should Contain  fancy schmancy logs go here