from sympy import solve_poly_system, Symbol, solve, Matrix, lambdify
import numpy as np
import matplotlib.pyplot as plt

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
k3mval=0.004
eq1 = k1*(1 - x - 2*y) - km1*x - k3*x*(1-x-2*y)+km3*y-k2*(1-x-2*y) ** 2*x
eq2 = k3*x*(1 - x - 2*y) - km3*y
A = Matrix([eq1, eq2])
var_vector = Matrix([x, y])
jacA = A.jacobian(var_vector) 
det_jacA = jacA.det()
trace_jacA = jacA.trace()
detf=lambdify((x,y,k1,km1,k2,k3,km3),det_jacA)
trf=lambdify((x,y,k1,km1,k2,k3,km3),trace_jacA)
fx=lambdify((x,y,k1,km1,k2,k3,km3),eq1)
fy=lambdify((x,y,k1,km1,k2,k3,km3),eq2)
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
#K2b=K2fb(X,Y,0.12,0.01,0.0032,0.002)
k2sn=[]
xsn=[]
ysn=[]
k2h=[]
xsh=[]
ysh=[]
for i in range(1,1000):
    if Det[i-1]*Det[i]<0:
        xb,yb=correction2(X[i-1],Y[i-1],X[i],Y[i],k1val,k1mval,K2[i-1],K2[i],k3val,k3mval,detf,detf)
        k2b=K2f(xb,k1val,k1mval,k3val,k3mval)
        k2sn.append(k2b)
        xsn.append(xb)
        ysn.append(yb)
    if Trace[i-1]*Trace[i]<0:
        xb,yb=correction2(X[i-1],Y[i-1],X[i],Y[i],k1val,k1mval,K2[i-1],K2[i],k3val,k3mval,trf,trf)
        k2b=K2f(xb,k1val,k1mval,k3val,k3mval)
        k2h.append(k2b)
        xsh.append(xb)
        ysh.append(yb)
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(K2,Y, label="Y")
plt.plot(K2,X,color="red",label="X")
if (len(k2sn)>0):
    plt.plot(k2sn,ysn,'go',label="Sadle-Node")
    plt.plot(k2sn,xsn,'go')
if (len(k2h)>0):
    plt.plot(k2h,ysh,'ks',label="Hopf")
    plt.plot(k2h,xsh,'ks')
ax.set_xlim(0,5)
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.show()