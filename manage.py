import sys
import importlib


def main():
    if len(sys.argv) < 2:
        print("Usage: python manage.py <command>")
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    try:
        module = importlib.import_module(f"commands.{cmd}")
        module.run(args)
    except ModuleNotFoundError as e:
        print(f"Import failed: {e}")


if __name__ == "__main__":
    main()