# Catena Vetus

A Terminal User Interface frontend for [Historical Christian Commentaries](https://historicalchristian.faith/) which does not require an internet
connection. This software is best used with a mouse, if you intend to use the table of contents, otherwise a keyboard will serve you well!

### [Gallery](https://imgur.com/a/KA3IkJV)

![Commentaries on John 3:16](https://i.imgur.com/KkwDODE.png)

![Screenshot showing the use of the table of contents](https://i.imgur.com/kqmMtNB.png)

### Credits

- @emeth- without whom this project would be impossible! This project utilises
  his [massive database](https://github.com/HistoricalChristianFaith/Commentaries-Database)!
- @davep for [helping me with textual](https://github.com/Textualize/textual/discussions/2853).
- Everyone on the Catholic Diocese of Discord!

### Setup

I'd thoroughly recommend you use a powerful terminal for this. Your default system one probably won't be the best experience. On Windows, go ahead and
get a copy of [Windows Terminal](https://github.com/microsoft/terminal). On Linux, get a copy of [Alacritty](https://github.com/alacritty/alacritty).

#### Easy Option

If you are windows you can download the `pyinstaller` exe file and the database file from the releases page. Place these in the same folder (make sure
the database file is called `commentaries.db`). Then open a Powershell window (preferably
use [Windows Terminal](https://github.com/microsoft/terminal) because it will work far better) in the same directory and execute the exe.

#### Do It Yourself

1. Download a copy of the code from GitHub (
   Follow [this guide](https://docs.github.com/en/repositories/working-with-files/using-files/downloading-source-code-archives) if you are unsure how
   to do this)
2. Unzip this into a new folder (
   Follow [this windows guide](https://support.microsoft.com/en-us/windows/zip-and-unzip-files-f6dde0a7-0fec-8294-e1d3-703ed85e7ebc) if you are unsure
   how to
   do this).
3. Install a copy of Python 3 (Head to [python.org](https://www.python.org/) if you are unsure how to do this) . I'd recommend Python 3.9 or 3.10 if
   you can, but any `Python >= 3.7` should work.
4. Open a terminal and head to the folder you downloaded this software to. Run `python -m venv venv` and then if you are on
   Windows `.\venv\Scripts\activate` and if on unix `source ./venv/bin/activate`.
5. Type `pip install -r requirements.txt`
6. Either download the database from the releases page or [compile your own](https://github.com/HistoricalChristianFaith/Commentaries-Database). Move
   the database file to be in the same folder as `main.py` with the name `commentaries.db`.
7. Run from your terminal window `python main.py`.
8. Enjoy!

#### Developers

##### Running the tests

You can run the unit tests using the following commands.

```shell
pip install -e '.[dev]'
pytest
```

If you want to compile your own binary, you can use `pyinstaller`.

On Windows:

```commandline
> pyinstaller --clean --onefile --add-data "main.css;." .\main.py
```

On Linux:

```commandline
pyinstaller --clean --onefile --add-data "main.css:." .\main.py
```
