import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import torch
from skimage import io
from torch import nn
import torch.nn.functional as F
from torch.autograd import Variable
import time
from PIL import Image
import os
import PIL
from PIL import ImageMath

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
  return model

def raspoznavanie(X_batch):
  model = get_model()
  #torch.do_something_cool(model)
  model.load_state_dict(torch.load("model_state_dict"))
  logits = model(Variable(torch.FloatTensor(X_batch)))        #логиты ответы модели
  y_pred = logits.max(1)[1].data.numpy()
  bukvi_pred = []
  bukvi = ["А","Б","В","Г","Д","Е","Ё","Ж","З","И","Й","К","Л","М","Н","О","П","Р","С","Т","У","Ф","Х","Ц","Ч","Ш","Щ","Ь","Ы","Ъ","Э","Ю","Я"]
  for i in range(len(y_pred)):
    bukvi_pred.append(bukvi[y_pred[i]])
  return ''.join(bukvi_pred)
