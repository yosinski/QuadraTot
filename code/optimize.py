#! /usr/bin/env python

'''

@date: 20 October 2010

'''

"""
Employs random hill-climbing to choose and evaluate the parameters of the robots'
motion. Evaluates each neighbor using user-inputed distance walked.

"""

def gradient_search(): 
    # Parameters are: amp, tau, scaleInOut, flipFB, flipLR
    
    android = Robot(commandRate = 40, loud = False)
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

    stateSoFar = set()

    RunManager.log_start()

    for ii in range(10000):
        print
        print 'Iteration %2d params' % ii, RunManager.prettyVec(currentState)

        beginDistance = WiiTrackClient.getPosition()

        # Make sure this state is new, skip otherwise
        if tuple(currentState) in statesSoFar:
            print '*** Skipping duplicate iteration!'
            continue

        stateSoFar.add(tuple(currentState))

        currentDistance = RunManager.run_robot(currentState)

        if currentDistance >= bestDistance:  # Is this a new best?
            bestState = copy(currentState)  # Save new neighbor to best found
            bestDistance = copy(currentDistance)

        # Prints best state and distance so far
        print '        best so far', prettyVec(bestState), bestDistance

        write_log(currentState, currentDistance)
        
        # Generate random policies near currentState
        random_policies = []
        
        epsilon = .1
        # Evaluate t=15 policies per iteration, decide this?
        for i in range(15):
            list.append(Neighbor.gradient(ranges, currentState, epsilon))
            
        # Evaluate each random policy.
        for neighbor in random_policies:
            random_policies[neighbor].append(RunManager.run_robot(neighbor))
        
        # Average the scores for all random policies
        adjustment = []  # Adjustment vector
        for n in range(len(ranges)):
             # Keep track of number of policies with pos/neg/0 perturbation
             # in dimension n
            num_epos = num_eneg = num_zero = 0
            avg_epos = avg_eneg = avg_zero = 0
            for neighbor in random_policies:
                if isinstance(ranges[n][0], bool):  # boolean parameter
                    if neighbor[n] == currentState[n]:
                        avg_zero = avg_zero + neighbor[len(neighbor) - 1]
                        num_zero = num_zero + 1
                    else:
                        avg_epos = avg_epos + neighbor[len(neighbor) - 1]
                        num_epos = num_epos + 1
                else:
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
        
        # Normalize adjustment vector and multiply it by a scalar step-size
        # eta (?), so that our adjustment will remain a fixed size each 
        # iteration
        for param in adjustment:
            param = param / math.fabs(param)
            param = param # TODO: eta = epsilon?? Hmm. Need to decide
        
        nextState = [currentState, adjustment]
        currentState = [sum(value) for value in zip(*nextState)]        

    return bestState  # Return the best solution found (a list of params)

    
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

        # Make sure this state is new, skip otherwise
        if tuple(currentState) in statesSoFar:
            print '*** Skipping duplicate iteration!'
            continue

        stateSoFar.add(tuple(currentState))
        
        currentDistance = RunManager.run_robot(currentState)

        if currentDistance >= bestDistance:  # Is this a new best?
            bestState = copy(currentState)  # Save new neighbor to best found
            bestDistance = copy(currentDistance)

        print '        best so far', prettyVec(bestState), bestDistance  # Prints best state and distance so far

        write_log(currentState, currentDistance)

        currentState = Neighbor.uniform(ranges, bestState)

    return bestState  # Return the best solution found (a list of params)

def main():
    doRun()

if __name__ == '__main__':
    main()
