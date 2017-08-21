# -*- coding: utf-8 -*-

from operator import itemgetter
from collections import deque

def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())


def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
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

            if(y == x.var2 and y.is_assigned()):
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
        return csp.assignment;

    else:
        variable = select_unassigned_variable(csp);
        # loop through varriable
        for value in order_domain_values(csp, variable):

            # if value is consistant to variable
            if (is_consistent_p2(csp, variable, value)):
                csp.variables.begin_transaction();
                variable.assign(value);

                inference(csp, variable);

                result = backtrack(csp);

                # if result is not null
                if (result != False):
                    return result;

                else:
                    # fail, backtrack
                    csp.variables.rollback();
        return False;


def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())

    # TODO implement this
    # loop through arcs
    while (queue_arcs):
        arc = queue_arcs.popleft();
        if (revise(csp, arc[0], arc[1])):

            # if domain is empty, return false
            if (len(arc[0].domain) == 0 or len(arc[1].domain) == 0):
                return False;

            else:

                for neighbor in csp.constraints[arc[0]].arcs():

                    # skip same arcs
                    if (neighbor[0] == arc[1] or neighbor[1] == arc[1]):
                        continue;
                    # if arc is revised, add neighbor
                    queue_arcs.append(neighbor);
    return True;

def revise(csp, xi, xj):
    # You may additionally want to implement the 'revise' method.
    #set revised to false
    boolToRet = False;

    # loop through xi
    for i in xi.domain:
        succ = False;

        # loop through xj
        for j in xj.domain:
            sat = True;

            for constraint in csp.constraints[xi, xj]:

                if (not constraint.is_satisfied(i, j)):
                    sat = False;
                    break;

            # if satisified
            if (sat):
                succ = True;
                break;

        # no constraints satisified
        if (succ == False):
            xi.domain.remove(i);
            boolToRet = True;
    return boolToRet;

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """

    # TODO implement this
    lowDomain = 99999.99;
    unassignedVars = deque();

    for var in csp.variables:
        curDomain = len(var.domain);

        # length is shorter
        if (curDomain < lowDomain and curDomain != 1):
            unassignedVars.clear();
            unassignedVars.append(var);
            # curDomain is the new lowDomain
            lowDomain = curDomain;

        # queue of unassigned vars
        elif (curDomain == lowDomain):
            unassignedVars.append(var);

    for var in unassignedVars:
        if (len(csp.constraints[var]) > -99999.99):
            nextVar = var;
    return nextVar;



def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the value
    that rules out the fewest choices for the neighboring variables in the constraint graph
    are placed before others.
    """

    # TODO implement this
    numCon = [];
    for value in variable.domain:
        conflicts = 0;
        # check all neighbors for conflicts
        for arc in csp.constraints[variable].arcs():
            conflicts += arc[0].domain.count(value);
            conflicts += arc[1].domain.count(value);
        numCon.append([value, conflicts]);

    # sort cons by increasing order
    numCon = sorted(numCon, key=itemgetter(1));
    domain = [];
    for value in numCon:
        domain.append(value[0]);

    return domain;