

def printf(content,indentation):
    str1=""
    for i in range(len(content)):
        str1+=(int(indentation[i])-len(str1))*" "
        str1+=str(content[i])

    print(str1)
