import sys

from . import parse_text_from_file
from . import Parser
from . import evaluate
from . import Environment
from . import NumberVal
from . import MK_NUMBER, MK_NULL, MK_BOOL, ExtName
from . import get_default_modules

import time
def run_file(lines: str, env: Environment) -> None:
    """Run file"""
    parser = Parser()
    program = parser.produce_ast(lines)
    start = time.perf_counter()
    result = evaluate(program, env)
    end = time.perf_counter()
    if result.value is not None:
        print(result)
    
    print(f"runtime: {end - start}")
    
    # print(program.build())


def setup_env() -> Environment:
    """Setup environment"""
    default_modules = get_default_modules()
    env = Environment()
    for key, value in default_modules.items():
        env.declare_var(key, ExtName(value))
    env.declare_var('None', MK_NULL())
    env.declare_var('true', MK_BOOL(True))
    env.declare_var('false', MK_BOOL(False))
    return env


def run_command() -> None:
    """Run command"""
    args = sys.argv
    if len(args) <= 1:
        print("no file found, interactive shell launched")
        print("====diddy=====")
        env = setup_env()
        while True:
            line = input('>>> ')
            if line == 'exit':
                print("===diddied====")
                break
            run_file(line, env)
    else:
        filename = args[1]
        lines = parse_text_from_file(filename)

        env = setup_env()
        run_file(lines, env)
