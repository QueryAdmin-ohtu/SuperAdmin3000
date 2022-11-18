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

Logged In User Can Delete Category Results
    Go To Survey  8
    Click Link  edit_button_6

    Set Category Result Text  To be deleted soon
    Set Category Result Cutoff Points  0.01
    Click Button  Add result
    Page Should Contain  To be deleted soon
    Page Should Contain Element  delete_16

    Set Category Result Text  yes yes
    Set Category Result Cutoff Points  0.02
    Click Button  Add result
    Page Should Contain Element  delete_17
    
    Click Button  delete_16
    Handle Alert  Accept
    Page Should Not Contain  To be deleted soon
    

A Category Result Having Cutoff 1.0 Has No Delete Button
    Go To Survey  8
    Click Link  edit_button_6
    Set Category Result Text  Not possible to delete this one
    Set Category Result Cutoff Points  1
    Click Button  Add result
    
    Page Should Contain Element  delete_17
    Page Should Not Contain Element  delete_18

    Page Should Contain  Not possible to delete this one