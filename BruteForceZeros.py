# finding the zeros of the eigenvalues

import math 
import cmath

xx = []
yy = []
zz = []
lam = []

for i in range(0, 201):
    xx.append((i-100)/10)
    x = xx[i]
    for j in range(0, 201):
        yy.append((j-100)/10)
        y = yy[j]
        for k in range(0, 2001):
            zz.append((k-1000)/100)
            z = zz[k]
            #print("x = {}    y = {}      z = {}".format(x, y, z))
            stuff1 = -16*(x**3) + 6*(x**2)*(y + z + 6)
            stuff2 = 4 * (-4*x**2 + x*(y + z + 6) - 4*y**2 + y*z + 6*y - 4*z**2 + 6*z - 9)**3 + \
                (-16*x**3 + 6*(x**2)*(y + z + 6) + 6*x*(y**2 - 7*y*z + 3*y + \
                z**2 + 3*z - 9) - 16*y**3 + 6*(y**2)*(z + 6) + \
                6*y*(z**2 + 3*z - 9) - 16*(z**3) + 36*(z**2) - 54*z + 54)**2
            stuff3 = 6*x*(y**2 - 7*y*z + 3*y + z**2 + 3*z - 9) - 16*(y**3) + \
                6*y*(y*z + 6*y + z**2 + 3*z - 9) - \
                16*(z**3) + 36*(z**2) - 54*z + 54

            #print("stuff1 = {}   stuff2 = {}     stuff3 = {}".format(stuff1, stuff2, stuff3))
            temp1 = 1/(3*(2**(1/3))) * ( (stuff1 + cmath.sqrt(stuff2) + stuff3 )**(1/3) )
            temp2 = 3*( (stuff1 + cmath.sqrt(stuff2) + stuff3 )**(1/3) ) + (1/3)*(-2*x - 2*y - 2*z + 3)


            #print("temp1 = {}          temp2 = {}".format(temp1, temp2))
            ans = temp1/temp2
            lam.append(ans)
            #print("\nanswer = {}".format(ans))
            if ans.real < 0:
                print("x = {}    y = {}      z = {}".format(x, y, z))
                print ("real = {}".format(ans.real))
    print("x = {}".format(x))

