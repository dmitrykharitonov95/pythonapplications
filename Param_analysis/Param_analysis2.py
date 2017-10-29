from sympy import solve_poly_system, Symbol, solve, Matrix, lambdify
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate 

k1 = Symbol("k1")
k2 = Symbol("k2")
k3 = Symbol("k3")
km1 = Symbol("km1")
km3 = Symbol("km3")
x = Symbol("x")
y = Symbol("y")
k1mval=0.01
k3val=0.0032
k3mval=0.002
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
f=lambda v, t, k1, km1, k2, k3, km3: [fx(v[0],v[1], k1, km1, k2, k3, km3), fy(v[0],v[1],k1, km1, k2, k3, km3)]
res = solve([eq1, eq2, det_jacA], y, k1, k2)
res2 = solve([eq1, eq2, trace_jacA], y, k1, k2)
X=np.linspace(0.001,0.999,1000)
Yf=lambdify((x,km1,k3,km3),list(res[0])[0])
K1f=lambdify((x,km1,k3,km3),list(res[0])[1])
K2f=lambdify((x,km1,k3,km3),list(res[0])[2])
Y=Yf(X,k1mval,k3val,k3mval)
K1=K1f(X,k1mval,k3val,k3mval)
K2=K2f(X,k1mval,k3val,k3mval)

Yf2=lambdify((x,km1,k3,km3),list(res2[0])[0])
K1f2=lambdify((x,km1,k3,km3),list(res2[0])[1])
K2f2=lambdify((x,km1,k3,km3),list(res2[0])[2])
Y2=Yf2(X,k1mval,k3val,k3mval)
K12=K1f2(X,k1mval,k3val,k3mval)
K22=K2f2(X,k1mval,k3val,k3mval)

j=0
while (K22[j]<0):
    j+=1
k=0
while(K2[k]<0):
    k+=1
for i in range(0,1000):
    if detf(X[i],Y2[i],K12[i],k1mval,K22[i],k3val,k3mval)<0:
        K22[i]=-1

k1i=0.11
k2i=0.86
res=solve(eq1, y)
Yfi1=lambdify((x,k1,km1,k2,k3,km3),(res[0]))
res=solve(eq2,y)
Yfi2=lambdify((x,k1,km1,k2,k3,km3),(res[0]))
t=np.linspace(0,10 ** 4,10 ** 4)
Mas=K1[k:1000]
jC=Mas.argmin()
#k1i=K1[jC+k]
#k2i=K2[jC+k]
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(K1[k:1000],K2[k:1000], label="saddle-node line")
plt.plot(K12[j:1000],K22[j:1000],"r--", label="hopf line")
plt.plot(K1[jC+k],K2[jC+k], 'go', label="C-point")
plt.text( k1i, k2i+0.2 , '$I$' , color ='k')
plt.text( k1i, k2i-0.2 , '$I$' , color ='k')
plt.text (K1[jC+k]+0.1,K2[jC+k]+1, '$II$' , color ='k')
plt.text (k1i, k2i, '$III$' , color ='k')
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand", borderaxespad=0.)
ax.set_xlim(0,0.25)
ax.set_ylim(0,2.5)
fig = plt.figure()
ax2=fig.add_subplot(111)
res3=scipy.integrate.odeint(f,[0.1,0.25], t, args=(k1i,k1mval,k2i,k3val, k3mval))
plt.plot(res3[:,0],res3[:,1],"b",label="path")
res3=scipy.integrate.odeint(f,[0.5,0.1], t, args=(k1i,k1mval,k2i,k3val, k3mval))
plt.plot(res3[:,0],res3[:,1],"b")
res3=scipy.integrate.odeint(f,[0.5,0.16], t, args=(k1i,k1mval,k2i,k3val, k3mval))
plt.plot(res3[:,0],res3[:,1],"b")
res3=scipy.integrate.odeint(f,[0.3,0.1], t, args=(k1i,k1mval,k2i,k3val, k3mval))
Xi=np.linspace(res3[:,0].min(),res3[:,0].max())
plt.plot(res3[:,0],res3[:,1],"b")
res4=scipy.integrate.odeint(f,[0.5,0.164], t, args=(k1i,k1mval,k2i,k3val, k3mval))
plt.plot(res4[:,0],res4[:,1],"k",label="cycle")
plt.plot(Xi,Yfi1(Xi,k1i,k1mval,k2i,k3val,k3mval),"r--",label="$f_1=0$")
plt.plot(Xi,Yfi2(Xi,k1i,k1mval,k2i,k3val,k3mval),"g--",label="$f_2=0$")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
ax2.set_xlim(res3[:,0].min(),res3[:,0].max())
fig = plt.figure()
ax = fig.add_subplot(111)
plt.plot(t,res3[:,0],label="X")
plt.plot(t,res3[:,1],label="Y")
plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0.)
plt.show()


