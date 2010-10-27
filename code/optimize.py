#! /usr/bin/env python

'''

@date: 27 October 2010

'''

"""
Different algorithms to find choose and evaluate the parameers of the robot's
motion. Evaluates each neighbor and state using WiiTrackClient.

"""

def gradient_search(currentState): 
    """
    N-dimensional policy gradient algorithm. During each iteration of the main
    loop we sample t policies near currentState to estimate the gradient
    around currentState, then move currentState by an amount of eta in the
    most favorable direction. Adapted from Nate Kohl and Peter Stone,
    UT Ausin/ICRA 2004.
    
    """
    # Generate random policies near currentState
    random_policies = []
    
    epsilon = .05
    # Evaluate t=8 policies per iteration
    for i in range(8):
        random_policies.append(Neighbor.gradient(ranges, currentState, epsilon))
        
    # Evaluate each random policy.
    for neighbor in random_policies:
        random_policies[neighbor].append(RunManager.run_robot(neighbor))
        print '        Random policy %2d params' % random_policies.index(neighbor), RunManager.prettyVec(neighbor)
    
    # Average the scores for all random policies
    adjustment = []  # Adjustment vector
    for n in range(len(ranges)):
         # Keep track of number of policies with pos/neg/0 perturbation
         # in dimension n
        num_epos = num_eneg = num_zero = 0
        avg_epos = avg_eneg = avg_zero = 0
        for neighbor in random_policies:
            if neighbor[n] > currentState[n]:  # positive perturbation
                avg_epos = avg_epos + neighbor[len(neighbor) - 1]
                num_epos = num_epos + 1
            if neighbor[n] < currentState[n]:  # negative perturbation
                avg_eneg = avg_eneg + neighbor[len(neighbor) - 1]
                num_eneg = num_eneg + 1
            if neighbor[n] == currentState[n]:  # zero perturbation
                avg_zero = avg_zero + neighbor[len(neighbor) - 1]
                num_zero = num_zero + 1
        
        # Finish calculating averages.        
        try:
            avg_epos = avg_epos / num_epos
        except ZeroDivisionError:
            avg_epos = 0
        
        try: 
            avg_eneg = avg_eneg / num_eneg
        except ZeroDivisionError:
            avg_eneg = 0
            
        try:
            avg_zero = avg_zero / num_zero
        except ZeroDivisionError:
            avg_zero = 0
        
        if avg_zero > avg_epos and avg_zero > avg_eneg:
            adjustment.append(0)
        else:
            adjustment.append(avg_epos - avg_eneg)
    
    # Calculate adjustment vector for each dimension, multiplying with a
    # scalar step-size eta, so that our adjustment will remain a fixed
    # size each iteration
    eta = .1
    for param in adjustment:
        if param < 0:
            param = - (eta * (ranges[n][1] - ranges[n][0]))
        if param > 0:
            param = eta * (ranges[n][1] - ranges[n][0])
        else:
            param = 0
    nextState = [currentState, adjustment]
    currentState = [sum(value) for value in zip(*nextState)]        

def doRun():
    # Parameters are: amp, tau, scaleInOut, flipFB, flipLR
    
    android = Robot(commandRate = 40, loud = False)
    # TODO: motion = Motion()
    # TODO: Move ranges below 
    #ranges = [(0, 400),
    #          (.5, 8),
    #          (-2, 2),
    #          (False, True),
    #          (False, True)]

    ranges = [(0, 400),
              (.5, 8),
              (-2, 2),
              (-1, 1),
              (-1, 1)]

    # Choose initialState, either from user-inputted parameters or randomly
    if len(sys.argv) > 1:
        currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        currentState = RunManager.initialState(ranges)

    statesSoFar = set()  # Keeps track of the states tested so far
    
    bestDistance = -1e100

    RunManager.log_start()

    for ii in range(10000):
        print
        print 'Iteration %2d params' % ii, RunManager.prettyVec(currentState)

        # Check if this state is new, and possibly skip it
        if tuple(currentState) in statesSoFar:
            print '*** Duplicate iteration!'
            # Skip only if using random hill climbing. In other words,
            # comment this line out if using gradient_search:
            currentState = Neighbor.uniform(ranges, bestState)
            continue

        stateSoFar.add(tuple(currentState))
        
        currentDistance = RunManager.run_robot(currentState)

        if currentDistance >= bestDistance:  # Is this a new best?
            bestState = copy(currentState)  # Save new neighbor to best found
            bestDistance = copy(currentDistance)

        print '        best so far', prettyVec(bestState), bestDistance  # Prints best state and distance so far

        write_log(currentState, currentDistance)

        currentState = Neighbor.uniform(ranges, bestState)
        # for gradient descent: currentState = gradient_search(currentState)

    return bestState  # Return the best solution found (a list of params)

def main():
    doRun()

if __name__ == '__main__':
    main()
