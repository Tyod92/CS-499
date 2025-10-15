# CS-499

Self Assesment

Throughout my time in the computer science program, I’ve worked on a range of projects that helped me build both technical skills and a better understanding of real world software development. I’ve had the chance to work with databases, create full stack applications, and build visual tools using OpenGL all of which helped shape my approach to coding, testing, and problem solving.

One of my main projects was a client/server dashboard using Python, Dash, and MongoDB. It connected a live database to a web interface that allowed users to filter animal shelter data, view charts, and map locations. I wrote the backend CRUD logic, used regex filtering, and built out the UI to be clean and functional. It gave me experience handling data, writing modular code, and thinking through how a user might interact with the system.

Another project involved building a 3D graphics scene in OpenGL. This helped me better understand how transformations, buffers, and rendering pipelines work. I had to pay attention to how data moves through the graphics pipeline and how small changes in math or structure can break rendering entirely. It was a different kind of challenge but just as valuable.

Along the way, I also worked on team based assignments, wrote documentation, and learned how to explain technical decisions clearly. I kept security in mind, validating input and writing code that wouldn’t break under unexpected conditions. These are all things that come up in real software development, not just coursework.

The artifacts in this portfolio reflect different areas of my skill set data handling, graphics, software engineering, and communication. Taken together, they show that I can design, build, and troubleshoot systems with a practical mindset.

 Artifact 1

The first artifact that I improved is from CS 330. It is a C++ OpenGL project created around 4 months ago. I wanted to include it because it is a good show of C++ proficiency, being reasonably complex and involving multiple files in the project. This showed ability in graphics and general C++ coding, including being able to work with vertices and normals in OpenGL. Moreover, there were very clear issues with the project that I wanted to improve on. Notably, I wanted to fix the rendering of the Rubix Cube object in the scene, and also wanted to change how the tapered cylinder object was coded, so the user could choose the radius of the top and bottom of the cylinder, effectively being able to set how much the object taperes. 

I completed both of these objectives successfully, being able to fix the issue causing the Rubix Cube to not render properly, and recoding the cylinder to behave appropriately. Getting the Rubix Cube to render was surprisingly difficult, as I had never been that involved in OpenGL. In the end, I had to completely rewrite the “normals” of the cube, which is the vector that sets the way the surface is facing. The cylinder was a bit more challenging, involving trigonometry and manipulating vertex vectors to make the shape appear properly.  

 Artifact 2

This milestone was centered on getting the second artifact running on a local machine and not a virtual environment. To accomplish this, there were a number of things needed. Firstly, MongoDB and MongoShell were installed. Afterwards, a fake dataset matching the expected format of the data was generated for testing. Jupyter Notebook was also installed. A MongoDB server was set up, and an account matching what was expected in the code was created. Afterward, numerous changes to the code had to be made, mostly in dealing with the account authentication, and updating some of the plugins. There were now numerous errors, but that is not from the database implementation, it has to do with how the data structures are laid out, and will be dealt with in the next milestone. This milestone focused on the completion of the Database part of the needed categories.

 Artifact 3

This milestone was centered on removing the errors from the second artifact, and implementing Add, Edit and Delete entry buttons in the project. Unfortunately for me, upon investigating the errors, along with how to implement the CRUD utilities, it became clear to me that most of the project was better off being wholly rewritten. The type filters were redone entirely, to facilitate the easy addition of future types. The pie chart was re written to solve a bug involving display issues when there were too many entries in the database. The map portion was re written to fix errors in the code. Furthermore, additional callbacks were added to interface fully with the existing CRUD code as well, manifesting for now as two text boxes and three buttons. 
