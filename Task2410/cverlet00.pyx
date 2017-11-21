from __future__ import division
from cython.parallel import prange
import numpy as np
import numpy.linalg as nlg
import copy
cimport numpy as np
DTYPE = np.float32
ctypedef np.float32_t DTYPE_t
cimport cython
@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def acceleration(np.ndarray[DTYPE_t, ndim=2] lst, np.ndarray[DTYPE_t, ndim=1] lstm, np.ndarray[DTYPE_t, ndim=2] a):
    cdef double G=6.67 * 10.0 ** (-11)
    cdef int N=lst.shape[0]
    cdef int i,j
    for i in range(0,N):
        a[i]=0
        for j in range(0,N):
            if i!=j:
                a[i]+=G*lstm[j]*(lst[j,0:3]-lst[i,0:3])/nlg.norm(lst[j,0:3]-lst[i,0:3],2) ** 3
def cverlet00(np.ndarray[DTYPE_t, ndim=2] lst, np.ndarray[DTYPE_t, ndim=1] lstm, int M, double T):
    print "I am here!"
    cdef int N=lst.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=3] res=np.zeros([M,N,6], dtype=DTYPE)
    cdef double tau=T/M;
    cdef np.ndarray[DTYPE_t, ndim=2] a=np.zeros([N,3],dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] b=np.zeros([N,3],dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] lst2=np.zeros([N,6], dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] lst3=np.zeros([N,6], dtype=DTYPE)
    cdef int i,j
    acceleration(lst,lstm,a)
    for i in range(1,M):
        for j in range(0,N):
            lst2[j,0:3]=lst[j,0:3]+lst[j,3:6]*tau+0.5*a[j]*tau**2
        acceleration(lst2,lstm,b)
        for j in range(0,N):
            lst2[j,3:6]=lst[j,3:6]+0.5*(a[j]+b[j])*tau
        lst=copy.copy(lst2)
        a=copy.copy(b)
        res[i]=copy.copy(lst)
    return res
def norm(DTYPE_t[:,:] lst, int i, int j):
    cdef int k
    cdef double temp=0
    for k in range(0,3):
        temp+=(lst[i,k]-lst[j,k])**2
    return temp ** 0.5
def acceleration2(DTYPE_t[:,:] lst, DTYPE_t[:] lstm, DTYPE_t[:,:] a):
    cdef double G=6.67 * 10.0 ** (-11)
    cdef int N=lst.shape[0]
    cdef int i,j,k
    for i in range(0,N):
        for k in range(0,3):
            a[i,k]=0
        for j in range(0,N):
            if i!=j:
                for k in range(0,3):
                    a[i,k]+=G*lstm[j]*(lst[j,k]-lst[i,k])/norm(lst,i,j) ** 3
def cverlet01(np.ndarray[DTYPE_t, ndim=2] cur, np.ndarray[DTYPE_t, ndim=1] masm, int M, double T):
    print "I am here!2"
    cdef DTYPE_t[:,:] lst=cur
    cdef DTYPE_t[:] lstm=masm
    cdef int N=lst.shape[0]
    cdef DTYPE_t[:,:,:] res=np.zeros([M,N,6], dtype=DTYPE)
    cdef double tau=T/M;
    cdef DTYPE_t[:,:] a=np.zeros([N,3],dtype=DTYPE)
    cdef DTYPE_t[:,:] b=np.zeros([N,3],dtype=DTYPE)
    cdef DTYPE_t[:,:] lst2=np.zeros([N,6], dtype=DTYPE)
    cdef int i,j,k
    acceleration2(lst,lstm,a)
    for i in range(1,M):
        for j in range(0,N):
            for k in range(0,3):
                lst2[j,k]=lst[j,k]+lst[j,k+3]*tau+0.5*a[j,k]*tau**2
        acceleration2(lst2,lstm,b)
        for j in range(0,N):
            for k in range(0,3):
                lst2[j,k+3]=lst[j,k+3]+0.5*(a[j,k]+b[j,k])*tau
        for j in range(0,N):
            for k in range(0,3):
                lst[j,k]=lst2[j,k]
                lst2[j,k]=0
                lst[j,k+3]=lst2[j,k+3]
                lst2[j,k+3]=0
                a[j,k]=b[j,k]
                res[i,j,k]=lst[j,k]
                res[i,j,k+3]=lst[j,k+3]
    return res
def acceleration3(np.ndarray[DTYPE_t, ndim=2] lst, np.ndarray[DTYPE_t, ndim=1] lstm, np.ndarray[DTYPE_t, ndim=2] a):
    cdef double G=6.67 * 10.0 ** (-11)
    cdef int N=lst.shape[0]
    cdef int i,j
    for i in prange(0,N, nogil=True):
        a[i]=0
        for j in range(0,N):
            if i!=j:
                a[i]+=G*lstm[j]*(lst[j,0:3]-lst[i,0:3])/nlg.norm(lst[j,0:3]-lst[i,0:3],2) ** 3
def cverlet10(np.ndarray[DTYPE_t, ndim=2] lst, np.ndarray[DTYPE_t, ndim=1] lstm, int M, double T):
    print "I am here!"
    cdef int N=lst.shape[0]
    cdef np.ndarray[DTYPE_t, ndim=3] res=np.zeros([M,N,6], dtype=DTYPE)
    cdef double tau=T/M;
    cdef np.ndarray[DTYPE_t, ndim=2] a=np.zeros([N,3],dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] b=np.zeros([N,3],dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] lst2=np.zeros([N,6], dtype=DTYPE)
    cdef np.ndarray[DTYPE_t, ndim=2] lst3=np.zeros([N,6], dtype=DTYPE)
    cdef int i,j
    acceleration3(lst,lstm,a)
    for i in range(1,M):
        for j in prange(0,N, nogil=True):
            lst2[j,0:3]=lst[j,0:3]+lst[j,3:6]*tau+0.5*a[j]*tau**2
        acceleration3(lst2,lstm,b)
        for j in prange(0,N, nogil=True):
            lst2[j,3:6]=lst[j,3:6]+0.5*(a[j]+b[j])*tau
        lst=copy.copy(lst2)
        a=copy.copy(b)
        res[i]=copy.copy(lst)
    return res