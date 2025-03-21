debug = False
screen = getscreen()
import math
speed(0)
bgcolor("white")

def concatXPos():
    fetchXY = str(pos())
    fetchXY = fetchXY[1:] # remove first character which is "("
    subX = fetchXY.split(".")[0] # splits the string into two at the comma, then only take in the first part
    outputX = subX.replace(".", "") # now remove the comma by replacing comma with nothing
    return int(outputX)
concatXPos()

def concatYPos():
    fetchXY = str(pos())
    subY = fetchXY.split(" ")[1][:-1] # splits the string into two at the space after the comma, then only take in the second part
    outputY = subY.split(".")[0] # splits after the decimal point and picks the first cut
    return int(outputY)
concatYPos()

Points = []

Vertices = [n for n in range(5)] # technically could make any shape using this: https://technology.cpm.org/general/3dgraph/
Vertices[0] = [[0], [0], [3]]
Vertices[1] = [[2], [0], [0]]
Vertices[2] = [[0], [2], [0]]
Vertices[3] = [[0], [-2], [0]]
Vertices[4] = [[-2], [0], [0]]


def evaluate_face_metric(segment_data, colour):
    color(colour)
    for i in range(0, len(segment_data), 2): # in range, i starts at 0 -> ends at length of the row, add 2 each time since x and y are pairs
        pendown()
        if debug == False:
            dot((5 * z_axis) / 100, "black" , 0, 0, 255)
        x = segment_data[i]
        y = segment_data[i + 1]
        setposition(x, y)

def geometric_faces(vertices, shape): # Automatically generate faces/connection points by going through every face combonation with 3 vertices
    
    # group the vertices into pairs (x, y)
    vertices = [(vertices[i], vertices[i + 1]) for i in range(0, len(vertices), 2)]
    
    faces = []
    
    # algorithm to go through each combonation of 3 vertices then append it to faces
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            for k in range(j + 1, len(vertices)):
                faces.append([vertices[i], vertices[j], vertices[k]])
    
    # prevent from drawing twice. remove every other item
    faces = [face for i, face in enumerate(faces) if i % 2 != 0]
    
    # to connect the faces, the starting vertex needs to also be the ending vertex
    for face in faces:
        face.append(face[0])
    
    # format the list so it can be read by evaluate_face_metrix function. [(x, y)] - > [x, y]
    unpacked_faces = []
    for face in faces:
        unpacked_faces.append([position for vertex in face for position in vertex])
    
    for i, points in enumerate(unpacked_faces): # points is the list of vertices to make current face
        evaluate_face_metric(points, "black")
        
    del Points[:] # clear points for reuse per "frame"
# visual for how matrix multiplication works: https://i.sstatic.net/ZoUDJ.gif
def matrix_multiply(A, B): # algorithm for multiplying the matrix:
    rows_A = len(A)
    cols_A = len(A[0])
    cols_B = len(B[0])

    C = [[0] * cols_B for _ in range(rows_A)]

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    
    return C
    
# projection matrix
projection_matrix = [[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]]
                     

angleX = angleY = angleZ = 0
z_axis = 100 # basically forward and backwards. start at 100 distance away
x_axis = 0 # basically left and right.
y_axis = 0 # basically up and down
def render_object():
    global angleX, angleY, angleZ
    # formula from: https://en.wikipedia.org/wiki/Rotation_matrix
    rotationX = [[1, 0, 0],
                [0, math.cos(angleX), -math.sin(angleX)],
                [0, math.sin(angleX), math.cos(angleX)]]
                
    rotationY = [[math.cos(angleY), 0, math.sin(angleY)],
                [0, 1, 0],
                [-math.sin(angleY), 0, math.cos(angleY)]]
                
    rotationZ = [[math.cos(angleZ), -math.sin(angleZ), 0],
                [math.sin(angleZ), math.cos(angleZ), 0],
                [0,0,1]]
                
    clear()
    screen.tracer(0)
    # converting xyz (3d) to xy (2d) using matrix multiplication algorithm
    for Vertex in Vertices:
        xRotation = matrix_multiply(rotationX, Vertex)
        yRotation = matrix_multiply(rotationY, xRotation)
        zRotation = matrix_multiply(rotationZ, yRotation)
        projection = matrix_multiply(projection_matrix, zRotation)
        xPos = projection[0][0] * z_axis
        yPos = projection[1][0] * z_axis
        penup()
        setposition(xPos + x_axis, yPos + y_axis)
        if debug == True:
            write(Vertex, move=False, align="top", font=("Arial", 13, "normal"))
        Points.append(concatXPos())
        Points.append(concatYPos())
    geometric_faces(Points, len(Points))
    screen.update()

render_object()

def update_angle(axis, value):
    global angleX, angleY
    if axis == 'X':
        angleX += value
    elif axis == 'Y':
        angleY += value
    render_object()

def update_position(axis, value):
    global x_axis, y_axis, z_axis
    if axis == 'X':
        x_axis += value
    elif axis == 'Y':
        y_axis += value
    elif axis == 'Z':
        z_axis += value
        pensize(1 + (z_axis / 100))
    render_object()

def keyInput():
    key_actions = {
        "Up": lambda: update_angle('X', -0.1),
        "Down": lambda: update_angle('X', 0.1),
        "Right": lambda: update_angle('Y', 0.1),
        "Left": lambda: update_angle('Y', -0.1),
        "w": lambda: update_position('Z', 10),
        "s": lambda: update_position('Z', -5) if z_axis >= 5 else None,
        "d": lambda: update_position('X', 5),
        "a": lambda: update_position('X', -5),
        "Space": lambda: update_position('Y', 5),
        "Control": lambda: update_position('Y', -5)
    }

    screen.listen()
    for key, action in key_actions.items():
        screen.onkey(action, key)

keyInput()
hideturtle()

screen.mainloop()