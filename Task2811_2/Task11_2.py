from __future__ import absolute_import
from __future__ import print_function
# example by Roger Pau Monn'e
import pyopencl as cl
import numpy as np
import matplotlib.pyplot as plt
import time
N=np.array(4)
M=np.array(29*1200)
T=np.array(29*365.025*24*3600)
demo_r = np.empty( (N,5), dtype=np.uint32)
demo_r2= np.empty( (N,5), dtype=np.float32)
ctx = cl.create_some_context()
queue = cl.CommandQueue(ctx)
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
lst=np.zeros((4,6), dtype=np.float32)
lst2=np.zeros((4,6), dtype=np.float32)
lst[0,:]=a
lst[1,:]=b
lst[2,:]=c
lst[3,:]=d
res=np.zeros((M,N,6),dtype=np.float32)
acs=np.zeros((N,3),dtype=np.float32)
bcs=np.zeros((N,3),dtype=np.float32)
lstm=np.array([7.3 * 10 ** 22, 6*10 ** 24, 2* 10 **30, 5.6846*10 ** 26], dtype=np.float32);
mf = cl.mem_flags
demo_buf = cl.Buffer(ctx, mf.WRITE_ONLY, demo_r.nbytes)
demo_buf2 = cl.Buffer(ctx, mf.WRITE_ONLY, demo_r2.nbytes)
buf=cl.Buffer(ctx, mf.READ_WRITE| mf.COPY_HOST_PTR, hostbuf=lst)
buf2=cl.Buffer(ctx, mf.READ_WRITE| mf.COPY_HOST_PTR, hostbuf=lst2)
bufa=cl.Buffer(ctx, mf.READ_WRITE| mf.COPY_HOST_PTR, hostbuf=a)
bufb=cl.Buffer(ctx, mf.READ_WRITE| mf.COPY_HOST_PTR, hostbuf=b)
bufm=cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=lstm)
bufres=cl.Buffer(ctx, mf.WRITE_ONLY, res.nbytes)
T_s=cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=T)
M_s=cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=M)
N_s=cl.Buffer(ctx, mf.READ_ONLY| mf.COPY_HOST_PTR, hostbuf=N)

prg = cl.Program(ctx,
"""
float norm(__global float *lst, int i, int j)
{
    double temp=0;
    for (int k=0; k<3; ++k)
        temp+=(lst[6*i+k]-lst[6*j+k])*(lst[6*i+k]-lst[6*j+k]);
    return sqrt(temp);
}
void acceleration(__global float *lst, __global float *lstm,__global float *a, int N, int i)
{
    double G=6.67 * pow(10.0,-11);
    //for (int i=0; i<N; ++i)
    //{
    for (int k=0; k<3; ++k)
        a[3*i+k]=0;
    for (int j=0; j<N; ++j)
        if (i!=j)
            for (int k=0; k<3; ++k)
                a[3*i+k]+=G*lstm[j]*(lst[6*j+k]-lst[6*i+k])/pow(norm(lst,i,j),3);
    //}
}
__kernel void verlet_cl(__global float *lst, __global float *lstm, __global float *res, __global double *T_s, __global int *M_s, __global int *N_s, __global float *a, __global float *b, __global float *lst2)
{
    int j = get_global_id(0);
    double T=*T_s;
    int M=*M_s;
    int N=*N_s;
    double tau=T/M;
    //float *a=new float[3*N];
    //float *b=new float[3*N];
    //float *lst2=new float[6*N];
    acceleration(lst,lstm,a, N, j);
    //for (int j=0; j<N; ++j)
    for (int k=0; k<6; ++k)
        res[6*j+k]=lst[6*j+k];
    for (int i=1; i<M; ++i)
    {
        //for (int j=0; j<N; ++j)
        for (int k=0; k<3; ++k)
            lst2[6*j+k]=lst[6*j+k]+lst[6*j+k+3]*tau+0.5*a[3*j+k]*tau*tau;
        //barrier(CLK_GLOBAL_MEM_FENCE);
        acceleration(lst2,lstm,b,N, j);
        //for (int j=0; j<N; ++j)
        for (int k=0; k<3; ++k)
            lst2[6*j+k+3]=lst[6*j+k+3]+0.5*(a[3*j+k]+b[3*j+k])*tau;
        //for (int j=0; j<N; ++j)
        for (int k=0; k<3; ++k)
        {
            lst[6*j+k]=lst2[6*j+k];
            lst2[6*j+k]=0;
            lst[6*j+k+3]=lst2[6*j+k+3];
            lst2[6*j+k+3]=0;
            a[3*j+k]=b[3*j+k];
            res[6*N*i+6*j+k]=lst[6*j+k];
            res[6*N*i+6*j+k+3]=lst[6*j+k+3];
        }
        //barrier(CLK_GLOBAL_MEM_FENCE);
    }
}""")

try:
    prg.build()
except:
    print("Error:")
    print(prg.get_build_info(ctx.devices[0], cl.program_build_info.LOG))
    raise
t=time.time()
prg.verlet_cl(queue, (N,), None, buf, bufm, bufres, T_s, M_s, N_s, bufa, bufb, buf2)
cl.enqueue_read_buffer(queue, bufres, res).wait()
print(time.time()-t)

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