'''
Created on May 29, 2013

@author: tristan
'''


################ Dependency Tests #################
try:
    import numpy as np
except ImportError:
    print "Please install Numpy"
    exit(0)

try:
    import pycuda.autoinit
    import pycuda.driver as cuda
    gpuValid = True
except ImportError:
    gpuValid = False
    print "Unable to load PyCUDA. Please install it for GPU functionality"

try:
    from mesh.meshBuilder import buildSlopingDomain
    from mesh.initialConditionsBuilder import buildPyramidWaterSurface, validateInitialConditions
    from gpu.gpuSimulation import runGPUsimulation
except ImportError:
    print "Error loading sweSolver libraries, please reinstall"
    exit(0)



######################################################
##### Testing
######################################################
testM = 64
testN = 64
testCellSize = 1.0
Coordinates, BottomIntPts = buildSlopingDomain(testCellSize, testM, testN, 0.0, 0.0, 0.0, 0)
U = buildPyramidWaterSurface(testM, testN, 10.0, 32, 32, 13.0, 0.1)
U = validateInitialConditions(testM, testN, BottomIntPts, U)

gpuTime = runGPUsimulation(testM, testN, U, Coordinates, BottomIntPts, 0, [False], 100, 0)
print "GPU simulation time: " + str(gpuTime) + " seconds"
