*** Settings ***
Resource  resource.robot
Resource  login_resource.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Home Page Should Be Open
    Title Should Be  SuperAdmin3000

User Logged In With Correct Credentials
    Go To Backdoor Login Page
    Login With Correct Credentials
    Page Should Contain  You are logged in as

Logged In User Can Edit Questionnaires
    Click Link  Edit existing questionnaire
    Title Should Be  SuperAdmin3000 Edit

Logged In User Can Create Questionnaires
    Go To Home Page
    Click Link  Create a new questionnaire
    Title Should Be  SuperAdmin3000 New

Logged Out User Cannot Access Questionnaires
    Logout
    Page Should Not Contain  You are logged in as

*** Keywords ***
Login With Correct Credentials
    Set Username  rudolf
    Set Password  secret
    Submit Credentials