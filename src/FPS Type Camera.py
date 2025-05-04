import math

# canvas setup
window_length_input = input("Set window size (default 400): ")

window_length = int(window_length_input) if window_length_input else 400

screen = getscreen()
screen.setup(window_length, window_length)
screen.bgcolor("white")
shape("turtle")

speed(0)
bgcolor("white")
ht()

# camera position and rotation
camera_pos = [0, 0, -10]  # camera position in 3D space
object_rot = [0, 0]  # camera rotation (pitch, yaw)
move_speed = 0.5  # movement speed
fov = 120  # field of view
near_clip = 0.01  # near clipping plane. lower = cube has to be closer before clipping logic sets in, further = cube will clip from further
far_clip = 100  # far clipping plane
aspect_ratio = window_length  # screen aspect ratio.
camera_turn = [0, 0]  # camera panning (x, y)

# game controls
sprinting = False
debug = True
collision = True  # toggle this when you want collision on/off

def sprint():  # maybe make this toggle not hold to prevent bugs
    global sprinting
    sprinting = not sprinting  # sprint logic should check if using W key only and if stopped, set speed back to 0


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
edges = [  # this is basically the connection points, not the vertices
    [0, 1], [1, 2], [2, 3], [3, 0],  # front face
    [4, 5], [5, 6], [6, 7], [7, 4],  # back face
    [0, 4], [1, 5], [2, 6], [3, 7]   # connecting edges
]

# this is for having multiple objects, later use nonlocals and include attributes such as colour, identifier, integrity
objects = [
    {"position": [3, 0, -5], "collision": True}, # positions are in xyz format
    {"position": [-3, 0, -5], "collision": False},
    {"position": [-1.5, 3, -5], "collision": True},
    {"position": [-4, -4.5, -4], "collision": False}
]

# matrix multiplication for transformations
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

def check_collision(new_position):
    for obj in objects:
        if not obj.get("collision", True):  # skip collision code if object has collision attribute set to False
            continue

        position = obj["position"]
        x, y, z = new_position
        
        # side faces need larger hitboxes because it looks like it needs more space for some reason
        hitbox_size = 1.5
        side_hitbox_size = 2.0
        
        # front and back faces bounding box
        cube_min_front_back = [position[0] - hitbox_size, position[1] - hitbox_size, position[2] - hitbox_size]
        cube_max_front_back = [position[0] + hitbox_size, position[1] + hitbox_size, position[2] + hitbox_size]
        
        # side faces bounding box
        cube_min_sides = [position[0] - side_hitbox_size, position[1] - hitbox_size, position[2] - hitbox_size]
        cube_max_sides = [position[0] + side_hitbox_size, position[1] + hitbox_size, position[2] + hitbox_size]
        
        # top and bottom bounding box (same as side faces)
        cube_min_top_bottom = [position[0] - hitbox_size, position[1] - hitbox_size, position[2] - hitbox_size]
        cube_max_top_bottom = [position[0] + hitbox_size, position[1] + hitbox_size, position[2] + hitbox_size]
        
        # front and back face hitbox check
        if (cube_min_front_back[0] < x < cube_max_front_back[0] and
            cube_min_front_back[1] < y < cube_max_front_back[1] and
            cube_min_front_back[2] < z < cube_max_front_back[2]):
            return True
        
        # side face hitbox check
        elif (cube_min_sides[0] < x < cube_max_sides[0] and
              cube_min_sides[1] < y < cube_max_sides[1] and
              cube_min_sides[2] < z < cube_max_sides[2]):
            return True
        # top and bottom hitbox check
        elif (cube_min_top_bottom[0] < x < cube_max_top_bottom[0] and
              cube_min_top_bottom[1] < y < cube_max_top_bottom[1] and
              cube_min_top_bottom[2] < z < cube_max_top_bottom[2]):
            return True

    return False

# move camera based on direction and speed
def move_camera(direction, speed):
    global camera_pos, sprinting, move_speed, debug, collision

    original_position = camera_pos[:]  # buffer original position before movement. used for collision check

    if direction == "forward" and sprinting == False:
        move_speed = 0.5  # if not sprinting then set speed back to default
        new_position = [camera_pos[0], camera_pos[1], camera_pos[2] + move_speed]

    elif direction == "forward" and sprinting == True:
        if speed < 1:  # max speed cap
            move_speed += 0.1  # accelerate by 0.1 each time
        new_position = [camera_pos[0], camera_pos[1], camera_pos[2] + move_speed]

    elif direction == "backward":
        sprinting = False  # toggle off sprinting
        move_speed = 0.5  # reset sprint when clicking S key, like S tapping in minecraft
        new_position = [camera_pos[0], camera_pos[1], camera_pos[2] - move_speed]
    elif direction == "left":
        new_position = [camera_pos[0] - move_speed, camera_pos[1], camera_pos[2]]
    elif direction == "right":
        new_position = [camera_pos[0] + move_speed, camera_pos[1], camera_pos[2]]
    elif direction == "up":
        new_position = [camera_pos[0], camera_pos[1] + move_speed, camera_pos[2]]
    elif direction == "down":
        new_position = [camera_pos[0], camera_pos[1] - move_speed, camera_pos[2]]

    if not check_collision(new_position) or collision == False:
        camera_pos = new_position  # if there is no collision then update position

    if debug == True:
        pass
        print("[Debug Logs]: " + str(camera_pos[0]) + "x " + str(camera_pos[1]) + "y " + str(camera_pos[2]) + "z" + " | Pitch: " + str(object_rot[0]) + " | Yaw: " + str(object_rot[1]) + " | Sprint: " + str(sprinting) + " | Speed: " + str(move_speed))
    render_objects()

# rotate camera along X or Y axis
def rotate_object(axis, angle_change):
    global object_rot
    if axis == "X":
        object_rot[0] += angle_change
    elif axis == "Y":
        object_rot[1] += angle_change

    if debug == True:
        pass
        print("[Debug Logs]: " + str(camera_pos[0]) + "x " + str(camera_pos[1]) + "y " + str(camera_pos[2]) + "z" + " | Pitch: " + str(object_rot[0]) + " | Yaw: " + str(object_rot[1]) + " | Sprint: " + str(sprinting) + " | Speed: " + str(move_speed))
    render_objects()

def perspective_projection(x, y, z):
    fov_rad = math.radians(fov)
    f = 1 / math.tan(fov_rad / 2)
    near_far_range = far_clip - near_clip

    projection_matrix = [
        [f / aspect_ratio, 0, 0],
        [0, f, 0, 0],
        [0, (far_clip + near_clip) / near_far_range, -1],
        [0, (2 * far_clip * near_clip) / near_far_range, 0]
    ]
    return projection_matrix

# render all objects based on camera position and rotation
def render_objects():
    clear()
    screen.tracer(0)

    # calculate rotation matrices for X and Y axis
    rotationX = [[1, 0, 0],
                 [0, math.cos(math.radians(object_rot[0])), -math.sin(math.radians(object_rot[0]))],
                 [0, math.sin(math.radians(object_rot[0])), math.cos(math.radians(object_rot[0]))]]

    rotationY = [[math.cos(math.radians(object_rot[1])), 0, math.sin(math.radians(object_rot[1]))],
                 [0, 1, 0],
                 [-math.sin(math.radians(object_rot[1])), 0, math.cos(math.radians(object_rot[1]))]]

    # loop through vertices and apply transformations
    for obj in objects:
        position = obj["position"]

        projected_vertices = []

        # loop through vertices and translate 3d matrix to 2d
        for Vertex in Vertices:
 
            xRotation = matrix_multiply(rotationX, [[Vertex[0]], [Vertex[1]], [Vertex[2]]])
            yRotation = matrix_multiply(rotationY, xRotation)

            # apply camera translation
            xPos = yRotation[0][0] + position[0] - camera_pos[0]
            yPos = yRotation[1][0] + position[1] - camera_pos[1]
            zPos = yRotation[2][0] + position[2] - camera_pos[2]

            # apply perspective projection
            if zPos != 0:
                x_screen = (xPos / zPos) * 300  # you can increase or decrease the multiplier to adjust scale
                y_screen = (yPos / zPos) * 300 # I found that increasing this from 100 to 300 made the fov stretch less extreme
            else:
                x_screen, y_screen = 0, 0

            # apply clipping
            if zPos < near_clip or zPos > far_clip:
                continue

            # store projected vertex
            projected_vertices.append([x_screen, y_screen, zPos])

        # render connection points based on projected vertices. 
        # notice that if you comment out this for loop, nothing will appear. its cuz i dont draw dots for vectices on this version of renderer
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

render_objects()  # render the initial frame

def keyInput():
    screen.listen()

    # camera movement bindings (along the xyz axis)
    screen.onkey(lambda: move_camera("forward", move_speed), "w")
    screen.onkey(lambda: move_camera("backward", move_speed), "s")
    screen.onkey(lambda: move_camera("left", move_speed), "a")
    screen.onkey(lambda: move_camera("right", move_speed), "d")
    screen.onkey(lambda: move_camera("up", move_speed), "Space")
    screen.onkey(lambda: move_camera("down", move_speed), "Control")

    # camera panning binds (looking left right up down) vertical panning fixed to 90 and -90. no, your neck cannot bend >90 degs
    screen.onkey(lambda: rotate_object("X", 5), "Up")
    screen.onkey(lambda: rotate_object("X", -5), "Down") # panning still hasnt been implemented yet
    screen.onkey(lambda: rotate_object("Y", 5), "Right")
    screen.onkey(lambda: rotate_object("Y", -5), "Left")
    
    # sprint toggle
    screen.onkey(lambda: sprint(), "Shift")

keyInput()
hideturtle()

screen.mainloop()
