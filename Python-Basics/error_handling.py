#This program demonstrates error_handling.

 #syntax
"""
try:
   (code that can cause error)
except error:
   (handles the error if occured)
else:
   (optional: runs when no error gets occured)
Finally:
   (optional: always runs)

"""

#syntax error
try:
    number = "x-=34ghj5"  
    exec(number)  
except SyntaxError as se:
    print("SyntaxError caught:", se)
else:
    print("No syntax error.")
finally:
    print("Finished SyntaxError block.\n")



#value error
try:
    num1 = int(input("Enter a number: "))
    num2 = int(input("Enter a number: "))  
except ValueError as ve:
    print("ValueError caught:", ve)
else:
    result = num1 + num2
    print("Result is:", result)
finally:
    print("Successfull!!!")


#zero division error
try:
    x = int(input("Enter a Dividend: "))
    y = int(input("Enter a Divisor: "))
    result = x / y   
except ZeroDivisionError as zde:
    print("ZeroDivisionError :", zde)
else:
    print("Division result :", result)
finally:
    print("Successfull")


#File handling error 
try:
    with open("sinchan.txt", "r") as f:
        content = f.read()
except FileNotFoundError as fe:
    print("FileNotFoundError caught:", fe)
else:
    print("File content:", content)
finally:
    print("Successfull")


#Index error
try:
    Prices = [10, 20, 30]
    print(Prices[5])  
except IndexError as ie:
    print("IndexError caught:", ie)
else:
    print("Accessed list element successfully.")
finally:
    print("Successfull")


#key error
try:
    my_dict = {"apple": 5, "banana": 3}
    print(my_dict["apple"]) 
except KeyError as ke:
    print("KeyError caught:", ke)
else:
    print("Accessed dictionary key successfully.")
finally:
    print("successfull")



