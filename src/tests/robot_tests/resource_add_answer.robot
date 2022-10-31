*** Keywords ***
Set Answer Text
    [Arguments]  ${text}
    Input Text  answer_text  ${text}

Set Points
    [Arguments]  ${points}
    Input Text  points  ${points}

Submit Answer
    Click Button  Save changes

Add New Answer
    [Arguments]  ${text}  ${points}
    Set Answer Text  ${text}
    Set Points  ${points}
    Submit Answer

Add Answer Without Arguments
    Submit Answer

Expand Answer Card
    [Arguments]  ${answer_index}
    Click Element  id:expandable-answer-${answer_index}

Edit Answer
    [Arguments]  ${text}  ${points}  ${id}
    Input Text  answer-${id}  ${text}
    Input Text  points-${id}  ${points}