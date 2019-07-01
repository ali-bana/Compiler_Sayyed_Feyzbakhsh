from tools.parallel_parser import Parser


if __name__ == '__main__':
    p = Parser('program.txt')
    p.print_parsed()
    print("\n", p.semantic_errors)

