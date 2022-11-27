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
    Click Link  edit-question-1
    Add New Question  changed  99.0
    Click Button  Save changes
    Page Should Contain  changed
    Page Should Not Contain  Question 1
    Go To Survey  1
    Click Link  edit-question-1
    Textfield Should Contain  cat1  99.0
    Page Should Contain  changed

Editing Without Changing Anything Works
    Go To Survey  1
    Click Link  edit-question-1
    Add Question Without Arguments
    Page Should Contain  changed

Edit Question View Should Display Survey Name
    Go To Survey  1
    Click Link  edit-question-1
    Page Should Contain  test_name

User Can Set Category Weights With A Precision Of 0.1
    Go To Survey  1
    Click Link  edit-question-1
    Add New Question  weight  1.1
    Click Button  Save changes
    Page Should Contain  weight

User Can Not Set Category Weights With A Precision Of 0.01
    Go To Survey  1
    Click Link  edit-question-1
    Add New Question  invalid_weight  1.11
    Click Button  Save changes
    Page Should Not Contain  invalid_weight

Back Button Opens Correct Survey Page
    Go To Survey  1
    Click Link  edit-question-1
    Click Link  Back to survey
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text

User Can Navigate To the Next Question
    Go To Survey  1
    Click Link  edit-question-1
    Click Link  Next question
    Page Should Contain  Question 2

Previous Button Does Not Exist for the First Questions
    Go To Survey  1
    Click Link  edit-question-1
    Page Should Not Contain  Previous question

Previous Button Does Exist for the Second Questions
    Go To Survey  1
    Click Link  edit-question-1
    Click Link  Next question
    Page Should Contain Link  Previous question

User Can Navigate To the Previous Questions
    Go To Survey  1
    Click Link  edit-question-1
    Click Link  Next question
    Click Link  Previous question
    Page Should Contain  weight
