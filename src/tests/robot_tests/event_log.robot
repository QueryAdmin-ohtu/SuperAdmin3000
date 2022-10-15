*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Logged In User Can View Event Logs
    Login Through Backdoor
    Click link  Logs
    Page Should Contain  EVENT

Logged Out User Cannot View Event Logs
    Logout
    Page Should Contain  Please login