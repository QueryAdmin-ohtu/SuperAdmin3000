*** Keywords ***
Set Category Description
    [Arguments]  ${description}
    Input Text  description  ${description}

Set Category Name
    [Arguments]  ${name}
    Input Text  name  ${name}

Set Content Link Url
    [Arguments]  ${url}
    Input Text  new_url  ${url}

Set Content Link Type
    [Arguments]  ${type}
    Input Text  new_type  ${type}

Set Category Result Text
    [Arguments]  ${text}
    Input Text  text  ${text}

Set Category Result Cutoff Points
    [Arguments]  ${points}
    Input Text  cutoff  ${points}


Create New Category
    Set Category Name  nimi
    Set Category Description  kuvaus
    Click Button  Save

Create New Category Without Name
    Set Category Description  kuvaus
    Click Button  Save

Create New Category Without Description
    Set Category Name  nimi
    Click Button  Save

Create New Category Without Content Links
    Set Category Name  abc
    Set Category Description  123
    Click Button  Save

Edit Category Name and Description
    Set Category Name  uusi nimi
    Set Category Description  uusi kuvaus
    Click Button  Save

Add Content Link
    Set Content Link Url  uusi url
    Set Content Link Type  uusi tyyppi
    Click Button  Add

Edit Content Link
    Input Text  url_0  kissa
    Input Text  type_0  koira
    Click Button  Save