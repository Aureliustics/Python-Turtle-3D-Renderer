<h1>Python Turtle 3D Renderer</h1>
<h3>Renders a 3D object to the screen by using projection matrix and vertices. Made this as a fun project for school so don't expect the code quality to be good.</h3>

<h1>Usage</h1>
<ul>
  <li>Must be ran in a <a href="https://codehs.com/" target="_blank">CodeHS</a> sandbox</li>
  <li>Once logged into Codehs, click "Sandbox" in the navigation bar</li>
  <li>Click "Create Program" then select "Python (turtle)" and create program</li>
  <li>Copy and paste the code from either the square example or triangle example into your sandbox then run</li>
  <li>Interact with the object using WASD and arrow keys. WASD moves the camera position and arrow keys changes the rotation of the object</li>
</ul>

<h1>Modify Object</h1>
<ul>
  <li>Create a shape using vertices on this <a href="https://technology.cpm.org/general/3dgraph/" target="_blank">site</a></li>
  <li>Once you have an object, put in the matrix values on line 42 (make sure to change the value of range to the amount of vertices you made)</li>
  <li>Understand that the value of the vertex will be like this: Point[0] for example is the X position of the first vertex, Points[1] is the Y position of the first vertex</li>
  <li>So Points[0] and Points[1] are directly linked. Knowing this we can tell that the second vertex's X and Y are Points[2] and Points[3]</li>
  <li>Now that you know this you can change the Points[] value in the setpositions in the function "connection_points()" to connect the vertices</li>
</ul>


