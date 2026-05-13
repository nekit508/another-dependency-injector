import importlib
import pkgutil

from ..wiring.anno import injections, InjectionType, wires
from .provider import Provider, Singleton, ValueProvider

class Container:
    providers: list[Provider]

    def __init__(self):
        self.providers = []

    def provider(self, provider: Provider):
        self.providers.append(provider)

    def singleton(self, cls):
        self.provider(Singleton(cls))

    def value[T](self, key: str, value: T):
        self.provider(ValueProvider(key, value))

    def resolve_provider[T](self, cls) -> Provider[T]:
        for provider in self.providers:
            if provider.can_provide(cls):
                return provider

        raise RuntimeError(f"Unable to find provider of {cls}")

    def wire(self, package):
        result = {}

        for module_info in pkgutil.walk_packages(package.__path__, package.__name__ + '.'):
            module = importlib.import_module(module_info.name)
            result[module_info.name] = module

        for injection in injections:
            match injection.injection_type:
                case InjectionType.SINGLETON:
                    self.singleton(injection.cls)

        for wire in wires:
            wire.connect(self.resolve_provider(wire.cls))