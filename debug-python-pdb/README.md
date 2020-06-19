# Python based debugging in Robot Framework

## Why

Unlike our ealier example where we want to simply [pause execution of a task on a failure](../debug-vanilla), in this case we want to set a breakpoint and drop to Python's debugger, `pdb`. This will allow us to do things like inspect a variable or run a keyword. We can also set multiple breakpoints to let us pause and inspect along the way.

## How

- We are creating a Python library to help with debugging. In our case, we created a Keyword called 'Set Breakpoint' to allow us to start pdb and set the trace at the point our keyword is called.

Below is an annoted version of the code:

```
class DebugLibrary:

    def __init__(self):
        self.__imported_required_libraries = False

    # Let's us call 'Set Breakpoint' anyhwere in our robot framework code.
    # Will drop to `pdb` at which point we can run anything we like from python interpreter
    def set_breakpoint(self):
        if self.__is_debug_mode():
            import sys, pdb; pdb.Pdb(stdout=sys.__stdout__).set_trace()

    # Can be performed on 'teardown'. Pauses using the Dialog library only if a
    # task has failed (SUITE_STATUS is set to 'FAIL')
    def pause_on_failure(self):
        has_failed = BuiltIn().get_variable_value("${SUITE_STATUS}") == 'FAIL'
        if self.__is_debug_mode and has_failed:
            self.__import_required_libraries()
            BuiltIn().run_keyword("Pause Execution", "Paused due to task failure, click OK to continue teardown")

    # Lets us pause using the Dialog library without dropping to `pdb`
    def pause_for_debug(self):
        if self.__is_debug_mode:
            self.__import_required_libraries()
            BuiltIn().run_keyword("Pause Execution", "Paused execution for debugging, click OK to continue")

    # Helper for letting us print out the current variables inside of `pdb`
    # Ex. `self.__print_variables()`
    def _print_variables(self):
        # TODO: Recursively dump the NormalizedDict and optionally hide secrets
        variables = {k: v for k, v in BuiltIn().get_variables().items()}
        pprint.pprint(variables)

    # Helper for letting us print out the environment variables inside of `pdb`
    # Ex. `self.__print_envs()`
    def _print_envs(self):
        for k, v in os.environ.items():
            print(f'*DEBUG*{k}={v}')
    
    # Returns true when we are in development mode, ie. the ROBOT_DEBUG env is set to TRUE
    # This prevents us from accidentally setting a breakpoint and launching it in production
    def __is_debug_mode(self):
        return os.environ['ROBOT_DEBUG'] == 'TRUE'

    # In order to use "Pause Execution" we need to import Dialog
    def __import_required_libraries(self):
        if not self.__imported_required_libraries:
            BuiltIn().import_library("Dialogs")
            self.__imported_required_libraries = True

```

## Running the code

#### Windows

`$Env:ROBOT_DEBUG = "TRUE"; robot -d output .`

#### Linux/OSX

`ROBOT_DEBUG=TRUE && robot -d output .`
