*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_create_survey.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page
*** Test Cases ***
Delete A Existing Question
    Delete Question  1  9
    Go To Survey  1
    Page Should Not Contain  Game of Thrones