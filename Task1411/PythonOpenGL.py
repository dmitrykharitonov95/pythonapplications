from OpenGL.GL import *
from OpenGL.GLUT import *
import OpenGL
from random import random
import numpy as np
import pyglet as pg

import pywavefront

global pointcolor, N

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
        for i in range(0,N//2):
            mas=[random(), random(), random()]
            pointcolor[2*i]=[mas, mas, mas]
            pointcolor[2*i+1]=pointcolor[2*i]



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
    glDrawArrays(GL_TRIANGLES,0,3*N)
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
name='earth.obj'
meshes = pywavefront.Wavefront(name)
ps=pywavefront.ObjParser(meshes,name)
ps.read_file(name)
pointdata2=ps.material.vertices
N=len(pointdata2)//24
pointdata=np.zeros((N,3,3))
pointcolor=np.zeros((N,3,3))
for i in range(0,N):
    for j in range(0,3):
        pointdata[i,j,0:3]=pointdata2[24*i+8*j+5:24*i+8*j+8]
pointdata/=pointdata.max()
for i in range(0,N//2):
    mas=[random(), random(), random()]
    pointcolor[2*i]=[mas, mas, mas]
    pointcolor[2*i+1]=pointcolor[2*i]
glutMainLoop()
