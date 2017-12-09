import numpy as np
import numpy.linalg as nlg
import copy
import matplotlib.pyplot as plt

def ZeroF(y):
    return np.zeros(2)
def Phi(x):
    return np.cos(np.pi*x)
def Solve(Lx,Lt,M,N,f,D,phi,eps):
    A=np.zeros((2,N+1,N+1))
    b=np.zeros((2,N+1))
    res=np.zeros((2,M+1,N+1))
    cur=np.zeros((2,N+1))
    prev=np.zeros((2,N+1))
    res[:,0,:]=phi(np.linspace(0,Lx,N+1))
    tau=Lt/M
    h=Lx/N
    A[:,0,0]=1
    A[:,0,1]=-1
    A[:,N,N]=1
    A[:,N,N-1]=-1
    for i in range(1,N):
        A[:,i,i-1]=-0.5*D*tau/h**2
        A[:,i,i]=1+D*tau/h**2
        A[:,i,i+1]=-0.5*D*tau/h**2
    for i in range(1,M+1):
        print(i)
        prev=copy.copy(res[:,i-1,:])
        bo=False
        while(not bo):
            for j in range(1,N):
                b[:,j]=res[:,i-1,j]+(D*tau/(2*h**2))*(res[:,i-1,j-1]-2*res[:,i-1,j]+res[:,i-1,j+1])+f(0.5*(res[:,i-1,j]+prev[:,j]))*tau
            cur=nlg.solve(A,b)
            bo=((np.abs(cur-prev)).max()<eps*((np.abs(cur)).max()+10**-3))
            #print(np.abs(cur-prev))
            prev=copy.copy(cur)
        res[:,i,:]=copy.copy(cur)
    return res

#M=1000
#N=1000
#T=np.linspace(0,1,M+1)
#X=np.linspace(0,1,N+1)
#print(len(X))
#res=Solve(1,1,M,N,ZeroF,np.ones(2),Phi,10**-3)
#print(len(res[1,M,:]))
#plt.plot(X,res[0,M,:])
#plt.plot(X,Phi(X)*np.exp(-np.pi**2))
#plt.show()