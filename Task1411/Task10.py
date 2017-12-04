from OpenGL.GL import *
from OpenGL.GLUT import *
import OpenGL
from random import random
import numpy as np
global pointcolor

lastx=0
lasty=0

def MouseMotion (x, y):
    global lastx, lasty
    glTranslatef(-(x-lastx)/300,(y-lasty)/300,0)
    lastx = x
    lasty = y
    glutPostRedisplay ()
def MouseRotate (x, y):
    global lastx, lasty, pointdata
    glRotatef((x-lastx)/3,0,1,0)
    glRotatef((y-lasty)/3,1,0,0)
    lastx = x
    lasty = y
    glutPostRedisplay ()
def specialkeys(key, x, y):
    global pointcolor
    if key == GLUT_KEY_UP:          
        glRotatef(5, 1, 0, 0)      
    if key == GLUT_KEY_DOWN:        
        glRotatef(-5, 1, 0, 0)      
    if key == GLUT_KEY_LEFT:        
        glRotatef(5, 0, 1, 0)       
    if key == GLUT_KEY_RIGHT:       
        glRotatef(-5, 0, 1, 0)      
    if key == GLUT_KEY_END:         
        pointcolor = [[random(), random(), random()], [random(), random(), random()], [random(), random(), random()]]


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);                    
    glEnableClientState(GL_VERTEX_ARRAY)            
    glEnableClientState(GL_COLOR_ARRAY)             
    glVertexPointer(3, GL_FLOAT, 0, pointdata)
    glColorPointer(3, GL_FLOAT, 0, pointcolor)
    glEnable(GL_DEPTH_TEST)
    glDrawArrays(GL_TRIANGLES,0,180)
    glDisableClientState(GL_VERTEX_ARRAY)           
    glDisableClientState(GL_COLOR_ARRAY)            
    glutSwapBuffers()                               


glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(300, 300)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"Shaders!")
glutDisplayFunc(draw)
glutIdleFunc(draw)
glutSpecialFunc(specialkeys)
glutPassiveMotionFunc(MouseMotion)
glutMotionFunc(MouseRotate)
glClearColor(0.2, 0.2, 0.2, 1)

vertex = create_shader(GL_VERTEX_SHADER, """
varying vec4 vertex_color;
            void main(){
                gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
                vertex_color = gl_Color;
            }""")
fragment = create_shader(GL_FRAGMENT_SHADER, """
varying vec4 vertex_color;
            void main() {
                gl_FragColor = vertex_color;
}""")
program = glCreateProgram()
glAttachShader(program, vertex)
glAttachShader(program, fragment)
glLinkProgram(program)
glUseProgram(program)

pointdata=np.zeros((60,3,3))
pointcolor=np.zeros((60,3,3))
pointdata[0]=[[-0.25,-0.25,-0.25],[-0.25, 0.25, -0.25], [0.25, 0.25, -0.25]]
pointdata[1]=[[-0.25, -0.25, -0.25], [0.25, -0.25, -0.25], [0.25,0.25,-0.25]]
pointdata[2]=[[-0.25, -0.25, 0.25], [0.25, -0.25, 0.25], [0.25,0.25,0.25]]
pointdata[3]=[[-0.25, -0.25, 0.25], [-0.25, 0.25, 0.25], [0.25,0.25,0.25]]
pointdata[4]=[[-0.25, -0.25, 0.25], [-0.25, -0.25, -0.25], [-0.25,0.25,-0.25]]
pointdata[5]=[[-0.25, -0.25, 0.25], [-0.25, 0.25, -0.25], [-0.25,0.25,0.25]]
pointdata[6]=[[0.25, -0.25, 0.25], [0.25, -0.25, -0.25], [0.25,0.25,-0.25]]
pointdata[7]=[[0.25, -0.25, 0.25], [0.25, 0.25, -0.25], [0.25,0.25,0.25]]
pointdata[8]=[[-0.25, -0.25, 0.25], [0.25, -0.25, -0.25], [0.25,-0.25,0.25]]
pointdata[9]=[[-0.25, -0.25, 0.25], [0.25, -0.25, -0.25], [-0.25,-0.25,-0.25]]
pointdata[10]=[[-0.25, 0.25, 0.25], [0.25, 0.25, -0.25], [0.25,0.25,0.25]]
pointdata[11]=[[-0.25, 0.25, 0.25], [0.25, 0.25, -0.25], [-0.25,0.25,-0.25]]
for i in range(12,36):
    pointdata[i]=[[0,0.5,0],[0.25*np.cos(2*np.pi*(i-12)/24),0.5,0.25*np.sin(2*np.pi*(i-12)/24)],
                  [0.25*np.cos(2*np.pi*(i-11)/24),0.5,0.25*np.sin(2*np.pi*(i-11)/24)]]
for i in range(36,60):
    pointdata[i]=[[0,0.75,0],[0.25*np.cos(2*np.pi*(i-12)/24),0.5,0.25*np.sin(2*np.pi*(i-12)/24)],
                  [0.25*np.cos(2*np.pi*(i-11)/24),0.5,0.25*np.sin(2*np.pi*(i-11)/24)]]
print(pointdata)
for i in range(0,8):
    pointcolor[i]=[[1, 1, 0], [1, 1, 0], [1, 1, 0]]
for i in range(8,10):
    pointcolor[i]=[[0, 1, 0], [0, 1, 0], [0, 1, 0]]
for i in range(10,36):
    pointcolor[i]=[[1, 0, 0], [1, 0, 0], [1, 0, 0]]
for i in range(36,60):
    pointcolor[i]=[[1, 1, 0], [1, 1, 0], [1, 1, 0]]
glutMainLoop()
