import numpy as np
import urllib.request
import cv2


def imdownload(url):
    """Read an image from the given URL

    Args:
        url (str): URL to read image from

    Returns:
        np.ndarray: downloaded image decoded with openCV
    """
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image
