x = int(input('enter value of x'))
y = int(input('enter value of y'))
second_x = int(input('enter second value of x'))
second_y = int(input('enter second value of y'))
if (x > 0 and y > 0 and second_x > 0 and second_y > 0):
    print('Yes,I четверть')
elif (x < 0 and y < 0 and second_x > 0 and second_y < 0):
    print('Yes, II четверть')
elif ( x < 0 and y < 0 and second_x < 0 and second_y < 0 ):
    print('Yes,III четверть')
elif (x > 0 and y < 0 and second_x > 0 and second_y < 0):
    print('Yes,IV четверть')
else:
    print('No')