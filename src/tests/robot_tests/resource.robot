*** Settings ***
Library  SeleniumLibrary

*** Variables ***
${SERVER}  localhost:5000
${BROWSER}  headlesschrome
${DELAY}  0 seconds
${HOME URL}  http://${SERVER}
${BACKDOOR URL}  http://${SERVER}/backdoor
${EDIT URL}  http://${SERVER}/edit
${NEW URL}  http://${SERVER}/new


*** Keywords ***
Open And Configure Browser
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}

Go To Home Page
    Go To  ${HOME URL}

Go To Backdoor Login Page
    Go To  ${BACKDOOR URL}

Go To Edit Questionnaires Page
    Go To  ${EDIT}

Go To Create New Questionnaire Page
    Go To  ${NEW}