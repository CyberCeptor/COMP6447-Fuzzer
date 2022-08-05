import numpy as np
from mutator_base import BaseMutator

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET


# xml bomb
'''
external xml bomb, inside the actual message being sent,
or a xml attachment
Overloads an XML Parser (typicall HTTP server).
exploits xml allowing defining entities.
    E.g. Let 'entityOne' be defines as 20 'entityTwo's', with entityTwo being defined as
        20 entityThree's, and so on. If continued until entityEight, the XML parser will unfold
        a single occurrance of entityOne to 1 280 000 000 entityEights (*Gb), causing DOS.
'''

# XML Root Tag
''' each xml has exactly one 'root element', enclosing all other elements, thus being the parent (ROOT).
Removing an ending tag? 
Change all tags, see what happens
'''

# Create a method to find all tags
'''
Using xml.etree.ElementTree: API for parsing and creating XML data.
using fromString to create a list of tags???
Loop through and set all of the tags to be a pre-determined tag multiplied.
'''

# Test memory with a large XML to check for buffer overflow attacks with tag parsing.
'''
In a loop send large xml files to the process and wait for the exit code, and then check the exit code,
if an error has occured, found a weakness.
'''