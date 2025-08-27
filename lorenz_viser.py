import time
import numpy as np

import viser


N_POINTS = 70
N_TRAIL = 30

MAX_SIZE = 0.3
MIN_SIZE = 0.1

TIME_STEP = 0.01

def update_lorenz(points, dt, sigma = 10., ro = 28., beta = 8./3.):
    x, y, z = points[:, 0], points[:, 1], points[:, 2]

    dx = sigma * (y - x)
    dy = x * (ro - z) - y
    dz = x * y - beta * z

    points += dt * np.stack([dx, dy, dz], axis=1)
    return points


server = viser.ViserServer()

@server.on_client_connect
def _(client: viser.ClientHandle) -> None:
    # only modify the camera the first time a client is connected
    
    # values taken from a previous run
    client.camera.wxyz = np.array([ 0.50376306, -0.79778261, -0.28013392,  0.1768917 ])
    client.camera.position = np.array([ 30.82498183, -41.40886391,  44.93191464])
    client.camera.fov = 1.3089969389957472

def main():

    # sample randomly position in 3D
    lorenz_points = np.random.rand(N_POINTS, 3)

    # The trail list stores the history of points.
    lorenz_trail = [lorenz_points.copy()] * (N_TRAIL + 1)
    point_sizes = np.linspace(MAX_SIZE, MIN_SIZE, N_TRAIL + 1)
    
    # Define the color gradient for the trails from yellow to red.
    red_color = np.full(N_TRAIL+1, 255, dtype=np.uint8)
    gradient_green = np.linspace(0, 255, N_TRAIL+1, dtype=np.uint8)
    blue_color = np.zeros(N_TRAIL+1, dtype=np.uint8) 

    red2yellow_gradient = np.stack([red_color, gradient_green, blue_color], axis=1) 

    while True:
        time.sleep(TIME_STEP)

        lorenz_points = update_lorenz(lorenz_points, TIME_STEP)
        
        # shift points in lorenz_trail
        lorenz_trail.pop()
        lorenz_trail.insert(0, lorenz_points.copy())
        
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