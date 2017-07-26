from collections import defaultdict


class modifier(object):
    def __init__(self, value):
        self.callbacks = []
        self._last_values = defaultdict(lambda: self._call_if(value))
        self._values = defaultdict(lambda: value)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        key = id(instance)

        value = self._call_if(self._values[key])
        if value != self._last_values[key]:
            print("get")
            self.trigger(instance, self._last_values[key], value)
            self._last_values[key] = value

        return value

    def __set__(self, instance, value):

        key = id(instance)

        if self._values[key] != value:
            print('set')
            self.trigger(instance, self._values[key], self._call_if(value))
            self._values[key] = value
            self._last_values[key] = self._call_if(self._values[key])

    def _call_if(self, func_or_var):
        if callable(func_or_var):
            return func_or_var()
        return func_or_var

    def trigger(self, instance, last_value, value):
        for call in self.callbacks:
            call(last_value, value)

    def add(self, callback):
        self.callbacks.append(callback)
        return self


class A(object):
    x = modifier(time.time).add(print)

    def __repr__(self):
        return f"<A({self.x})>"


a = A()
print("*", a.x)
print("*", a.x)
print("*", a.x)
print("*", a.x)

b = A()
print("^", b.x)

print('ok', A.x)
