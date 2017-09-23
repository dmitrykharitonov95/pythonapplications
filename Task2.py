
import random as rnd
lst=[];
N=100;
k=10;
for i in range(0,k):
    lst.append(rnd.randint(1,N))
lst2=[0]*(N+1);
cnt=0;
lst[0]=lst[1]
print(lst);
for i in range(0,k):
    lst2[lst[i]]+=1;
    if (lst2[lst[i]]==1):
        cnt+=1;
print(cnt)



