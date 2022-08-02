
def try_json(text: bytes) -> bool:
    """
    Attempt to decode as json. Returns if it was successful.
    """
    import json
    try:
        json.loads(text)
    except json.JSONDecodeError:
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
    #### BIG NOTE NOT STANDARD LIBRARY. NEEDS INSTALL SCRIPT TO INSTALL.
    from defusedxml.ElementTree import parse
    try:
        parse(text.splitlines())
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
        Image.open(BytesIO(text), formats=["JPEG"])
    except:
        return False
    return True

def try_elf(text: bytes) -> bool:
    """
    Attempt to decode as elf. Returns if it was successful.
    """
    # Is there really any other way to test?
    return text[:4] == b"\x7fELF"
