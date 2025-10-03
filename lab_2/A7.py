x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

flag = False
flag2 = False


if (x1 + y1) % 2 == 0:
    flag = False
else:
    flag = True


if (x2 + y2) % 2 == 0:
    flag2 = False
else:
    flag2 = True


if flag == flag2:
    print("YES")
    if flag:
        print("Black")
    else:
        print("White")
else:
    print("NO")