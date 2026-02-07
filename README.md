# sixelmath

Render LaTeX Math expressions or Sympy objects in the terminal using sixel graphics.
Math rendering is done using [ziamath](https://ziamath.readthedocs.io), a pure-Python LaTeX math renderer that does not require a Latex installation.
Any math-enabled truetype/opentype font may be used; STIXTwoMath-Regular is included and used by default.
Also uses [cairosvg](https://pypi.org/project/CairoSVG/), [timg](https://pypi.org/project/timg/), and [Pillow](https://pypi.org/project/pillow/).

See list of sixel-supported terminal emulators [here](https://www.arewesixelyet.com).


## Usage

Installation:

    pip install sixelmath


### Command Line

Render a LaTeX expression:

    sixelmath "\frac{1}{1+x}"

Options include:

* '-s': Font size in points
* '-f': Path to font file (must include MATH table)
* '-c': Color as a supported named color, or hex value such as `#FFFFFF`
* '-b': Background color as a supported named color, or hex value such as `#FFFFFF`
* '-m': Margin width in pixels

In POSIX environments, the font and background color are detected automatically if not manually specified.


### Python

To render LaTeX from Python code:

    from sixelmath import sixelmath
    sixelmath(r'\frac{1}{1+x}')
    
Keyword arguments may be passed to `sixelmath` to change options:

* `color`: Font color. A named terminal color like 'white', or RGB hex color such as `#FFFFFF`
* `bgcolor`: Background color.
* `font`: Path to a TTF or OTF font file. Must contain a MATH table. STIXTwoMath-Regular is used by default.
* `fontsize`: Font size in pixels
* `margin`: Pixel margin around the euqation


### Sympy

Import the `sixelmath.sympysixel` module to install a Sympy Printer that automatically displays Sympy expressions as sixel graphics.

    import sympy
    from sixelmath import sympysixel
    sympy.sympify('A * exp(-x^2)')


To change display format, use `sixelmath.sixel_defaults`, with the same keyword arguments listed above for `sixelmath`.
The sixel printer may be turned off using `sympysixel.disable()` and turned on with `sympysixel.enable()`.
