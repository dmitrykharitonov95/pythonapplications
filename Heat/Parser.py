import numpy as np
import copy
#def interscetion(lst1, lst2):
#    lst=[]
#    lind1=[]
#    lind2=[]
#    for i in range(len(lst1)):
#        for j in range(len(lst2)):
#            if (np.linalg.norm(lst1[i]-lst2[j])<10**-6):
#                lst.append(lst1[i])
#                lind1.append(i)
#                lind2.append(j)
#    return lst, lind1, lind2

#def triangles_intersection(mind, lind):
#    for i in range(3):
#        if (lind.count(mind[i])==0):
#            return False
#    return True
#def triangle_S(lst,mind):
#    l1=np.linalg.norm(lst[mind[0]]-lst[mind[1]])
#    l2=np.linalg.norm(lst[mind[0]]-lst[mind[2]])
#    l3=np.linalg.norm(lst[mind[2]]-lst[mind[1]])
#    p=(l1+l2+l3)/2
#    return (p*(p-l1)*(p-l2)*(p-l3))**0.5
#def intersection_S(glob,locind,i,j):
#    sect, lind1, lind2=interscetion(glob[i],glob[j])
#    S=0
#    for el in locind[j]:
#        if (triangles_intersection(el,lind2)):
#            S+=triangle_S(glob[j],el)
#    return S
def read(filename):
    f=open(filename,'r')
    count=0
    lst=[]
    glob=[]
    glob2=[]
    lst2=[]
    lst22=[]
    lst3=[]
    lst4=[]
    for line in f:
        if line[0] == '#':
            lst=line.split()
            if lst.count('object')>0:
                if count>0:
                    glob.append(lst2)
                    glob2.append(lst22)
                lst2=[]
                lst22=[]
                count+=1
        elif line[0]=='v':
            lst4=[]
            lst3=line[3:len(line)-1].split(' ')
            for el in lst3:
                lst4.append(float(el))
            lst2.append(np.array(lst4))
        elif line[0]=='f':
            lst4=[]
            lst3=line[2:len(line)-2].split(' ')
            for el in lst3:
                lst4.append(float(el))
            lst22.append(np.array(lst4, dtype=np.int))
    glob.append(lst2)
    glob2.append(lst22)
    locind=copy.deepcopy(glob2)
    for i in range(len(glob2)):
        for el in locind[i]:
            el-=1
            for j in range(0,i):
                el-=len(glob[j])
    return glob,locind