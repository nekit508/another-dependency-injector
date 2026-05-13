class Provider[T]:
    cls: type[T]
    args: tuple
    kwargs: dict

    def __init__(self, cls: type[T], *args, **kwargs):
        self.cls = cls
        self.args = args
        self.kwargs = kwargs

    def get(self) -> T: ...

class Singleton[T](Provider[T]):
    obj: T | None

    def __init__(self, cls: type[T], *args, **kwargs):
        super().__init__(cls, *args, **kwargs)
        self.obj = None

    def get(self):
        if self.obj is None:
            self.obj = self.cls()

        return self.obj