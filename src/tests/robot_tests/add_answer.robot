*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Resource  resource_add_answer.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Add Answer To New Question
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Link  Add question
    Page Should Not Contain  Question answers
    Set Question Text  Why
    Set Category Weight  44
    Add New Answer  Because  22
    Page Should Contain  Why
    Page Should Contain  44
    Page Should Contain  Because
    Page Should Contain  22
    Page Should Contain  Question answers

Logged In User Can Add Answer While Editing Question
    Go To Survey  1
    Click Button  EDIT
    Add New Answer  Hammer  11
    Page Should Contain  Hammer

Points Must Be Numbers
    Go To Survey  1
    Click Link  Add question
    Add New Answer  Because  I say so
    Page Should Contain  Invalid points

Empty Points Are Interpreted As Zeros
    Click Element  id:survey-1
    Click Link  Add question
    Add Answer Without Arguments
    Page Should Contain  Question answers
    Page Should Contain  0

Logged In User Can Delete Answer
    Go To Survey  1
    Click Button  EDIT
    Page Should Contain  Hammer
    Click Button  Delete answer
    Handle Alert  Accept
    Page Should Not Contain  Hammer