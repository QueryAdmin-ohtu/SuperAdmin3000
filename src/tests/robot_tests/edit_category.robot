*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Resource  resource_edit_category.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page

*** Test Cases ***

Logged In User Can Create Categories
    Login Through Backdoor
    Go To Survey  1
    Page Should Contain  Survey categories
    Click Link  Add category
    Create New Category
    Page Should Contain  nimi
    Page Should Contain  kuvaus

Category Edit View Should Display Survey Name
    Go To Survey  1
    Click Link  edit_button_1
    Page Should Contain  test_name

Back Button Opens Correct Survey Page On New Category Page
    Go To Survey  1
    Click Link  Add category
    Click Link  Back to survey
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text

Back Button Opens Correct Survey Page On Edit Category Page
    Go To Survey  1
    Click Link  edit_button_1
    Click Link  Back to survey
    Page Should Contain  test_name
    Page Should Contain  test_title
    Page Should Contain  test_text

Logged In User Cannot Create Categories Without Name
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Name
    Page Should Not Contain  Add content link

Logged In User Cannot Create Categories Without Description
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Description
    Page Should Not Contain  Add content link

Logged In User Can Create Categories Without Content Links
    Go To Survey  1
    Click Link  Add category
    Create New Category Without Content Links
    Page Should Contain  abc
    Page Should Contain  123
    Page Should Contain  Your skills in this topic are excellent!
    Click Element  categoryresults
    Page Should Contain  Result at cutoff point 1.0:

Logged Out User Cannot Create Categories
    Logout
    Go To Survey  1
    Page Should Contain  Please login

Logged In User Cannot Delete a Category With Results
    Go To Backdoor Login Page
    Login With Correct Credentials
    Go To Survey  1
    Page Should Contain  Survey categories
    Click Button  delete_button_1
    Handle Alert  Accept
    Notification Is Displayed
    Page Should Contain  Could not delete category because it has results linked to it


Logged In User Can Edit Category Name and Description
    Go To Survey  1
    Click Link  edit_button_1
    Page Should Contain  Edit a category
    Edit Category Name and Description
    Page Should Contain  uusi nimi
    Page Should Contain  uusi kuvaus

Logged In User Can Add a New Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Add Content Link
    Page Should Contain  uusi url
    Page Should Contain  uusi tyyppi

Logged In User Can Edit a Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Edit Content Link
    Click Link  edit_button_1
    Page Should Contain  kissa
    Page Should Contain  koira

Logged In User Can Delete a Content Link
    Go To Survey  1
    Click Link  edit_button_1
    Page Should Contain  kissa    
    Click Button  delete_url_0
    Click Link  edit_button_1
    Page Should Not Contain  kissa

