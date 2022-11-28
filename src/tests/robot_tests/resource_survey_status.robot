*** Settings ***
Resource  resource_create_survey.robot

*** Keywords ***
Create Survey With Details 
    [Arguments]  ${name}  ${title}  ${description}
    Set Survey Name  ${name}
    Set Survey Title  ${title}
    Set Survey Text  ${description}
    Create A Survey

Create New Category
    [Arguments]  ${name}  ${description}
    Click Link  Add category
    Set Category Name  ${name}
    Set Category Description  ${description}
    Click Button  Save
    Click Link  Back to survey

Survey Status Is Red
    Page Should Contain Element  id:status-badge-red

Survey Status Is Yellow
    Page Should Contain Element  id:status-badge-yellow

Survey Status Is Green
    Page Should Contain Element  id:status-badge-green


Add New Question
    [Arguments]  ${text}  ${weight}
    Click Link  Add question
    Set Question Text  ${text}
    Set Category Weight  ${weight}
    Submit Question

Add New Answer
    [Arguments]  ${text}  ${points}
    Set Answer Text  ${text}
    Set Points  ${points}
    Submit Answer


Set Category Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set Category Description
    [Arguments]  ${description}
    Input Text  description  ${description}

Set Question Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Category Weight
    [Arguments]  ${weight}
    Input Text  cat-8-weight  ${weight}

Submit Question
    Click Button  submit

Set Answer Text
    [Arguments]  ${text}
    Input Text  answer_text  ${text}

Set Points
    [Arguments]  ${points}
    Input Text  points  ${points}

Submit Answer
    Click Button  Save changes