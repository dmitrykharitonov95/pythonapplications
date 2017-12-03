import Task7
import numpy as np
import numpy.linalg as nlg
import matplotlib.pyplot as plt
import random as rnd
import time
def get_solar():
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
    lst=np.zeros((3,6), dtype=np.float32)
    #lst[0,:]=a
    lst[0,:]=b
    lst[1,:]=c
    lst[2,:]=d
    t=time.time()
    lstm=np.array([6*10 ** 24, 2* 10 **30, 5.6846*10 ** 26], dtype=np.float32);
    M, T = 29*1200, 29*365.025*24*3600
    return lst, lstm, M, T
def get_particles(K):
    lst=np.zeros((K,6), dtype=np.float32)
    lstm=np.zeros(K, dtype=np.float32)
    lstm[0]=10**15
    for i in range(1,K):
        lstm[i]=abs(rnd.gauss(1,1))*10**11
        lst[i,0]=abs(rnd.gauss(1,1))*(-1)**i*10**(i/5+3)
        lst[i,4]=1*(-1)**i
    T=10*abs(lst[:,0:3]).max()/abs(lst[:,3:6]).max()
    M=10000
    return lst, lstm, M, T
def difference(type):
    lst,lstm,M,T=get_particles(10)
    t=time.time()
    res1=Task7.verlet(lst,lstm,M,T,type)
    print(time.time()-t)
    t=time.time()
    res2=Task7.verlet(lst,lstm,M,T,"verlet")
    print(time.time()-t)
    dif=abs(res1-res2).max()/abs(res1).max()
    print(dif)
    return dif
def average_time(type,N):
    t=0
    for i in range(N):
        t2=time.time()
        Task7.sunandco(type)
        t+=time.time()-t2
    return t/N

difference("verlet-opencl")
grid=[10, 20, 50, 100, 500, 1000]
f=open('res3.txt','w')
for el in grid:
    print("Number",el)
    f.write(str(el))
    f.write(" ")
    lst, lstm, M, T = get_particles(el)
    t=time.time()
    res=Task7.verlet(lst,lstm,M,T,"scipy")
    dif=(time.time()-t)/100
    print("scipy",dif)
    f.write(str(dif))
    f.write(" ")
    t=time.time()
    res2=Task7.verlet(lst,lstm,M,T,"verlet")
    dif=time.time()-t
    print("verlet",dif)
    f.write(str(dif))
    f.write(" ")
    t=time.time()
    res=Task7.verlet(lst,lstm,M,T,"verlet-threading")
    dif=time.time()-t
    print("verlet-threading",dif)
    f.write(str(dif))
    f.write(" ")
    t=time.time()
    res=Task7.verlet(lst,lstm,M,T,"verlet-cython1")
    dif=time.time()-t
    print("verlet-cython",dif)
    f.write(str(dif))
    f.write(" ")
    t=time.time()
    res=Task7.verlet(lst,lstm,M,T,"verlet-cython2")
    dif=time.time()-t
    print("verlet-cython2",dif)
    f.write(str(dif))
    f.write(" ")
    t=time.time()
    res=Task7.verlet(lst,lstm,M,T,"verlet-opencl")
    dif=time.time()-t
    print("verlet-opencl",dif)
    f.write(str(dif))
    f.write("\n")
mas=np.loadtxt("res0.txt")
lab=["scipy","verlet","verlet-threading","verlet-cython1","verlet-cython2","verlet-opencl"]
for i in range(1,7):
    plt.plot(mas[:,0],mas[:,i], label=lab[i-1])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.xlabel("Number of points")
plt.ylabel("Time")
plt.show()
for i in range(2,7):
    plt.plot(mas[:,0],mas[:,3]/mas[:,i], label=lab[i-1])
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.xlabel("Number of points")
plt.ylabel("Acceleration")
plt.show()