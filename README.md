### Here will be a name of this text editor

## Description

In future, this project will be a simple text editor, that will support Latex and Markdown. But also he will has a plugin, that will add images of organic compounds to .pdf files by their SMILES code.

## Progress

Now, we actually wrote a small part of code. It can draw a chemical structure by their SMILES code. You only need to write some lines of python code:

```python
# Import necessary libraries
from chem_drawer.compound import Compound
from chem_drawer.drawer import Drawer

# Draw a acethone for example
Drawer().genImage(Compound("CC(=O)C").generate())
```



## Installing

1. Clone this repository for your computer:

```bash
git clone https://github.com/IvanBespalov64/chem_drawer
```

2. Run in shell:

```bash
make install
```

3. Run your scripts
