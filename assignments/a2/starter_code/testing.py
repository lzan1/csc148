import csv
from typing import List, Dict

from tm_trees import TMTree

DATA_FILE = 'cs1_papers.csv'

def a() -> Dict:
    dic = {}
    cats = []
    with open(DATA_FILE, newline='') as csvfile:
        load_file = csv.reader(csvfile, delimiter=',')
        next(load_file)
        for row in load_file:
            cats.append([row[2]] + row[3].split(': ') + [
                load_file.line_num])
    return cats

e = a()
print(e)

def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.
    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    dic = {}
    cats = []

    with open(DATA_FILE, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for row in csv_reader:
            if by_year:
                cats.append([row[2]] + row[3].split(': ') + [
                    csv_reader.line_num])
            else:
                cats.append(row[3].split(': ') + [csv_reader.line_num])
    return cats

b = _load_papers_to_dict()
print(b == e)
