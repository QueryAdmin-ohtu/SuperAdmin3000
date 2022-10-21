*** Keywords ***

Click Delete Question
    [Arguments]  ${id}
    Submit Form  id:delete-question-${id}
    Handle Alert