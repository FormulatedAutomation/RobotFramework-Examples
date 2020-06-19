import os
import pprint
from robot.libraries.BuiltIn import BuiltIn

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
        variables = {k: v for k, v in os.environ.items()}
        pprint.pprint(variables)
    
    # Returns true when we are in development mode, ie. the ROBOT_DEBUG env is set to TRUE
    # This prevents us from accidentally setting a breakpoint and launching it in production
    def __is_debug_mode(self):
        return os.environ['ROBOT_DEBUG'] == 'TRUE'

    # In order to use "Pause Execution" we need to import Dialog
    def __import_required_libraries(self):
        if not self.__imported_required_libraries:
            BuiltIn().import_library("Dialogs")
            self.__imported_required_libraries = True
