def intersect2(A1,A2,A3,A4):
    val1=(A1[0]-A2[0])*(A4[2]-A3[2])-(A1[2]-A2[2])*(A4[0]-A3[0])
    val2=(A1[0]-A2[0])*(A4[1]-A3[1])-(A1[1]-A2[1])*(A4[0]-A3[0])
    val3=(A1[1]-A2[1])*(A4[2]-A3[2])-(A1[2]-A2[2])*(A4[1]-A3[1])
    if (val1==0) and (val2==0) and (val3==0):
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
        if (inp2==inp1) and (inp2==0) and (((v>=0) and (v<=1)) and ((u>=0) and (u<=1))):
            return 4
        else:
            return -1


P1=(0,0,0)
P2=(1,0,0)
P3=(-2,2,0)
P4=(0,0,1)
P5=(-2,0,0)
P6=(-4,0,0)

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
res=0
for a in isct:
    if a>0:
        res=1
for a in isct:
    if a==-5:
        res=-1

if res==1:
    print("Треугольники пересекаются.")
elif res==-1:
    print("Один из треугольников не является таковым")
else:
    print("Треугольники не пересекаются.")
