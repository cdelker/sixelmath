''' Render LaTeX math expressions as sixel graphics '''
import io
import os
from functools import partial

import cairosvg
import timg
import ziamath as zm


def _sixelmath(
    tex,
    fontsize,
    font,
    color,
    bgcolor,
    margin
):
    ''' Print LaTeX math expression to sixel

        Args:
            tex: LaTeX expression to render
            fontsize: Font size in points
            font: Path to font file with MATH table.
                STIXTwoMath-Regular used by default.
            color: Font color as named color or hex #RRGGBB
            bgcolor: Background color
            margin: Pixel margin around equation
    '''
    svg = zm.Latex(
        tex,
        font=font,
        size=fontsize,
        color=color,
        margin=margin
    ).svg()
    png = cairosvg.svg2png(svg, background_color=bgcolor)
    renderer = timg.Renderer()
    renderer.load_image_from_file(io.BytesIO(png))
    renderer.render(timg.SixelMethod)


sixelmath = partial(
    _sixelmath, fontsize=24, font=None,
    color='#fcfcfc', bgcolor='#232627',
    margin=4)
sixelmath.__doc__ = _sixelmath.__doc__


def sixel_defaults(
    fontsize=None,
    font=None,
    color=None,
    bgcolor=None,
    margin=None
):
    ''' Set default parameters. Use None to leave unchanged.

        Args:
            fontsize: Font size in points
            font: Path to font file with MATH table
            color: Font color as named color or hex #RRGGBB
            bgcolor: Background color
            margin: Pixel margin around equation
    '''
    if fontsize:
        sixelmath.keywords['fontsize'] = fontsize
    if font:
        sixelmath.keywords['font'] = font
    if color:
        sixelmath.keywords['color'] = color
    if bgcolor:
        sixelmath.keywords['bgcolor'] = bgcolor
    if margin is not None:
        sixelmath.keywords['margin'] = margin


if os.name == 'posix':
    # Detect terminal foreground/background colors.
    # Only works on POSIX, and may not supoprt all terminals.
    from . import querycolor
    fg = querycolor.get_default_fg()
    bg = querycolor.get_default_bg()
    if fg is not None:
        sixel_defaults(color=fg)
    if bg is not None:
        sixel_defaults(bgcolor=bg)
