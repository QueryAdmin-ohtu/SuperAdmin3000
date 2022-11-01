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
    Page Should Contain  Event log

Logged Out User Cannot View Event Logs
    Logout
    Page Should Contain  Please login

Logged In User Can Change The The Log Sort Order
    Login Through Backdoor
    Click Link  Logs
    Click Link  Oldest first
    Page Should Contain  Newest first