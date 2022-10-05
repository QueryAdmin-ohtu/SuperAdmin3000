*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Create Surveys
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Home Page
    Click Link  New survey
    Make A Survey
    Page Should Contain  Testi
    Page Should Contain  Toimiikohan
    Page Should Contain  Surveyn tekeminen testauksessa

Logged In User Cannot Create Surveys Without Name
    Click Link  New survey
    Make Survey Without Name
    Alert Should Be Present  Must have a name

Logged In User Cannot Create Surveys Without Title
    Click Link  New survey
    Make Survey Without Title
    Alert Should Be Present  Must have a title

Logged In User Cannot Create Surveys Without Text
    Click Link  New survey
    Make Survey Without Text
    Alert Should Be Present  Must have a flavor text

A New Survey Does Not Contain Questions
    Click Link  New survey
    Make A Survey
    Page Should Contain  Survey has no questions

Questions Of Survey Are Displayed On Survey Page
    Go To Survey  1
    Page Should Contain  Question 1
    Page Should Contain  Question 2
    Page Should Contain  Question 3
    Page Should Contain  Question 4
    Page Should Contain  Question 5
    Page Should Contain  Question 6

Logged Out User Cannot Create Surveys
    Logout
    Go To Create New Survey Page
    Page Should Contain  Please login

Logged Out User Cannot See Surveys
    Go To Survey  1
    Page Should Contain  Please login
    Go To Home Page
    Page Should Contain  Please login