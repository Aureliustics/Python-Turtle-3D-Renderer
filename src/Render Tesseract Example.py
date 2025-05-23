debug = False
print("Camera Controls: \nW = Forward\nA = Left\nS = Backward\nD = Right\nSpace = Up\nLControl = Down\n\nRotation:\nUse Arrow Keys")
# Matrix: https://technology.cpm.org/general/3dgraph/?graph3ddata=____bIxmuxmuwWaJxmuwWawWaKwWawWawWaLwWaxmuwWaMwWawWaxmuHwWaxmuxmuIxmuwWaxmuJxmuxmuxmuKxBExBExBELxBEwG0xBEMwG0wG0xBEHwG0xBExBEIxBExBEwG0JwG0xBEwG0KxBEwG0wG0LwG0wG0wG0
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
def connection_points():
    penup()
    setposition(Points[0], Points[1])
    pendown()
    setposition(Points[2], Points[3])
    setposition(Points[12], Points[13])
    setposition(Points[14], Points[15])
    setposition(Points[0], Points[1])
    setposition(Points[6], Points[7])
    setposition(Points[4], Points[5])
    setposition(Points[2], Points[3])
    setposition(Points[4], Points[5])
    setposition(Points[8], Points[9])
    setposition(Points[10], Points[11])
    setposition(Points[14], Points[15])
    setposition(Points[12], Points[13])
    setposition(Points[8], Points[9])
    setposition(Points[4], Points[5])
    setposition(Points[6], Points[7])
    setposition(Points[10], Points[11])
    setposition(Points[22], Points[23])
    setposition(Points[26], Points[27])
    setposition(Points[6], Points[7])
    setposition(Points[26], Points[27])
    setposition(Points[24], Points[25])
    setposition(Points[0], Points[1])
    setposition(Points[24], Points[25])
    setposition(Points[28], Points[29])
    setposition(Points[30], Points[31])
    setposition(Points[4], Points[5])
    setposition(Points[30], Points[31])
    setposition(Points[20], Points[21])
    setposition(Points[8], Points[9])
    setposition(Points[20], Points[21])
    setposition(Points[22], Points[23])
    setposition(Points[26], Points[27])
    setposition(Points[30], Points[31])
    setposition(Points[28], Points[29])
    setposition(Points[2], Points[3])
    setposition(Points[28], Points[29])
    setposition(Points[18], Points[19])
    setposition(Points[12], Points[13])
    setposition(Points[18], Points[19])
    setposition(Points[16], Points[17])
    setposition(Points[14], Points[15])
    setposition(Points[16], Points[17])
    setposition(Points[22], Points[23])
    setposition(Points[16], Points[17])
    setposition(Points[24], Points[25])
    penup()
    setposition(Points[18], Points[19])
    pendown()
    setposition(Points[20], Points[21])
    del Points[:] # emptys the list for reuse. took a while to figure out why the line was moving during rotation lol
    
Vertices = [n for n in range(16)] # technically could make any shape using this: https://technology.cpm.org/general/3dgraph/
Vertices[0] = [[1], [1], [-1]]
Vertices[1] = [[1], [-1], [-1]]
Vertices[2] = [[-1], [-1], [-1]]
Vertices[3] = [[-1], [1], [-1]]
Vertices[4] = [[-1], [-1], [1]]
Vertices[5] = [[-1], [1], [1]]
Vertices[6] = [[1], [-1], [1]]
Vertices[7] = [[1], [1], [1]] # next is outter cube
Vertices[8] = [[2], [2], [2]]
Vertices[9] = [[2], [-2], [2]]
Vertices[10] = [[-2], [-2], [2]]
Vertices[11] = [[-2], [2], [2]]
Vertices[12] = [[2], [2], [-2]]
Vertices[13] = [[-2], [2], [-2]]
Vertices[14] = [[2], [-2], [-2]]
Vertices[15] = [[-2], [-2], [-2]]

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
    
# Projection matrix
projection_matrix = [[1, 0, 0],
                     [0, 1, 0],
                     [0, 0, 1]]
                     

angleX = angleY = angleZ = 0
z_axis = 100 # basically forward and backwards. start at 100 distance away (camera movement)
x_axis = 0 # basically left and right. (camera movement)
y_axis = 0 # basically up and down (camera movement)
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
        setposition(xPos + x_axis, yPos + y_axis) # later make it so it sets position from 1 vertex to the other just like in the old renderer
        Points.append(concatXPos())
        Points.append(concatYPos())
        if debug == False:
            dot((5 * z_axis) / 100, "black" , 0, 0, 255)
        elif debug == True:
            write(Vertex, move=False, align="top", font=("Arial", 13, "normal"))
        #print("[DEBUG]: Rendered Matrix: " + str(Vertex) + " at " + str(PreviousX) + "x " + str(PreviousY) + "y")
        showturtle()
    connection_points()
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