
### Python

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

* #### Force
The program could not start correctly due to the accidental deletion of one of the virtual environment files<br>
or an interruption during setup, which prevented it from finishing as expected.<br>
These commands force the program to reinstall the entire environment, if any errors occur:
```bash
python main.py --setup --force
```

<br>

However, the main purpose of the command below is to ensure the program runs properly,<br>
even if any errors are displayed at the beginning:
```bash
python main.py --start --force
```

<br>

*...and the rest is history.*

<br>
<br>

> Ignore .old entries.