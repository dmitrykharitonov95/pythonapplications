import Task3
import numpy as np
import Parser
import scipy.optimize as so
import scipy.integrate as si
import copy

def huge_intersect(P1, P2, P3, P4, P5, P6):
    if Task3.intersect(P1,P2,P3,P4,P5,P6)==1:
        if abs(Task3.deter(P1,P2,P3,P4))>10**(-6):
            return False
        if abs(Task3.deter(P1,P2,P3,P5))>10**(-6):
            return False
        if abs(Task3.deter(P1,P2,P3,P6))>10**(-6):
            return False
        return True
    return False
def little_S(hx,hy):
    l1=np.linalg.norm(hx)
    l2=np.linalg.norm(hy)
    l3=np.linalg.norm(hx-hy)
    p=(l1+l2+l3)/2
    return 2*(p*(p-l1)*(p-l2)*(p-l3))**0.5
def triangle_IS(P1, P2, P3, P4, P5, P6):
    if not huge_intersect(P1,P2,P3,P4,P5,P6):
        return 0.0
    N=100
    S=0.0
    x=P3-P1
    y=P2-P1
    hx=x/N
    hy=y/N
    Sh=little_S(hx,hy)
    for i in range(N):
        for j in range(N-i):
            temp=0
            pp=[P1+i*hx+j*hy, P1+(i+1)*hx+j*hy, P1+i*hx+(j+1)*hy, P1+(i+1)*hx+(j+1)*hy]
            for P in pp:
                if Task3.internal(P4,P5,P6,P)==1:
                    temp+=0.25
            if j<N-i-1:
                S+=temp*Sh
            else:
                S+=temp*Sh/2
    return S
def triangle_S(lst,mind):
    l1=np.linalg.norm(lst[mind[0]]-lst[mind[1]])
    l2=np.linalg.norm(lst[mind[0]]-lst[mind[2]])
    l3=np.linalg.norm(lst[mind[2]]-lst[mind[1]])
    p=(l1+l2+l3)/2
    return (p*(p-l1)*(p-l2)*(p-l3))**0.5
def intersection_S(glob,locind,i,j):
    S=0
    for ind1 in locind[i]:
        for ind2 in locind[j]:
            P1=glob[i][ind1[0]]
            P2=glob[i][ind1[1]]
            P3=glob[i][ind1[2]]
            P4=glob[j][ind2[0]]
            P5=glob[j][ind2[1]]
            P6=glob[j][ind2[2]]
            S+=triangle_IS(P1,P2,P3,P4,P5,P6)
    return S
def object_S(glob,locind,i):
    S=0.0
    for el in locind[i]:
        S+=triangle_S(glob[i],el)
    return S
def matrix_s(glob,locind):
    mas_s=np.zeros((len(glob),len(glob)))
    f=open('mass.txt','w')
    for i in range(len(glob)):
        for j in range(len(glob)):
            print(i,j)
            if i==j:
                mas_s[i,j]=object_S(glob,locind,i)
            else:
                mas_s[i,j]=intersection_S(glob,locind,i,j)
            f.write(str(mas_s[i][j]))
            f.write(' ')
        f.write('\n')
    f.close()
    return mas_s
class HeatSolver:
    def __init__(self, lambada, Q_R, C, Eps, S, tau):
        self.lambada=lambada
        self.Q_R=Q_R
        self.C=C
        self.Num=len(self.C)
        self.Eps=Eps
        self.S=S
        self.counter=0
        self.T0=so.fsolve(rightright,np.zeros(self.Num),args=(0,lambada,Q_R,C,Eps,S,))
        self.T=copy.copy(self.T0)
        self.tau=tau
    def next_step(self):
        Tm=np.linspace((self.counter-1)*self.tau,self.counter*self.tau,2)
        self.counter+=1
        self.T=si.odeint(rightright,self.T0,Tm,args=(self.lambada,self.Q_R,self.C,self.Eps,self.S,))
        self.T0=copy.copy(self.T[1])
        return self.T[1]
def rightright(T,t,lambada, Q_R, C, Eps, S):
    Num=len(C)
    right=np.zeros(Num)
    C0=5.67
    for i in range(Num):
        for j in range(Num):
            if i!=j:
                right[i]-=lambada[i,j]*S[i,j]*(T[i]-T[j])
        #print(right[i])
        right[i]-=Eps[i]*S[i,i]*C0*(T[i]/100)**4
        #print(Eps[i]*S[i,i]*C0*(T[i]/100)**4)
        right[i]+=Q_R[i](t)
        right[i]/=C[i]
    return right

#glob, locind =Parser.read('model2.obj')
#Num=len(glob)
##mas=matrix_s(glob,locind)
#mas=np.loadtxt('mass.txt')
#for i in range(Num):
#    for j in range(i+1,Num):
#        temp=(mas[i,j]+mas[j,i])/2
#        mas[i,j]=temp
#        mas[j,i]=temp

#lambada=np.zeros((Num,Num))
#lambada[0,1]=240
#lambada[1,0]=240
#lambada[1,3]=130
#lambada[3,1]=130
#lambada[2,3]=118
#lambada[3,2]=118
#lambada[2,4]=10.5
#lambada[4,2]=10.5

#C=np.zeros(Num)
#C[0]=900
#C[1]=900
#C[2]=1930
#C[3]=520
#C[4]=520


#Eps=np.zeros(Num)
#Eps[0]=0.1
#Eps[1]=0.1
#Eps[2]=0.02
#Eps[3]=0.05
#Eps[4]=0.05


#Q_R=[]
#for i in range(Num):
#    f=lambda t: [0]
#    Q_R.append(f)
#A=1
#Q_R[4]=lambda t:[A*(20+3*np.sin(t/4))]


#TT=10**6
#tau=10**2
#M=int(TT/tau)
#Tm=np.linspace(0,TT,M)

#T0=so.fsolve(rightright,np.zeros(Num),args=(0,lambada,Q_R,C,Eps,mas,))
#print(T0)
##print(rightright(T0,0,lambada,Q_R,C,Eps,mas))
##T=si.odeint(rightright,T0,Tm,args=(lambada,Q_R,C,Eps,mas,))
##print(T)
#slv=HeatSolver(lambada,Q_R,C,Eps,mas,tau)
#for i in range(1,M):
#    #Tm=np.linspace((i-1)*tau,i*tau,2)
#    #T=si.odeint(rightright,T0,Tm,args=(lambada,Q_R,C,Eps,mas,))
#    T=slv.next_step()
#    #T0=copy.copy(T[1])
#    print(i*tau, T)
#    #print(rightright(T0,i*tau,lambada,Q_R,C,Eps,mas))
#print(locind[0])
#print(intersection_S(glob,locind,2,3))
#print(object_S(glob,locind,0))
#P1=np.array([0,0,0])
#P2=np.array([1,2,0])
#P3=np.array([2,0,0])
#P4=np.array([1,0,0])
#P5=np.array([2,2,0])
#P6=np.array([3,0,0])
#print(intersection_S(P1,P2,P3,P4,P5,P6))
