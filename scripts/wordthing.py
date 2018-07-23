import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import nn
import torch.nn.functional as F
from torch.autograd import Variable
import time
from PIL import Image
import os
import PIL
from PIL import ImageMath
import requests
from skimage import io
from scipy.ndimage import rotate

def main(url = "", *kwargs):
    text = ""
    if url == "":
        return("Введите URL.")
    try:
        image = io.imread(url)
    except:
        return("Введите правильный URL.")

    letter_list = splitter(image)
    for x in range(len(letter_list)):
        for y in range(len(letter_list[x])):
            word = []
            for z in range(len(letter_list[x][y])):
                word.append(milinki(Image.fromarray(np.array(letter_list[x][y][z]).astype("uint8"))))
                word[z] = word[z].reshape((120, 120))
            get_model()
            x1 = raspoznavanie(np.array(word))
            word = spellcheck(x1)
            text.append(word)
    s = ' '
    s = s.join(text)
    return s




def str_split(in_arr, out_list, acc=None, m=None):
    if acc == None:
        acc = 8
    if m == None:
        m = in_arr.shape[1] * 255
    b = False
    if out_list == None:
        out_list = []
        b = True
    prev = 0
    r = 0
    for i in range(in_arr.shape[0]):
        if np.sum(in_arr[i]) // 255 >= maximum // 255 - acc and np.sum(in_arr[i]) // 255 <= maximum // 255 + acc or i == \
                in_arr.shape[0] - 1:
            if i - prev >= 5:
                out_list.append(in_arr[prev:i])
                r += 1
            prev = i
    if b == True:
        in_arr = out_list
    return r


def word_split(in_arr, out_list, acc=None, m=None):
    if acc == None:
        acc = 8
    if m == None:
        m = in_arr.shape[0] * 255
    prev = 0
    r = 0
    letter_ignore = 0
    for i in range(in_arr.shape[1]):
        if np.sum(in_arr[:, i]) // 255 >= m // 255 - acc and np.sum(in_arr[:, i]) // 255 <= m // 255 + acc or i == \
                in_arr.shape[1] - 1:
            if i - prev < 5:
                prev = i
                letter_ignore = 0
            if letter_ignore >= 3 and i - prev >= 5:
                out_list.append(in_arr[:, prev:i])

                r += 1
                prev = i
                letter_ignore = 0
            else:
                letter_ignore += 1
        else:
            letter_ignore = 0
    return r


def letter_split(in_arr, out_list, acc=None, m=None):
    if acc == None:
        acc = 12
    if m == None:
        m = in_arr.shape[0] * 255
    prev = 0
    r = 0
    for i in range(in_arr.shape[1]):
        if np.sum(in_arr[:, i]) >= m - acc * 90 and np.sum(in_arr[:, i]) <= m + acc * 90 or i == in_arr.shape[1] - 1:
            if i - prev >= 3:
                out_list.append(in_arr[:, prev:i])
                r += 1
                prev = i
    return r


def splitter(image, save_as_image=False, path=None):
    image = image.convert("L")

    sz = image.size
    img_np = np.array(image.getdata())
    img_np = img_np.reshape(sz[::-1])

    mean = img_np.mean()
    mean -= 10

    # Разделение на строки

    h1 = np.sum(img_np, axis=1)
    maximum = h1.max()

    def str_split(in_arr, out_list, acc=None, m=None):
        if acc == None:
            acc = 8
        if m == None:
            m = in_arr.shape[1] * 255
        b = False
        if out_list == None:
            out_list = []
            b = True
        prev = 0
        r = 0
        for i in range(in_arr.shape[0]):
            if np.sum(in_arr[i]) // 255 >= maximum // 255 - acc and np.sum(
                    in_arr[i]) // 255 <= maximum // 255 + acc or i == in_arr.shape[0] - 1:
                if i - prev >= 5:
                    out_list.append(in_arr[prev:i])
                    r += 1
                prev = i
        if b == True:
            in_arr = out_list
        return r

    str_list = []
    strlen = []
    str_split(img_np, str_list, acc=8, m=h1.max())
    first = len(str_list)
    new = first
    angle = 0
    d = 1
    while (d > -2):
        while new == first:
            angle += d * 3
            img_new = rotate(img_np, angle)
            str_new = []
            str_split(img_new, str_new, acc=8, m=h1.max())
            new = len(str_new)
        if new > first:
            first = new
            str_split = str_new
        else:
            if d == 1:
                d = -1
                angle = 0
            else:
                d = -3
                break
    str_list = np.array(str_list)
    strlen = np.array([i.shape[0] for i in str_list])

    strlens = sorted(strlen)
    mid = len(strlens) // 2
    norm = strlens[mid]
    str_list_new = []
    i = 0
    while i < len(str_list):
        arr_now = str_list[i]
        if str_list[i].shape[0] > norm * 1.3:
            i1 = norm
            accuracy = 13
            str_split(arr_now, str_list_new, acc=accuracy, m=h1.max())
        else:
            str_list_new.append(arr_now)
        i += 1
    str_list = np.array(str_list_new)

    # представим, что это работает

    # Разделение на слова

    word_list = []
    for i in range(str_list.shape[0]):
        str_arr = str_list[i]
        str_bump = []
        word_split(str_arr, str_bump, acc=2)
        word_list.append(str_bump)

    # ## Разделение на буквы

    letter_list = []
    for i in range(len(word_list)):
        # for i in [0]:
        str1 = word_list[i]
        str2 = []
        for j in range(len(str1)):
            try:
                word1 = np.array(str1[j])
            except:
                print(i)
                print(j)
                print(str1[j])
                break
            letters = []
            letter_split(word1, letters, acc=3)
            str2.append(letters)
        letter_list.append(str2)

    letterlen = []
    i = 0
    for x in range(len(letter_list)):
        for y in range(len(letter_list[x])):
            for z in range(len(letter_list[x][y])):
                letterlen.append(letter_list[x][y][z].shape[1])
                i += 1
    mid = np.array(letterlen).mean()
    letter_list_new = []
    for x in range(len(letter_list)):
        str1 = []
        for y in range(len(letter_list[x])):
            word1 = []
            for z in range(len(letter_list[x][y])):
                arr_now = letter_list[x][y][z]
                if letter_list[x][y][z].shape[1] > mid:
                    accuracy = 50
                    let1 = []
                    letter_split(arr_now, let1, acc=5)
                    for i1 in range(len(let1)):
                        if mid * 1.1 < let1[i1].shape[1]:
                            word1.append(let1[i1][:, :let1[i1].shape[1] // 2 + 3])
                            word1.append(let1[i1][:, let1[i1].shape[1] // 2 - 3:])
                        else:
                            word1.append(let1[i1])
                else:
                    word1.append(arr_now)
            str1.append(word1)
        letter_list_new.append(str1)
    letter_list = letter_list_new

    # Сохранение в файл

    # все буквы сохраняются таким образом:
    #
    # pathfile/img{номер строчки}.{номер слова}.{номер буквы}.png
    #
    # Образец:
    # <code>img0.0.0.png<endcode>

    if save_as_image:
        if path == None:
            path = './'
        if not os.path.exists(path):
            os.makedirs(path)

        for x in range(len(letter_list)):
            for y in range(len(letter_list[x])):
                for z in range(len(letter_list[x][y])):
                    Image.fromarray(letter_list[x][y][z]).convert('L').save(
                        path + 'img' + str(x) + '.' + str(y) + '.' + str(z) + '.jpg')

    return letter_list


def spellcheck(word):
    while word.find('III') >= 1:
        word = word.replace('III', 'Ш')
    while word.find('ЬI') >= 1:
        word = word.replace('ЬI', 'Ы')
    while word.find('II') >= 1:
        word = word.replace('II', 'н')

    params = {'text': word, 'lang': 'ru'}
    r = requests.get('http://speller.yandex.net/services/spellservice.json/checkText', params=params)
    if r.status_code == 200:
        if len(r.json()) > 0:
            out = r.json()[0]
            variants = [v for v in out['s']]
            if len(variants) <= 0:
                return word
            return variants[0]
        else:
            return word



def milinki(l, size=None):
  if size == None:
    size = 120
  basewidth = size
  l= l.resize((basewidth,basewidth), Image.ANTIALIAS)
  l = np.array(l.getdata())
  return l

class Flatten(nn.Module):
    def forward(self, input):
        return input.view(input.size(0), -1) #переделвает размер матрицы
def get_model():

  model = nn.Sequential()
  model.add_module('conv1', nn.Conv1d(120, 316, kernel_size=(5), stride=1, padding=0)) #cвёрточный слой падинг обораивает картинку нулями чтобы она не сжималась
  model.add_module('conv2', nn.Conv1d(316, 632, kernel_size=(5), stride=1, padding=0)) # страйд- на сколько клеток двигаем ядро

  model.add_module("maxpool1", torch.nn.MaxPool2d(kernel_size=4))   #ядро 2х2 превращается в 1 пиксель
  model.add_module('dropout1', nn.Dropout(p=0.25))                  # минус 1/4 связи
  model.add_module("flatten", Flatten())                            #растягмвает картинку в вектор 3*3=9

  model.add_module("linear1", torch.nn.Linear(4424, 200))            #линер=декс, типа получилось 384 нейрона
  model.add_module('dropout1', nn.Dropout(p=0.5))                    #ещё минус пол связей
  model.add_module("linear2", torch.nn.Linear(200, 33))           #выходной слой

def raspoznavanie(X_batch):
  model = torch.load("model")
  logits = model(Variable(torch.FloatTensor(X_batch)))        #логиты ответы модели
  y_pred = logits.max(1)[1].data.numpy()
  bukvi_pred = []
  bukvi = ["А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ь","Ы","Ъ","Э","Ю","Я"]
  for i in range(len(y_pred)):
    bukvi_pred.append(bukvi[y_pred[i]])
  return ''.join(bukvi_pred)