from numpy import random


class Task:
    def __init__(self, name, poisson_lam, exponential_scale):
        self.name = name
        self.priority = random.randint(0, 10)
        self.arriving_time = random.poisson(lam=poisson_lam)
        self.execution_time = int(random.exponential(scale=exponential_scale)) + 1

    def __str__(self):
        return f"{{name: {self.name}, priority: {self.priority}, execution_time: {self.execution_time}}}"

    def __repr__(self):
        return f"{{name: {self.name}, priority: {self.priority}, arriving_time: {self.arriving_time}, execution_time: "\
         f"{self.execution_time}}}"

    def __lt__(self, other):
        return self.priority < other.priority

    def __gt__(self, other):
        return self.priority > other.priority

    def __eq__(self, other):
        return self.priority == other.priority

    def __ne__(self, other):
        return not self.__eq__(other)
