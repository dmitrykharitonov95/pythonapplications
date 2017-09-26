import random as rnd
lst=[];
lst2=[];
M=5;
k=10;
n=20;
res=0;
temp=0;
for i in range(0,k):
    lst.append(rnd.randint(0,M))
for i in range(0,n):
    lst2.append(rnd.randint(0,M))
for i in range(0,k):
    for j in range(0,n):
        temp=0;
        l=0;
        while (i+l<k) and (j+l<n) and (lst[i+l]==lst2[j+l]):
            temp+=1
            l+=1
        if (temp>res):
            res=temp
print(lst)
print(lst2)
print(res)
