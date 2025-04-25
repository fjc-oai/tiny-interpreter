from printer import test_ast_printer
from parser import test_parser
from scanner import test_scan
from interpreter import test_interpreter
from utils import color_print

def test_all_runnable():
    print("Running tests...")

    print("-" * 80)
    print(color_print("Test scanner...", "green"))
    test_scan()

    print("-" * 80)
    print(color_print("Test printer...", "green"))
    test_ast_printer()

    print("-" * 80)
    print(color_print("Test parser...", "green"))
    test_parser()

    print("-" * 80)
    print(color_print("Test interpreter...", "green"))
    test_interpreter()


def main():
    test_all_runnable()


if __name__ == "__main__":
    main()
