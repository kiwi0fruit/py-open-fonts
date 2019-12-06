import os.path as p
import sys
from .conda import conda


class PyOpenFontsError(Exception):
    pass


def open_fonts_css(*fonts: str, pref: str=None, out: str=None) -> str:
    """
    Generates CSS source with @font-face definitions with absolute paths
    to fonts files as URL.

    Multiple ``fonts`` like ``"FontName"`` can be provided. For example ``"FontName"``
    argument means using ``$PYTHONPREFIX/fonts/open-fonts/css/FontName.css``
    If none were provided (``fonts`` is ``()``) then all fonts definitions from
    ``$PYTHONPREFIX/fonts/open-fonts/css/`` would be used.

    :param pref:
        Generated CSS would have ``pref`` as prefix in URL to fonts files (instead
        of default absolute path as URL). Like: ``f"{pref}FontName.ttf"``
        ("<...>" to ``pref`` replacement actually).
    :param out:
        Save CSS to ``out`` filepath. ``"-"`` or ``None`` mean do nothing.

    :return: CSS source code
    """
    raise NotImplementedError


def default_prefix() -> str:
    """
    returns ``$PYTHONPREFIX/fonts/open-fonts/`` absolute path as URL ending with /.
    """
    import pathlib

    if conda:
        import os
        pyexedir = p.dirname(p.abspath(sys.executable))
        if os.name == 'nt':
            open_fonts = p.join(pyexedir, 'fonts', 'open-fonts')
        else:
            open_fonts = p.join(p.dirname(pyexedir), 'fonts', 'open-fonts')
    else:
        open_fonts = p.join(p.dirname(p.abspath(__file__)), 'open-fonts')
    if not p.isdir(open_fonts):
        raise PyOpenFontsError(f"'{open_fonts}' dir wasn't found.")

    return pathlib.Path(open_fonts).as_uri() + '/'


def cli():
    raise NotImplementedError


if __name__ == '__main__':
    cli()
