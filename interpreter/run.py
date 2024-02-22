import sys
from pprint import pprint

from . import parse_text_from_file
from . import Parser
from . import evaluate
from . import Environment
from . import NumberVal
from . import MK_NUMBER, MK_NULL, MK_BOOL


def run_file(lines: str) -> None:
    """Run file"""
    parser = Parser()
    env = Environment()
    env.declare_var('x', MK_NUMBER(100))
    env.declare_var('None', MK_NULL())
    env.declare_var('true', MK_BOOL(True))
    env.declare_var('false', MK_BOOL(False))
    program = parser.produce_ast(lines)
    result = evaluate(program, env)
    print(result)
    # pprint(program.ast, sort_dicts=False, width=5)
    # print(program.build())


def run_command() -> None:
    """Run command"""
    args = sys.argv
    if len(args) <= 1:
        print("no file found, interactive shell launched")
        print("====shell=====")
        while True:
            line = input('>>> ')
            if line == 'exit':
                print("===shelled====")
                break
            run_file(line)
    else:
        filename = args[1]
        lines = parse_text_from_file(filename)

        run_file(lines)
