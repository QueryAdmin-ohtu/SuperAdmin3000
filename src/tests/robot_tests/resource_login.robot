*** Keywords ***
Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Text  password  ${password}

Submit Credentials
    Click Button  Login

Logout
    Click Button  Logout

Login With Correct Credentials
    Set Username  rudolf
    Set Password  secret
    Submit Credentials