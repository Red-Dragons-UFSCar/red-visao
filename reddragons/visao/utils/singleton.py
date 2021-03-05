class _Singleton (type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


if __name__ == '__main__':
    class Teste (metaclass=_Singleton):
        def __init__ (self, a, b):
            self._a = a
            self._b = b
        def run(self):
            return self._a+self._b

    foo = Teste(1,2)
    print(foo)
    bar = Teste(3,4)
    print(bar)
