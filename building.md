# building

To build this project, we use pyinstaller. There [is an issue with pyinstaller](https://stackoverflow.com/a/69521558) and python 3.10. I managed to get past that by ensuring I use the `--exclude-module _bootlocale` option.

`pyinstaller --onefile blind.py --exclude-module _bootlocale --windowed`