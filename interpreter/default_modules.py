"""
In this file we define default modules for the interpreter
"""
import random
def get_default_modules() -> dict:
    modules = {
        "print": print,
        "random": random.randint,
        "input": input,
    }

    return modules