*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Add a New Question
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Home Page
    Click Element  id:survey-1
    Page Should Contain  Add question
    Click Link  Add question
    Page Should Contain  Insert category weights
    Add New Question  kysymys1  0.5
    Page Should Contain  kysymys1

Category Weights Must Be Numbers
    Click Element  id:survey-1
    Click Link  Add question
    Add New Question  kysymys2  abc
    Page Should Contain  Invalid weights

Empty Category Weights Are Interpreted As Zeros
    Click Element  id:survey-1
    Click Link  Add question
    Add Question With No Weights  kysymys3
    Page Should Contain  kysymys3