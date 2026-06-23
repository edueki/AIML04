from .base import AbsCalculator


class Calculator(AbsCalculator):
    def add(self,a,b):
        return a+b
    def sub(self,a,b):
        return a-b
    def mul(self,a,b):
        return a*b
    def div(self,a,b):
        return a/b
    def __call__(self):
        return "welcome! How can I help you?"