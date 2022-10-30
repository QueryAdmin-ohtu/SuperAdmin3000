*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Resource  resource_add_answer.robot
Resource  resource_create_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Delete Answers
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Button  EDIT
    Expand Answer Card  1
    Click Button  Delete answer
    Expand Answer Card  1
    Click Button  Delete answer
    Expand Answer Card  1
    Click Button  Delete answer
    Expand Answer Card  1
    Click Button  Delete answer
    Expand Answer Card  1
    Click Button  Delete answer

Logged In User Can Add Answer To New Question
    Go To Survey  1
    Click Link  Add question
    Page Should Not Contain  Question answers
    Set Question Text  Why
    Set Category Weight  44
    Click Button  Save changes
    Add New Answer  Because  22
    Expand Answer Card  1
    Page Should Contain  Why
    Textfield Should Contain  cat1  44
    Page Should Contain  Because
    Textfield Should Contain  points-1  22

Logged In User Can Add Answer While Editing Question
    Go To Survey  1
    Click Button  EDIT
    Add New Answer  Hammer  11
    Expand Answer Card  1
    Page Should Contain  Hammer

Points Must Be Numbers
    Go To Survey  1
    Click Link  Add question
    Click Button  Save changes
    Add New Answer  Because  I say so
    Expand Answer Card  1
    Textfield Should Contain  points-1  0
    Page Should Contain  Because

Empty Points Are Interpreted As Zeros
    Click Element  id:survey-1
    Click Link  Add question
    Click Button  Save changes
    Add Answer Without Arguments
    Page Should Contain  Answer 1:
    Expand Answer Card  1
    Textfield Should Contain  points-1  0

Logged In User Can Delete Answer
    Go To Survey  1
    Click Button  EDIT
    Page Should Contain  Hammer
    Expand Answer Card  1
    Click Button  Delete answer
    Page Should Not Contain  Hammer

Logged In User Can Edit Answer
    Click Link  New survey
    Make A Survey
    Click Link  Add question
    Click Button  Save changes
    Add New Answer  Do Not  44
    Expand Answer Card  1
    Page Should Contain  Do Not
    Edit Answer  toivo  12  1
    Click Button  Save changes
    Expand Answer Card  1
    Page Should Not Contain  Do Not
    Page Should Contain  toivo
    Textfield Should Contain  points-1  12