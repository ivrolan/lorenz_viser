import time
import numpy as np

import viser


def update_lorenz(points, time_step):
    # σ = 10
    # ρ = 28
    # β = 8/3
    for i in range(len(points)):

        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        dx = 10 * (y - x)
        dy = x * (28 - z) - y
        dz = x * y - 8.0/3.0 * z

        x = x + time_step * dx
        y = y + time_step * dy
        z = z + time_step * dz
        points[i, 0] = x
        points[i, 1] = y
        points[i, 2] = z
    return points

def main():
    server = viser.ViserServer()

    n_points = 10

    # sample randomly position in 3D
    lorenz_points = np.random.rand(n_points, 3)

    n_trail = 30
    point_sizes = np.linspace(0.1, 0.01, n_trail + 1)
    lorenz_trail = [lorenz_points] * (n_trail + 1)

    print(type(lorenz_trail))
    # colors = np.zeros((n_points, 3), dtype=np.uint8)

 
    print("Visit: http://localhost:8080")

    time_step = 0.01


    while True:

        time.sleep(time_step)

        lorenz_points = update_lorenz(lorenz_points, time_step)
        
        # shift points in lorenz_trail
        for i in range(len(lorenz_trail) - 2, -1, -1):
            lorenz_trail[i+1] = lorenz_trail[i]

        lorenz_trail[0] = lorenz_points


        # display lorenz_trail
        for i in range(len(lorenz_trail)):

            server.scene.add_point_cloud(
                name="/lorenz_cloud_" + str(i),
                points=lorenz_trail[i],
                colors=(0, 0, 0), 
                point_size=point_sizes[i],
                point_shape = "rounded"
            )



if __name__ == "__main__":
    main()