#!/bin/sh

echo "Installing requirements"
pip install -r requirements.txt

echo "Installing nltk dependencies"
python install.py

echo "Creating dataset"
python construct-final-dataset.py

echo "Text preprocessing"
python text-filter-frequent-words.py
