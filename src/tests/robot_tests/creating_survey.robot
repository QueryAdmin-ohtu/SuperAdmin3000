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