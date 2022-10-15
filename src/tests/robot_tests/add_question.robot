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
    Go To Survey  1
    Page Should Contain  Add question
    Click Link  Add question
    Page Should Contain  Category weights
<<<<<<< HEAD
    Add New Question  kysymys1  1
=======
    Add New Question  kysymys1  0.5
>>>>>>> main
    Page Should Contain  kysymys1

Invalid Category Weights Default to Zeros
    Go To Survey  1
    Click Link  Add question
    Add New Question  kysymys2  abc
    Go To Home Page
    Go To Survey  1
    Page Should Contain  kysymys2
    Edit Question By Table Row  14
    Textfield Should Contain  cat1  0

Empty Category Weights Are Interpreted As Zeros
    Click Element  id:survey-1
    Click Link  Add question
    Add Question With No Weights  kysymys3
    Page Should Contain  kysymys3