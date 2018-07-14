import random
def main(num1 = "1024", num2 = "0", amount = "1", *kwargs):
    try:
        num1 = int(num1)
        num2 = int(num2)
        amount = int(amount)
    except:
        return("Введите аргументы как цифры.")
    randarray = ""
    for i in range(amount):
        if num2 > num1:
            randarray = randarray + " " + str(random.randint(num1,num2))
        else:
            randarray = randarray + " " + str(random.randint(num2,num1))
    return randarray