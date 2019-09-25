import argparse

from model import LoggiPuzzleCreator


def create_loggi_puzzle():
    parser = argparse.ArgumentParser(description='Create puzzle.')
    parser.add_argument('-ip', '--image-path',
                        help='image path')
    parser.add_argument('-size-x', '--puzzle-size-x',
                        help='Puzzle size x')
    parser.add_argument('-size-y', '--puzzle-size-y',
                        help='Puzzle size y')
    args = parser.parse_args()

    lc = LoggiPuzzleCreator(image_path=args.image_path,
                            out_width=int(args.puzzle_size_x),
                            out_height=int(args.puzzle_size_y))
    lc.prepare_loggi()


if __name__ == '__main__':
    create_loggi_puzzle()
