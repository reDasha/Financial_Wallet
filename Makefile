.PHONY: all clean test

all: run

run:
	python main.py

test:
	python -m unittest discover -s . -p "test_*.py"

clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

.SILENT:
