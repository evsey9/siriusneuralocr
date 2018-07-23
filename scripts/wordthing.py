import string_splitter as ss
import recognizer as rcg

def main(url = "", *kwargs):
    text = ""
    if url == "":
        return("Введите URL.")
    try:
        image = io.imread(url)
    except:
        return("Введите правильный URL.")

    letter_list = ss.splitter(image)
    for x in range(len(letter_list)):
        for y in range(len(letter_list[x])):
            word = []
            for z in range(len(letter_list[x][y])):
                word.append(rcg.milinki(Image.fromarray(np.array(letter_list[x][y][z]).astype("uint8"))))
                word[z] = word[z].reshape((120, 120))
            get_model()
            x1 = rcg.raspoznavanie(np.array(word))
            word = ss.spellcheck(x1)
            text.append(word)
    s = ' '
    s = s.join(text)
    return s
