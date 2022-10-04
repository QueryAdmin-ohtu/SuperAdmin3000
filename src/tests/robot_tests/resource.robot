*** Settings ***
Library  SeleniumLibrary


*** Variables ***
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${URL}  http://localhost:5000
${BACKDOOR URL}  ${URL}/backdoor
${EDIT URL}  ${URL}/edit
${NEW URL}  ${URL}/new

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
    Go To  ${NEW URL}

Go To Survey
    [Arguments]  ${survey_id}
    Go To  ${URL}/surveys/${survey_id}
