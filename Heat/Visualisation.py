from OpenGL.GL import *
from OpenGL.GLUT import *
import OpenGL
from random import random
import numpy as np
import copy
import pyglet as pg
import Parser
import pywavefront
import Heat as ht

global pointcolor, N

lastx=0
lasty=0
def From_heat_to_color(Te):
    B=500
    D=500
    if Te<50:
        return [np.exp(-(Te-50)**2/B), np.exp(-(Te)**2/B),np.exp(-(Te+50)**2/B)]
    return [max(np.exp(-(Te-50)**2/B),np.exp(-(Te-100)**2/D)), np.exp(-(Te-100)**2/D),np.exp(-(Te-100)**2/D)]
def Form_Triangles(glob, locind):
    triangles=[]
    diapazon=np.zeros(len(glob)+1, dtype=np.int)
    for i in range(len(glob)):
        diapazon[i+1]=diapazon[i]+len(locind[i])
        lst=[]
        for el in locind[i]:
            triangle=np.array([glob[i][el[0]],glob[i][el[1]],glob[i][el[2]]])
            #lst.append(triangle)
            triangles.append(triangle)
        #triangles.append(lst)
    return np.array(triangles), diapazon
def MouseMotion (x, y):
    global lastx, lasty
    glMatrixMode(GL_PROJECTION)
    glTranslatef(-(x-lastx)/300,(y-lasty)/300,0)
    glMatrixMode(GL_MODELVIEW)
    lastx = x
    lasty = y
    glutPostRedisplay ()
def MouseRotate (x, y):
    global lastx, lasty, pointdata
    #glMatrixMode(GL_PROJECTION)
    glRotatef((x-lastx)/3,0,1,0)
    glRotatef((y-lasty)/3,1,0,0)
    #glMatrixMode(GL_MODELVIEW)
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
        for i in range(len(glob)):
            mas=[random(), random(), random()]
            for j in range(diapazon[i],diapazon[i+1]):
                pointcolor[j]=[mas,mas,mas]



def create_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    return shader


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);                    
    glEnableClientState(GL_VERTEX_ARRAY)            
    glEnableClientState(GL_COLOR_ARRAY)            
    glVertexPointer(3, GL_FLOAT, 0, triangles)
    for i in range(len(glob)):
        Col=From_heat_to_color(slv.T0[i])
        for j in range(diapazon[i],diapazon[i+1]):
            pointcolor[j]=[Col,Col,Col]
        slv.next_step()
        print(slv.T0)
    glColorPointer(3, GL_FLOAT, 0, pointcolor)
    glEnable(GL_DEPTH_TEST)
    glDrawArrays(GL_TRIANGLES,0,3*diapazon[len(glob)])
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
#glutPassiveMotionFunc(MouseMotion)
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
info = """
    Vendor: {0}
    Renderer: {1}
    OpenGL Version: {2}
    Shader Version: {3}
""".format(
    glGetString(GL_VENDOR),
    glGetString(GL_RENDERER),
    glGetString(GL_VERSION),
    glGetString(GL_SHADING_LANGUAGE_VERSION)
)
print(info)
name='model2bis.obj'
glob, locind = Parser.read('model2.obj')
triangles, diapazon=Form_Triangles(glob,locind)
triangles/=(2*triangles.max())
pointcolor=np.zeros((diapazon[len(glob)],3,3))
for i in range(len(glob)):
    mas=[random(), random(), random()]
    for j in range(diapazon[i],diapazon[i+1]):
        pointcolor[j]=[mas,mas,mas]
Num=len(glob)
#mas=matrix_s(glob,locind)
mas=np.loadtxt('mass.txt')
for i in range(Num):
    for j in range(i+1,Num):
        temp=(mas[i,j]+mas[j,i])/2
        mas[i,j]=temp
        mas[j,i]=temp

lambada=np.zeros((Num,Num))
lambada[0,1]=240
lambada[1,0]=240
lambada[1,3]=130
lambada[3,1]=130
lambada[2,3]=118
lambada[3,2]=118
lambada[2,4]=10.5
lambada[4,2]=10.5

C=np.zeros(Num)
C[0]=900
C[1]=900
C[2]=1930
C[3]=520
C[4]=520


Eps=np.zeros(Num)
Eps[0]=0.1
Eps[1]=0.1
Eps[2]=0.02
Eps[3]=0.05
Eps[4]=0.05


Q_R=[]
for i in range(Num):
    f=lambda t: [0]
    Q_R.append(f)
A=1
Q_R[4]=lambda t:[A*(20+3*np.sin(t/4))]
tau=10**2
slv=ht.HeatSolver(lambada,Q_R,C,Eps,mas,tau)
print(From_heat_to_color(75))
glutMainLoop()

