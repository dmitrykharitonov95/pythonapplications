import random as rnd
import math
lst=[];
lst2=[];
M=50;
k=10;
res=1;
temp=1;
for i in range(0,k):
    lst.append(rnd.randint(0,M))
i=0
#lst[0]=0.5
print(lst)
try:
    P=[0]*k
    M=[0]*(k+1)
    L=0
    for i in range(0,k):
        if not isinstance(lst[i],int):
            raise TypeError("Неправильный тип")
        lo=1
        hi=L
        while (lo<=hi):
            mid=math.ceil((lo+hi)/2)
            if (lst[M[mid]]<lst[i]):
                lo=mid+1
            else:
                hi=mid-1
        newl=lo
        P[i]=M[newl-1]
        M[newl]=i
        if newl>L:
            L=newl
        #print(P)
    S=[0]*L
    k=M[L]
    for i in range(L-1,-1,-1):
        S[i]=lst[k]
        k=P[k]
    print(L)
    print(S)
except (TypeError) as inst:
    print(type(inst))
    print(inst)
    res=0

