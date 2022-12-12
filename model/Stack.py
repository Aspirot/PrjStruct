import ctypes


class Stack(object):
    def __init__(self, capacity: int = 100):
        self.__capacity = capacity
        self.__items = Stack.build_array(self.__capacity)
        # top: index of the last added item
        self.__top = -1

    def push(self, item):
        # check for overflow
        if self.__top >= self.__capacity:
            print('Error: Can not push item. Stack Overflow')
        self.__top += 1
        self.__items[self.__top] = item

    def pop(self):
        if self.__top < 0:
            print('Error: Can not pop item. Stack Underflow')
            return None
        self.__top -= 1
        return self.__items[self.__top + 1]

    def peek(self):
        if self.__top < 0:
            print('Error: Can not read item. Stack Underflow')
            return None
        return self.__items[self.__top]

    top = peek

    def tasks(self):
        to_return = []
        for i in range(self.__top + 1):
            to_return.append(self.__items[i])
        return to_return

    def is_empty(self):
        if self.__top == -1:
            return True
        return False

    @staticmethod
    def build_array(new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __str__(self):
        to_return = "["
        for i in range(self.__top + 1):
            to_return = to_return + str(self.__items[i])
            if i < self.__top:
                to_return = to_return + ","
        return to_return + ']'
