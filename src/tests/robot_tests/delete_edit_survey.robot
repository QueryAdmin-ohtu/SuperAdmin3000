*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_delete_edit_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Delete An Existing Survey
    Go To Backdoor Login Page
    Login With Correct Credentials
    Make A Survey To Delete
    Delete The Survey
    Page Should Not Contain  Poistuisikohan

Logged In User Can Edit Survey
    Go To Survey  1
    ${updated}=  Get Text  updated
    Click Button  EDIT SURVEY
    Edit Survey With Valid Info
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text
    Element Should Not Contain  updated  ${updated}

Logged Out User Cannot Edit Survey
    Logout
    Go To Edit Surveys Page
    Page Should Not Contain  Edit survey
