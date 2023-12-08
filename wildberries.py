from sys import argv
import settings


def main() -> None:
    product: list[str] = argv[1:]
    settings.parsing(product=product)


if __name__ == '__main__':
    main()
