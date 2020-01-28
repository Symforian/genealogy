

# genealogy
## Requirements
The genealogy program requires graphviz and PyQt5

Installing graphviz:

    sudo apt-get install graphviz

Installing PyQt5:

    sudo apt-get install python3-pyqt5

Other dependencies are in `requirements.txt`.

Use:
	`pip install -r requirements.txt`

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

## Documentation
As for now only few files are documented:

    tree_env.py
    graph.py
    application.py
    tree_env.py
    program.py 


