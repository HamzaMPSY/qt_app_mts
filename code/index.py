from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
import os
import sys
from os import path
import torch
import numpy as np

FORM_CLASS,_= loadUiType(path.join(path.dirname(__file__),"ui/main.ui"))