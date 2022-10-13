*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can View Admins
    Go To Backdoor Login Page
    Login With Correct Credentials
    Click Link  Admins
    Page Should Contain  Authorized users
    Page Should Contain  2
    Page Should Contain  8