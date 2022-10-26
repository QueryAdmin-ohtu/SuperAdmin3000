*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${URL}  http://localhost:5000
${BACKDOOR URL}  ${URL}/backdoor
${EDIT URL}  ${URL}/surveys/1/edit
${NEW SURVEY URL}  ${URL}/surveys/new-survey
${ADMIN URL}  ${URL}/admins

*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Go To Home Page
    Go To  ${URL}

Go To Backdoor Login Page
    Go To  ${BACKDOOR URL}

Go To Edit Surveys Page
    Go To  ${EDIT URL}

Go To Create New Survey Page
    Go To  ${NEW SURVEY URL}

Go To Survey
    [Arguments]  ${survey_id}
    Go To  ${URL}/surveys/${survey_id}

Delete Question
    [Arguments]  ${survey_id}  ${question_id}
    Go To  ${URL}/delete/${survey_id}/${question_id}

Go To Admins Page
    Go To  ${ADMIN URL}

Login Through Backdoor
    Go To Backdoor Login Page
    Set Username  rudolf
    Set Password  secret
    Click Button  Login

Logout
    Click Button  Logout

Notification Is Displayed
    Element Should Be Visible  id:notification

Notification Is Not Displayed
    Element Should Not Be Visible  id:notification