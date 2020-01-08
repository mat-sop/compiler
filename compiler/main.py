import sys
from parser import parser

from process import determine_jumps


def main():
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except Exception:
        print('Not enoght arguments')
        exit()

    with open(input_file, 'r') as f:
        input_data = f.read()

    result = parser.parse(input_data, tracking=True)
    result = determine_jumps(result)

    print(result)
    with open(output_file, 'w') as f:
        f.write('\n'.join(result))


if __name__ == '__main__':
    main()
