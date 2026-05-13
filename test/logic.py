from src.another_dependency_injector.anno import inject, Wire, injection, Type
from test.interfaces import *

@injection(Type.SINGLETON)
class A(IA):
    def __init__(self, prefix: str = "prefix"):
        self.prefix = prefix

    def print(self, message: str):
        print(f"[{self.prefix}] {message}")

@injection(Type.SINGLETON)
class B(IB):
    @inject
    def __init__(self, a: IA = Wire[IA]):
        self.a = a

    def work(self):
        self.a.print("working now")


@injection(Type.SINGLETON)
class C(IC):
    @inject
    def __init__(self, a: IA = Wire[IA]):
        self.a = a

    @inject
    def process(self, data: str, b: IB = Wire[IB]):
        self.a.print(f"Working with {data}")
        b.work()

@inject
def handle(data: str = "default", c: IC = Wire[IC]):
    c.process(data)