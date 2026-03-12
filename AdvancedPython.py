# DECORATORS
print("=" * 60 + "\nDECORATORS\n" + "=" * 60)

def my_decorater(func):
    def wrapper():
        print("Before the function is called.")
        func()
        print("After the function is called.")
    return wrapper

@my_decorater
def hello_world():
    print("Hello, World!")

hello_world()


# PROPERTY DECORATORS
print("\n" + "=" * 60 + "\nPROPERTY DECORATORS\n" + "=" * 60)

class Person:
    def __init__(self, name, age):
        self.__name = name
        self.__age = age

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        if len(value) == 0:
            raise ValueError("Name cannot be empty.")
        self.__name = value

    @name.deleter
    def name(self):
        self.__name == None

    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError("Age must be an integer.")
        if value < 0:
            raise ValueError("Age cannot be negative.")
        self.__age = value

irem = Person("Irem", 20)
print(f"Name: {irem.name}, Age: {irem.age}")


#STATIC METHODS
print("\n" + "=" * 60 + "\nSTATIC METHODS\n" + "=" * 60)

class MathOperations:
    @staticmethod
    def add(a, b):
        return a + b
    
    @staticmethod
    def subtract(a, b):
        return a - b
    
    @staticmethod
    def multiply(a, b):
        return a * b
    
    @staticmethod
    def divide(a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

print(f"Addition: {MathOperations.add(5, 3)}")
print(f"Subtraction: {MathOperations.subtract(5, 3)}")
print(f"Multiplication: {MathOperations.multiply(5, 3)}")
print(f"Division: {MathOperations.divide(5, 3)}")


# CLASS METHODS
print("\n" + "=" * 60 + "\nCLASS METHODS\n" + "=" * 60)

class Pizza:

    total_pizzas = 0

    def __init__(self, ingredients):
        self.ingredients = ingredients
        Pizza.total_pizzas += 1

    @classmethod
    def margherita(cls):
        return cls(["mozzarella", "tomatoes"])

    @classmethod
    def pepperoni(cls):
        return cls(["mozzarella", "tomatoes", "pepperoni"])
    
    @classmethod
    def get_total_pizzas(cls):
        return cls.total_pizzas
    
pizza1 = Pizza.margherita()
pizza2 = Pizza.pepperoni()  
print(f"Pizza 1 ingredients: {pizza1.ingredients}")
print(f"Pizza 2 ingredients: {pizza2.ingredients}")
print(f"Total pizzas: {Pizza.get_total_pizzas()}")