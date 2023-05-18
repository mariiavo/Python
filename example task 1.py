def snowflake(n):
    matrix=[]
    for i in range(n):
        temp=[]
        for j in range(n):
            temp.append('.')
        matrix.append(temp)
        
    middle_line=n//2
    for i in matrix:
        i[middle_line]='*'
    for i in range(n):
        matrix[middle_line][i]='*'
    return matrix
n=15
pattern=snowflake(n)
count1=0
count2=n-1
for i in range(len(pattern)):
    for j in range(len(pattern[i])):
        if j==count1:
            pattern[i][j]='*'
        if j==count2:
            pattern[i][j]='*'
    count1+=1
    count2-=1
for i in pattern:
    print(' '.join(i))
#print(x, end='')