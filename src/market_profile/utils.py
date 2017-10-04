import numpy as np


# Find the index of the maximum closest to middle
def midmax_idx(array):
    # Find candidate maxima
    maxima_idxs = np.argwhere(array == np.amax(array))[:,0]

    # Find the distances from the midpoint to find
    # the maxima with the least distance
    midpoint = len(array) / 2
    v_norm = np.vectorize(np.linalg.norm)
    maximum_idx = np.argmin(v_norm(maxima_idxs - midpoint))

    return maxima_idxs[maximum_idx]
