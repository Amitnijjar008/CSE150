# -*- coding: utf-8 -*-

from collections import deque


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
            if (len(arc[0].domain) == 0):
                return False;

            else:

                for neighbor in csp.constraints[arc[0]].arcs():

                    # skip same arcs
                    if (neighbor[0] == arc[0] or neighbor[1] == arc[0]):
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
        found = False;

        # loop through xj
        for j in xj.domain:
            sat = True;

            for constraint in csp.constraints[xi, xj]:

                if (not constraint.is_satisfied(i, j)):
                    sat = False;
                    break;

            # if satisified
            if (sat):
                found = True;
                break;

        # no constraints satisified
        if (not found):
            xi.domain.remove(i);
            boolToRet = True;
    return boolToRet;