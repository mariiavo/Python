file1=input('Please enter the file name: ')
try:
    file=open(file1)
except:
    print('File can not be opened')
    quit()
    
text=[]
for line in file:
    line=line.strip()
    line=line.split(' ')
    text.append(line)
    
words=[]
string=input('Please enter the string: ')
for i in text:
    for j in i:
        if string in j:
            words.append(j)
            
print('Words are:')
count=0
for i in words:
    print(i)
    count+=1

print('The number of words containing', string, 'is', count) 
    
file.close()
#words.txt