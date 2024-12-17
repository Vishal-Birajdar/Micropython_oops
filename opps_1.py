class Person:
#__init__() function is called automatically every time the class is being used to create new object
    
    def __init__(self,name,age):
        self.name = name
        self.age = age
#__str__() function control what should be returned when the class object is represented as string
    def __str__(self):
        return f"{self.name}({self.age})"
#OBJECT METHOD
#object can also contain methods. method in objects are functions that belong to the object
    def myfunc(self):
        print("Hello my name is "+self.name)
p2 = Person("snwhal",23)
print(p2)
p1 = Person("Vishal",24)
p1.age = 45
print(p1.name)
print(p1.age)
p1.myfunc()
