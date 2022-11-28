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