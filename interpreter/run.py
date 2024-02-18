import sys
from pprint import pprint

from . import parse_text_from_file
from . import Parser
from . import evaluate


def run_file(lines: str) -> None:
    """Run file"""
    parser = Parser()
    program = parser.produce_ast(lines)
    result = evaluate(program)
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
