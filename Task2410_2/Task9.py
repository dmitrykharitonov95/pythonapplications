import numpy as np
from threading import *
import threading
import time
import multiprocessing
from multiprocessing import Process, freeze_support, set_start_method, Queue, Array, Lock
import random as rnd

def multiple(A,B,C,m,n,k,i,count):
    mp=int(m/count)+1
    for ind in range(0,mp):
        if (i*mp+ind<m):
            for j in range(0,k):
                for l in range(0,n):
                    C[i*mp+ind,j]+=A[i*mp+ind,l]*B[l,j]
def multiple2(A,B,m,n,k,i,q,count):
    mp=int(m/count)+1
    for ind in range(0,mp):
        if (i*mp+ind<m):
            for j in range(0,k):
                temp=0
                for l in range(0,n):
                    temp+=A[i*mp+ind,l]*B[l,j]
                q.put([i*mp+ind,j,temp])

def multiple3(A,B,C,m,n,k,i,count):
    mp=int(m/count)+1
    for ind in range(0,mp):
        if (i*mp+ind<m):
            for j in range(0,k):
                for l in range(0,n):
                    C[k*(i*mp+ind)+j]+=A[n*(i*mp+ind)+l]*B[k*l+j]

if __name__ == '__main__':
    M=1000
    N=1000
    K=100
    A=np.zeros((M,N))
    B=np.zeros((N,K))
    C=np.zeros((M,K))
    D=np.zeros((M,K))
    count=multiprocessing.cpu_count()
    print(count)
    for i in range(0,M):
        for j in range(0,N):
            A[i,j]=rnd.randint(0,1000)
    for j in range(0,N):
        for k in range(0,K):
            B[j,k]=rnd.randint(0,1000)
    #A[0,0]=1
    #A[1,0]=3
    #A[1,1]=2
    #A[0,1]=4
    #B[0,0]=5
    #B[1,1]=10
    q=Queue()
    lst=[]
    freeze_support()
    t=time.time()
    for i in range(0,count):
        p = Process(target=multiple2,args=(A,B,M,N,K,i,q,count))
        p.start()
        lst.append(p)
    for i in range(M*K):
        temp=q.get()
        D[temp[0],temp[1]]=temp[2]
    for elem in lst:
        elem.join()
    print("Multiprocessing with queues: ",-t+time.time())
    t=time.time()
    lock=Lock()
    A1=Array('f', A.reshape(M*N))
    B1=Array('f', B.reshape(N*K))
    C1=Array('f', C.reshape(M*K))
    for i in range(0,count):
        p = Process(target=multiple3,args=(A1,B1,C1,M,N,K,i,count))
        p.start()
        lst.append(p)
    for elem in lst:
        elem.join()
    C2=np.array(C1[:]).reshape((M,K))
    print("Multiprocessing with shared memory: ",-t+time.time())
    t=time.time()
    for i in range(0,count):
        tn=Thread(target=multiple,name="thread"+str(i),args=(A,B,C,M,N,K,i,count))
        tn.start()
        lst.append(tn)
    for elem in lst:
        elem.join()
    print("Threading: ",-t+time.time())
    t=time.time()
    C=np.zeros((M,K))
    for i in range(0,count):
        multiple(A,B,C,M,N,K,i,count)
    print("Simple: ",-t+time.time())
    
