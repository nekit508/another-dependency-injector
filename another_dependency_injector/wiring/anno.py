import enum

injections: list[Injection] = []
wires: list[Wire]  =[]


class InjectionType(enum.Enum):
    SINGLETON = 0


class Injection:
    injection_type: InjectionType

    def __init__(self, cls, injection_type: InjectionType):
        self.cls = cls
        self.injection_type = injection_type

class Wire:
    def __class_getitem__(cls, clz):
        return Wire(clz)

    def __init__(self, cls):
        wires.append(self)
        self.provider = None
        self.cls = cls

    def connect(self, provider):
        self.provider = provider

def inject(obj):
    if type(obj) is type:
        for element in obj.__dict__.keys():
            oobj = obj.__dict__[element]
            if isinstance(oobj, type(inject)):
                setattr(obj, element, inject(oobj))

        return obj
    elif isinstance(obj, type(inject)):
        obj.__dict__["__initial_defaults__"] = obj.__defaults__
        obj.__defaults__ = ()

        def wrapper(*args, **kwargs):
            obj.__defaults__ = tuple(o.provider.get() if isinstance(o, Wire) else o for o in obj.__initial_defaults__)
            return obj(*args, **kwargs)

        return wrapper
    else:
        raise ValueError("inject decorator must be applied only to classes, it's methods and functions.")

def injection(injection_type: InjectionType):
    def decorator(cls):
        injections.append(Injection(cls, injection_type))
        return cls

    return decorator