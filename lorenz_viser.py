import time
import numpy as np

import viser


N_POINTS = 70
N_TRAIL = 30

MAX_SIZE = 0.3
MIN_SIZE = 0.2

LINE_WIDTH = 4.0

SHAPE_TO_USE = "LINES" # check shape to use: ["LINES", "POINTS"]
assert SHAPE_TO_USE in ["LINES", "POINTS"]

TIME_STEP = 0.01

def update_lorenz(points, dt, sigma = 10., ro = 28., beta = 8./3., integration="rk4"):
    def lorenz_dot(u):
        x, y, z = u[:, 0], u[:, 1], u[:, 2]

        dx = sigma * (y - x)
        dy = x * (ro - z) - y
        dz = x * y - beta * z

        return np.stack([dx, dy, dz], axis=1)

    ## RK4
    if integration == "rk4":
        k1 = lorenz_dot(points)
        k2 = lorenz_dot(points + dt * k1 / 2.)
        k3 = lorenz_dot(points + dt * k2 / 2.)
        k4 = lorenz_dot(points + dt * k3)
        points += dt / 6. * (k1 + 2*k2 + 2*k3 + k4)
    elif integration == "euler":
        points += dt * lorenz_dot(points)
    else:
        raise ValueError(f"Integration chosen: {integration} is not valid. Choose [rk4 | euler]")
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

        lorenz_points = update_lorenz(lorenz_points, TIME_STEP, integration="euler") # euler diverges faster
        
        # shift points in lorenz_trail
        lorenz_trail.pop()
        lorenz_trail.insert(0, lorenz_points.copy())
        
        # display lorenz_trail
        if SHAPE_TO_USE == "POINTS":
            for i in range(len(lorenz_trail)):
                server.scene.add_point_cloud(
                    name="/lorenz_cloud_" + str(i),
                    points=lorenz_trail[i],
                    colors=red2yellow_gradient[i, :], 
                    point_size=point_sizes[i], # we need the for loop to give different point_sizes
                    point_shape = "rounded"
                )
        elif SHAPE_TO_USE == "LINES": # check for redundancy
            all_starts = np.vstack(lorenz_trail[:-1])
            all_ends = np.vstack(lorenz_trail[1:])

            # stack to get the shape (N, 2, 3) required by add_line_segments,
            # where N = N_TRAIL * N_POINTS.
            line_points = np.stack([all_starts, all_ends], axis=1)

            # create start and end colors for the line segments to match the gradient.
            color_starts = np.repeat(red2yellow_gradient[:-1], repeats=N_POINTS, axis=0)
            color_ends = np.repeat(red2yellow_gradient[1:], repeats=N_POINTS, axis=0)

            # stack to get the shape (N, 2, 3) for per-vertex coloring.
            line_colors = np.stack([color_starts, color_ends], axis=1)

            # add all line segments
            server.scene.add_line_segments(
                name="/lorenz_trail",
                points=line_points,
                colors=line_colors,
                line_width=LINE_WIDTH,
            )



if __name__ == "__main__":
    main()