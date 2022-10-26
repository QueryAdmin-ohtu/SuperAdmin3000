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
    Open Delete Modal
    Write Confirmation Text To Modal  Must Not Contain
    Click Delete Modal Delete
    Page Should Not Contain  Poistuisikohan
    Notification Is Displayed
    Page Should Contain  survey was deleted

Try To Delete A Survey But Write Invalid Confirmation Text
    Go To Home Page
    Make A Survey To Delete
    Open Delete Modal
    Write Confirmation Text To Modal  Masa Mainio
    Click Delete Modal Delete
    Page Should Contain  Poistuisikohan
    Notification Is Displayed
    Page Should Contain  Confirmation did not match name of survey

Deletition Modal Is Closed By Clicking Cancel
    Go To Survey  1
    Element Should Not Be Visible  id:modal
    Open Delete Modal
    Element Should Be Visible  id:modal
    Click Delete Modal Cancel
    Element Should Not Be Visible  id:modal
    Notification Is Not Displayed

Logged In User Can Edit Survey
    Go To Survey  1
    ${updated}=  Get Text  updated
    Click Link  Edit survey
    Edit Survey With Valid Info
    Notification Is Displayed
    Page Should Contain  Test_name survey was updated
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text
    Element Should Not Contain  updated  ${updated}

Logged Out User Cannot Edit Survey
    Logout
    Go To Edit Surveys Page
    Page Should Not Contain  Edit survey
