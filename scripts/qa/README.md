# QA

This is a script written to check if slides on disk are also in the mongo database

## Python virutal environment
This script uses a few python packages that should be installed in a python virtual environment

To create a virtual environment:

```python3 -m venv ./```

This will create a virtual environment in your current directory and name it according to the name of your directory

To install the packages needed: 

```pip3 install -r requirements.txt```

## How to use
1. Copy the .env.example in this directory and rename it to .env

2. Edit the .env file as needed

3. Create a text file

4. Place participant ids inside of the text file and separate them by newline

5. ```python3 qa_dpr_pp.py -f <path_to_participants>.txt```