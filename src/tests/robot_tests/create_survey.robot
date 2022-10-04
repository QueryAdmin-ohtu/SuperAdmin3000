*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Create Questionnaires
    Go To Backdoor Login Page
    Login With Correct Credentials
    Make Two Surveys
    Go To Home Page
    Click Link  Create a new survey
    Make A Survey
    Page Should Contain  Testi
    Page Should Contain  Toimiikohan
    Page Should Contain  Surveyn tekeminen testauksessa

Logged In User Cannot Create Questionnaires Without Name
    Click Link  Create a new survey
    Make Survey Without Name
    Alert Should Be Present  Must have a name

Logged In User Cannot Create Questionnaires Without Title
    Click Link  Create a new survey
    Make Survey Without Title
    Alert Should Be Present  Must have a title

Logged In User Cannot Create Questionnaires Without Text
    Click Link  Create a new survey
    Make Survey Without Text
    Alert Should Be Present  Must have a flavor text

A New Survey Does Not Contain Questions
    Click Link  Create a new survey
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
