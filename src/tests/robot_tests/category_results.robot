*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_add_question.robot
Resource  resource_edit_category.robot
Resource  resource_manage_results.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can View Category Results
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Click Link  edit_button_1
    Page Should Contain  0% - 40% of the max points
    Page Should Contain  Dynamically fetched feedback text for category score.
    Click Element  categoryresults
    Page Should Contain   Category results for Category 1

Logged In User Can Delete Category Results
    Go To Survey  1
    Click Link  edit_button_1
    Click Element  categoryresults
    Expand Result Card  1
    Click Button  Delete
    Page Should Not Contain  Result at cutoff point 0.4

A Category Result Having Cutoff 1.0 Has No Delete Button
    Go To Survey  2
    Click Link  Add category
    Create New Category
    Click Element  categoryresults
    Expand Result Card  1
    Page Should Not Contain  Delete


User Can Create Subsequent Category Results With Cutoff Values Between 0 And 1
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Set Result Text  Category result cutoff 0.5
    Set Result Cutoff  0.5
    Save Result
    Expand Result Card  2
    Page Should Contain  Category result cutoff 0.5

User Can Not Create Category Results With Cutoff Values Above 1
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Set Result Text  Invalid cutoff  
    Set Result Cutoff  1.1
    Save Result
    Expand Result Card  2
    Page Should Not Contain  Result at cutoff point 1.1


User Can Edit A Category Result
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Expand Result Card  1
    Edit Result  New Cutoff Text one  0.2  1
    Save Result
    Page Should Contain  Result at cutoff point 0.2
    Expand Result Card  1
    Page Should Contain  New Cutoff Text

Category Result Cannot Be Edited To Have Duplicate Cutoffs
    Go To Survey  2
    Click Link  edit_button_8
    Click Element  categoryresults
    Expand Result Card  1
    Page Should Contain  New Cutoff Text one
    Edit Result  New Cutoff Text two  1  1
    Save Result
    Page Should Contain  There must not be any identical cutoff values
    Expand Result Card  1
    Page Should Contain  New Cutoff Text one