# py-open-fonts

[Open Fonts](https://github.com/kiwi0fruit/open-fonts) in pip and conda.

# Install

Needs python 3.6+

```bash
conda install -c defaults -c conda-forge py-open-fonts
```

or

```bash
pip install py-open-fonts
```


# API

### CLI

```
Usage: open-fonts-css [OPTIONS] [FONTS]

  Generates CSS source with @font-face definitions with absolute paths
  to fonts files as URL.

  Multiple FONTS like FontName can be provided. For example "FontName"
  argument means using $PYTHONPREFIX/fonts/open-fonts/css/FontName.css
  If none were provided then all fonts definitions from
  $PYTHONPREFIX/fonts/open-fonts/css would be used.

Options:
  -p, --pref TEXT   Generated CSS would have TEXT as prefix in URL to
                    fonts files (instead of default absolute path as URL).
                    Like: ${PREFIX}FontName.ttf ("<...>" to "TEXT"
                    replacement actually)
  -o, --out TEXT    Save CSS to TEXT filepath. "-" means write to stdout
                    (default behaviour)
  --help            Show this message and exit.
```

### open_fonts_css

```py
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
```
