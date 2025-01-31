
## Python version
The Python version used to create the project is 3.12.7.

<br>

## Commands
At first, navigate to the folder named `py_version`. Open a terminal and run one of the following commands:

* #### Setup
For setup only.
```bash
python main.py --setup
```

* #### Setup & start
For setup and start the program after it.
```bash
python main.py --setup --start
```

* #### Start
After installing the virtual environment (which happens with `--setup` or `--setup --start`),<br>
you will be able to simply use one of these commands to quickly start the program:
```bash
python main.py --start
```
or
```bash
python main.py
```

* #### Force (setup & start)
The program could not start correctly due to the accidental deletion of one of the virtual environment files<br>
or an interruption during setup, which prevented it from finishing as expected.<br>
The following commands force the program to reinstall the entire environment,<br>
if any of these errors occur:
```bash
python main.py --setup --force
```

<br>

Also, the main purpose of the following command is to ensure the program starts correctly,<br>
even if any errors occur:
```bash
python main.py --start --force
```

* #### Rm files
Remove any existing output files placed inside the `documents` and `processing_files` directories while keeping the directory structure intact. 
```bash
python main.py --rm-files
```

* #### Rm venv
Remove the virtual environment directory `venv`. This directory needs an additional parent directory to avoid certain bugs when deleting python.exe.
```bash
python main.py --rm-venv
```

* #### Clear logs
Clear the logs stored in the `logs` directory. This flag can be used with others.
```bash
python main.py --clear-logs
```

* #### Rm files & rm venv & setup & start
Remove the files, delete the virtual environment directory, set up the new virtual environment, and start the program.
```bash
python main.py --rm-files --rm-venv --setup --start
```

<br>

*...and the rest is history.*

<br>
<br>

> Ignore .old entries.