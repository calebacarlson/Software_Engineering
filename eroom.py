def CipherWorker(encodedString):
    decodedString = ''
    encodedString = encodedString.lower()
    listOptions = []

    for i in range(24):
        option = ''
        
        for j in encodedString:
            if ord(j)+i > 122:
                option = option+chr(ord(j)+i-24)
            else:
                option = option+chr(ord(j)+i)
        listOptions.append(option)
        print(str(i)+": "+option)

    choice = int(input("Pick the itoration of the right encoded text: 1-24?"))

    decodedString = listOptions[choice]

    return decodedString

print(CipherWorker("KHoOr"))