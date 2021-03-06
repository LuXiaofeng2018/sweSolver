'''
Created on May 21, 2013

@author: tristan
'''

import os
import numpy as np
from pycuda.compiler import SourceModule
from gpu.gpuSimulation import useCachedKernels

fluxCode = open(os.path.join(os.path.dirname(__file__), './fluxCalculations.cu'), 'r')

try:

    # Put the kernel code into a SourceModule
    if useCachedKernels:
        fluxModule = SourceModule(fluxCode.read())
    else:
        fluxModule = SourceModule(fluxCode.read(), cache_dir=False)
    fluxCode.close()

    # Create reference to the specific functions in the SourceModule
    FluxSolverFn = fluxModule.get_function("FluxSolver")
    BuildRFn = fluxModule.get_function("buildRValues")

    # Create callable functions
    def FluxSolver(FluxesGPU, UIntPtsGPU, BottomIntPtsGPU, propSpeedsGPU, m, n, blockDims, gridDims):

        FluxSolverFn(FluxesGPU, UIntPtsGPU, BottomIntPtsGPU, propSpeedsGPU,
                     np.int32(m), np.int32(n),
                     block=(blockDims[0], blockDims[1], 1), grid=(gridDims[0], gridDims[1]))

    def BuildRValues(RValuesGPU, FluxesGPU, SlopeSourceGPU, WindSourceGPU, m, n, blockDims, gridDims):

        BuildRFn(RValuesGPU, FluxesGPU, SlopeSourceGPU, WindSourceGPU,
                 np.int32(m), np.int32(n),
                 block=(blockDims[0], blockDims[1], 1), grid=(gridDims[0], gridDims[1]))

except IOError:
    print "Error opening fluxCalculations.cu"
