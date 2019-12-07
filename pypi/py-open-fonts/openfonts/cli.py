from typing import Tuple, Optional as Opt
import sys
import os
import os.path as p
import sys
import click
from .conda import conda


class PyOpenFontsError(Exception):
    pass


def open_fonts_dir() -> str:
    if conda:
        import os
        pyexedir = p.dirname(p.abspath(sys.executable))
        if os.name == 'nt':
            open_fonts = p.join(pyexedir, 'fonts', 'open-fonts')
        else:
            open_fonts = p.join(p.dirname(pyexedir), 'fonts', 'open-fonts')
    else:
        open_fonts = p.join(p.dirname(p.abspath(__file__)), 'open-fonts')
    return open_fonts


def open_fonts_css(*fonts: str, pref: str=None, out: str=None) -> str:
    """
    Generates CSS source with @font-face definitions with absolute paths
    to fonts files as URL.

    Multiple ``fonts`` like ``"FontName"`` can be provided. For example ``"FontName"``
    argument means using ``$PYTHONPREFIX/fonts/open-fonts/css/FontName.css``
    If none were provided (``fonts`` is ``()``) then all fonts definitions from
    ``$PYTHONPREFIX/fonts/open-fonts/css/`` would be used.

    Note that spaces would be removed from provided font names and CSS files
    do not contain spaces in their names. 

    :param pref:
        Generated CSS would have ``pref`` as prefix in URL to fonts files (instead
        of default absolute path as URL). Like: ``f"{pref}FontName.ttf"``
        ("<...>" to ``pref`` replacement actually).
    :param out:
        Save CSS to ``out`` filepath. ``"-"`` or ``None`` mean do nothing.

    :return: css_source if (out in (None, '-')) else ''
    """
    open_fonts = open_fonts_dir()
    if not p.isdir(open_fonts):
        raise PyOpenFontsError(f"'{open_fonts}' dir wasn't found.")
    css_dir = p.join(open_fonts, 'css')
    if not p.isdir(css_dir):
        raise PyOpenFontsError(f"'{css_dir}' dir wasn't found.")

    # preprocess arguments:
    # ---------------------------
    if pref is None:
        import pathlib
        pref_ = pathlib.Path(open_fonts).as_uri() + '/'
    else:
        pref_ = pref
    if out == '-':
        out = None
    elif out == '':
        raise ValueError('out should not be an empty string')
    if not fonts:
        fonts = tuple(f[:-4] for f in os.listdir(css_dir)
                      if p.isfile(p.join(css_dir, f)) and f.endswith('.css'))
        if not fonts:
            raise PyOpenFontsError(f'*.css files were not found in {css_dir}')
    else:
        fonts = tuple(font.replace(' ', '') for font in fonts)
        for f in fonts:
            if not f:
                raise ValueError('empty or space-only font name was provided')

    # create CSS source code:
    # ---------------------------
    css_list = []
    for font in fonts:
        with open(p.join(css_dir, font + '.css'), 'r', encoding='utf-8') as f:
            css_list.append(f.read().replace('<...>', pref_))
    css_source = '\n\n'.join(css_list)
    if out:
        print(css_source, file=open(out, 'w', encoding='utf-8'))
        return ''

    return css_source


@click.command(help="""Generates CSS source with @font-face definitions with
absolute paths to fonts files as URL.

Multiple FONTS like FontName can be provided. For example "FontName"
argument means using $PYTHONPREFIX/fonts/open-fonts/css/FontName.css
If none were provided then all fonts definitions from
$PYTHONPREFIX/fonts/open-fonts/css/ would be used.

Note that spaces would be removed from provided font names and CSS files
do not contain spaces in their names.""")
@click.argument('fonts', nargs=-1, required=False)
@click.option('-p', '--pref', type=str, default=None,
              help='Generated CSS would have TEXT as prefix in URL to fonts files (instead of '
                   + 'default absolute path as URL). Like: ${PREFIX}FontName.ttf ("<...>" to "TEXT"'
                   + 'replacement actually)')
@click.option('-o', '--out', type=str, default=None,
              help='Save CSS to TEXT filepath. "-" means write to stdout (default behaviour)')
def cli(fonts: Tuple[str, ...], pref: Opt[str], out: Opt[str]):
    css_source = open_fonts_css(*fonts, pref=pref, out=out)
    if css_source:
        sys.stdout.write(css_source)
