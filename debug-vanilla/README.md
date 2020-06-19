# Vanilla Debugging in Robot Framework

## Why

We want to stop the task in Robot Framework when it fails in development using vanilla Robot Framework built-in keywords

__Notes__
- Unlike typical debugging, we are merely pausing the execution of the task in order to view the state of the applications. This is great for browser or UI debugging, but not very useful for more in depth debugging where we need to do things like execute code or look at variables.
- This should only happen in development mode, never in production. We don't want a task hanging in production so we use an environment variable to let the task know that we are in development mode.
- We will pause the script at the point of failure, just before the 'teardown'. After 'unpausing' it, the task will fail and the teardown will be run.

## How

Here's the code we are using to pause the task runner.

- We first check to see if the ROBOT_DEBUG environment variable is set, letting us know we are in development mode and not production
- Next we check to see if the SUITE_STATUS variable is set to "FAIL", in which case we know that a task has failed.
- If both the above statements are true then we run the `Pause for Debug` keyword which uses the Dialogs built-in library to stop execution until we click the 'OK' buton.

```
*** Keywords ***
Teardown Actions
    ${debug}=   Get Environment Variable    ROBOT_DEBUG     FALSE
    Run Keyword If  '${debug}' == 'TRUE' and '${SUITE_STATUS}' == 'FAIL'    Pause For Debug
    Close All Browsers

*** Keywords ***
Pause For Debug
    Pause Execution     Paused execution due to failure, click OK to continue teardown
```

## Running the code

#### Windows

`$Env:ROBOT_DEBUG = "TRUE"; robot -d output .`

#### Linux/OSX

`ROBOT_DEBUG=TRUE && robot -d output .`
