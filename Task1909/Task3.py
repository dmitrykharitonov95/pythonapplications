eps=10 ** -6
def intersect2(A1,A2,A3,A4):
    val1=(A1[0]-A2[0])*(A4[2]-A3[2])-(A1[2]-A2[2])*(A4[0]-A3[0])
    val2=(A1[0]-A2[0])*(A4[1]-A3[1])-(A1[1]-A2[1])*(A4[0]-A3[0])
    val3=(A1[1]-A2[1])*(A4[2]-A3[2])-(A1[2]-A2[2])*(A4[1]-A3[1])
    if (val1==0) and (val2==0) and (val3==0):#проверка параллельности прямых
        val4=(A4[0]-A2[0])*(A1[2]-A2[2])-(A4[2]-A2[2])*(A1[0]-A2[0])
        val5=(A4[1]-A2[1])*(A1[2]-A2[2])-(A4[2]-A2[2])*(A1[1]-A2[1])
        val6=(A4[0]-A2[0])*(A1[1]-A2[1])-(A4[1]-A2[1])*(A1[0]-A2[0])
        inp1=val4 ** 2 + val5 ** 2 + val6 ** 2

        val7=(A3[0]-A2[0])*(A1[2]-A2[2])-(A3[2]-A2[2])*(A1[0]-A2[0])
        val8=(A3[1]-A2[1])*(A1[2]-A2[2])-(A3[2]-A2[2])*(A1[1]-A2[1])
        val9=(A3[0]-A2[0])*(A1[1]-A2[1])-(A3[1]-A2[1])*(A1[0]-A2[0])
        inp2=val7 ** 2 + val8 ** 2 + val9 ** 2

        if (A1[0]!=A2[0]):
            u=(A4[0]-A2[0])/(A1[0]-A2[0])
            v=(A3[0]-A2[0])/(A1[0]-A2[0])
        elif (A1[1]!=A2[1]):
            u=(A4[1]-A2[1])/(A1[1]-A2[1])
            v=(A3[1]-A2[1])/(A1[1]-A2[1])
        elif (A1[2]!=A2[2]):
            u=(A4[2]-A2[2])/(A1[2]-A2[2])
            v=(A3[2]-A2[2])/(A1[2]-A2[2])
        else:
            print("Точки совпадают")
            return -5

        #наличие совпадающих точек у отрезков
        if (inp2==inp1) and (inp2==0) and (((v>=0) and (v<=1)) or ((u>=0) and (u<=1)) or ((u>=1) and (v<=0)) or ((v>=1) and (u<=0))):
            return 1
        elif (inp1==0) and ((v>=0) and (v<=1)):
            return 2
        elif (inp2==0) and ((u>=0) and (u<=1)):
            return 3
        else:
            return 0
    else:
        if (val1!=0):
            u=((A3[0]-A2[0])*(A4[2]-A3[2])-(A3[2]-A2[2])*(A4[0]-A3[0]))/val1;
            v=-((A3[0]-A2[0])*(A2[2]-A1[2])-(A3[2]-A2[2])*(A2[0]-A1[0]))/val1;
        elif (val3!=0):
            u=((A3[1]-A2[1])*(A4[2]-A3[2])-(A3[2]-A2[2])*(A4[1]-A3[1]))/val3;
            v=-((A3[1]-A2[1])*(A2[2]-A1[2])-(A3[2]-A2[2])*(A2[1]-A1[1]))/val3;
        else:
            u=((A3[0]-A2[0])*(A4[1]-A3[1])-(A3[1]-A2[1])*(A4[0]-A3[0]))/val2;
            v=-((A3[0]-A2[0])*(A2[1]-A1[1])-(A3[1]-A2[1])*(A2[0]-A1[0]))/val2;
        A5=[0]*3;
        for i in range(0,3):
            A5[i]=A2[i]+(A1[i]-A2[i])*u;
        val4=(A5[0]-A2[0])*(A1[2]-A2[2])-(A5[2]-A2[2])*(A1[0]-A2[0])
        val5=(A5[1]-A2[1])*(A1[2]-A2[2])-(A5[2]-A2[2])*(A1[1]-A2[1])
        val6=(A5[0]-A2[0])*(A1[1]-A2[1])-(A5[1]-A2[1])*(A1[0]-A2[0])
        inp1=val4 ** 2 + val5 ** 2 + val6 ** 2

        val7=(A5[0]-A3[0])*(A4[2]-A3[2])-(A5[2]-A3[2])*(A4[0]-A3[0])
        val8=(A5[1]-A3[1])*(A4[2]-A3[2])-(A5[2]-A3[2])*(A4[1]-A3[1])
        val9=(A5[0]-A3[0])*(A4[1]-A3[1])-(A5[1]-A3[1])*(A4[0]-A3[0])
        inp2=val7 ** 2 + val8 ** 2 + val9 ** 2
        #проверка, принадлежит ли точка прямым и лежит ли она внутри отрезков
        if (inp2==inp1) and (inp2==0) and (((v>=0) and (v<=1)) and ((u>=0) and (u<=1))):
            return 4
        else:
            return -1

def deter(A1,A2,A3,A4):
    return ((A4[0]-A1[0])*((A2[1]-A1[1])*(A3[2]-A1[2])-(A3[1]-A1[1])*(A2[2]-A1[2]))-
            (A4[1]-A1[1])*((A2[0]-A1[0])*(A3[2]-A1[2])-(A3[0]-A1[0])*(A2[2]-A1[2]))+
            (A4[2]-A1[2])*((A2[0]-A1[0])*(A3[1]-A1[1])-(A3[0]-A1[0])*(A2[1]-A1[1])))

def internal(A1,A2,A3,A4):
    val1=(A2[0]-A1[0])*(A3[1]-A1[1])-(A3[0]-A1[0])*(A2[1]-A1[1])
    val2=(A2[0]-A1[0])*(A3[2]-A1[2])-(A3[0]-A1[0])*(A2[2]-A1[2])
    val3=(A2[1]-A1[1])*(A3[2]-A1[2])-(A3[1]-A1[1])*(A2[2]-A1[2])
    if (abs(val1)>eps):
        u=((A4[0]-A1[0])*(A3[1]-A1[1])-(A3[0]-A1[0])*(A4[1]-A1[1]))/val1
        v=-((A4[0]-A1[0])*(A2[1]-A1[1])-(A2[0]-A1[0])*(A4[1]-A1[1]))/val1
    elif (abs(val2)>eps):
        u=((A4[0]-A1[0])*(A3[2]-A1[2])-(A3[0]-A1[0])*(A4[2]-A1[2]))/val2
        v=-((A4[0]-A1[0])*(A2[2]-A1[2])-(A2[0]-A1[0])*(A4[2]-A1[2]))/val2
    elif (abs(val3)>eps):
        u=((A4[1]-A1[1])*(A3[2]-A1[2])-(A3[1]-A1[1])*(A4[2]-A1[2]))/val3
        v=-((A4[1]-A1[1])*(A2[2]-A1[2])-(A2[1]-A1[1])*(A4[2]-A1[2]))/val3
    else:
        print("Точки совпадают")
        return -1
    if (abs(u-0.5)<0.5+eps) and (abs(v-0.5)<0.5+eps):
        return 1
    else:
        return 0

def intersect3(A1,A2,A3,A4,A5):
    return deter(A1,A2,A3,A4)/(deter(A1,A2,A3,A4)-deter(A1,A2,A3,A5));

def dist(A1,A2):
    sum=0
    for i in range(0,3):
        sum+= (A1[i]-A2[i]) ** 2
    return sum ** 0.5

def intersect(A1,A2,A3,A4,A5,A6):
    if (dist(A1,A2)<eps) or (dist(A1,A3)<eps) or (dist(A3,A2)<eps) or (dist(A4,A5)<eps) or (dist(A4,A6)<eps) or (dist(A5,A6)<eps):
        print("Точки совпадают")
        return -1
    val1=(A2[0]-A1[0])*(A3[1]-A1[1])-(A3[0]-A1[0])*(A2[1]-A1[1])
    val2=(A2[0]-A1[0])*(A3[2]-A1[2])-(A3[0]-A1[0])*(A2[2]-A1[2])
    val3=(A2[1]-A1[1])*(A3[2]-A1[2])-(A3[1]-A1[1])*(A2[2]-A1[2])
    if (abs(val1)<eps) and (abs(val2)<eps) and (abs(val3)<eps):
        print("Три точки лежат на одной прямой")
        return -1
    val1=(A5[0]-A4[0])*(A6[1]-A4[1])-(A6[0]-A4[0])*(A5[1]-A4[1])
    val2=(A5[0]-A4[0])*(A6[2]-A4[2])-(A6[0]-A4[0])*(A5[2]-A4[2])
    val3=(A5[1]-A4[1])*(A6[2]-A4[2])-(A6[1]-A4[1])*(A5[2]-A4[2])
    if (abs(val1)<eps) and (abs(val2)<eps) and (abs(val3)<eps):
        print("Три точки лежат на одной прямой")
        return -1
    isct=[0]*9;
    isct[0]=intersect2(P1,P2,P4,P5)
    isct[1]=intersect2(P1,P2,P4,P6)
    isct[2]=intersect2(P1,P2,P6,P5)
    isct[3]=intersect2(P1,P3,P4,P5)
    isct[4]=intersect2(P1,P3,P4,P6)
    isct[5]=intersect2(P1,P3,P6,P5)
    isct[6]=intersect2(P2,P3,P4,P5)
    isct[7]=intersect2(P2,P3,P4,P6)
    isct[8]=intersect2(P2,P3,P6,P5)
    for a in isct:
        if a>0:
            return 1
        if a==-5:
            return -1
    mas1=[0]*3
    mas2=[0]*3
    mas1[0]=deter(A1,A2,A3,A4)
    mas1[1]=deter(A1,A2,A3,A5)
    mas1[2]=deter(A1,A2,A3,A6)
    mas2[0]=deter(A4,A5,A6,A1)
    mas2[1]=deter(A4,A5,A6,A2)
    mas2[2]=deter(A4,A5,A6,A3)
    if (abs(mas1[0])<eps):
        if internal(A1,A2,A3,A4)==1:
            return 1
    if (abs(mas1[1])<eps):
        if internal(A1,A2,A3,A5)==1:
            return 1
    if (abs(mas1[2])<eps):
        if internal(A1,A2,A3,A6)==1:
            return 1
    if (abs(mas2[0])<eps):
        if internal(A4,A5,A6,A1)==1:
            return 1
    if (abs(mas2[1])<eps):
        if internal(A4,A5,A6,A2)==1:
            return 1
    if (abs(mas2[2])<eps):
        if internal(A4,A5,A6,A3)==1:
            return 1
    if (mas1[0]*mas1[1]<0) and (abs(mas1[0])>eps) and (abs(mas1[1])>eps):
        t=intersect3(A1,A2,A3,A4,A5)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A4[i]+t*A5[i]
            if internal(A1,A2,A3,A7)==1:
                return 1
    if (mas1[0]*mas1[2]<0) and (abs(mas1[0])>eps) and (abs(mas2[1])>eps):
        t=intersect3(A1,A2,A3,A4,A6)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A4[i]+t*A6[i]
            if internal(A1,A2,A3,A7)==1:
                return 1
    if (mas1[1]*mas1[2]<0) and (abs(mas1[2])>eps) and (abs(mas1[1])>eps):
        t=intersect3(A1,A2,A3,A5,A6)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A5[i]+t*A6[i]
            if internal(A1,A2,A3,A7)==1:
                return 1
    if (mas2[0]*mas2[1]<0) and (abs(mas2[0])>eps) and (abs(mas2[1])>eps):
        t=intersect3(A4,A5,A6,A1,A2)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A1[i]+t*A2[i]
            if internal(A4,A5,A6,A7)==1:
                return 1
    if (mas2[0]*mas2[2]<0) and (abs(mas2[0])>eps) and (abs(mas2[2])>eps):
        t=intersect3(A4,A5,A6,A1,A3)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A1[i]+t*A3[i]
            if internal(A4,A5,A6,A7)==1:
                return 1
    if (mas2[1]*mas2[2]<0) and (abs(mas2[2])>eps) and (abs(mas2[1])>eps):
        t=intersect3(A4,A5,A6,A2,A3)
        if (abs(t-0.5)<0.5+eps):
            A7=[0]*3
            for i in range(0,3):
                A7[i]=A2[i]+t*A3[i]
            if internal(A4,A5,A6,A7)==1:
                return 1
    return 0

P1=[0,0,0]
P2=[1,0,0]
P3=[-2,4,0]
P4=[-2,0,0]
P5=[-1,0,0]
P6=[0,0,1]

res=intersect(P1,P2,P3,P4,P5,P6)
if res==1:
    print("Треугольники пересекаются.")
elif res==-1:
    print("Один из треугольников не является таковым")
else:
    print("Треугольники не пересекаются.")
