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
    Page Should Contain  Static descriptive text about the category 2

Statistics Page Shows the Number Of Users Who Have Answered
    Go To Statistics  8
    Page Should Contain  Total submissions: 5

Statistics Page Shows Question Names For Charts
    Go To Statistics  8
    Page Should Contain  Describe the size of your ears
    Page Should Contain  Where do you prefer to hang out

Statistics Page Shows Answer Distribution Charts
    Go To Statistics  8
    Page Should Contain Element  chart_23
    Page Should Contain Element  chart_24

Statistics Page Shows Filtered Charts After Applying Filter
    Go To Statistics  8
    # Choose user group B-ryhmä
    Select From List By Value  name:filter_group_id  bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20
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
    # Choose user group B-ryhmä
    Select From List By Value  name:filter_group_id  bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20
    Click Button  Filter
    Click Button  toggle_filter_chart_23
    Click Button  toggle_filter_chart_24
    Element Should Not Be Visible  chart_23_filtered
    Element Should Not Be Visible  chart_24_filtered
    Element Should Be Visible  chart_23_unfiltered
    Element Should Be Visible  chart_24_unfiltered

Statistics Page Shows Filtered Charts After Toggling Filter Second Time
    Go To Statistics  8
    # Choose user group B-ryhmä
    Select From List By Value  name:filter_group_id  bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20
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
    Press Keys  filter_start_date  2+TAB+2+TAB+2002+TAB+12+TAB+00
    Press Keys  filter_end_date  2+TAB+2+TAB+2002+TAB+12+TAB+01
    Click Button  Filter
    Page Should Contain  Users with submissions (0 / 5)    
    
Entering Invalid Date to User Filter Does Not Filter Anything
    Go To Statistics  8
    Page Should Contain  Total submissions: 5

Filtering By Group Name Filters Users
    Go To Statistics  8
    # Choose user group Supertestaajat
    Select From List By Value  name:filter_group_id  737cdf09-cc6f-47de-adcd-e7aaab0adc39
    Click Button  Filter
    Page Should Contain  Users with submissions (1 / 5)

Statistics Page Displays Average Zero If There Is No Answers
    Go To Statistics  1
    Page Should Contain  None

Statistics Page Displays Correct Average Values
    Go To Statistics  8
    Page Should Contain  3.0
    Page Should Contain  2.0

Filtering By Email Filters Users
    Go To Statistics  8
    Input Text  filter_email  duser
    Click Button  Filter
    Page Should Contain  Users with submissions (2 / 5)

With Filtering Unfiltered Average Is Shown
    Go To Statistics  8
    # Choose user group B-ryhmä
    Select From List By Value  name:filter_group_id  bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20
    Click Button  Filter
    Page Should Contain  Average score
    Page Should Contain  5.0   
    Page Should Contain  Unfiltered average
    Page Should Contain  3.0

Filtering With Email And Group Shows Correct Averages
    Go To Statistics  8
    # Choose user group B-ryhmä
    Select From List By Value  name:filter_group_id  bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20
    Input Text  filter_email  duser
    Click Button  Filter    
    Page Should Contain  5.0

Without Filtering Unfiltered Average Is Not Shown
    Go To Statistics  8
    Page Should Not Contain  Unfiltered average

No Charts Are Shown When There Is No Submission Data To Shown
    Go To Statistics  1
    Page Should Contain  No answers yet