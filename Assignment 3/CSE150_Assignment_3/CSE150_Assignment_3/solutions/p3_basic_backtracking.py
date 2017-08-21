# -*- coding: utf-8 -*-



def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None

def is_complete_p1(csp):
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



def is_consistent_p2(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    # TODO implement this
    # loops through all the X variables
    for x in csp.constraints[variable]:
        # Loops through all the Y variables

        for y in csp.variables:
            # if X and Y are both assigned, makes sure they don't violate anything

            if(y.is_assigned() and y == x.var2):
                # look for violation

                if not x.is_satisfied(value, y.value):
                    return False
    #no violationss
    return True




def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns True; otherwise, it returns False.
    """

    # TODO implement this
    # recursive check to see if csp is complete
    if (is_complete_p1(csp)):
        return True;

    else:
        variable = select_unassigned_variable(csp);
        # loop through varriable
        for value in order_domain_values(csp, variable):

            # if value is consistant to variable
            if (is_consistent_p2(csp, variable, value)):
                csp.variables.begin_transaction();
                variable.assign(value);
                result = backtrack(csp);

                # if result is not null
                if (result != None):
                    return result;

                else:
                    # fail, backtrack
                    csp.variables.rollback();
        return None;



