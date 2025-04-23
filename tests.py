from printer import test_ast_printer
from parser import test_parser
from scanner import test_scan


def test_all_runnable():
    print("Running tests...")

    print("-" * 80)
    print("Test scanner...")
    test_scan()

    print("-" * 80)
    print("test printer...")
    test_ast_printer()

    print("-" * 80)
    print("Test parser...")
    test_parser()


def main():
    test_all_runnable()


if __name__ == "__main__":
    main()
