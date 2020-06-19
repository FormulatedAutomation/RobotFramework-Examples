*** Settings ***
Documentation   Opens the browser and searches Bing
Library         RPA.Browser
Library         OperatingSystem
Library         Dialogs
Suite Teardown  Teardown Actions

*** Variables ***
${BING_URL}     https://bing.com

*** Keywords ***
Teardown Actions
    ${debug}=   Get Environment Variable    ROBOT_DEBUG     FALSE
    Run Keyword If  '${debug}' == 'TRUE' and '${SUITE_STATUS}' == 'FAIL'    Pause For Debug
    Close All Browsers

*** Keywords ***
Pause For Debug
    Pause Execution     Paused execution due to failure, click OK to continue teardown

*** Keywords ***
Open Bing
    Open Available Browser  ${BING_URL}

*** Keywords ***
Perform Search
    [Arguments]     ${query}
    Wait Until Element Is Visible   name:q
    # Input Text  name:q  ${query}  # Will Work, input name is correct
    Input Text  name:search_box  ${query}   # Will Fail, input name is incorrect
    Submit Form  //form[@id="sb_form"]

*** Task ***
Search Bing
    Open Bing
    Perform Search      Formulated Automation Github
