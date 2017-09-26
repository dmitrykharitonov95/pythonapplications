import random as rnd
lst=[];
lst2=[];
M=5;
k=10;
res=1;
temp=1;
for i in range(0,k):
    lst.append(rnd.randint(0,M))
i=0
lst[0]=0.5
try:
    if not isinstance(lst[0],int):
        raise TypeError("Неправильный тип")
    while (i<k-1):
        if not isinstance(lst[i+1],int):
            raise TypeError("Неправильный тип")
        l=0
        temp=1
        while (i+l<k-1) and (lst[i+l]<lst[i+l+1]):
            temp+=1
            l+=1
        if (temp>res):
            res=temp
        i+=l+1
except (TypeError) as inst:
    print(type(inst))
    print(inst)
    res=0
finally:
    print(lst)
    if (res>0):
        print(res)

