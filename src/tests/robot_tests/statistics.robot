*** Settings ***
Resource  resource.robot
Resource  resource_login.robot
Suite Setup  Open And Configure Browser
Suite Teardown  Close Browser
Test Setup  Go To Home Page



*** Test Cases ***

Logged In User Can View Statistics Page
    Login Through Backdoor
    Go To Survey  1
    Click Link  Detailed statistics
    Page Should Contain  Category scores

User Can Access Edit Categories Page From Statistics
    Go To Statistics  1
    Click Element  edit_button_2
    Page Should Contain  Static descriptive text about the category 2.

Statistics Page Shows the Number Of Users Who Have Answered
    Go To Statistics  8
    Page Should Contain  Users with submissions (4 / 4)

Statistics Page Shows Question Names For Charts
    Go To Statistics  8
    Page Should Contain  Question: Describe the size of your ears
    Page Should Contain  Question: Where do you prefer to hang out

Statistics Page Shows Answer Distribution Charts
    Go To Statistics  8
    Page Should Contain Element  chart_23
    Page Should Contain Element  chart_24

Statistics Page Shows Filtered Charts After Applying Filter
    Go To Statistics  8
    Select From List By Value  name:filter_group_name  B-ryhmä
    Click Button  Filter
    Element Should Be Visible  chart_23_filtered
    Element Should Be Visible  chart_24_filtered
    Element Should Not Be Visible  chart_23_unfiltered
    Element Should Not Be Visible  chart_24_unfiltered

Toggle Filter For Charts Works When Only Time Filter Applied
    Go To Statistics  8
    Click Button  Filter
    Click Button  toggle_filter_chart_23
    Click Button  toggle_filter_chart_24
    Element Should Not Be Visible  chart_23_filtered
    Element Should Not Be Visible  chart_24_filtered
    Element Should Be Visible  chart_23_unfiltered
    Element Should Be Visible  chart_24_unfiltered

Statistics Page Shows Unfiltered Charts After Toggling Filter First Time
    Go To Statistics  8
    Select From List By Value  name:filter_group_name  B-ryhmä
    Click Button  Filter
    Click Button  toggle_filter_chart_23
    Click Button  toggle_filter_chart_24
    Element Should Not Be Visible  chart_23_filtered
    Element Should Not Be Visible  chart_24_filtered
    Element Should Be Visible  chart_23_unfiltered
    Element Should Be Visible  chart_24_unfiltered

Statistics Page Shows Filtered Charts After Toggling Filter Second Time
    Go To Statistics  8
    Select From List By Value  name:filter_group_name  B-ryhmä
    Click Button  Filter
    Click Button  toggle_filter_chart_23
    Click Button  toggle_filter_chart_23
    Click Button  toggle_filter_chart_24
    Click Button  toggle_filter_chart_24
    Element Should Be Visible  chart_23_filtered
    Element Should Be Visible  chart_24_filtered
    Element Should Not Be Visible  chart_23_unfiltered
    Element Should Not Be Visible  chart_24_unfiltered

Entering Valid Range To Filter Dates Filters Users
    Go To Statistics  8
    Input Text  filter_start_date  02.02.2002 12:00
    Input Text  filter_end_date  02.02.2002 12:01
    Click Button  Filter
    Page Should Contain  Users with submissions (0 / 4)    
    
Entering Invalid Date to User Filter Does Not Filter Anything
    Go To Statistics  8
    Page Should Contain  Users with submissions (4 / 4)

Filtering By Group Name Filters Users
    Go To Statistics  8
    Select From List By Value  name:filter_group_name  Supertestaajat
    Click Button  Filter
    Page Should Contain  Users with submissions (1 / 4)

Statistics Page Displays Correct Average Value Message When No Answers Are Present
    Go To Statistics  1
    Page Should Contain  Average score: 0.0

Statistics Page Displays Correct Average Values
    Go To Statistics  8
    Page Should Contain  Average score: 3.75
    Page Should Contain  Average score: 1.25

Filtering By Email Filters Users
    Go To Statistics  8
    Input Text  filter_email  duser
    Click Button  Filter
    Page Should Contain  Users with submissions (2 / 4)
