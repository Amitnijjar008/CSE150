# -*- coding: utf-8 -*-



def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""

    # Hint: The list of all variables for the CSP can be obtained by csp.variables.
    # Also, if the variable is assigned, variable.is assigned() will be True.
    # (Note that this can happen either by explicit assignment using variable.assign(value),
    # or when the domain of the variable has been reduced to a single value.)

    # TODO implement this
    # loop through all the variables in csp.variables
    for var in csp.variables:
        # check if any are not assigned

    	if (var.is_assigned() == False):
    		return False;
    # return true if all are assigned
    return True;