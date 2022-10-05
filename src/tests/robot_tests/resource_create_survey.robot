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

Make A Survey
    Set Survey Name  Testi
    Set Survey Title  Surveyn tekeminen testauksessa
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Name
    Set Survey Title  Surveyn tekeminen testauksessa
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Title
    Set Survey Name  Testi
    Set Survey Text  Toimiikohan
    Create A Survey

Make Survey Without Text
    Set Survey Name  Testi
    Set Survey Title  Surveyn tekeminen testauksessa
    Create A Survey