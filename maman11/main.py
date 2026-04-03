# This function receive 2 numbers and op and returns the result of the Arithmetic Operation.
def calc(num1, num2, op):
    if op == "+":
        return num1 + num2
    elif op == "-":
        return num1 - num2
    elif op == "*":
        return num1 * num2
    elif op == "/":
        if num2 == 0:
            return None
        else:
            return num1 / num2
    return  "invalid"

# This function receive How many times will the function be called and then print the result to the user.
def compute_calcs(n):
    for i in range(n):
        num1 = int(input("Enter first number: "))
        num2 = int(input("Enter second number: "))
        op = input("Enter operation: ")
        result = (calc(num1, num2, op)) # Call to calc function.
        if result == "invalid":
            print("The requested calculation is invalid")
        elif result is None:
            print("Can't divide by zero")
        else:
            print(num1, op, num2, "=", result)



# This function receive a number and returns True if the number is armstrong number and False if not.
def is_armstrong(num):
    alt = num
    sum = 0
    count = 0
    while alt > 0: # Calculate the power.
        alt = alt // 10
        count += 1

    alt = num
    while alt > 0: # Calculate the result.
        sum += (alt % 10) ** count
        alt = alt // 10
    return sum == num


# This function count the armstrong numbers between 1 and 10000.
def count_armstrong_numbers():
    count = 0
    for num in range(1, 10000):
        if is_armstrong(num):
            count += 1
            print(num)
    return count



# This function calculate how many substring are in the string.
def decompressed(compress):
    str = ""
    lastChar = ""
    for char in compress:
        if char.isdigit():
            for i in range(int(char)-1):
                str += lastChar
        else:
            str+=char
        lastChar = char
    return str




def count_sub(s, sub):
    count = 0
    for i in range(len(s)-len(sub)+1):
        if s[i] == sub[0]:
            j = i
            match = True
            for k in range(len(sub)):
                if s[j] != sub[k]:
                    match = False
                    break
                else:
                    j+=1
            if match:
                count += 1
    return count