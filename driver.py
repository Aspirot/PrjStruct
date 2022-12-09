import time
import model


def add_tasks():
    for u in range(10):
        new = model.Task("Task " + str(u))
        temporary_list.append(new)


def get_current_time_temporary_list(current_time):
    current_time_tasks = []
    for t in temporary_list:
        if t.arriving_time == current_time:
            current_time_tasks.append(t)
    return current_time_tasks


if __name__ == '__main__':
    TaskPriorityQueue = model.PriorityQueue()
    OnHoldStack = model.Stack()
    temporary_list = []
    add_tasks()
    for t in temporary_list:
        print(str(t))
    current_task = None
    time_left = 60
    time_elapsed = 0
    while time_left > 0:
        for task in get_current_time_temporary_list(time_elapsed):
            TaskPriorityQueue.enqueue(task)
        if current_task is None:
            if TaskPriorityQueue.size() > 1:
                current_task = TaskPriorityQueue.dequeue()
                time.sleep(1)
                current_task.execution_time -= 1
                print("Running " + str(current_task))
            else:
                time.sleep(1)
                print("No task at the moment")
        else:
            if current_task.execution_time == 0:
                print("Finished " + str(current_task))
                if OnHoldStack.is_empty():
                    if TaskPriorityQueue.size() == 1:
                        current_task = None
                        time.sleep(1)
                        print("No task at the moment")
                    else:
                        current_task = TaskPriorityQueue.dequeue()
                        print("Starting " + str(current_task))
                        time.sleep(1)
                        current_task.execution_time -= 1
                        print("Running " + str(current_task))
                elif TaskPriorityQueue.size() == 1:
                    current_task = OnHoldStack.pop()
                    print("Starting " + str(current_task))
                    time.sleep(1)
                    current_task.execution_time -= 1
                    print("Running " + str(current_task))
                elif TaskPriorityQueue.first() < OnHoldStack.peek():
                    current_task = TaskPriorityQueue.dequeue()
                    print("Starting " + str(current_task))
                    time.sleep(1)
                    current_task.execution_time -= 1
                    print("Running " + str(current_task))
                else:
                    current_task = OnHoldStack.pop()
                    print("Starting " + str(current_task))
                    time.sleep(1)
                    current_task.execution_time -= 1
                    print("Running " + str(current_task))
            else:
                if TaskPriorityQueue.size() > 1:
                    if TaskPriorityQueue.first() < current_task:
                        print("Putting " + str(current_task) + " on hold")
                        OnHoldStack.push(current_task)
                        current_task = TaskPriorityQueue.dequeue()
                        print("Starting " + str(current_task))
                        time.sleep(1)
                        current_task.execution_time -= 1
                        print("Running " + str(current_task))
                    else:
                        time.sleep(1)
                        current_task.execution_time -= 1
                        print("Running " + str(current_task))
                else:
                    time.sleep(1)
                    current_task.execution_time -= 1
                    print("Running " + str(current_task))
        time_elapsed += 1
        time_left -= 1
    print("Process is terminated!")




