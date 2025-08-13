#This program demonstrates error_handling.

#Syntax:
# {key_expr: value_expr for item in iterable if condition}

#simple example
numbers = [1, 2, 3, 4, 5]
squares = {num: num**2 for num in numbers}
print("Squares:", squares)

#conditions
even_squares = {num: num**2 for num in numbers if num % 2 == 0}
print("Even squares:", even_squares)

#using Function
words = ['apple', 'banana', 'cherry']
word_length = {word: len(word) for word in words}
print("Word lengths:", word_length)

#methods

#get()
d = {'a': 1, 'b': 2}
print(d.get('a')) 
print(d.get('c', 0))  

#keys()
print(d.keys())  

#values()
print(d.values())  

#items()
print(d.items())  

#pop()
val = d.pop('a')
print(val)  
print(d)    

#clear()
d.clear()
print(d) 
