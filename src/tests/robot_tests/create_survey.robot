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
    Click Link  New survey
    Make A Survey
    Element Should Be Visible  id:notification
    Page Should Contain  Testi survey was created
    Page Should Contain  Testi
    Page Should Contain  Toimiikohan
    Page Should Contain  Surveyn tekeminen testauksessa
    Page Should Contain  0% - 100% of the max points
    Page Should Contain  Your skills in this topic are excellent!

Logged In User Cannot Create Surveys Without Name
    Click Link  New survey
    Make Survey Without Name
    Page Should Contain  Create a new survey
    Page Should Not Contain  Statistics
    Page Should Not Contain  Survey has no questions

Logged In User Cannot Create Surveys Without Title
    Click Link  New survey
    Make Survey Without Title
    Page Should Not Contain  Statistics
    Page Should Not Contain  Survey has no questions

Logged In User Cannot Create Surveys Without Text
    Click Link  New survey
    Make Survey Without Text
    Page Should Not Contain  Statistics
    Page Should Not Contain  Survey has no questions

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