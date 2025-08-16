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

    colors = np.zeros((n_points, 3), dtype=np.uint8)
    colors[:, 0] = (lorenz_points[:, 0] * 255).astype(np.uint8)  # Red channel.
    colors[:, 1] = (lorenz_points[:, 1] * 255).astype(np.uint8)  # Green channel.
    colors[:, 2] = (lorenz_points[:, 2] * 255).astype(np.uint8)  # Blue channel.

    server.scene.add_point_cloud(
        name="/lorenz_cloud",
        points=lorenz_points,
        colors=colors,
        point_size=0.5,

    )

 
    print("Visit: http://localhost:8080")

    time_step = 0.01


    while True:

        time.sleep(time_step)

        lorenz_points = update_lorenz(lorenz_points, time_step)

        server.scene.add_point_cloud(
            name="/lorenz_cloud",
            points=lorenz_points,
            colors=colors,
            point_size=0.5,
            point_shape = "rounded"
        )



if __name__ == "__main__":
    main()