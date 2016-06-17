# -*- coding: utf-8 -*-
'''
Created on 15 июня 2016 г.

@author: gudach
'''

# подключает все методы из всех модулей
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
__all__ = [ basename(f)[:-3] for f in modules if isfile(f)]