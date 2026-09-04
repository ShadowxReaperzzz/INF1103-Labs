print("==================================")
print("Welcome")
print("It's my first post")
print("==================================")

username = input("Enter Username: ")
age =  int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("==================================")
print("Username:", username)
print("Age: ", age)
print("Category: ", category)

if age>40 and category == "Food":
    print("You are old what food do you like???")