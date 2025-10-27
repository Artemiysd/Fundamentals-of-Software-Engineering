import re


def isValidNumber(string):
    return string.isdigit() and len(string) in [13, 15, 16]


def getCheckSum(string):
    checkSum = 0

    for i in range(len(string) - 2, -1, -2):
        digit = int(string[i])
        doubled = digit * 2
        if doubled > 9:
            checkSum += 1 + (doubled - 10)
        else:
            checkSum += doubled

    for i in range(len(string) - 1, -1, -2):
        checkSum += int(string[i])

    return checkSum


def getCardType(string):
    if (len(string) == 13 or len(string) == 16) and string.startswith("4"):
        return "Visa"
    if len(string) == 15 and (string.startswith("34") or string.startswith("37")):
        return "American Express"
    if len(string) == 16 and re.match(r"5[1-5]", string[:2]):
        return "MasterCard"
    return "Invalid"


def main():
    cardNumber = input("Введите номер банковской карты: ").strip()

    if isValidNumber(cardNumber):
        if getCheckSum(cardNumber) % 10 == 0:
            print(getCardType(cardNumber))
        else:
            print("Invalid")
    else:
        print("Invalid")


main()