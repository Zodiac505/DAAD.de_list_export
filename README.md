# DAAD.de list export
This piece of code can be used to export German univesity programs from DAAD.de website.
It gets a search term from user and shows possible filters based on it and exports university programs to an excel file.

How to install locally (assuming you have git and python >= 3.9 installed):

```console
git clone https://github.com/Zodiac505/DAAD.de_list_export.git
cd DAAD.de_list_export
pipenv install
pipenv shell
```

To run:

```console
pipenv run python Main.py