class MinHeap:
    def __init__(self):
        self.__tasks = [None]
        self.current_size = 0

    def insert(self, task):
        self.__tasks.append(task)
        self.current_size += 1
        self.heapify_up(self.current_size)

    def heapify_up(self, index):
        while index // 2 > 0:
            if self.__tasks[index] < self.__tasks[index // 2]:
                self.__tasks[index], self.__tasks[index // 2] = self.__tasks[index // 2], self.__tasks[index]
            index = index // 2

    def peek(self):
        return self.__tasks[1]

    def remove(self):
        to_remove = self.__tasks[1]
        self.current_size -= 1
        self.__tasks.pop(1)
        self.heapify_down(1)
        return to_remove

    def heapify_down(self, index):
        while (index * 2) <= self.current_size:
            min_child = self.min_child(index)
            if self.__tasks[index] > self.__tasks[min_child]:
                self.__tasks[index], self.__tasks[min_child] = self.__tasks[min_child], self.__tasks[index]
            index = min_child

    def min_child(self, index):
        if index * 2 + 1 > self.current_size:
            return index * 2
        else:
            if self.__tasks[index * 2] < self.__tasks[index * 2 + 1]:
                return index * 2
            else:
                return index * 2 + 1

    def tasks(self):
        return self.__tasks

    def is_empty(self):
        return len(self.__tasks) == 0

    def size(self):
        return len(self.__tasks)

