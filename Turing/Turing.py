from sympy import solve_poly_system, Symbol, solve, Matrix, lambdify
import numpy as np
import matplotlib.pyplot as plt
import PDESolver 

def correction2(x0,y0,x1,y1,k1,k1m,k2,k22,k3,k3m,f,g):
    yr=0
    xr=0
    if (abs((f(x1,y1,k1,k1m,k22,k3,k3m)-f(x0,y0,k1,k1m,k2,k3,k3m)))<10 ** -15):
        xr=x0
    elif abs(f(x0,y0,k1,k1m,k2,k3,k3m))<abs(f(x1,y1,k1,k1m,k22,k3,k3m)):
        xr=x0-f(x0,y0,k1,k1m,k2,k3,k3m)*(x1-x0)/(f(x1,y1,k1,k1m,k22,k3,k3m)-f(x0,y0,k1,k1m,k2,k3,k3m))
    else:
        xr=x1-f(x1,y1,k1,k1m,k22,k3,k3m)*(x1-x0)/(f(x1,y1,k1,k1m,k22,k3,k3m)-f(x0,y0,k1,k1m,k2,k3,k3m))
    if (abs((g(x1,y1,k1,k1m,k22,k3,k3m)-g(x0,y0,k1,k1m,k2,k3,k3m)))<10 ** -15):
        yr=y0
    elif abs(g(x0,y0,k1,k1m,k2,k3,k3m))<abs(g(x1,y1,k1,k1m,k22,k3,k3m)):
        yr=y0-g(x0,y0,k1,k1m,k2,k3,k3m)*(y1-y0)/(g(x1,y1,k1,k1m,k22,k3,k3m)-g(x0,y0,k1,k1m,k2,k3,k3m))
    else:
        yr=y1-g(x1,y1,k1,k1m,k22,k3,k3m)*(y1-y0)/(g(x1,y1,k1,k1m,k22,k3,k3m)-g(x0,y0,k1,k1m,k2,k3,k3m))
    return xr,yr

k1 = Symbol("k1")
k2 = Symbol("k2")
k3 = Symbol("k3")
km1 = Symbol("km1")
km3 = Symbol("km3")
x = Symbol("x")
y = Symbol("y")
k1val=0.12
k1mval=0.01
k3val=0.0032
k3mval=0.002
eq1 = k1*(1 - x - 2*y) - km1*x - k3*x*(1-x-2*y)+km3*y-k2*(1-x-2*y) ** 2*x
eq2 = k3*x*(1 - x - 2*y) - km3*y
A = Matrix([eq1, eq2])
var_vector = Matrix([x, y])
jacA = A.jacobian(var_vector) 
Af=lambdify((x,y,k1,km1,k2,k3,km3),jacA)
det_jacA = jacA.det()
trace_jacA = jacA.trace()
detf=lambdify((x,y,k1,km1,k2,k3,km3),det_jacA)
trf=lambdify((x,y,k1,km1,k2,k3,km3),trace_jacA)
fx=lambdify((x,y,k1,km1,k2,k3,km3),eq1)
fy=lambdify((x,y,k1,km1,k2,k3,km3),eq2)
f=lambda v, k1, km1, k2, k3, km3: np.array([fx(v[0],v[1], k1, km1, k2, k3, km3), fy(v[0],v[1],k1, km1, k2, k3, km3)])
res = solve([eq1, eq2], y, k2)
X=np.linspace(0.001,0.999,1000)
Yf=lambdify((x,k1,km1,k3,km3),list(res[0])[0])
K2f=lambdify((x,k1,km1,k3,km3),list(res[0])[1])
#K2fe=(k1*(1-x-2*y)-km1*x-k3*x*(1-x-2*y)+km3*y)/((1-x-2*y) ** 2*x)
#K2fb=lambdify((x,y,k1,km1,k3,km3),K2fe)
Y=Yf(X,k1val,k1mval,k3val,k3mval)
K2=K2f(X,k1val,k1mval,k3val,k3mval)
Det=detf(X,Y,k1val,k1mval,K2,k3val,k3mval)
Trace=trf(X,Y,k1val,k1mval,K2,k3val,k3mval)
A11=Af(X,Y,k1val,k1mval,K2,k3val,k3mval)[0,0]
A22=Af(X,Y,k1val,k1mval,K2,k3val,k3mval)[1,1]
#K2b=K2fb(X,Y,0.12,0.01,0.0032,0.002)
k2t=[]
xt=[]
yt=[]
k2h=[]
xsh=[]
ysh=[]
for i in range(1,1000):
    if Trace[i-1]*Trace[i]<0:
        xb,yb=correction2(X[i-1],Y[i-1],X[i],Y[i],k1val,k1mval,K2[i-1],K2[i],k3val,k3mval,trf,trf)
        k2b=K2f(xb,k1val,k1mval,k3val,k3mval)
        k2h.append(k2b)
        xsh.append(xb)
        ysh.append(yb)
    if (A11[i-1]*A11[i]<0) or (A22[i-1]*A22[i]<0):
        xt.append(X[i])
        yt.append(Y[i])
        k2t.append(K2[i])
tempx=np.array(k2t)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(K2,Y, label="Y")
plt.plot(K2,X,color="red",label="X")
if (len(k2h)>0):
    plt.plot(k2h,ysh,'ks',label="Hopf")
    plt.plot(k2h,xsh,'ks')
if (len(k2h)>0):
    plt.plot(k2t,yt,'go',label="Sign")
    plt.plot(k2t,xt,'go')
ax.set_xlim(0.8,1.1)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(K2,A11, label="$a_{11}$")
plt.plot(K2,A22,color="red",label="$a_{22}$")
plt.plot(K2,Trace,color="green",label="Trace")
plt.plot(K2,0*K2,color="black")
ax.set_xlim(tempx.min()-0.05,tempx.max()+0.05)
ax.set_ylim(-0.05,0.05)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

D1=0.001
D2=1
D=np.array([D1, D2])
DISC=(D1*A22+D2*A11)**2-4*D1*D2*Det
KP1=((D1*A22+D2*A11)+DISC**0.5)/(2*D1*D2)
KP2=((D1*A22+D2*A11)-DISC**0.5)/(2*D1*D2)

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(KP1,K2, label="$k_2(k)$")
plt.plot(KP2,K2)
ax.set_xlim(0,25)
ax.set_ylim(0.8,1.1)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

k2val=0.92;
indoft=(np.abs(K2-k2val)).argmin()
print(X[indoft],Y[indoft])
a11=A11[indoft]
a22=A22[indoft]
KPM=np.linspace(0,6,60)
detB=Det[indoft]-(D1*a22+D2*a11)*KPM+D1*D2*KPM **2
print(Det[indoft])
traceB=Trace[indoft]-(D1+D2)*KPM
print(traceB[0])
Gamma1=0.5*(traceB+(traceB**2-4*detB)**0.5)
Gamma2=0.5*(traceB-(traceB**2-4*detB)**0.5)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(KPM,detB, label="$\Delta B(k)$")
ax.set_xlim(0,6)
#ax.set_ylim(0.8,1.1)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(KPM,Gamma1, label="$\gamma (k)$")
plt.plot(KPM,Gamma2)
plt.plot(KPM,0*KPM,'k')
ax.set_xlim(0.4,6)
ax.set_ylim(-5*10**-3,5*10**-3)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

kc=KP1[indoft]
Lmin=np.pi/kc ** 0.5
L=np.ceil(10*Lmin)
NM=KPM**0.5 * L/np.pi

fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(NM,Gamma1, label="$\gamma (n)$")
plt.plot(NM,Gamma2)
plt.plot(NM,0*NM,'k')
ax.set_xlim(1.5,11)
ax.set_ylim(-10**-3,5*10**-3)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)

phi=lambda x: ([X[indoft]+0.1*np.cos(np.pi*7*x/L),Y[indoft]+x-x])
ffin=lambda v: f(v,k1val,k1mval,k2val,k3val,k3mval)
Lt=1000000
M=100000
N=100
res=PDESolver.Solve(L,Lt,M,N,ffin,D,phi,10**-3)
Z=np.linspace(0,L,N+1)
fig = plt.figure()
ax = fig.add_subplot(121)
plt.plot(Z,res[0,M,:])
plt.plot(Z,res[0,M//2,:],label="$y_1$")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
ax2=fig.add_subplot(122)
plt.plot(Z,res[1,M,:])
plt.plot(Z,res[1,M//2,:], label="$y_2$")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.show()