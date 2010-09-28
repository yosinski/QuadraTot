from math import sin, pi

def sineModel(time, parameters, croppingFunction = None):
    '''This model uses 5 parameters....'''

    if len(parameters) != 5:
        raise Exception('sineModel expected parameter vector of length 5, got' + repr(parameters))

    pFloat = [float(xx) for xx in parameters]
    amp, tau, scaleInOut, flipFB, flipLR = pFloat

    centerConst = 512
    ret = [centerConst] * 9
    
    offset = 512
    
    # Compute base sine wave
    base = amp * sin(2*pi*time/tau)

    idxInner = [0, 2, 4, 6]
    idxOuter = [1, 3, 5, 7]
    idxFB    = [0, 1, 2, 3]
    idxLR    = [6, 7, 0, 1]
    
    for ii in idxInner:
        ret[ii] = base
    for ii in idxOuter:
        ret[ii] = base * scaleInOut

    if flipFB:
        for ii in idxFB:
            ret[ii] = -ret[ii]
    if flipLR:
        for ii in idxLR:
            ret[ii] = -ret[ii]

    for ii in idxInner + idxOuter:
        ret[ii] += offset
        
    if croppingFunction:
        ret = croppingFunction(ret)

    return ret
