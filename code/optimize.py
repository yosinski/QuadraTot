#! /usr/bin/env python

'''

@date: 20 October 2010

'''

"""
Employs random hill-climbing to choose and evaluate the parameters of the robots'
motion, either by changing one parameter completely randomly, or changing one
parameter slightly. Evaluates each neighbor using user-inputed distance
walked.

"""


    
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

    if len(sys.argv) > 1:
        currentState = [eval(xx) for xx in sys.argv[1].split()]
    else:
        currentState = initialState(ranges)

    statesSoFar = set()  # Keeps track of the states tested so far
    
    bestDistance = -1e100

    stateSoFar = set()

    RunManager.log_start()

    for ii in range(10000):
        print
        print 'Iteration %2d params' % ii, prettyVec(currentState)

        # Make sure this state is new, skip otherwise
        if tuple(currentState) in statesSoFar:
            print '*** Skipping duplicate iteration!'
            continue

        stateSoFar.add(tuple(currentState))

        motionModel = lambda time: sineModel(time,
                                             parameters = currentState)

        android.run(motionModel, runSeconds = 10, resetFirst = False,
                    interpBegin = 3, interpEnd = 3)

        currentDistance = float(raw_input('             Enter distance walked: '))

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
