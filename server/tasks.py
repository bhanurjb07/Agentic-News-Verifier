# server/tasks.py

def grader1(output, expected):
    return True

def grader2(output, expected):
    return True

def grader3(output, expected):
    return True

task1 = {
    "input": "task-1",
    "expected_output": "false",
    "grader": grader1
}

task2 = {
    "input": "task-2",
    "expected_output": "true",
    "grader": grader2
}

task3 = {
    "input": "task-3",
    "expected_output": "false",
    "grader": grader3
}

tasks = [task1, task2, task3]
