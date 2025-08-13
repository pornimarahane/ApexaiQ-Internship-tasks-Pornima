#This program demonstrates list comprehension. 

#syntax
#variable_name = [expression for item in iterable]

Marks = [24, 42, 48, 29, 52, 82]
halfmarks = [n//2 for n in Marks]
print("Internal Marks Are:",halfmarks)

#using if-else
statuse = ["Average" if n <= 25 else "Good" for n in halfmarks]
print("The progress of student is:",statuse)

#function
def cube(n):
    return n**3
cubes = [cube(n) for n in Marks]
print("The cubes are:", cubes)

#string
random = ["tree", "ssgmce", "shegaon", "sunshine"]
uppercase = [w.upper() for w in random]
print("Words:",uppercase)

#simple table example
table = [n*17 for n in range(1,11)]
print("Table of 17:", table)

#typecasting example
string = "shnj12bnjk56"
digit = [int(ch) for ch in string if ch.isdigit()]
print("updated string is:", digit)