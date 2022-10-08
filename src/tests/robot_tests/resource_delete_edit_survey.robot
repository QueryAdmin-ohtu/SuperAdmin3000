*** Keywords ***
Set New Survey Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set New Survey Title
    [Arguments]  ${title}
    Input Text  title  ${title}

Set New Survey Text
    [Arguments]  ${text}
    Input Text  survey  ${text}

Set Existing Survey Name
    [Arguments]  ${updated_name}
    Input Text  name  ${updated_name}

Set Existing Survey Title
    [Arguments]  ${updated_title}
    Input Text  title  ${updated_title}

Set Existing Survey Text
    [Arguments]  ${updated_text}
    Input Text  description  ${updated_text}

Create A Survey
    Click Button  Create Survey

Delete The Survey
    Click Button  DELETE SURVEY
    Handle Alert  Accept

Make A Survey To Delete
    Go To Home Page
    Click Link  New survey
    Set New Survey Name  Must Not Contain
    Set New Survey Title  Poistuisikohan
    Set New Survey Text  On Home Page
    Create A Survey

Edit Survey With Valid Info
    Set Existing Survey Name  test_name
    Set Existing Survey Title  test_title
    Set Existing Survey Text  test_text
    Click Button  SAVE
    Handle Alert  Accept