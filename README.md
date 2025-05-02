<h1>Python Turtle 3D Renderer</h1>
<h3>Renders a 3D object to the screen by using projection matrix and vertices. Made this as a fun project for school so don't expect the code quality to be good.</h3>

<h1>Usage</h1>
<ul>
  <li>Must be ran in a <a href="https://codehs.com/" target="_blank">CodeHS</a> sandbox</li>
  <li>Once logged into Codehs, click "Sandbox" in the navigation bar</li>
  <li>Click "Create Program" then select "Python (turtle)" and create program</li>
  <li>Copy and paste the code from either the <a href="https://github.com/Aureliustics/Python-Turtle-3D-Renderer/blob/main/src/Render%20Square%20Example.py" target="_blank">square example</a>, <a href="https://github.com/Aureliustics/Python-Turtle-3D-Renderer/blob/main/src/Render%20Triangle%20Example.py" target="_blank">triangle example</a> or <a href="https://github.com/Aureliustics/Python-Turtle-3D-Renderer/blob/main/src/Render%20Tesseract%20Example.py" target="_blank">tesseract example</a> into your sandbox then run</li>
  <li>Interact with the object using WASD and arrow keys. WASD moves the camera position and arrow keys changes the rotation of the object</li>
  <li>If you prefer a camera that is in a first person style (letting you move past the object and through it) run the <a href="https://github.com/Aureliustics/Python-Turtle-3D-Renderer/blob/main/src/FPS%20Type%20Camera.py" target="_blank">fps camera version</a></li>
</ul>

<h1>Modify Object</h1>
<ul>
  <li>Create a shape using vertices on this <a href="https://technology.cpm.org/general/3dgraph/" target="_blank">site</a></li>
  <li>Once you have an object, put in the matrix values on the "Vertices = [n for n in range()]" line (make sure to change the value of range to the amount of vertices you made)</li>
  <li>Understand that the value of the vertex will be like this: Point[0] for example is the X position of the first vertex, Points[1] is the Y position of the first vertex</li>
  <li>So Points[0] and Points[1] are directly linked. Knowing this we can tell that the second vertex's X and Y are Points[2] and Points[3]</li>
  <li>Now that you know this you can change the Points[] value in the setpositions in the function "connection_points()" to connect the vertices</li>
</ul>

<h1>Textures/Colors</h1>
<p>Currently, I have not implemented support for the object to have textures but I may do so in the future. You could try implementing it by:</p>
<ul>
  <li>1. Creating a system that detects (optional) and stores the vertices of each face into a list (So you can set the individual color per face)</li>
  <li>2. Using the data, you can replace the connection_points function to draw each individual face and fill it with a color</li>
  <li>3. Since by default, the colors will not draw in order causing issues with drawing priority and overlapping colors. You will need to create a <a href="https://en.wikipedia.org/wiki/Z-buffering" target="_blank">Z buffer</a> which stores the average of each vertice's Z axis per face</li>
  <li>4. Using a sorting algorithm like <a href="https://en.wikipedia.org/wiki/Bubble_sort" target="_blank">bubble sort</a> or whatever you prefer, sort the data inside the Z buffer so it is furthest Z distance -> closest Z distance</li>
  <li>5. Draw each face in that order with a specific color and it should work and draw colors in the correct order to prevent overlap</li>
</ul>
<p>(*) Optimization note: you could just not render the faces that aren't shown. For example, since a cube can only show 3 faces at a time, you can only make it renderer the first 3 closest faces instead of all 6 faces of the cube.</p>
<p>(*) If you need an example to go off of, I made an <a href="https://github.com/Aureliustics/Python-Turtle-3D-Renderer/blob/main/src/Geometric%20Face%20Generation.py" target="_blank">updated system</a> that does not use connection_points() and instead generates all possible unique faces (Including faces that cut through the object which makes the "X" shape on the base). You should tweak it so the algorithm ignores faces that go through the object. This will allow you to fill in the faces with color without breaking the shape.</p>
