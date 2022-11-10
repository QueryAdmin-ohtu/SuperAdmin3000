*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page


*** Test Cases ***
User Can Create New Survey Result
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  8
    Click Link  Add result
    Set Result Text  You most resemble an African elephant
    Save Result
    Page Should Contain  You most resemble an African elephant
    Page Should Contain  Add result

First Survey Result Must Have Cutoff Value Of One
    Go To Survey  7
    Click Link  Add result
    Set Result Text  You're Hanko!
    Set Result Cutoff  0.5
    Save Result
    Page Should Contain  Add a result to

User Can Create Subsequent Survey Results With Cutoff Values Between 0 And 1
    Go To Survey  8
    Click Link  Add result
    Set Result Text  You look like an Indian elephant
    Set Result Cutoff  0.5
    Save Result
    Page Should Contain  You look like an Indian elephant
    Page Should Contain  Add result

Survey Results Can't Have Duplicate Cutoff Values
    Go To Survey  8
    Click Link  Add result
    Set Result Text  You don't look like an elephant at all
    Set Result Cutoff  0.5
    Save Result
    Page Should Not Contain  You don't look like an elephant at all

Subsequent Survey Results Must Have Cutoff Value Between 0 And 1
    Go To Survey  8
    Click Link  Add result
    Set Result Text  You transcend all earthly elephants
    Set Result Cutoff  15
    Save Result
    Page Should Contain  Add a result to
    

*** Keywords ***
Set Result Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Result Cutoff
    [Arguments]  ${value}
    Input Text  cutoff  ${value}

Save Result
    Click Button  Save changes