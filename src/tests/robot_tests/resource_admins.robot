*** Keywords ***
Set Admin Email
    [Arguments]  ${email}
    Input Text  email  ${email}

Add New User
    Click Button  Add user