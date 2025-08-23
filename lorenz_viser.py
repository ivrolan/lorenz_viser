import time
import numpy as np

import viser


def update_lorenz(points, time_step):
    sigma = 10.
    ro = 28.
    beta = 8./3.
    for i in range(len(points)):

        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        dx = sigma * (y - x)
        dy = x * (ro - z) - y
        dz = x * y - beta * z

        x = x + time_step * dx
        y = y + time_step * dy
        z = z + time_step * dz
        points[i, 0] = x
        points[i, 1] = y
        points[i, 2] = z
    return points

def main():
    server = viser.ViserServer()

    n_points = 15

    # sample randomly position in 3D
    lorenz_points = np.random.rand(n_points, 3)

    n_trail = 30
    MAX_SIZE = 0.3
    MIN_SIZE = 0.1
    point_sizes = np.linspace(MAX_SIZE, MIN_SIZE, n_trail + 1)
    lorenz_trail = [lorenz_points.copy()] * (n_trail + 1)

    red_color = np.full(n_trail+1, 255, dtype=np.uint8)
    gradient_green = np.linspace(0, 255, n_trail+1, dtype=np.uint8)
    blue_color = np.zeros(n_trail+1, dtype=np.uint8) 

    red2yellow_gradient = np.stack([red_color, gradient_green, blue_color], axis=1) 

    print("Visit: http://localhost:8080")

    time_step = 0.01

    while True:

        time.sleep(time_step)

        lorenz_points = update_lorenz(lorenz_points, time_step)
        
        # shift points in lorenz_trail, start from the back
        for i in range(len(lorenz_trail) - 2, -1, -1):
            lorenz_trail[i+1] = lorenz_trail[i].copy()

        lorenz_trail[0] = lorenz_points.copy()

        # display lorenz_trail
        for i in range(len(lorenz_trail)):
            server.scene.add_point_cloud(
                name="/lorenz_cloud_" + str(i),
                points=lorenz_trail[i],
                colors=red2yellow_gradient[i, :], 
                point_size=point_sizes[i],
                point_shape = "rounded"
            )



if __name__ == "__main__":
    main()