def pow(a,n):
    if n==1:
        return a
    elif (n==2):
        return a*a
    else:
        b=pow(a,n//2)
        if n%2==0:
            return b*b
        else:
            return b*b*a
print(pow(2,6))
