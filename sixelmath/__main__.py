''' Command-line program to print tex to sixel '''
import argparse
import pathlib

from sixelmath import sixelmath, sixel_defaults


def main():
    parser = argparse.ArgumentParser(
        description='Render LaTeX math in terminal using sixel graphics')
    parser.add_argument(
        'tex', type=str, default='',
        help='LaTeX math expression')
    parser.add_argument(
        '-s', '--size', type=float, default=24,
        help='Font size')
    parser.add_argument(
        '-f', '--font', type=pathlib.Path, default=None,
        help='Path to TTF or OTF font with MATH tables')
    parser.add_argument(
        '-c', '--color', type=str, default=None,
        help='Font color as named color or hex #RRGGBB')
    parser.add_argument(
        '-b', '--bgcolor', type=str, default=None,
        help='Background color')
    parser.add_argument(
        '-m', '--margin', type=int, default=4,
        help='Pixel margin surrounding equation')

    args = parser.parse_args()
    sixel_defaults(
        font=args.font,
        fontsize=args.size,
        color=args.color,
        bgcolor=args.bgcolor,
        margin=args.margin)
    sixelmath(args.tex)
