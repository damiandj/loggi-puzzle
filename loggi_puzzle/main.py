import argparse

from model.loggi_puzzle_creator import LoggiPuzzleCreator


def prepare_args():
    parser = argparse.ArgumentParser(description='Create puzzle.')
    parser.add_argument('-ip', '--image-path', required=True,
                        help='image path')
    parser.add_argument('-size-x', '--puzzle-size-x', required=True,
                        help='Puzzle size x')
    parser.add_argument('-size-y', '--puzzle-size-y', required=True,
                        help='Puzzle size y')
    parser.add_argument('-sp', '--save-path', required=False, default='.',
                        help='Output save path')
    args = parser.parse_args()

    return args


def create_loggi_puzzle():
    args = prepare_args()

    lc = LoggiPuzzleCreator(image_path=args.image_path,
                            out_width=int(args.puzzle_size_x),
                            out_height=int(args.puzzle_size_y),
                            save_path=args.save_path)
    lc.prepare_loggi()


if __name__ == '__main__':
    create_loggi_puzzle()
