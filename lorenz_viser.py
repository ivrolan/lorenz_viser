import time
import numpy as np

import viser


N_POINTS = 35
N_TRAIL = 30

MAX_SIZE = 0.3
MIN_SIZE = 0.1

TIME_STEP = 0.01

def update_lorenz(points, dt, sigma = 10., ro = 28., beta = 8./3.):
    for i in range(len(points)):

        x = points[i, 0]
        y = points[i, 1]
        z = points[i, 2]

        dx = sigma * (y - x)
        dy = x * (ro - z) - y
        dz = x * y - beta * z

        x = x + dt * dx
        y = y + dt * dy
        z = z + dt * dz
        points[i, 0] = x
        points[i, 1] = y
        points[i, 2] = z
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

    
    point_sizes = np.linspace(MAX_SIZE, MIN_SIZE, N_TRAIL + 1)
    lorenz_trail = [lorenz_points.copy()] * (N_TRAIL + 1)

    red_color = np.full(N_TRAIL+1, 255, dtype=np.uint8)
    gradient_green = np.linspace(0, 255, N_TRAIL+1, dtype=np.uint8)
    blue_color = np.zeros(N_TRAIL+1, dtype=np.uint8) 

    red2yellow_gradient = np.stack([red_color, gradient_green, blue_color], axis=1) 

    while True:

        time.sleep(TIME_STEP)

        lorenz_points = update_lorenz(lorenz_points, TIME_STEP)
        
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