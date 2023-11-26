from sys import argv
import parser


def main() -> None:
    parser.create_csv()
    space: str = '%20'
    product: str = space.join(argv[1:])
    parser.parsing(product=product)
        


if __name__ == '__main__':
    main()
