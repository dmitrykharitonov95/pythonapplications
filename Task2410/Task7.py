import scipy.integrate 
import numpy as np
import numpy.linalg as nlg
import copy
import matplotlib.pyplot as plt
from threading import *
import threading
import time

def f(y,t,lstm):
    G=6.67 * 10 ** (-11)
    N=int(len(y)/6)
    mas=np.zeros(6*N)
    for i in range(0,N):
        mas[6*i:6*i+3]=y[6*i+3:6*i+6]
        for j in range(0,N):
            if i!=j:
                mas[6*i+3:6*i+6]+=G*lstm[j]*(y[6*j:6*j+3]-y[6*i:6*i+3])/nlg.norm(y[6*j:6*j+3]-y[6*i:6*i+3],2) ** 3
    return mas


def calc1(lst,lst2,a,tau,j):
    lst2[j,0:3]=lst[j,0:3]+lst[j,3:6]*tau+0.5*a*tau**2
def calc2(lst,lst2,a,b,tau,j):
    lst2[j,3:6]=lst[j,3:6]+0.5*(a+b)*tau
def calc3(a,lst,lstm,i):
    N=len(lst)
    G=6.67 * 10 ** (-11)
    for j in range(0,N):
        if i!=j:
            a[i]+=G*lstm[j]*(lst[j,0:3]-lst[i,0:3])/nlg.norm(lst[j,0:3]-lst[i,0:3],2) ** 3

def acceleration(lst,lstm,i):
    N=len(lst)
    if (i==-1):
        a=np.zeros((N,3))
        for i in range(0,N):
            calc3(a,lst,lstm,i)
        return a
    else:
        a=np.zeros((N,3))
        calc3(a,lst,lstm,i)
        return a[i]
def calc(res,lst,lst2,lstm,tau,j,M,evs,e):
    N=len(lst)
    a=acceleration(lst,lstm,j)
    for i in range(1,M):
        lst2[j]=np.zeros(6)
        calc1(lst,lst2,a,tau,j)
        evs[j].set()
        e.wait()
        e.clear()
        b=acceleration(lst2,lstm,j)
        calc2(lst,lst2,a,b,tau,j)
        lst[j]=copy.copy(lst2[j])
        a=copy.copy(b)
        res[i,j]=copy.copy(lst[j])
        evs[j].set()
        e.wait()
        e.clear()
def bosswork(M,N,evs,e):
    for i in range(1,M):
        #time.sleep(10 ** -8 *M)
        for ev in evs:
            ev.wait()
            ev.clear()
        e.set()
        for ev in evs:
            ev.wait()
            ev.clear()
        e.set()
def verlet(lst, lstm, M, T, type):
    tau=T/M
    N=len(lst)
    res=np.zeros((M,N,6))
    res[0]=copy.copy(lst)
    if type=="verlet":
        a=acceleration(lst,lstm,-1)
        for i in range(1,M):
            lst2=np.zeros((N,6))
            for j in range(0,N):
                calc1(lst,lst2,a[j],tau,j)
            b=acceleration(lst2,lstm,-1)
            for j in range(0,N):
                calc2(lst,lst2,a[j],b[j],tau,j)
            lst=copy.copy(lst2)
            a=copy.copy(b)
            res[i]=copy.copy(lst)
    elif type=="verlet-threading":
        e=threading.Event()
        lst2=np.zeros((N,6))
        evs=[]
        for j in range(0,N):
            ev=threading.Event()
            evs.append(ev)
        boss=Thread(target=bosswork,name="boss",args=(M,N,evs,e))
        boss.start()
        for j in range(0,N):
            tn=Thread(target=calc,name="thread"+str(j),args=(res,lst,lst2,lstm,tau,j,M,evs,e))
            tn.start()
        boss.join()
    elif type=="scipy":
        t=np.linspace(0,T,M)
        res2=scipy.integrate.odeint(f,lst.reshape((6*N)),t,args=(lstm,))
        res=res2.reshape((M,N,6))
    return res

def sunandco(type="verlet"):
    a=np.zeros(6)
    b=np.zeros(6)
    c=np.zeros(6)
    d=np.zeros(6)
    a[0]=-1.496*10 ** 11
    a[1]=-384467000
    a[3]=1022
    a[4]=-29.783*10 **3
    b[0]=-1.496*10 ** 11
    b[4]=-29.783*10 **3
    d[0]=9.5*1.496*10 ** 11
    d[4]=9690
    #a[0]=1
    #a[4]=1
    #lst=[]
    #lst.append(a)
    #lst.append(b)
    lst=np.zeros((4,6))
    lst[0,:]=a
    lst[1,:]=b
    lst[2,:]=c
    lst[3,:]=d
    t=time.time()
    lstm=[7.3 * 10 ** 22, 6*10 ** 24, 2* 10 **30, 5.6846*10 ** 26]
    #lstm=[1, 1*10 ** 11]
    res = verlet(lst,lstm, 29*1200, 29*365.025*24*3600, type)
    #res=verlet(lst,lstm,10000,1,"verlet-threading")
    print(time.time()-t)
    N=len(res)
    print(N)
    x1=res[:,0,0]
    y1=res[:,0,1]
    x2=res[:,1,0]
    y2=res[:,1,1]
    x3=res[:,2,0]
    y3=res[:,2,1]
    x4=res[:,3,0]
    y4=res[:,3,1]
    #plt.plot(x1,y1)
    #plt.plot(x2,y2,color="red")
    #plt.plot(x3,y3,color="yellow")
    #plt.plot(x4,y4, color="pink")
    #plt.show()
    return res

#sunandco("verlet")