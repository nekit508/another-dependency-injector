from another_dependency_injector.wiring import Wire, injection, InjectionType, inject

@inject
@injection(InjectionType.SINGLETON)
class B:
    value: str

    def __init__(self, value: str = Wire["config.value"]):
        self.value = value

@inject
@injection(InjectionType.SINGLETON)
class A:
    b: B

    def __init__(self, b: B = Wire[B]):
        self.b = b

class AA(A):
    def __init__(self):
        super().__init__()