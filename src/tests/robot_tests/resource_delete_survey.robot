*** Keywords ***
Set Survey Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set Survey Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set Survey Text
    [Arguments]  ${text}
    Input Text  survey  ${text}

Create A Survey
    Click Button  Create Survey

Delete The Survey
    Click Button  DELETE SURVEY
    Handle Alert  Accept

Make A Survey To Delete
    Go To Home Page
    Click Link  New survey
    Set Survey Name  Must Not Contain
    Set Survey Title  Poistuisikohan
    Set Survey Text  On Home Page
    Create A Survey