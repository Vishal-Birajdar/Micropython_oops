"""Inheritance allows us to define a class that inherits all th method and properties from anothe class"""
#parent class and chield class
class division:
    def __init__(self,a,b):
        self.n = a
        self.m = b
    def divide(self):
        return self.n/self.m
class modules:
    def __init__(self,a,b):
        self.n = a
        self.m = b
    def mod_divide(self):
        return self.n %self.m
class div_mod(division,modules):
    def __init__(self,a,b):
        self.n=a
        self.m=b
    def div_and_mod(self):
      divval=division.divide(self)
      modval=modules.mod_divide(self)
      return (divval, modval)
    
x = div_mod(10,3)
print("division",x.divide())
print("mod_division",x.mod_divide())
print("div and mod",x.div_and_mod())