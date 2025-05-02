import math
screen = getscreen()

speed(0)
bgcolor("white")

# camera position and rotation
camera_pos = [0, 0, -5]  # camera position in 3D space
camera_rot = [0, 0]  # camera rotation (pitch, yaw)
move_speed = 1  # movement speed
fov = 90  # field of view
near_clip = 0.5  # near clipping plane
far_clip = 100  # far clipping plane
aspect_ratio = 400  # screen aspect ratio

# cube vertices
Vertices = [
    [-1, -1, 1],  # vertex 0
    [1, -1, 1],   # vertex 1
    [1, 1, 1],    # vertex 2
    [-1, 1, 1],   # vertex 3
    [-1, -1, -1], # vertex 4
    [1, -1, -1],  # vertex 5
    [1, 1, -1],   # vertex 6
    [-1, 1, -1]   # vertex 7
]

# cube edges
edges = [
    [0, 1], [1, 2], [2, 3], [3, 0],  # front face
    [4, 5], [5, 6], [6, 7], [7, 4],  # back face
    [0, 4], [1, 5], [2, 6], [3, 7]   # connecting edges
]

# matrix multiplication
def matrix_multiply(A, B):  
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])

    C = [[0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]

    return C

# move camera based on direction and speed
def move_camera(direction, speed):
    global camera_pos
    if direction == "forward":
        camera_pos[2] -= speed
    elif direction == "backward":
        camera_pos[2] += speed
    elif direction == "left":
        camera_pos[0] -= speed
    elif direction == "right":
        camera_pos[0] += speed
    elif direction == "up":
        camera_pos[1] -= speed
    elif direction == "down":
        camera_pos[1] += speed
    render_object()

# rotate camera along X or Y axis
def rotate_camera(axis, angle_change):
    global camera_rot
    if axis == "X":
        camera_rot[0] += angle_change
    elif axis == "Y":
        camera_rot[1] += angle_change
    render_object()

# perspective projection matrix
def perspective_projection(x, y, z):
    fov_rad = math.radians(fov)
    f = 1 / math.tan(fov_rad / 2)
    near_far_range = far_clip - near_clip
    
    projection_matrix = [
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far_clip + near_clip) / near_far_range, -1],
        [0, 0, (2 * far_clip * near_clip) / near_far_range, 0]
    ]
    return projection_matrix

# render the 3D object based on camera position and rotation
def render_object():
    clear()  # clear the screen
    screen.tracer(0)  # disable animation

    # calculate rotation matrices for X and Y axes
    rotationX = [[1, 0, 0],
                 [0, math.cos(math.radians(camera_rot[0])), -math.sin(math.radians(camera_rot[0]))],
                 [0, math.sin(math.radians(camera_rot[0])), math.cos(math.radians(camera_rot[0]))]]

    rotationY = [[math.cos(math.radians(camera_rot[1])), 0, math.sin(math.radians(camera_rot[1]))],
                 [0, 1, 0],
                 [-math.sin(math.radians(camera_rot[1])), 0, math.cos(math.radians(camera_rot[1]))]]

    # loop through vertices and apply transformations
    projected_vertices = []
    for Vertex in Vertices:
        xRotation = matrix_multiply(rotationX, [[Vertex[0]], [Vertex[1]], [Vertex[2]]])
        yRotation = matrix_multiply(rotationY, xRotation)

        # apply camera translation
        xPos = yRotation[0][0] - camera_pos[0]
        yPos = yRotation[1][0] - camera_pos[1]
        zPos = yRotation[2][0] - camera_pos[2]

        # apply perspective projection
        if zPos != 0:
            x_screen = (xPos / zPos) * 100
            y_screen = (yPos / zPos) * 100
        else:
            x_screen, y_screen = 0, 0

        # apply clipping
        if zPos < near_clip or zPos > far_clip:
            continue

        # store projected vertex
        projected_vertices.append([x_screen, y_screen, zPos])

    # render edges based on projected vertices
    for edge in edges: # p1 means projected screen pos of Vertices[0] and p2 means projected screen pos of Vertices[1]
        p1_idx, p2_idx = edge # idx means index btw
        if p1_idx < len(projected_vertices) and p2_idx < len(projected_vertices):
            p1 = projected_vertices[p1_idx]
            p2 = projected_vertices[p2_idx]
            penup()
            setposition(p1[0], p1[1])
            pendown()
            setposition(p2[0], p2[1])

    # clear screen if no vertices are visible
    if len(projected_vertices) == 0:
        clear()

    screen.update()

render_object()  # render the initial frame

def keyInput():
    screen.listen()

    # camera movement bindings
    screen.onkey(lambda: move_camera("forward", move_speed), "w")
    screen.onkey(lambda: move_camera("backward", move_speed), "s")
    screen.onkey(lambda: move_camera("left", move_speed), "a")
    screen.onkey(lambda: move_camera("right", move_speed), "d")
    screen.onkey(lambda: move_camera("up", move_speed), "Space")
    screen.onkey(lambda: move_camera("down", move_speed), "Control")

    # camera rotation bindings
    screen.onkey(lambda: rotate_camera("X", 5), "Up")
    screen.onkey(lambda: rotate_camera("X", -5), "Down")
    screen.onkey(lambda: rotate_camera("Y", 5), "Right")
    screen.onkey(lambda: rotate_camera("Y", -5), "Left")

keyInput()
hideturtle()

screen.mainloop()
