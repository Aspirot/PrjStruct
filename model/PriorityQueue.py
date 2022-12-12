from model.MinHeap import MinHeap


class PriorityQueue:
    def __init__(self):
        self.__task_heap = MinHeap()

    def enqueue(self, task):
        self.__task_heap.insert(task)

    def first(self):
        return self.__task_heap.peek()

    def tasks(self):
        return self.__task_heap.tasks()

    def dequeue(self):
        if self.__task_heap.is_empty():
            raise ValueError("Queue is empty!")
        return self.__task_heap.remove()

    def size(self):
        return self.__task_heap.size()

    def __str__(self):
        to_return = "["
        for i in range(len(self.__task_heap.tasks())):
            to_return = to_return + str(self.__task_heap.tasks()[i])
            if i < len(self.__task_heap.tasks()) - 1:
                to_return = to_return + ',\n'
        return to_return + "]"

