*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page



*** Test Cases ***

Logged In User Can View Statistics Page
    Login Through Backdoor
    Go To Statistics  1
    Page Should Contain  Related categories

User Can Access Edit Categories Page From Statistics
    Go To Statistics  1
    Click Element  edit_button_2
    Page Should Contain  Static descriptive text about the category 2.
