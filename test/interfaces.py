from abc import ABC


class IA(ABC):
    prefix: str
    def print(self, message: str): ...

class IB(ABC):
    a: IA
    def work(self): ...

class IC(ABC):
    a: IA
    def process(self, data: str, b: IB = None): ...