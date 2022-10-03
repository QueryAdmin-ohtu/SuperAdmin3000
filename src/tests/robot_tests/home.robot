*** Settings ***
Resource  resource.robot
Resource  login_resource.robot
Resource  creating_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Home Page Should Be Open
    Title Should Be  Super Admin 3000

User Logged In With Correct Credentials
    Go To Backdoor Login Page
    Login With Correct Credentials
    Page Should Contain  Hello rudolf!

Logged In User Can Edit Questionnaires
    Click Link  Edit an existing survey
    Page Should Contain  Here you can eventually edit or delete existing questionnaires

Logged In User Can Create Questionnaires
    Make Two Surveys
    Go To Home Page
    Click Link  Create a new survey
    Make A Survey
    Page Should Contain  Testi
    Page Should Contain  Toimiikohan
    Page Should Contain  Surveyn tekeminen testauksessa

Logged In User Cannot Create Questionnaires Without Name
    Go To Home Page
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

A new survey does not contain questions
    Click Link  Create a new survey
    Make A Survey
    Page Should Contain  Survey has no questions

Questions of survey are displayed on survey Page
    Go To Survey  1
    Page Should Contain  Question 1
    Page Should Contain  Question 2
    Page Should Contain  Question 3
    Page Should Contain  Question 4
    Page Should Contain  Question 5
    Page Should Contain  Question 6

Logged Out User Cannot Access Questionnaires
    Logout
    Page Should Not Contain  You are logged in as

Logged Out User Cannot Edit Questionnaires
    Go To Edit Questionnaires Page
    Page Should Contain  Please login 

Logged Out User Cannot Create Questionnaires
    Go To Create New Questionnaire Page
    Page Should Contain  Please login

*** Keywords ***
Login With Correct Credentials
    Set Username  rudolf
    Set Password  secret
    Submit Credentials

Make Two Surveys
    Go To Home Page
    Click Link  Create a new survey
    Set Survey Name  Making two surveys
    Set Survey Title  Which fail
    Set Survey Text  To make the third one work
    Create A Survey
    Go To Home Page
    Click Link  Create a new survey
    Set Survey Name  Making two surveys
    Set Survey Title  Which fail
    Set Survey Text  To make the third one work
    Create A Survey

Make A Survey
    Set Survey Name  Testi
    Set Survey Title  Surveyn tekeminen testauksessa
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Name
    Set Survey Title  Surveyn tekeminen testauksessa
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Title
    Set Survey Name  Testi
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Text
    Set Survey Name  Testi
    Set Survey Title  Surveyn tekeminen testauksessa
    Create A Survey