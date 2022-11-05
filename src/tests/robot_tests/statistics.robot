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

Statistics Page Shows the Number Of Users Who Have Answered
    Go To Statistics  1
    Page Should Contain  Users with submissions (0 / 0)

Statistics Page Shows Question Names For Charts
    Go To Statistics  8
    Page Should Contain  Question: Describe the size of your ears
    Page Should Contain  Question: Where do you prefer to hang out

Statistics Page Shows Answer Distribution Charts
    Go To Statistics  8
    Page Should Contain Element  chart_23
    Page Should Contain Element  chart_24