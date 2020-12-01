import numpy as np
from classify import *
import math

##
## CSP portion of lab 4.
##
from csp import BinaryConstraint, CSP, CSPState, Variable,\
    basic_constraint_checker, solve_csp_problem

# Implement basic forward checking on the CSPState see csp.py
def forward_checking(state, verbose=False):
    # Before running Forward checking we must ensure
    # that constraints are okay for this state.
    basic = basic_constraint_checker(state, verbose)
    if not basic:
        return False

    # Add your forward checking logic here.
    cur_var= state.get_current_variable()
    if cur_var is None: return True
    cur_val= cur_var.get_assigned_value()
    cur_cons= state.get_constraints_by_name(cur_var.get_name())

    for constraint in cur_cons:
        var_i = state.get_variable_by_name(constraint.get_variable_i_name())
        var_j = state.get_variable_by_name(constraint.get_variable_j_name())
        for y in var_j.get_domain():
            if not constraint.check(state, value_i= var_i.get_assigned_value(), value_j= y):
                var_j.reduce_domain(y)
            if len(var_j.get_domain())==0:
                return False
    return True
# Now Implement forward checking + (constraint) propagation through
# singleton domains.
def forward_checking_prop_singleton(state, verbose=False):
    # Run forward checking first.
    fc_checker = forward_checking(state, verbose)
    if not fc_checker:
        return False

    # Add your propagate singleton logic here.
    if forward_checking(state, verbose=False) is False: return False
    vars= state.get_all_variables()
    sing_vars= [var for var in vars if var.domain_size() is 1]
    visited_sings= []
    while len(sing_vars) is not 0:
        X=sing_vars[0]
        sing_vars.remove(X)
        visited_sings.append(X)
        cur_cons = state.get_constraints_by_name(X.get_name())

        for constraint in cur_cons:
            var_i = state.get_variable_by_name(constraint.get_variable_i_name())
            var_j = state.get_variable_by_name(constraint.get_variable_j_name())
            for y in var_j.get_domain():
                if not constraint.check(state, value_i=var_i._domain[0], value_j=y):
                    var_j.reduce_domain(y)
                if len(var_j.get_domain()) == 0:
                    return False
    return True

## The code here are for the tester
## Do not change.
from moose_csp import moose_csp_problem
from map_coloring_csp import map_coloring_csp_problem

def csp_solver_tree(problem, checker):
    problem_func = globals()[problem]
    checker_func = globals()[checker]
    answer, search_tree = problem_func().solve(checker_func)
    return search_tree.tree_to_string(search_tree)

##
## CODE for the learning portion of lab 4.
##

### Data sets for the lab
## You will be classifying data from these sets.
senate_people = read_congress_data('S110.ord')
senate_votes = read_vote_data('S110desc.csv')

house_people = read_congress_data('H110.ord')
house_votes = read_vote_data('H110desc.csv')

last_senate_people = read_congress_data('S109.ord')
last_senate_votes = read_vote_data('S109desc.csv')


### Part 1: Nearest Neighbors
## An example of evaluating a nearest-neighbors classifier.
senate_group1, senate_group2 = crosscheck_groups(senate_people)
#evaluate(nearest_neighbors(hamming_distance, 7), senate_group1, senate_group2, verbose=2)

## Write the euclidean_distance function.
## This function should take two lists of integers and
## find the Euclidean distance between them.
## See 'hamming_distance()' in classify.py for an example that
## computes Hamming distances.

def euclidean_distance(list1, list2):
    # this is not the right solution!
    assert isinstance(list1, list)
    assert isinstance(list2, list)

    dist= np.sum((np.array(list1)-np.array(list2))**2)
    return dist



#Once you have implemented euclidean_distance, you can check the results:
#evaluate(nearest_neighbors(euclidean_distance, 5), senate_group1, senate_group2, verbose=2)

## By changing the parameters you used, you can get a classifier factory that
## deals better with independents. Make a classifier that makes at most 3
## errors on the Senate.

my_classifier = nearest_neighbors(hamming_distance, 1)
#evaluate(my_classifier, senate_group1, senate_group2, verbose=1)

### Part 2: ID Trees
#print(CongressIDTree(senate_people, senate_votes, homogeneous_disorder))

## Now write an information_disorder function to replace homogeneous_disorder,
## which should lead to simpler trees.

def information_disorder(yes, no):
    plus, neg=0, 0
    for item in range(len(yes)):
        if yes[item] is yes[0]:
            plus+=1
        else:
            neg+=1

    if (plus==0) or (neg==0): disyes= 0
    else: disyes= -(plus/(plus+neg))*math.log2((plus/(plus+neg)))-(neg/(plus+neg))*math.log2((neg/(plus+neg)))

    plus, neg = 0, 0

    for item in range(len(no)):
        if no[item] is no[0]:
            plus += 1
        else:
            neg += 1

    if (plus == 0) or (neg == 0):
        disno = 0
    else: disno = -(plus / (plus + neg)) * math.log2((plus / (plus + neg))) - (neg / (plus + neg)) * math.log2(
        (neg / (plus + neg)))

    dis= (len(yes)/(len(yes)+len(no)))*disyes + (len(no)/(len(yes)+len(no)))*disno
    return dis

#print(CongressIDTree(senate_people, senate_votes, information_disorder))
#evaluate(idtree_maker(senate_votes, information_disorder), senate_group1, senate_group2, verbose=2)

## Now try it on the House of Representatives. However, do it over a data set
## that only includes the most recent n votes, to show that it is possible to
## classify politicians without ludicrous amounts of information.

def limited_house_classifier(house_people, house_votes, n, verbose = 0):
    house_limited, house_limited_votes = limit_votes(house_people,
                                                     house_votes, n)
    house_limited_group1, house_limited_group2 = crosscheck_groups(house_limited)

    if verbose:
        print("ID tree for first group:")
        print(CongressIDTree(house_limited_group1, house_limited_votes,
                             information_disorder))
        print("ID tree for second group:")
        print(CongressIDTree(house_limited_group2, house_limited_votes,
                             information_disorder))

    return evaluate(idtree_maker(house_limited_votes, information_disorder),
                    house_limited_group1, house_limited_group2, verbose=verbose)
#    evaluate(nearest_neighbors(euclidean_distance, 5), house_limited_group1, house_limited_group2, verbose=verbose)


                                   
## Find a value of n that classifies at least 430 representatives correctly.
## Hint: It's not 10.
N_1 = 44
rep_classified = limited_house_classifier(house_people, house_votes, N_1, verbose= 0)
#31 for k_nearest and 44 for ID_tree

## Find a value of n that classifies at least 90 senators correctly.
N_2 =11
senator_classified = limited_house_classifier(senate_people, senate_votes, N_2, verbose= 0)
#71 for IDtree and 11 for k_nearest!

## Now, find a value of n that classifies at least 95 of last year's senators correctly.
N_3 = 23
old_senator_classified = limited_house_classifier(last_senate_people, last_senate_votes, N_3, verbose= 2)
#22 for k_nearest and 23 for IDtree :))

## The standard survey questions.
HOW_MANY_HOURS_THIS_PSET_TOOK = ""
WHAT_I_FOUND_INTERESTING = ""
WHAT_I_FOUND_BORING = ""


## This function is used by the tester, please don't modify it!
def eval_test(eval_fn, group1, group2, verbose = 0):
    """ Find eval_fn in globals(), then execute evaluate() on it """
    # Only allow known-safe eval_fn's
    if eval_fn in [ 'my_classifier' ]:
        return evaluate(globals()[eval_fn], group1, group2, verbose)
    else:
        raise Exception("Error: Tester tried to use an invalid evaluation function: '%s'" % eval_fn)

    
