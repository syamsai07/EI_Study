from datetime import datetime,timedelta

# Memento Pattern
class Memento:
    def __init__(self, state):
        self.state = state

class Originator:
    def __init__(self):
        self.state = []

    def create_memento(self):
        return Memento(self.state.copy())

    def set_memento(self, memento):
        self.state = memento.state

# Builder Pattern
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.set_due_date(due_date)
        return self

    def set_tags(self, tags):
        self.task.set_tags(tags)
        return self

    def build(self):
        return self.task

# Task Class
class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False
        self.due_date = None
        self.tags = []

    def set_due_date(self, due_date):
        self.due_date = due_date

    def set_tags(self, tags):
        self.tags = tags

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        info = f"{self.description} - {status}"
        if self.due_date:
            info += f", Due: {self.due_date}"
        if self.tags:
            info += f", Tags: {', '.join(self.tags)}"
        return info

# To-Do List Manager
class ToDoListManager:
    def __init__(self):
        self.tasks = []
        self.memento_caretaker = Originator()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_state()

    def mark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.mark_completed()
                self.save_state()
                return
        print("Task not found")

    def delete_task(self, description):
        self.tasks = [task for task in self.tasks if task.description != description]
        self.save_state()

    def view_tasks(self, filter_type="all"):
        if filter_type == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_type == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        else:
            filtered_tasks = self.tasks

        for task in filtered_tasks:
            print(task)

    def mark_completed(self, description):
        for task in self.tasks:
            if task.description == description:
                task.mark_completed()
                self.save_state()
                return
        print("Task not found")

    def save_state(self):
        memento = self.memento_caretaker.create_memento()
        self.memento_caretaker.set_memento(memento)

# Example Usage
if __name__ == "__main__":
    todo_manager = ToDoListManager()

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. View Tasks")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date_str = input("Enter due date (YYYY-MM-DD), or leave blank: ")
            tags_str = input("Enter tags (comma-separated), or leave blank: ")

            due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None
            tags = tags_str.split(",") if tags_str else []

            task = TaskBuilder(description).set_due_date(due_date).set_tags(tags).build()
            todo_manager.add_task(task)
            print("Task added successfully!")

        elif choice == "2":
            description = input("Enter task description to mark as completed: ")
            todo_manager.mark_completed(description)

        elif choice == "3":
            description = input("Enter task description to delete: ")
            todo_manager.delete_task(description)

        elif choice == "4":
            filter_type = input("Enter filter type (all/completed/pending): ")
            todo_manager.view_tasks(filter_type)

        elif choice == "5":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

    # Additional: Display tasks as completed or pending based on current date
    current_date = datetime.now()
    print("\nTasks Status:")
    for task in todo_manager.tasks:
        status = "Completed" if task.completed or (task.due_date and task.due_date < current_date) else "Pending"
        print(f"{task.description} - {status}")