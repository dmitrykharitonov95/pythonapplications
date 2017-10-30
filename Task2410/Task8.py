import tkinter
from tkinter import messagebox, filedialog
import numpy as np
import matplotlib as mpb
import xml.etree.cElementTree as ET
from xml.dom import minidom
import lxml.etree
import lxml.builder   

#from tkinter import *
from tkinter import Tk, Button, Label, Scale, Entry, colorchooser, ttk, Radiobutton
#from matplotlib import *
from matplotlib.backends import backend_tkagg
from matplotlib.figure import Figure
import Task7
import threading
import time

class MyCircle:
    """Class for colored circles"""
    _x=0
    _y=0
    _radius=1
    _color='#ff0000'
    def __init__(self, x,y,radius,color):
        self._x=x
        self._y=y
        self._radius=radius
        self._color=color



root = tkinter.Tk()
flt=tkinter.DoubleVar();
str1=tkinter.StringVar();
str2=tkinter.StringVar();
radio=tkinter.IntVar()
radio.set(1)
n = ttk.Notebook(root)
n.pack(fill='both', expand=True)
pages = []

child1 = ttk.Frame(root)
n.add(child1, text ='Edit')
pages.append(child1)

def act():
    global a, asize, canvas, RChooser
    asize*=1.5
    RChooser["to"]=asize
    RChooser["from_"]=asize/100
    RChooser["resolution"]=asize/100
    a.set_xlim(-asize,asize)
    a.set_ylim(-asize,asize)
    canvas.show()
    canvas.get_tk_widget().update()

def act2():
    global a, asize, canvas, RChooser
    asize/=1.5
    RChooser["to"]=asize
    RChooser["from_"]=asize/100
    RChooser["resolution"]=asize/100
    a.set_xlim(-asize,asize)
    a.set_ylim(-asize,asize)
    canvas.show()
    canvas.get_tk_widget().update()

def save_xml(filename, xml_code):
    xml_string = ET.tostring(xml_code).decode()
 
    xml_prettyxml = minidom.parseString(xml_string).toprettyxml()
    with open(filename, 'w') as xml_file:
        xml_file.write(xml_prettyxml)

def createXML(filename, lst):
    """
    Создаем XML файл.
    """
    root = ET.Element("root")
    i=0;
    for el in lst:
        name="circle"+str(i)
        i+=1
        doc = ET.SubElement(root, name)
        ET.SubElement(doc, "x").text = str(el._x)
        ET.SubElement(doc, "y").text = str(el._y)
        ET.SubElement(doc, "radius").text = str(el._radius)
        ET.SubElement(doc, "color").text = str(el._color)
    tree = ET.ElementTree(root)
    save_xml(filename, root)
def onMouseEvent(event):
    global Xcoor, Ycoor
    if (isinstance(event.xdata,float) and isinstance(event.ydata,float)):
        Xcoor['text']=event.xdata
        Ycoor['text']=event.ydata
    else:
        Xcoor['text']=0
        Ycoor['text']=0
def onMouseClick(event):
    global f, colortype, canvas, lst
    circle=MyCircle(event.xdata, event.ydata, flt.get(), colortype[1])
    lst.append(circle)
    crcl=mpb.patches.Circle((event.xdata, event.ydata), radius=flt.get(), fill=True, color=colortype[1])
    f.gca().add_patch(crcl)
    canvas.show()
    canvas.get_tk_widget().update()
def recoord(x,y,asize,t):
    if (x<0):
        f1,f2=recoord(-x,y,asize,t)
        return -f1,f2
    elif (y<0):
        f1,f2=recoord(x,-y,asize,t)
        return f1,-f2
    else:
        lst=[(1.496*10 ** 11) **2, 1.496*10 ** 11, (9.5*1.496*10 ** 11) **2, 9.5*1.496*10 ** 11]
        A=np.array(lst, dtype=float).reshape((2,2))
        B=np.array([asize/t,asize])
        c=np.linalg.solve(A,B)
        f1=c[0]*x**2+c[1]*x
        f2=c[0]*y**2+c[1]*y
    return f1,f2
def Coord(lst,t, asize):
    N=len(lst)
    arr=np.zeros((N,6))
    lstm=[0]*N
    me=asize/50
    ms=asize/20
    msun=asize/10
    A=np.array([[me**3,me**2,me], [ms**3,ms**2,ms], [msun**3,msun**2,msun]], dtype=float)
    b=np.array([6, 5.6846*10 ** 2, 2* 10 **6])
    c=np.linalg.solve(A,b)
    for i in range(0,N):
        lstm[i]=(c[0]*(lst[i]._radius)**3+c[1]*lst[i]._radius**2+c[2]*lst[i]._radius)*10 **24
    print(lstm)
    A=np.array([[(asize/t)**2,asize/t], [asize**2,asize]], dtype=float)
    b=np.array([1.496*10 ** 11, 9.5*1.496*10 ** 11])
    c=np.linalg.solve(A,b)
    ns=np.array(lstm).argmax()
    arr[ns,0]=c[0]*lst[ns]._x**2+c[1]*lst[ns]._x
    arr[ns,1]=c[0]*lst[ns]._y**2+c[1]*lst[ns]._y
    for i in range(0,N):
        if i!=ns:
            arr[i,0]=c[0]*lst[i]._x**2+c[1]*lst[i]._x-arr[ns,0]
            arr[i,1]=c[0]*lst[i]._y**2+c[1]*lst[i]._y-arr[ns,1]
    arr[ns,0]=0
    arr[ns,1]=0
    A=np.array([[1.496*10 ** 11,1], [9.5*1.496*10 ** 11,1]], dtype=float)
    b=np.array([1/(29.783*10 **3), 1/9690])
    c=np.linalg.solve(A,b)
    for i in range(0,N):
        if i!=ns:
            r=np.linalg.norm(arr[i,0:3],2)
            v=1.0/(c[0]*r+c[1])
            arr[i,3]=-v*arr[i,1]/r
            arr[i,4]=v*arr[i,0]/r
    return arr, lstm

def Evaluate():
    global f2, canvas2, asize, a2, lst
    arr, lstm = Coord(lst,7,asize)
    if radio.get()==1:
        res=Task7.verlet(arr,lstm, 29*1200, 29*365.025*24*3600,"scipy")
    elif radio.get()==2:
        res=Task7.verlet(arr,lstm, 29*1200, 29*365.025*24*3600,"verlet")
    elif radio.get()==3:
        res=Task7.verlet(arr,lstm, 29*1200, 29*365.025*24*3600,"verlet-threading")
    N=600
    M=len(lst)
    L=int(len(res)/N)
    for i in range(1,N):
        #print(i)
        f2.clf()
        a2 = f2.add_subplot(111)
        a2.set_xlim(-asize,asize)
        a2.set_ylim(-asize,asize)
        for j in range(0,M):
            x,y=recoord(res[i*L][j][0],res[i*L][j][1],asize,7)
            crcl=mpb.patches.Circle((x,y), radius=lst[j]._radius, fill=True, color=lst[j]._color)
            f2.gca().add_patch(crcl)
            ##crcl=mpb.patches.Circle((res[(i-1)*L][1][0]*2*asize/(3*10 **11)-asize,res[(i-1)*L][1][1]*2*asize/(3*10 **11)), radius=2, fill=True, color="white")
            ##f2.gca().add_patch(crcl)
            ##crcl=mpb.patches.Circle((res[(i-1)*L][2][0]*2*asize/(3*10 **11)-asize,res[(i-1)*L][2][1]*2*asize/(3*10 **11)), radius=10, fill=True, color="white")
            ##f2.gca().add_patch(crcl)
            #x,y=recoord(res[i*L][2][0],res[i*L][2][1],asize,7)
            #crcl=mpb.patches.Circle((x,y), radius=10, fill=True, color="yellow")
            #f2.gca().add_patch(crcl)
            #x,y=recoord(res[i*L][3][0],res[i*L][3][1],asize,7)
            ##print(x,y)
            #crcl=mpb.patches.Circle((x,y), radius=5, fill=True, color="#ffe375")
            #f2.gca().add_patch(crcl)
        canvas2.show()
        canvas2.get_tk_widget().update()
        #time.sleep(0.01)
def ChooseColor():
    global colortype
    colortype=colorchooser.askcolor()

def BSave():
    global lst
    savestr=filedialog.asksaveasfile()
    if (savestr):
        createXML(savestr.name,lst)

def BLoad():
    global f, lst, canvas, a 
    lst=[]
    lst1=[]
    lst2=[]
    lst3=[]
    lst4=[]
    try:
        loadstr=filedialog.askopenfile()
        tree=ET.parse(loadstr.name)
        f.clf()
        a = f.add_subplot(111)
        a.set_xlim(-asize,asize)
        a.set_ylim(-asize,asize)
        root=tree.getroot()
        for elem in root.iter("x"):
            lst1.append(elem.text)
        for elem in root.iter("y"):
            lst2.append(elem.text)
        for elem in root.iter("radius"):
            lst3.append(elem.text)
        for elem in root.iter("color"):
            lst4.append(elem.text)
        for i in range(0,len(lst1)):
            circle=MyCircle(float(lst1[i]), float(lst2[i]), float(lst3[i]), lst4[i])
            lst.append(circle)
            crcl=mpb.patches.Circle((circle._x, circle._y), circle._radius, fill=True, color=lst4[i])
            f.gca().add_patch(crcl)
        canvas.show()
        canvas.get_tk_widget().update()
    except(Exception):
        messagebox.showerror("Oh no", "Your file is invalid")

foo = Button(child1,text="+", command=act)
foo.grid(row=2, column=1)
foo2 = Button(child1,text="-", command=act2)
foo2.grid(row=2, column=2)
lst=[]
asize=100.0;
colortype=((255, 0.0, 0.0), '#ff0000')
f = Figure(figsize=(5, 4), dpi=100)
a = f.add_subplot(111)
a.set_xlim(-asize,asize)
a.set_ylim(-asize,asize)
canvas = backend_tkagg.FigureCanvasTkAgg(f, master=child1)
canvas.show()
canvas.get_tk_widget().grid(row=1, column=1)

button_press_event_id = f.canvas.mpl_connect('motion_notify_event', onMouseEvent)
button_press_event_id2 = f.canvas.mpl_connect('button_press_event', onMouseClick)
Xtext=Label(child1,text="X")
Xtext.grid(row=3, column=1)
Xcoor = Label(child1)
Xcoor.grid(row=3, column=2)

Ytext=Label(child1,text="Y")
Ytext.grid(row=4, column=1)
Ycoor = Label(child1)
Ycoor.grid(row=4, column=2)

Butcolor=Button(child1,text="ChooseColor",command=ChooseColor)
Butcolor.grid(row=5, column=1)

RChooser=Scale(child1,from_=1.0, to=asize, orient='horizontal', variable=flt, resolution=asize/100, showvalue=0)
RChooser.grid(row=5, column=2)

RText=Entry(child1, textvariable=flt)
RText.grid(row=5, column=3)

ButSave=Button(child1,text="Save",command=BSave)
ButSave.grid(row=6, column=1)

ButLoad=Button(child1,text="Load",command=BLoad)
ButLoad.grid(row=6, column=2)
#str2.set("third.xml")

child2 = ttk.Frame(root)
n.add(child2, text ='Model')
pages.append(child2)  

Radio1=Radiobutton(child2, text="scipy", value=1, variable=radio)
Radio1.grid(row=1, column=1)
Radio2=Radiobutton(child2, text="verlet", value=2, variable=radio)
Radio2.grid(row=2, column=1)
Radio3=Radiobutton(child2, text="verlet-threading", value=3, variable=radio)
Radio3.grid(row=3, column=1)
Radio4=Radiobutton(child2, text="verlet-multiprocessing", value=4, variable=radio)
Radio4.grid(row=4, column=1)
Radio5=Radiobutton(child2, text="verlet-cython", value=5, variable=radio)
Radio5.grid(row=5, column=1)
Radio5=Radiobutton(child2, text="verlet-opencl", value=6, variable=radio)
Radio5.grid(row=6, column=1)

f2 = Figure(figsize=(5, 4), dpi=100)
a2 = f2.add_subplot(111)
a2.set_xlim(-asize,asize)
a2.set_ylim(-asize,asize)
canvas2 = backend_tkagg.FigureCanvasTkAgg(f2, master=child2)
canvas2.show()
canvas2.get_tk_widget().grid(column=2)
ButEval=Button(child2,text="Solar",command=Evaluate)
ButEval.grid(row=7, column=1)
root.mainloop()
