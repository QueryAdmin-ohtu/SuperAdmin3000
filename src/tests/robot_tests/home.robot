*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Home Page Should Be Open
    Title Should Be  Super Admin 3000

User Logged In With Correct Credentials
    Go To Backdoor Login Page
    Login With Correct Credentials
    Page Should Contain  Logged in
    Page Should Contain  rudolf

Logged In User Can See Surveys On Home Page
    Go To Home Page
    Page Should Contain Element  xpath://div[@id="survey-1"]
    Page Should Contain  Questions: 15
    Page Should Contain  Submissions: 0
    Page Should Contain  Questions: 0
    Page Should Contain  How well are you doing Agile?

Logged Out User Should Be On Login Page
    Logout
    Go To Home Page
    Page Should Contain  Please login with your Google account:

Logged Out User Trying To Create Surveys Is Redirected To Login And Displayed Notification
    Go To Create New Survey Page
    Page Should Contain  Please login with your Google account:
    Notification Is Displayed

