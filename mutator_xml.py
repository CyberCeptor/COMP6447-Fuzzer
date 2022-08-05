from inspect import findsource
import subprocess
import sys
import threading
import numpy as np
from mutator_base import BaseMutator
import _thread as thread

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

# Test memory with a large XML to check for buffer overflow attacks with tag parsing.
'''
In a loop send large xml files to the process and wait for the exit code, and then check the exit code,
if an error has occured, found a weakness.
'''
# Creates a simple xml with the entities being multiplied by the number in the large range.
def XMLOverflow(program):
    xmlTemplate="""
    {tag1}
        {input}
    {tag2}
    """
    for number in range(20000, 50000, 2000):
        largeXML = xmlTemplate.format(tag1=("<tag>"*number), input=("<input>" * number), tag2=("</tag>" * number))
        try:
            p = subprocess.run(program, input=largeXML, timeout=1.0, capture_output=True)
            if p.returncode != 0:
                write_out_bad(input)
        except subprocess.TimeoutExpired:
            pass



lock = threading.Lock()
def write_out_bad(text: bytes):
    """
    Write out the failing text. Also acquire a lock and kill the fuzzer to stop
    it immediately and to prevent multiple writers.
    """
    lock.acquire() # never release so that nothing else can possibly write out.
    with open("bad.txt", "wb") as f:
        f.write(text)
    thread.interrupt_main()


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
def xmlBomb(program):
    xmlBomb = """
    <?xml version="1.0"?>
    <!DOCTYPE lolz [
    <!ENTITY lol "lol">
    <!ENTITY lol1 "&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;&lol;">
    <!ENTITY lol2 "&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;&lol1;">
    <!ENTITY lol3 "&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;&lol2;">
    <!ENTITY lol4 "&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;&lol3;">
    <!ENTITY lol5 "&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;&lol4;">
    <!ENTITY lol6 "&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;&lol5;">
    <!ENTITY lol7 "&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;&lol6;">
    <!ENTITY lol8 "&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;&lol7;">
    <!ENTITY lol9 "&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;&lol8;">
    <!ENTITY lolz "&lol9;">
    ]>
    <root>&lolz;</root>
    """
    try:
        p = subprocess.run(program, input=xmlBomb, timeout=1.0, capture_output=True)
        if p.returncode != 0:
            write_out_bad(input)
    except subprocess.TimeoutExpired:
        pass


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

# https://stackoverflow.com/questions/29596584/getting-a-list-of-xml-tags-in-file-using-xml-etree-elementtree
def findXMLTags(file):
    xmlTree = ET.parse(file)
    tags_list = []
    for tag in xmlTree.iter():
        tags_list.append(tag)

    # Remove duplicates to reduce time.
    tags_list = list(set(tags_list))

    return tags_list


# https://stackoverflow.com/questions/7465455/how-to-read-root-xml-tag-in-python
def findRootTag(file):
    et = ET.parse(file)
    root = et.getroot()
    return root



def changeRootTag(file, root):
    # print(root.tag)
    tree = ET.parse(file)
    for elem in tree.iter():
        if elem.tag == root.tag:
            elem.tag = "EEEE"

    # tree.write(file)


# https://stackoverflow.com/questions/54796054/xml-change-tag-name-using-python
# Goes through the file and modifies all of the tags in the file, except for the html tag.
def changeTags(file, tags_list):
    tree = ET.parse(file)

    for tag in tags_list:
        for elem in tree.findall(tag.tag):
            elem.tag = "Different TAG"
    
    # Writes to the file, changing the actual file.
    tree.write(file)
    return tree


def changeAttributes(file, tags_list):
    tree = ET.parse(file)

    for tag in tags_list:
        for elem in tree.iter():
            elem.attrib = {"":"%p"}

    # tree.write(file)





def main():

    file = sys.argv[1]
    tags_list = findXMLTags(file)
    # changeTags(file, tags_list)
    root = findRootTag(file)
    # changeAttributes(file, tags_list)

    changeRootTag(file, root)


main()