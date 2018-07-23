import string_splitter as ss
import recognizer as rcg
from skimage import io
from PIL import Image
import numpy as np

def main(url = "", *kwargs, save=False):
    text = ""
    if url == "":
        return("Введите URL.")
    try:
        image = io.imread(url)
    except:
        return("Введите правильный URL.")
    letter_list = ss.splitter(image, save_as_image=save)
    for x in range(len(letter_list)):
        for y in range(len(letter_list[x])):
            word = []
            for z in range(len(letter_list[x][y])):
                word.append(rcg.milinki(Image.fromarray(np.array(letter_list[x][y][z]).astype("uint8"))))
                word[z] = word[z].reshape((120, 120))
            rcg.get_model()
            x1 = rcg.raspoznavanie(np.array(word))
            word = ss.spellcheck(x1)
            text += word
    s = ' '
    s = s.join(text)
    return s
