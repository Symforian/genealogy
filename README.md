
# genealogy
## Requirements
The genealogy program requires graphviz and PyQt5 
Installing graphviz:

    sudo apt-get install graphviz

Installing PyQt5:

    sudo apt-get install python3-pyqt5
 Other dependencies should be in virtual environment.

## Running
Enter the virtual environment

	source venv_gene/bin/activate
Run the genealogy program

	python3 application.py

> Note:
> For command line interface use:
> `python3 program.py -c` 


## Tests
Run

	python3 -m unittest tests_tree_env.py

