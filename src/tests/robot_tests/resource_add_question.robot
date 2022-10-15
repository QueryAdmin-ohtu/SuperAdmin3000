*** Keywords ***
Set Question Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Category Weight
    [Arguments]  ${weight}
    Input Text  cat-1-weight  ${weight}

Submit Question
    Click Button  submit

Add New Question
    [Arguments]  ${text}  ${weight}
    Set Question Text  ${text}
    Set Category Weight  ${weight}
    Submit Question

Add Question With No Weights
    [Arguments]  ${text}
    Set Question Text  ${text}
    Submit Question

Add Question Without Arguments
    Submit Question

Edit Question By Table Row
    [Arguments]  ${table_row}
    Click Element  id:edit-question-${table_row}