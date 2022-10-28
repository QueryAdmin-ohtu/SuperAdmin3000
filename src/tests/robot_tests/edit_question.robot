*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Resource  resource_add_question.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Edit a Question
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Button  EDIT
    Add New Question  changed  99.0
    Click Button  Save changes
    Page Should Contain  changed
    Page Should Not Contain  Question 1
    Go To Survey  1
    Click Button  EDIT
    Textfield Should Contain  cat1  99.0
    Page Should Contain  changed

Editing Without Changing Anything Works
    Go To Survey  1
    Click Button  EDIT
    Add Question Without Arguments
    Page Should Contain  changed

Back Button Opens Correct Survey Page
    Go To Survey  1
    Click Button  EDIT
    Click Link  Back
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text