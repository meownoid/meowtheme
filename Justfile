set shell := ["sh", "-cu"]

generate:
    PYTHONPATH=src python3 -m meowtheme generate meowtheme.yaml --out output

test:
    PYTHONPATH=src python3 -m unittest discover -s tests
