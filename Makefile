NAME_OF_TEST_FILE = test.py

all: test

test:
	python3 $(NAME_OF_TEST_FILE)

install:
	pip3 install Pillow

clean:
	rm -rf chem_drawer/__pycache__
