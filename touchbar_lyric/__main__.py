
import argparse
from touchbar_lyric import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Lyric script')
    parser.add_argument('--api', type=str, help='Random proxy for netease', default=None)
    parser.add_argument('--debug', action='store_true', help='Debug mode', default=False)

    args = parser.parse_args()
    main(api=args.api, debug=args.debug)
