import glob

from PIL import Image


def load_decks() -> dict:
    """loads all available decks in /decks returning a dict"""
    images = [img for img in glob.glob("decks/*/*.png")]
    decks = {deck.split('/')[1]: {} for deck in glob.glob("decks/*")}

    for image in images:
        img = Image.open(image)
        card = image.split('/')[-1].split('.')[0]
        deck = image.split('/')[1]
        decks[deck][card] = img

    return decks
