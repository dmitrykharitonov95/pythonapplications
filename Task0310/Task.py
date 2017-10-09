import tkinter
#import numpy as np
import matplotlib as mpb
import xml.etree.cElementTree as ET
from xml.dom import minidom
import lxml.etree
import lxml.builder    
#from tkinter import *
from tkinter import Tk, Button, Label, Scale, Entry, colorchooser, ttk
#from matplotlib import *
from matplotlib.backends import backend_tkagg
from matplotlib.figure import Figure

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

def ChooseColor():
    global colortype
    colortype=colorchooser.askcolor()

def BSave():
    global lst
    createXML(str1.get(),lst)

def BLoad():
    global f, lst, canvas
    lst=[]
    lst1=[]
    lst2=[]
    lst3=[]
    lst4=[]
    tree=ET.parse(str2.get())
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
TextSave=Entry(child1, textvariable=str1)
TextSave.grid(row=6, column=2)

ButLoad=Button(child1,text="Load",command=BLoad)
ButLoad.grid(row=7, column=1)
TextLoad=Entry(child1, textvariable=str2)
TextLoad.grid(row=7, column=2)
#str2.set("third.xml")
child2 = ttk.Frame(root)
n.add(child2, text ='Model')
pages.append(child2)  

root.mainloop()
