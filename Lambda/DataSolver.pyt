def dataSolver_mean(data):
    sum = 0
    divisor = len(data)

    for i in data:
        sum += i

    return sum/divisor
    

data  = [1,2,3,4,5,6,7,8]

print(dataSolver_mean(data))
