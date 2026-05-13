from another_dependency_injector.providing import Container

import test
from test.test import *

if __name__ == "__main__":
    cont = Container()

    cont.value("config.value", "value")

    cont.wire(test)

    aa = AA()
    print(aa, aa.b, aa.b.value)