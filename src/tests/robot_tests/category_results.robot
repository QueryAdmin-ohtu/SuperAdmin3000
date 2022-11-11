*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Resource  resource_edit_category.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can View Category Results
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Link  edit_button_1
    Page Should Contain  Dynamically fetched feedback text for category score.
    