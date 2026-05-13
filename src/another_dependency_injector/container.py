import importlib
import pkgutil

from anno import injections, Type, wires
from provider import Provider, Singleton

class StaticWrapper[T]:
    obj: T

    def __init__(self, obj: T):
        self.obj = obj

    def get(self) -> T:
        return self.obj

class Container:
    providers: list[Provider]

    def __init__(self):
        self.providers = []

    def provider(self, provider: Provider):
        self.providers.append(provider)

    def singleton(self, cls, *args, **kwargs):
        self.provider(Singleton(cls, args, kwargs))

    def resolve_provider[T](self, cls: type[T]) -> Provider[T]:
        for provider in self.providers:
            if issubclass(provider.cls, cls):
                return provider

        raise RuntimeError(f"Unable to find provider of {cls}")

    def wire(self, package):
        result = {}

        for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            module = importlib.import_module(module_info.name)
            result[module_info.name] = module

        for injection in injections:
            match injection.injection_type:
                case Type.SINGLETON:
                    self.singleton(injection.cls)

        for wire in wires:
            wire.connect(self.resolve_provider(wire.cls))