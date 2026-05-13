from container import Container
from test.logic import handle
import test


if __name__ == "__main__":
    container = Container()
    container.wire(test)
    handle("jkfdg")