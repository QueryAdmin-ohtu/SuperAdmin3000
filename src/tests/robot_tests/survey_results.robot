*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_manage_results.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page


*** Test Cases ***
User Can Create New Survey Result
     Go To Backdoor Login Page
     Login With Correct Credentials
     Go To Survey  8
     Click Link  Manage results
     Set Result Text  You most resemble an African elephant
     Save Result
     Page Should Contain  Result at cutoff point 1.0:
# TODO: Expand Result Card doesn't work
#     Expand Result Card  1
#     Page Should Contain  You most resemble an African elephant


First Survey Result Must Have Cutoff Value Of One
    Go To Survey  7
    Click Link  Manage results
    Set Result Text  You're Hanko!
    Set Result Cutoff  0.5
    Save Result
    Page Should Not Contain  Result at cutoff point

User Can Create Subsequent Survey Results With Cutoff Values Between 0 And 1
    Go To Survey  8
    Click Link  Manage results
    Set Result Text  You look like an Indian elephant
    Set Result Cutoff  0.5
    Save Result
    Page Should Contain  Result at cutoff point 0.5:
    Expand Result Card  1
    Page Should Contain  You look like an Indian elephant

Survey Results Can't Have Duplicate Cutoff Values
    Go To Survey  8
    Click Link  Manage results
    Set Result Text  You don't look like an elephant at all
    Set Result Cutoff  0.5
    Save Result
    Expand Result Card  1
    Expand Result Card  2
    Page Should Not Contain  You don't look like an elephant at all

Subsequent Survey Results Must Have Cutoff Value Between 0 And 1
    Go To Survey  8
    Click Link  Manage results
    Set Result Text  You transcend all earthly elephants
    Set Result Cutoff  15
    Save Result
    Page Should Not Contain  Result at cutoff point 15
