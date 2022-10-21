*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_admins.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***
Logged In User Can Add New Admin
    Go To Backdoor Login Page
    Login With Correct Credentials
    Click Link  Admins
    Set Admin Email  jorma@uotinen.net
    Add New User

Logged In User Can View Admins
    Go To Admins Page
    Page Should Contain  Email address
    Page Should Contain  id
    Page Should Contain  Email
    Page Should Contain  9
    Page Should Contain  jorma@uotinen.net

Logged Out User Cannot View Admins
    Logout
    Go To Admins Page
    Page Should Not Contain  Add user