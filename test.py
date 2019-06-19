class a():
    def bbb(self):
        B=0
    def ccc(self):
        self.C=1
    def __init__(self):
        self.bbb()
        self.ccc()
        self.ddd()
    def ddd(self):
        self.D=self.C

    
k=a()
print(k.D)
