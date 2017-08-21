# -*- coding: utf-8 -*-
from operator import itemgetter
from collections import deque


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