*** Settings ***
Resource  resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged Out User Cannot List All Surveys
    Go To List All Surveys Page
    Page Should Contain  Please login

Logged In User Can List All Surveys
    Click Link  List all surveys
    Page Should Contain  List all surveys
    Page Should Contain  Title: This will be survey title text
    Page Should Contain  Questions: 9
    Page Should Contain  Submissions: 3
    