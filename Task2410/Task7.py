import scipy.integrate 
import numpy as np
import numpy.linalg as nlg
import copy
import matplotlib.pyplot as plt
from threading import *
import threading
import time
import multiprocessing
from multiprocessing import Process, freeze_support, set_start_method, Queue, Array, Lock
import cverlet00

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

def calc1_m(lst,lst2,a,tau,j):
    r1=np.array(lst[6*j:6*j+6])
    lst2[6*j:6*j+3]=list(r1[0:3]+r1[3:6]*tau+0.5*a*tau**2)

def calc2(lst,lst2,a,b,tau,j):
    lst2[j,3:6]=lst[j,3:6]+0.5*(a+b)*tau

def calc2_m(lst,lst2,a,b,tau,j):
    r1=np.array(lst[6*j+3:6*j+6])
    lst2[6*j+3:6*j+6]=list(r1+0.5*(a+b)*tau)

def calc3(a,lst,lstm,i):
    N=len(lst)
    G=6.67 * 10 ** (-11)
    for j in range(0,N):
        if i!=j:
            a[i]+=G*lstm[j]*(lst[j,0:3]-lst[i,0:3])/nlg.norm(lst[j,0:3]-lst[i,0:3],2) ** 3

def calc3_m(a,lst,lstm,i,N):
    G=6.67 * 10 ** (-11)
    for j in range(0,N):
        if i!=j:
            r1=np.array(lst[6*j:6*j+3])
            r2=np.array(lst[6*i:6*i+3])
            a[i]+=G*lstm[j]*(r1-r2)/nlg.norm(r1-r2,2) ** 3

def acceleration2(lst, lstm):
    G=6.67 * 10 ** (-11)
    N=lst.shape[0]
    a=np.zeros([N,3])
    for i in range(0,N):
        for j in range(0,N):
            if i!=j:
                a[i]+=G*lstm[j]*(lst[j,0:3]-lst[i,0:3])/nlg.norm(lst[j,0:3]-lst[i,0:3],2) ** 3
    return a
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

def acceleration_m(lst,lstm,i,N):
    if (i==-1):
        a=np.zeros((N,3))
        for i in range(0,N):
            calc3_m(a,lst,lstm,i, N)
        return a
    else:
        a=np.zeros((N,3))
        calc3_m(a,lst,lstm,i, N)
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

def calc_m(res,lst,lst2,lstm,tau,j,M,e,e2,N):
    a=acceleration_m(lst,lstm,j,N)
    for i in range(1,M):
        lst2[6*j:6*j+6]=np.zeros(6)
        calc1_m(lst,lst2,a,tau,j)
        e2.set()
        e.wait()
        e.clear()
        #q1.put(1)
        #q1.get()
        b=acceleration_m(lst2,lstm,j,N)
        calc2_m(lst,lst2,a,b,tau,j)
        lst[6*j:6*j+6]=copy.copy(lst2[6*j:6*j+6])
        a=copy.copy(b)
        res[i*N*6+j*6:i*N*6+j*6+6]=copy.copy(lst[6*j:6*j+6])
        #q1.put(1)
        #q1.get()
        e2.set()
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
        a=acceleration2(lst,lstm)
        print(a.max())
        for i in range(1,M):
            lst2=np.zeros((N,6))
            for j in range(0,N):
                calc1(lst,lst2,a[j],tau,j)
            b=acceleration2(lst2,lstm)
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
    elif type=="verlet-multiprocessing":
        lst2=np.zeros((N,6))
        lstoproc=[]
        freeze_support()
        lock=Lock()
        A1=Array('f', res.reshape(M*N*6), lock=False)
        B1=Array('f', lst.reshape(6*N), lock=False)
        C1=Array('f', lst2.reshape(6*N), lock=False)
        lst2=np.zeros((N,6))
        evs=[]
        evs2=[]
        for j in range(0,N):
            e=multiprocessing.Event()
            e2=multiprocessing.Event()
            evs.append(e)
            evs2.append(e2)
            p = Process(target=calc_m,args=(A1,B1,C1,lstm,tau,j,M,e,e2,N))
            p.start()
            lstoproc.append(p)
        for i in range (1,M):
            for ev in evs2:
                ev.wait()
                ev.clear()
            for ev in evs:
                ev.set()
            for ev in evs2:
                ev.wait()
                ev.clear()
            for ev in evs:
                ev.set()
        for elem in lstoproc:
            elem.join()
        #boss.join()
        res=np.array(A1[:]).reshape((M,N,6))
    elif type=="verlet-cython1":
        print("YES!")
        res=cverlet00.cverlet00(lst,lstm,M,T)
        return res;
    elif type=="verlet-cython2":
        print("YES!")
        res=cverlet00.cverlet01(lst,lstm,M,T)
        return res;
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
    lst=np.zeros((4,6), dtype=np.float32)
    lst[0,:]=a
    lst[1,:]=b
    lst[2,:]=c
    lst[3,:]=d
    t=time.time()
    lstm=np.array([7.3 * 10 ** 22, 6*10 ** 24, 2* 10 **30, 5.6846*10 ** 26], dtype=np.float32);
    #lstm=[1, 1*10 ** 11]
    res = verlet(lst,lstm, 29*1200, 29*365.025*24*3600, type)
    #res=verlet(lst,lstm,1000,1,type)
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
    plt.plot(x1,y1)
    plt.plot(x2,y2,color="red")
    plt.plot(x3,y3,color="yellow")
    plt.plot(x4,y4, color="pink")
    plt.show()
    return res

if __name__ == '__main__':
    sunandco("verlet-cython")