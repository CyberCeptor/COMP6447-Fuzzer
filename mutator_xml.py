import copy
import sys
from mutator_base import BaseMutator
import numpy as np

# https://docs.python.org/3/library/xml.etree.elementtree.html
import xml.etree.ElementTree as ET

class xmlOverFlowMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        number = int.from_bytes(input[0].tobytes()[2:4], "little")
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


class AttributeMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return AttributeMutator.changeAttributes(text, "A" * int.from_bytes(input[0].tobytes()[2:4], "little"))

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

class HREFAttributeMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)

        for element in tree.iter():
            if 'href' in element.attrib:
                print(element.attrib)
                element.attrib['href'] = "%p" * int.from_bytes(input[0].tobytes()[2:4], "little")

        return ET.tostring(tree)
    
    def get_dimension(self) -> "int":
        return 0 # ???


class TagMutator():
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        return TagMutator.changeTags(text, "A" * int.from_bytes(input[0].tobytes()[2:4], "little"))

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
                elem.tag = "A" * int.from_bytes(input[0].tobytes()[2:4], "little")

        return ET.tostring(tree)

    #returns the root tag.
    def get_RootTag(sample_text):
        tree = ET.ElementTree(ET.fromstring(sample_text))
        root = tree.getroot()
        return root
    
# Add's a copy of the xml the end of the xml multiple times.
class XMLChildrenMutator(BaseMutator):
    def get_mutation(self, text: bytes, input: np.ndarray) -> bytes:
        tree = ET.fromstring(text)
        new_tree = copy.deepcopy(tree)
        for i in range(0, int.from_bytes(input[0].tobytes()[2:4], "little")):
            tree.append(new_tree)

        return ET.tostring(tree)


# def main():
#     file = sys.argv[1]
#     with open(file, "r+") as f:
#         sample_text = f.read()

#         array = np.random.rand(10)
#         print(XMLChildrenMutator.get_mutation(TagMutator, sample_text, array).decode())


# if __name__ == "__main__":
#     main()