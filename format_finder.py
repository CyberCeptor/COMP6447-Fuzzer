
from io import StringIO


def try_json(text: bytes) -> bool:
    """
    Attempt to decode as json. Returns if it was successful.
    """
    import json
    try:
        json.loads(text)
    except:
        return False
    return True

def try_csv(text: bytes) -> bool:
    """
    Attempt to decode as csv. Returns if it was successful.
    Due to how csv works, this can produce false negatives/positives.
    """
    import csv
    try:
        dialect = csv.Sniffer().sniff(text.decode())
        if dialect is None:
            return False
        csv.reader(text.splitlines(), dialect)
    except:
        return False
    return True

def try_xml(text: bytes) -> bool:
    """
    Attempt to decode as xml. Returns if it was successful.
    Uses defusedxml because xml is vulnerable to bombs.
    """
    import xml.etree.ElementTree as ET
    try:
        ET.fromstring(text)
    except:
        return False
    return True

def try_jpg(text: bytes) -> bool:
    """
    Attempt to decode as jpg. Returns if it was successful.
    """
    from io import BytesIO
    from PIL import Image
    try:
        Image.open(BytesIO(text), formats=["JPEG"]).load()
    except:
        return False
    return True

def try_elf(text: bytes) -> bool:
    """
    Attempt to decode as elf. Returns if it was successful.
    """
    # Is there really any other way to test?
    return text[:4] == b"\x7fELF"

def try_pdf(input: str) -> bool:
    """
    Attempt to decode as pdf. Returns if it was successful.
    Only returns True if the file is a PDF and is readable
    """
    from pdfminer.high_level import extract_text

    try:
        extract_text(input)
        return True
    except:
        return False
