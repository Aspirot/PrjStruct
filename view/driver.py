import time
import model


# Fait par Denis Aspirot et William Guilbault

# Method to add tasks
def add_tasks(amount, time_to_add, exponential_scale):
    poisson_lam = 0
    for u in range(amount):
        new = model.Task("Task " + str(u), poisson_lam, exponential_scale)
        temporary_list.append(new)
        poisson_lam += time_to_add


# Method to return tasks with same arriving_time as current_time
def get_current_time_temporary_list(current_time):
    current_time_tasks = []
    for t in temporary_list:
        if t.arriving_time == current_time:
            current_time_tasks.append(t)
    return current_time_tasks


# Driver
if __name__ == '__main__':
    # Variable Initialisation
    TaskPriorityQueue = model.PriorityQueue()
    OnHoldStack = model.Stack()
    total_time = int(input("Entrer la durée de la simulation : "))
    time_elapsed = 0
    estimated_amount_of_tasks = int(input("Entrer le nombre de tâches faites dans la durée en général : "))
    temporary_list = []
    amount_tasks = int(input("Entrer le nombre de tâches à créer : "))
    add_tasks(amount_tasks, total_time/amount_tasks, total_time/estimated_amount_of_tasks)
    for t in temporary_list:
        print(repr(t))
    current_task = None

    # KPI variables initialisations
    kpi_intervals = []
    kpi_current_interval = 0
    kpi_service_time = 0
    kpi_waiting_time = dict()
    kpi_max_size = 0
    kpi_tasks_finished = 0

    while time_elapsed < total_time:
        # kpi_waiting_time for the Queue
        for task in TaskPriorityQueue.tasks():
            if task is not None:
                kpi_waiting_time[task.name] = 1 + kpi_waiting_time.get(task.name, 0)
        # kpi_waiting_time for the Stack
        if not OnHoldStack.is_empty():
            for task in OnHoldStack.tasks():
                kpi_waiting_time[task.name] = 1 + kpi_waiting_time.get(task.name, 0)
        # Add tasks with same arriving_time as current_time to the Queue
        for task in get_current_time_temporary_list(time_elapsed):
            TaskPriorityQueue.enqueue(task)
            kpi_intervals.append(kpi_current_interval)
            kpi_current_interval = 0

        # Check if the size of the queue is bigger than kpi_max_size and replace kpi_max_size if it was
        if TaskPriorityQueue.size() - 1 > kpi_max_size:
            kpi_max_size = TaskPriorityQueue.size() - 1

        # Check if no tasks were being run
        if current_task is None:
            # If there are tasks in the Queue, start the first tasks of the queue
            if TaskPriorityQueue.size() > 1:
                current_task = TaskPriorityQueue.dequeue()
                print("-----Starting-----")
                time.sleep(1)
                current_task.execution_time -= 1
                kpi_service_time += 1
                print("Running  : " + str(current_task))
            # Else, wait
            else:
                time.sleep(1)
                print("Running  : No task at the moment")
        # If a task was being run
        else:
            # If the task is donne
            if current_task.execution_time == 0:
                kpi_tasks_finished += 1
                print("-----Finished-----")
                # If both the Queue and the Stack are empty, make the current_task None
                if OnHoldStack.is_empty() and TaskPriorityQueue.size() == 1:
                    current_task = None
                else:
                    # If only the Stack is empty, take from the Queue
                    if OnHoldStack.is_empty():
                        current_task = TaskPriorityQueue.dequeue()
                    # Else, if only the queue is empty, take from the Stack
                    elif TaskPriorityQueue.size() == 1:
                        current_task = OnHoldStack.pop()
                    # Else, if the first from the Queue is more important than the one from the Stack, take from it
                    elif TaskPriorityQueue.first() < OnHoldStack.peek():
                        current_task = TaskPriorityQueue.dequeue()
                    # Else, take from the Stack
                    else:
                        current_task = OnHoldStack.pop()
                    print("-----Starting-----")
            # If the task is not done
            else:
                # If the Queue is not empty and its first is more important than the current_task, switch
                if TaskPriorityQueue.size() > 1 and TaskPriorityQueue.first() < current_task:
                    print("-----Holding-----")
                    OnHoldStack.push(current_task)
                    current_task = TaskPriorityQueue.dequeue()
                    print("-----Starting-----")
            # If the task is none, wait
            if current_task is None:
                time.sleep(1)
                print("Running  : No task at the moment")
            # Else, run the current_task
            else:
                time.sleep(1)
                current_task.execution_time -= 1
                kpi_service_time += 1
                print("Running  : " + str(current_task))
        time_elapsed += 1
        kpi_current_interval += 1
    # Check if the last task was finished, and add 1 to the kpi for the amount of finished tasks
    if current_task is not None and current_task.execution_time == 0:
        kpi_tasks_finished += 1
        print("-----Finished-----")
    print("Process is terminated!")
    print()

    # KPI for the average interval of the arrivals
    kpi_average_interval = 0
    size = 0
    for interval in kpi_intervals:
        kpi_average_interval += interval
        size += 1
    kpi_average_interval = kpi_average_interval / size
    kpi_average_interval = round(kpi_average_interval * 100) / 100
    print("Average interval of arrivals is  : " + str(kpi_average_interval) + " time unit")

    # KPI for the average service time
    kpi_average_service_time = kpi_service_time / total_time
    print("Average service time is : " + str(kpi_average_service_time) + " per time unit")

    # KPI for the average waiting time
    kpi_average_waiting_time = 0
    kpi_amount_waited = 0
    for value in kpi_waiting_time.values():
        kpi_average_waiting_time += value
        kpi_amount_waited += 1
    kpi_average_waiting_time = kpi_average_waiting_time / size
    kpi_average_waiting_time = round(kpi_average_waiting_time * 100) / 100
    print("Average waiting time of tasks is  : " + str(kpi_average_waiting_time) + " time unit")

    # KPI for the all-time maximum size of the Queue
    print("The maximum size of the queue was : " + str(kpi_max_size))

    # KPI for the probability a task will have to wait, either in the Queue or the Stack
    kpi_probability_tasks = kpi_amount_waited / amount_tasks * 100
    kpi_probability_tasks = round(kpi_probability_tasks * 100) / 100
    print("Probability to wait is : " + str(kpi_probability_tasks) + "%")
