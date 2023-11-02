# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from math import log
from scipy.stats import gmean

def exponente(IMint):
    ok = 0
    i = 1
    if IMint >= 1 and IMint < 10:
        exponente=0
    elif IMint < 1:
        while ok == 0:
            num = IMint*10**i
            if num>=1 and num < 10:
                exponente = -i
                ok = 1
            i = i+1
    else:
        while ok == 0:
            num = IMint/10**i
            if num>=1 and num < 10:
                exponente = i
                ok = 1
            i = i+1
    return exponente
