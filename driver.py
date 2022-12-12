import time
import model


def add_tasks(amount):
    for u in range(amount):
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

    total_time = int(input("Entrer la durée de la simulation : "))
    time_elapsed = 0

    temporary_list = []
    amount_tasks = int(input("Entrer le nombre de tâches à créer : "))
    add_tasks(amount_tasks)
    for t in temporary_list:
        print(str(t))
    current_task = None

    kpi_intervals = []
    kpi_current_interval = 0

    kpi_service_time = 0

    kpi_waiting_time = dict()
    while time_elapsed < total_time:
        # kpi_waiting_time
        for task in TaskPriorityQueue.tasks():
            if task is not None:
                kpi_waiting_time[task.name] = 1 + kpi_waiting_time.get(task.name, 0)
        if not OnHoldStack.is_empty():
            for task in OnHoldStack.tasks():
                kpi_waiting_time[task.name] = 1 + kpi_waiting_time.get(task.name, 0)
        for task in get_current_time_temporary_list(time_elapsed):
            TaskPriorityQueue.enqueue(task)
            kpi_intervals.append(kpi_current_interval)
            kpi_current_interval = 0
        if current_task is None:
            if TaskPriorityQueue.size() > 1:
                current_task = TaskPriorityQueue.dequeue()
                print("-----Starting-----")
                time.sleep(1)
                current_task.execution_time -= 1
                kpi_service_time += 1
                print("Running  : " + str(current_task))
            else:
                time.sleep(1)
                print("Running  : No task at the moment")
        else:
            if current_task.execution_time == 0:
                print("-----Finished-----")
                if OnHoldStack.is_empty() and TaskPriorityQueue.size() == 1:
                    current_task = None
                else:
                    if OnHoldStack.is_empty():
                        current_task = TaskPriorityQueue.dequeue()
                    elif TaskPriorityQueue.size() == 1:
                        current_task = OnHoldStack.pop()
                    elif TaskPriorityQueue.first() < OnHoldStack.peek():
                        current_task = TaskPriorityQueue.dequeue()
                    else:
                        current_task = OnHoldStack.pop()
                    print("-----Starting-----")
            else:
                if TaskPriorityQueue.size() > 1 and TaskPriorityQueue.first() < current_task:
                    print("-----Holding-----")
                    OnHoldStack.push(current_task)
                    current_task = TaskPriorityQueue.dequeue()
                    print("-----Starting-----")
            if current_task is None:
                time.sleep(1)
                print("Running  : No task at the moment")
            else:
                time.sleep(1)
                current_task.execution_time -= 1
                kpi_service_time += 1
                print("Running  : " + str(current_task))
        time_elapsed += 1
        kpi_current_interval += 1
    print("Process is terminated!")
    print()
    kpi_average_interval = 0
    size = 0
    for interval in kpi_intervals:
        kpi_average_interval += interval
        size += 1
    kpi_average_interval = kpi_average_interval / size
    print("Average interval of arrivals is  : " + str(kpi_average_interval) + " time unit")
    kpi_average_service_time = kpi_service_time / total_time * 100
    print("Average service time is : " + str(kpi_average_service_time) + "%")
    kpi_average_waiting_time = 0
    for value in kpi_waiting_time.values():
        kpi_average_waiting_time += value
    kpi_average_waiting_time = kpi_average_waiting_time / size
    print("Average waiting time of tasks is  : " + str(kpi_average_waiting_time) + " time unit")

