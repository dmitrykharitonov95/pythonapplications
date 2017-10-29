import random as rnd
lst=[];
lst2=[];
M=5;
k=5;
n=6;
res=0;
temp=0;
for i in range(0,k):
    lst.append(rnd.randint(0,M))
for i in range(0,n):
    lst2.append(rnd.randint(0,M))
c=[]
for i in range(0,k+1):
    d=[0]*(n+1)
    c.append(d)
for i in range(0,k+1):
    for j in range(0,n+1):
        print(c[i][j],end=' ')
    print()
for i in range(1,k+1):
    for j in range(1,n+1):
        if lst[i-1]==lst2[j-1]:
            c[i][j]=c[i-1][j-1]+1
        else:
            c[i][j]=max(c[i-1][j],c[i][j-1])
print(lst)
print(lst2)
print(c[k][n])
#for i in range(0,k+1):
#    for j in range(0,n+1):
#        print(c[i][j],end=' ')
#    print()
