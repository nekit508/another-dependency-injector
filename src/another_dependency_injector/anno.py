import enum

injections: list[Injection] = []
wires: list[Wire]  =[]


class Type(enum.Enum):
    SINGLETON = 0


class Injection:
    cls: type
    injection_type: Type

    def __init__(self, cls: type, injection_type: Type):
        self.cls = cls
        self.injection_type = injection_type

class Wire:
    def __class_getitem__(cls, clz: type):
        return Wire(clz)

    cls: type

    def __init__(self, cls: type):
        wires.append(self)
        self.provider = None
        self.cls = cls

    def connect(self, provider):
        self.provider = provider

def inject(obj):
    if type(obj) is type:
        for element in obj.__dict__.keys():
            if isinstance(obj.__dict__[element], type(inject)):
                obj.__dict__[element] = inject(obj.__dict__[element])

        return obj
    else:
        obj.__dict__["__initial_defaults__"] = obj.__defaults__
        obj.__defaults__ = ()

        def wrapper(*args, **kwargs):
            obj.__defaults__ = tuple(o.provider.get() if isinstance(o, Wire) else o for o in obj.__initial_defaults__)
            return obj(*args, **kwargs)

        return wrapper

def injection(injection_type: Type):
    def decorator(cls):
        injections.append(Injection(cls, injection_type))
        return cls

    return decorator