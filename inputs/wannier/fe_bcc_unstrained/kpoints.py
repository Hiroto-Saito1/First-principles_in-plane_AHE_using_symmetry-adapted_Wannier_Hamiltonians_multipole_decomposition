import numpy as np
nx, ny, nz = 8, 8, 8

for x in np.linspace(0, 1, nx, endpoint=False):
    for y in np.linspace(0, 1, ny, endpoint=False):
        for z in np.linspace(0, 1, nz, endpoint=False):
            x_adj = x - 1 if x >= 0.5 else x
            y_adj = y - 1 if y >= 0.5 else y
            z_adj = z - 1 if z >= 0.5 else z
            print(f"{x_adj:.10f}\t{y_adj:.10f}\t{z_adj:.10f}")