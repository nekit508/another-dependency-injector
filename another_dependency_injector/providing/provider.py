class Provider[T]:
    def __init__(self):
        if type(self) == Provider:
            raise NotImplementedError

    def can_provide(self, cls) -> bool: ...

    def get(self) -> T: ...

class Singleton[T](Provider[T]):
    obj: T | None
    cls: type[T]

    def __init__(self, cls: type[T]):
        super().__init__()
        self.cls = cls
        self.obj = None
        
    def can_provide(self, cls) -> bool:
        return type(cls) is type and issubclass(self.cls, cls)

    def get(self) -> T:
        if self.obj is None:
            self.obj = self.cls()

        return self.obj

class ValueProvider[T](Provider[T]):
    cls: str
    value: T

    def __init__(self, cls: str, value):
        super().__init__()
        self.cls = cls
        self.value = value

    def can_provide(self, cls) -> bool:
        return type(cls) is str and self.cls == cls

    def get(self) -> T:
        return self.value