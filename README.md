# SoS language module for Apache UIMA Ruta

[SoS Notebook](https://github.com/vatlab/sos-notebook) is a [Jupyter](https://jupyter.org/) kernel that allows the use of multiple kernels in one Jupyter notebook. This module provides a language module for the [IRuta kernel](https://github.com/averbis/IRuta) that is based on the [Apache UIMA Ruta](http://uima.apache.org/ruta.html) programming language. 

## PIP installation

To install this repository from PyPI, use `pip install sos-ruta`. To install this repository from source, clone it and run `pip install .` in this directory. 

## Usage

### Transfering String variables from Python to Ruta

Using the `%expand` magic, one can transfer String variables from Ruta to Python Cells in the same notebook. Please see the example below.

#### Python Cell
```python
documentText = '"Patient has fevers, but no chills."'
problem_list = '"fevers|chills|nausea"'
newTypeName  = "Diagnosis"
```

#### Ruta Cell
``` Ruta
%expand
%documentText {documentText}
DECLARE {newTypeName};
{problem_list} -> {newTypeName};
COLOR({newTypeName},"green");
``` 

is automatically expanded to

``` Ruta
%documentText "Patient has fevers, but no chills."
DECLARE Diagnosis;
"fevers|chills|nausea" -> Diagnosis;
COLOR(Diagnosis,"green");
``` 
This annotates *"fevers"* and *"chills"* as annotations of type *"Diagnosis"*.

### Transfering an Apache UIMA Cas object from Python to Ruta and back

A Cas object holds information about the document text and all annotations together with a TypeSystem. They can be exchanged between UIMA Ruta and Python using the Python library [dkpro-cassis](https://github.com/dkpro/dkpro-cassis) and this sos-ruta package.

#### Sending a Cas from Python to Ruta

*(In a Python cell)* Load a UIMA Cas with dkpro-cassis.
```python
import cassis
with open('MyTypeSystem.xml', 'rb') as f:
    typesystem = cassis.load_typesystem(f)   
    
with open("MyCasExample.xmi", "rb") as f:
    cas1 = cassis.load_cas_from_xmi(f, typesystem=typesystem)
```

Transfer it to UIMA Cas using the `%get cas1` magic command in a Ruta Cell. This automatically loads the content of the variable `cas1` together with its TypeSystem into the current Cas in Ruta.

*(In a Ruta cell) Execute the following magic that is provided by sos-ruta to pass a Cas from Python to Ruta.* 
``` ruta
%get cas1`
```

One can for instance inspect the results with a basic AnnotationViewer using the magic `%displayMode DYNAMIC_HTML`. 

#### Sending a Cas from Ruta to Python

If required, the Cas object can be passed back to Python using `%put cas_output` which assigns the content of the current Cas in Uima Ruta to a variable named `cas_output` in Python.

*(In a Ruta cell) Execute the following magic that is provided by sos-ruta to pass the Cas from Ruta to Python.* 
``` ruta
%put cas_output
```

## Tests

The tests in this repository use Selenium and Google Chrome to simulate a Jupyter Notebook. Please read more about sos-notebook tests here: https://vatlab.github.io/sos-docs/doc/user_guide/language_module.html#Testing.