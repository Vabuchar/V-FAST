# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 09:36:15 2022

@author: Verónica Jesús Abuchar Soto
"""

import sys
import os
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor
# from PyQt5.QtCore import Qt
import math
import statsmodels.api as sm
from scipy.stats import norm
import glob


class Ui_FragilityCurvesTool(object):
    def setupUi(self, FragilityCurvesTool):
        
        # ################################################################
        # DEFINICIÓN DE VENTANA
        # ################################################################
        
        # Definición de la ventana de la interfaz
        FragilityCurvesTool.setObjectName("FragilityCurvesTool")
        FragilityCurvesTool.resize(1658, 935)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(FragilityCurvesTool.sizePolicy().hasHeightForWidth())
        FragilityCurvesTool.setSizePolicy(sizePolicy)
        
        # TABWIDGET GENERAL
        self.tabWidget_General = QtWidgets.QTabWidget(FragilityCurvesTool)
        self.tabWidget_General.setGeometry(QtCore.QRect(0, 70, 1658, 821))
        self.tabWidget_General.setObjectName("tabWidget_General")
        # self.tabWidget_General.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        
        # Benners
        self.Banner_Abajo = QtWidgets.QLabel(FragilityCurvesTool)
        self.Banner_Abajo.setGeometry(QtCore.QRect(0, 890, 1658, 53))
        self.Banner_Abajo.setText("")
        self.Banner_Abajo.setPixmap(QtGui.QPixmap("Banner2.jpg"))
        self.Banner_Abajo.setScaledContents(True)
        self.Banner_Abajo.setObjectName("Banner_Abajo")
        
        self.Banner_Arriba = QtWidgets.QLabel(FragilityCurvesTool)
        self.Banner_Arriba.setGeometry(QtCore.QRect(0, 0, 1658, 70))
        self.Banner_Arriba.setText("")
        self.Banner_Arriba.setPixmap(QtGui.QPixmap("Banner1.jpg"))
        self.Banner_Arriba.setScaledContents(True)
        self.Banner_Arriba.setObjectName("Banner_Arriba")
        
        # ################################################################
        # TABWIDGET FRAGILITY OF BUILDINGS
        # ################################################################
        
        # Tab de análisis estructural
        self.FragilityAnalysis = QtWidgets.QWidget()
        self.FragilityAnalysis.setObjectName("FragilityAnalysis")
        
        # Area Scroll del Tab de análisis estructural
        self.scrollArea_Structural = QtWidgets.QScrollArea(self.FragilityAnalysis)
        self.scrollArea_Structural.setGeometry(QtCore.QRect(0, 0, 1651, 811))
        self.scrollArea_Structural.setWidgetResizable(True)
        self.scrollArea_Structural.setObjectName("scrollArea_Structural")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 1649, 809))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        
        # Boton para cargar excel de edificaciones guia
        self.Load_Guide_Data = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.Load_Guide_Data.setGeometry(QtCore.QRect(20, 20, 241, 28))
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Load_Guide_Data.setFont(font)
        self.Load_Guide_Data.setObjectName("Load_Guide_Data")
        
        # ----------------------------------------------------------
        ## LOAD FOLDERS
        
        # Subtítulo de sección para cargar archivos de la edificación 1
        self.LoadFiles_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.LoadFiles_1.setGeometry(QtCore.QRect(50, 75, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.LoadFiles_1.setFont(font)
        self.LoadFiles_1.setObjectName("LoadFiles_1")
        
        # Subtítulo de sección para cargar archivos de la edificación 2
        self.LoadFiles_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.LoadFiles_2.setGeometry(QtCore.QRect(1380, 75, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.LoadFiles_2.setFont(font)
        self.LoadFiles_2.setObjectName("LoadFiles_2")
        
        # Botón para busqueda de carpeta de Hazards de edificación 1
        self.HazardLevelButton_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.HazardLevelButton_1.setGeometry(QtCore.QRect(20, 100, 131, 28))
        self.HazardLevelButton_1.setObjectName("HazardLevelButton_1")
        
        # Botón para busqueda de carpeta de Hazards de edificación 2
        self.HazardLevelButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.HazardLevelButton_2.setGeometry(QtCore.QRect(1350, 100, 131, 28))
        self.HazardLevelButton_2.setObjectName("HazardLevelButton_2")
        
        # Botón para busqueda de carpeta de respuestas de la edificación 1
        self.EDPButton_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.EDPButton_1.setGeometry(QtCore.QRect(20, 135, 131, 28))
        self.EDPButton_1.setObjectName("EDPButton_1")
        
        # Botón para busqueda de carpeta de respuestas de la edificación 2
        self.EDPButton_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.EDPButton_2.setGeometry(QtCore.QRect(1350, 135, 131, 28))
        self.EDPButton_2.setObjectName("EDPButton_2")
        
        # Texto que muestra el nombre la edificación seleccionada de la edificación 1
        self.EDP_text_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDP_text_1.setGeometry(QtCore.QRect(160, 135, 121, 28))
        self.EDP_text_1.setObjectName("EDP_text_1")
        self.EDP_text_1.setText("CSS_277")      # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # Texto que muestra el nombre la edificación seleccionada de la edificación 2
        self.EDP_text_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDP_text_2.setGeometry(QtCore.QRect(1490, 135, 121, 28))
        self.EDP_text_2.setObjectName("EDP_text_2")
        self.EDP_text_2.setText("CSS_211")          # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # Texto que muestra el nombre de la carpeta de selección de acelerogramas de la edificación 1
        self.Hazard_text_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Hazard_text_1.setGeometry(QtCore.QRect(160, 100, 121, 28))
        self.Hazard_text_1.setObjectName("Hazard_text_1")
        self.Hazard_text_1.setText("CSS_BOG_Soil_T1s")      # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Texto que muestra el nombre de la carpeta de selección de acelerogramas de la edificación 2
        self.Hazard_text_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Hazard_text_2.setGeometry(QtCore.QRect(1490, 100, 121, 28))
        self.Hazard_text_2.setObjectName("Hazard_text_2")
        self.Hazard_text_2.setText("CCS_BAQ_Soil_T1s")      # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # ----------------------------------------------------------
        ## TEST
         
        # Subtítulo de sección para introducir parámetros para verificación de la data de la edificación 1 
        self.Test1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Test1.setGeometry(QtCore.QRect(50, 184, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.Test1.setFont(font)
        self.Test1.setObjectName("Test1")
         
        # Subtítulo de sección para introducir parámetros para verificación de la data de la edificación 2
        self.Test1_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Test1_2.setGeometry(QtCore.QRect(1380, 184, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.Test1_2.setFont(font)
        self.Test1_2.setObjectName("Test1_2")
        
        # Etiqueta de selección del tiempo mínimo de corrida para la curvas para la edificación 1
        self.tminLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.tminLabel_1.setGeometry(QtCore.QRect(50, 205, 61, 21))
        self.tminLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tminLabel_1.setObjectName("tminLabel_1")
         
        # Etiqueta de selección del tiempo mínimo de corrida para la curvas para la edificación 2
        self.tminLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.tminLabel_2.setGeometry(QtCore.QRect(1390, 205, 51, 21))
        self.tminLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tminLabel_2.setObjectName("tminLabel_2")
         
        # Línea para introducir valor del tiempo mínimo de corrida para la curvas para la edificación 1
        self.tmin_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.tmin_value_1.setGeometry(QtCore.QRect(120, 205, 81, 21))
        self.tmin_value_1.setObjectName("tmin_value_1")
        self.tmin_value_1.setText("0.9")       # Valor por defecto
         
        # Línea para introducir valor del tiempo mínimo de corrida para la curvas para la edificación 2
        self.tmin_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.tmin_value_2.setGeometry(QtCore.QRect(1450, 205, 81, 21))
        self.tmin_value_2.setObjectName("tmin_value_2")
        self.tmin_value_2.setText("0.9")       # Valor por defecto
        
        # Texto que indica el rango del tiempo minimo de la edificación 1
        self.range_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.range_1.setGeometry(QtCore.QRect(205, 205, 71, 21))
        self.range_1.setObjectName("range_1")
         
        # Texto que indica el rango del tiempo minimo de la edificación 2
        self.range_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.range_2.setGeometry(QtCore.QRect(1535, 205, 71, 21))
        self.range_2.setObjectName("range_2")
        
        # Etiqueta de selección de SDR limite para aceptación de un tiempo menor al minimo de la edificación 1
        self.EDPlimLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPlimLabel_1.setGeometry(QtCore.QRect(50, 230, 61, 21))
        self.EDPlimLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPlimLabel_1.setObjectName("EDPlimLabel_1")
         
        # Etiqueta de selección de SDR limite para aceptación de un tiempo menor al minimo de la edificación 2
        self.EDPlimLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPlimLabel_2.setGeometry(QtCore.QRect(1380, 230, 61, 21))
        self.EDPlimLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPlimLabel_2.setObjectName("EDPlimLabel_2")
         
        # Línea para introducir SDR limite para aceptación de un tiempo menor al minimo de la edificación 1
        self.EDP_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDP_value_1.setGeometry(QtCore.QRect(120, 230, 81, 21))
        self.EDP_value_1.setObjectName("EDP_value_1")
        self.EDP_value_1.setText("0.04")          # Valor por defecto
         
        # Línea para introducir SDR limite para aceptación de un tiempo menor al minimo de la edificación 2
        self.EDP_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDP_value_2.setGeometry(QtCore.QRect(1450, 230, 81, 21))
        self.EDP_value_2.setObjectName("EDP_value_2")
        self.EDP_value_2.setText("0.04")          # Valor por defecto
         
        # # Texto que indica que SDRlim se introduce en % de la edificación 1
        # self.porc_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        # self.porc_1.setGeometry(QtCore.QRect(205, 230, 51, 21))
        # self.porc_1.setObjectName("porc_1")
         
        # # Texto que indica que SDRlim se introduce en % de la edificación 2
        # self.porc_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        # self.porc_2.setGeometry(QtCore.QRect(1535, 230, 61, 21))
        # self.porc_2.setObjectName("porc_2")
        
        # ----------------------------------------------------------
        ## IM AND EDP DEFINITION
        
        # Subtítulo de sección para introducir parámetros IM y EDP de la edificación 1
        self.IM_EDP_selection_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.IM_EDP_selection_1.setGeometry(QtCore.QRect(50, 280, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.IM_EDP_selection_1.setFont(font)
        self.IM_EDP_selection_1.setObjectName("IM_EDP_selection_1")
        
        # Subtítulo de sección para introducir parámetros IM y EDP de la edificación 2
        self.IM_EDP_selection_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.IM_EDP_selection_2.setGeometry(QtCore.QRect(1380, 280, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.IM_EDP_selection_2.setFont(font)
        self.IM_EDP_selection_2.setObjectName("IM_EDP_selection_2")
        
        # Etiqueta del periodo de la edificación 1 
        self.PeriodoLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.PeriodoLabel_1.setGeometry(QtCore.QRect(50, 300, 61, 21))
        self.PeriodoLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PeriodoLabel_1.setObjectName("PeriodoLabel_1")
        
        # Etiqueta del periodo de la edificación 2 
        self.PeriodoLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.PeriodoLabel_2.setGeometry(QtCore.QRect(1390, 300, 51, 21))
        self.PeriodoLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PeriodoLabel_2.setObjectName("PeriodoLabel_2")
        
        # Línea para introducir periodo estructural de la edificación 1
        self.periodo_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.periodo_value_1.setGeometry(QtCore.QRect(120, 300, 73, 21))
        self.periodo_value_1.setObjectName("periodo_value_1")
        self.periodo_value_1.setText("1")                       # Valor por defecto
        
        # Línea para introducir periodo estructural de la edificación 2
        self.periodo_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.periodo_value_2.setGeometry(QtCore.QRect(1450, 300, 73, 21))
        self.periodo_value_2.setObjectName("periodo_value_2")
        self.periodo_value_2.setText("1")                       # Valor por defecto
        
        # Etiqueta para el desplegable de la selección del tipo de IM en la edificación 1
        self.IMType_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.IMType_Label_1.setGeometry(QtCore.QRect(60, 325, 51, 20))
        self.IMType_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IMType_Label_1.setObjectName("IMType_Label_1")
        
        # Etiqueta para el desplegable de la selección del tipo de IM en la edificación 2
        self.IMType_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.IMType_Label_2.setGeometry(QtCore.QRect(1400, 325, 41, 20))
        self.IMType_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IMType_Label_2.setObjectName("IMType_Label_2")
        
        # Desplegable para selección del tipo de IM de la edificación 1
        self.IMType_Value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.IMType_Value_1.setGeometry(QtCore.QRect(120, 325, 73, 22))
        self.IMType_Value_1.setObjectName("IMType_Value_1")
        self.IMType_Value_1.addItem("Sa")            # Adiciona opción de desplegable
        self.IMType_Value_1.addItem("SaAVG")         # Adiciona opción de desplegable
        
        # Desplegable para selección del tipo de IM de la edificación 2
        self.IMType_Value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.IMType_Value_2.setGeometry(QtCore.QRect(1450, 325, 73, 22))
        self.IMType_Value_2.setObjectName("IMType_Value_2")
        self.IMType_Value_2.addItem("Sa")            # Adiciona opción de desplegable
        self.IMType_Value_2.addItem("SaAVG")         # Adiciona opción de desplegable
        
        # Etiqueta para el desplegable de la selección del tipo de EDP en la edificación 1
        self.EDPType_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPType_Label_1.setGeometry(QtCore.QRect(50, 350, 61, 20))
        self.EDPType_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPType_Label_1.setObjectName("EDPType_Label_1")
        
        # Etiqueta para el desplegable de la selección del tipo de EDP en la edificación 2
        self.EDPType_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPType_Label_2.setGeometry(QtCore.QRect(1390, 350, 51, 20))
        self.EDPType_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPType_Label_2.setObjectName("EDPType_Label_2")
        
        # Desplegable para selección del tipo de EDP de la edificación 1
        self.EDPType_Value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.EDPType_Value_1.setGeometry(QtCore.QRect(120, 350, 73, 22))
        self.EDPType_Value_1.setObjectName("EDPType_Value_1")
        self.EDPType_Value_1.addItem("SDR")         # Adiciona opción de desplegable
        self.EDPType_Value_1.addItem("RDR")        # Adiciona opción de desplegable
        self.EDPType_Value_1.addItem("PFA")         # Adiciona opción de desplegable
        self.EDPType_Value_1.addItem("RSDR")        # Adiciona opción de desplegable
        
        # Desplegable para selección del tipo de EDP de la edificación 2
        self.EDPType_Value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.EDPType_Value_2.setGeometry(QtCore.QRect(1450, 350, 73, 22))
        self.EDPType_Value_2.setObjectName("EDPType_Value_2")
        self.EDPType_Value_2.addItem("SDR")         # Adiciona opción de desplegable
        self.EDPType_Value_2.addItem("RDR")        # Adiciona opción de desplegable
        self.EDPType_Value_2.addItem("PFA")         # Adiciona opción de desplegable
        self.EDPType_Value_2.addItem("RSDR")        # Adiciona opción de desplegable
        
        # Desplegable para selección del piso a evaluar de la edificación 1
        self.EDPType_ValueStory_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.EDPType_ValueStory_1.setGeometry(QtCore.QRect(200, 350, 61, 22))
        self.EDPType_ValueStory_1.setObjectName("EDPType_ValueStory_1")

        # Desplegable para selección del piso a evaluar de la edificación 2
        self.EDPType_ValueStory_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.EDPType_ValueStory_2.setGeometry(QtCore.QRect(1530, 350, 61, 22))
        self.EDPType_ValueStory_2.setObjectName("EDPType_ValueStory_2")
        
        # Etiqueta para selección de EDP max de la edificación 1
        self.EDP_cens_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDP_cens_Label_1.setGeometry(QtCore.QRect(40, 375, 71, 21))
        self.EDP_cens_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDP_cens_Label_1.setObjectName("EDP_cens_Label_1")
        
        # Etiqueta para selección de EDP max de la edificación 2
        self.EDP_cens_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDP_cens_Label_2.setGeometry(QtCore.QRect(1370, 375, 71, 21))
        self.EDP_cens_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDP_cens_Label_2.setObjectName("EDP_cens_Label_2")
        
        # Línea para introducir EDP max que limitará los valores que sobrepasen ese EDP de la edificación 1
        self.EDPcens_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDPcens_value_1.setGeometry(QtCore.QRect(120, 375, 73, 21))
        self.EDPcens_value_1.setObjectName("EDPcens_value_1")
        self.EDPcens_value_1.setText("0.1")     # Valor por defecto
        
        # Línea para introducir EDP max que limitará los valores que sobrepasen ese EDP de la edificación 2
        self.EDPcens_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDPcens_value_2.setGeometry(QtCore.QRect(1450, 375, 73, 21))
        self.EDPcens_value_2.setObjectName("EDPcens_value_2")
        self.EDPcens_value_2.setText("0.1")     # Valor por defecto
        
        # Desplegable para definición de inclusión o no de censuta en el bineado de la edificación 1
        self.includeCens_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.includeCens_1.setGeometry(QtCore.QRect(200, 375, 61, 21))
        self.includeCens_1.setObjectName("includeCens_1")
        self.includeCens_1.addItem("Yes")        # Adiciona opción de desplegable
        self.includeCens_1.addItem("No")         # Adiciona opción de desplegable
        
        # Desplegable para definición de inclusión o no de censuta en el bineado de la edificación 2
        self.includeCens_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.includeCens_2.setGeometry(QtCore.QRect(1530, 375, 61, 21))
        self.includeCens_2.setObjectName("includeCens_2")
        self.includeCens_2.addItem("Yes")        # Adiciona opción de desplegable
        self.includeCens_2.addItem("No")         # Adiciona opción de desplegable
        
        # Etiqueta de selección de Hazards para la edificación 1       
        self.Hazard_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Hazard_Label_1.setGeometry(QtCore.QRect(40, 400, 71, 21))
        self.Hazard_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Hazard_Label_1.setObjectName("Hazard_Label_1")
        
        # Etiqueta de selección de Hazards para la edificación 2
        self.Hazard_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.Hazard_Label_2.setGeometry(QtCore.QRect(1370, 400, 71, 21))
        self.Hazard_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Hazard_Label_2.setObjectName("Hazard_Label_2")
        
        # Línea para introducir selección de Hazards para la edificación 1
        self.hazard_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.hazard_value_1.setGeometry(QtCore.QRect(120, 400, 141, 21))
        self.hazard_value_1.setObjectName("hazard_value_1")
        self.hazard_value_1.setText("1,2,3,4,5,6,7,8,9,10")     # Valores por defecto
        
        # Línea para introducir selección de Hazards para la edificación 2
        self.hazard_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.hazard_value_2.setGeometry(QtCore.QRect(1450, 400, 141, 21))
        self.hazard_value_2.setObjectName("hazard_value_2")
        self.hazard_value_2.setText("1,2,3,4,5,6,7,8,9,10")     # Valores por defecto
        
        # ----------------------------------------------------------
        ## FRAGILITY PARAMETERS
        
        # Subtítulo de sección para introducir parámetros para estimar fragildiad de la edificación 1
        self.FragilityTittle_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.FragilityTittle_1.setGeometry(QtCore.QRect(50, 445, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.FragilityTittle_1.setFont(font)
        self.FragilityTittle_1.setObjectName("FragilityTittle_1")
        
        # Subtítulo de sección para introducir parámetros para estimar fragildiad de la edificación 2
        self.FragilityTittle_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.FragilityTittle_2.setGeometry(QtCore.QRect(1380, 445, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.FragilityTittle_2.setFont(font)
        self.FragilityTittle_2.setObjectName("FragilityTittle_2")
        
        # Etiqueta de selección de niveles j para curvas deterministicas para la edificación 1 
        self.j_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.j_Label_1.setGeometry(QtCore.QRect(0, 465, 111, 21))
        self.j_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.j_Label_1.setObjectName("j_Label_1")
        
        # Etiqueta de selección de niveles j para curvas deterministicas para la edificación 2
        self.j_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.j_Label_2.setGeometry(QtCore.QRect(1340, 465, 101, 21))
        self.j_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.j_Label_2.setObjectName("j_Label_2")
        
        # Línea para introducir selección de niveles j para la curvas deterministicas para la edificación 1
        self.j_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.j_value_1.setGeometry(QtCore.QRect(120, 465, 141, 21))
        self.j_value_1.setObjectName("j_value_1")
        self.j_value_1.setText("0.005,0.01,0.02,0.03")      # Valores por defecto
        
        # Línea para introducir selección de niveles j para la curvas deterministicas para la edificación 2
        self.j_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.j_value_2.setGeometry(QtCore.QRect(1450, 465, 141, 21))
        self.j_value_2.setObjectName("j_value_2")
        self.j_value_2.setText("0.005,0.01,0.02,0.03")      # Valores por defecto
        
        # Etiqueta de selección de parámetros theta de las curvas probabilisticas para la edificación 1
        self.theta_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.theta_Label_1.setGeometry(QtCore.QRect(10, 490, 101, 21))
        self.theta_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.theta_Label_1.setObjectName("theta_Label_1")
        
        # Etiqueta de selección de parámetros theta de las curvas probabilisticas para la edificación 2
        self.theta_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.theta_Label_2.setGeometry(QtCore.QRect(1340, 490, 101, 21))
        self.theta_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.theta_Label_2.setObjectName("theta_Label_2")
        
        # Línea para introducir parámetros theta de las curvas probabilisticas para la edificación 1
        self.theta_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.theta_value_1.setGeometry(QtCore.QRect(120, 490, 141, 21))
        self.theta_value_1.setObjectName("theta_value_1")
        self.theta_value_1.setText("0.003,0.015,0.022,0.03")      # Valores por defecto
        
        # Línea para introducir parámetros theta de las curvas probabilisticas para la edificación 2
        self.theta_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.theta_value_2.setGeometry(QtCore.QRect(1450, 490, 141, 21))
        self.theta_value_2.setObjectName("theta_value_2")
        self.theta_value_2.setText("0.003,0.015,0.022,0.03")      # Valores por defecto
        
        # Etiqueta de selección de parámetros sigma de las curvas probabilisticas para la edificación 1
        self.sigma_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.sigma_Label_1.setGeometry(QtCore.QRect(10, 515, 101, 21))
        self.sigma_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sigma_Label_1.setObjectName("sigma_Label_1")
        
        # Etiqueta de selección de parámetros sigma de las curvas probabilisticas para la edificación 2
        self.sigma_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.sigma_Label_2.setGeometry(QtCore.QRect(1340, 515, 101, 21))
        self.sigma_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sigma_Label_2.setObjectName("sigma_Label_2")
        
        # Línea para introducir parámetros sigma de las curvas probabilisticas para la edificación 1
        self.sigma_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.sigma_value_1.setGeometry(QtCore.QRect(120, 515, 141, 21))
        self.sigma_value_1.setObjectName("sigma_value_1")
        self.sigma_value_1.setText("0.4,0.4,0.4,0.4")      # Valores por defecto
        
        # Línea para introducir parámetros sigma de las curvas probabilisticas para la edificación 2
        self.sigma_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.sigma_value_2.setGeometry(QtCore.QRect(1450, 515, 141, 21))
        self.sigma_value_2.setObjectName("sigma_value_2")
        self.sigma_value_2.setText("0.4,0.4,0.4,0.4")      # Valores por defecto
        
        # Etiqueta de selección de valor de colapso de edificación 1
        self.EDPCollapse_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPCollapse_Label_1.setGeometry(QtCore.QRect(10, 540, 101, 21))
        self.EDPCollapse_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPCollapse_Label_1.setObjectName("EDPCollapse_Label_1")
        
        # Etiqueta de selección de valor de colapso de edificación 2
        self.EDPCollapse_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.EDPCollapse_Label_2.setGeometry(QtCore.QRect(1340, 540, 101, 21))
        self.EDPCollapse_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPCollapse_Label_2.setObjectName("EDPCollapse_Label_2")
        
        # Línea para introducir valor de colapso de edificación 1
        self.EDPCollapse_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDPCollapse_value_1.setGeometry(QtCore.QRect(120, 540, 141, 21))
        self.EDPCollapse_value_1.setObjectName("EDPCollapse_value_1")
        self.EDPCollapse_value_1.setText("0.1")                   # Valor por defecto
        
        # Línea para introducir valor de colapso de edificación 2
        self.EDPCollapse_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.EDPCollapse_value_2.setGeometry(QtCore.QRect(1450, 540, 141, 21))
        self.EDPCollapse_value_2.setObjectName("EDPCollapse_value_2")
        self.EDPCollapse_value_2.setText("0.1")                   # Valor por defecto
        
        # Etiqueta para colocar nombres de estados de daño para fragilidad de la edificación 1
        self.DSTags_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.DSTags_Label_1.setGeometry(QtCore.QRect(10, 565, 101, 21))
        self.DSTags_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DSTags_Label_1.setObjectName("DSTags_Label_1")
        
        # Etiqueta para colocar nombres de estados de daño para fragilidad de la edificación 2
        self.DSTags_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.DSTags_Label_2.setGeometry(QtCore.QRect(1340, 565, 101, 21))
        self.DSTags_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DSTags_Label_2.setObjectName("DSTags_Label_2")
        
        # Línea para colocar nombres de estados de daño para fragilidad de la edificación 1
        self.DSTags_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.DSTags_value_1.setGeometry(QtCore.QRect(120, 565, 141, 21))
        self.DSTags_value_1.setObjectName("DSTags_value_1")
        self.DSTags_value_1.setText("Slight,Moderate,Severe,Collapse")          # Valor por defecto
        
        # Línea para colocar nombres de estados de daño para fragilidad de la edificación 2
        self.DSTags_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.DSTags_value_2.setGeometry(QtCore.QRect(1450, 565, 141, 21))
        self.DSTags_value_2.setObjectName("DSTags_value_2")
        self.DSTags_value_2.setText("Slight,Moderate,Severe,Collapse")          # Valor por defecto
        
        # Etiqueta de vector para porcentajes de curvas de fragilidad de la edificación 1
        self.porc_fit_curves_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.porc_fit_curves_Label_1.setGeometry(QtCore.QRect(0, 590, 111, 21))
        self.porc_fit_curves_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.porc_fit_curves_Label_1.setObjectName("porc_fit_curves_Label_1")
        
        # Etiqueta de vector para porcentajes de curvas de fragilidad de la edificación 2
        self.porc_fit_curves_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.porc_fit_curves_Label_2.setGeometry(QtCore.QRect(1330, 590, 111, 21))
        self.porc_fit_curves_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.porc_fit_curves_Label_2.setObjectName("porc_fit_curves_Label_2")
        
        # Línea para introducir porcentajes de curvas de fragilidad de la edificación 1
        self.porc_fit_curves_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.porc_fit_curves_1.setGeometry(QtCore.QRect(120, 590, 141, 21))
        self.porc_fit_curves_1.setObjectName("porc_fit_curves_1")
        self.porc_fit_curves_1.setText("1,1,1,0.50")                            # Valor por defecto
        
        # Línea para introducir porcentajes de curvas de fragilidad de la edificación 2
        self.porc_fit_curves_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.porc_fit_curves_2.setGeometry(QtCore.QRect(1450, 590, 141, 21))
        self.porc_fit_curves_2.setObjectName("porc_fit_curves_2")
        self.porc_fit_curves_2.setText("1,1,1,0.50")                            # Valor por defecto
        
        # Etiqueta de selección de tipo métodología para estimar colapso de la edificación 1
        self.collapseMethod_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.collapseMethod_Label_1.setGeometry(QtCore.QRect(0, 615, 111, 21))
        self.collapseMethod_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collapseMethod_Label_1.setObjectName("collapseMethod_Label_1")
        
        # Etiqueta de selección de tipo métodología para estimar colapso de la edificación 2
        self.collapseMethod_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.collapseMethod_Label_2.setGeometry(QtCore.QRect(1330, 615, 111, 21))
        self.collapseMethod_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collapseMethod_Label_2.setObjectName("collapseMethod_Label_2")
        
        # Desplegable de selección de tipo métodología para estimar colapso de la edificación 1
        self.collapseMethod_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.collapseMethod_1.setGeometry(QtCore.QRect(120, 615, 141, 22))
        self.collapseMethod_1.setObjectName("collapseMethod_1")
        self.collapseMethod_1.addItem("count")           # Adiciona opción de desplegable
        self.collapseMethod_1.addItem("fit")             # Adiciona opción de desplegable
        self.collapseMethod_1.addItem("count columns")   # Adiciona opción de desplegable
        
        # Desplegable de selección de tipo métodología para estimar colapso de la edificación 2
        self.collapseMethod_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.collapseMethod_2.setGeometry(QtCore.QRect(1450, 615, 141, 22))
        self.collapseMethod_2.setObjectName("collapseMethod_2")
        self.collapseMethod_2.addItem("count")           # Adiciona opción de desplegable
        self.collapseMethod_2.addItem("fit")             # Adiciona opción de desplegable
        self.collapseMethod_2.addItem("count columns")   # Adiciona opción de desplegable
        
        # Etiqueta de selección de tipo de bineado de la edificación 1
        self.binLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.binLabel_1.setGeometry(QtCore.QRect(40, 640, 71, 21))
        self.binLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binLabel_1.setObjectName("binLabel_1")
        
        # Etiqueta de selección de tipo de bineado de la edificación 2
        self.binLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.binLabel_2.setGeometry(QtCore.QRect(1380, 640, 61, 21))
        self.binLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binLabel_2.setObjectName("binLabel_2")
        
        # Desplegable para selección del tipo de bineado de la edificación 1
        self.Bintype_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.Bintype_1.setGeometry(QtCore.QRect(120, 640, 141, 22))
        self.Bintype_1.setObjectName("Bintype_1")
        self.Bintype_1.addItem("Logspace")      # Adiciona opción de desplegable
        self.Bintype_1.addItem("Linespace")     # Adiciona opción de desplegable
        
        # Desplegable para selección del tipo de bineado de la edificación 2
        self.Bintype_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_2)
        self.Bintype_2.setGeometry(QtCore.QRect(1450, 640, 141, 22))
        self.Bintype_2.setObjectName("Bintype_2")
        self.Bintype_2.addItem("Logspace")      # Adiciona opción de desplegable
        self.Bintype_2.addItem("Linespace")     # Adiciona opción de desplegable
        
        # Etiqueta de selección de tipo de mínimo número de datos por bin de la edificación 1
        self.binMinLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.binMinLabel_1.setGeometry(QtCore.QRect(20, 665, 91, 21))
        self.binMinLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binMinLabel_1.setObjectName("binMinLabel_1")
        
        # Etiqueta de selección de tipo de mínimo número de datos por bin de la edificación 2
        self.binMinLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.binMinLabel_2.setGeometry(QtCore.QRect(1350, 665, 91, 21))
        self.binMinLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binMinLabel_2.setObjectName("binMinLabel_2")
        
        # Línea para introducir mínimo número de datos por bin de la edificación 1
        self.binminvalue_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.binminvalue_1.setGeometry(QtCore.QRect(120, 665, 141, 21))
        self.binminvalue_1.setObjectName("binminvalue_1")
        self.binminvalue_1.setText("15")        # Valor por defecto
        
        # Línea para introducir mínimo número de datos por bin de la edificación 2
        self.binminvalue_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.binminvalue_2.setGeometry(QtCore.QRect(1450, 665, 141, 21))
        self.binminvalue_2.setObjectName("binminvalue_2")
        self.binminvalue_2.setText("15")        # Valor por defecto
        
        # Etiqueta de selección de cantidad de bines inicial de la edificación 1
        self.initialBinLabel_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.initialBinLabel_1.setGeometry(QtCore.QRect(10, 690, 101, 21))
        self.initialBinLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.initialBinLabel_1.setObjectName("initialBinLabel_1")
        
        # Etiqueta de selección de cantidad de bines inicial de la edificación 2
        self.initialBinLabel_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_2)
        self.initialBinLabel_2.setGeometry(QtCore.QRect(1340, 690, 101, 21))
        self.initialBinLabel_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.initialBinLabel_2.setObjectName("initialBinLabel_2")
        
        # Línea para introducir cantidad de bines inicial de la edificación 1
        self.bininitialvalue_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.bininitialvalue_1.setGeometry(QtCore.QRect(120, 690, 141, 21))
        self.bininitialvalue_1.setObjectName("bininitialvalue_1")
        self.bininitialvalue_1.setText("50")    # Valor por defecto
        
        # Línea para introducir cantidad de bines inicial de la edificación 2
        self.bininitialvalue_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_2)
        self.bininitialvalue_2.setGeometry(QtCore.QRect(1450, 690, 141, 21))
        self.bininitialvalue_2.setObjectName("bininitialvalue_2")
        self.bininitialvalue_2.setText("50")    # Valor por defecto
        
        # Botón para generación de curvas de excedecnia de edificación 1
        self.SEC_bulding_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.SEC_bulding_1.setGeometry(QtCore.QRect(20, 750, 120, 31))
        self.SEC_bulding_1.setObjectName("SEC_bulding_1")
        
        # Botón para generación de curvas de excedecnia de edificación 2
        self.SEC_bulding_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.SEC_bulding_2.setGeometry(QtCore.QRect(1350, 750, 120, 31))
        self.SEC_bulding_2.setObjectName("SEC_bulding_2")
        
        # Botón para generación de curvas de fragilidad de edificación 1
        self.Fragility_bulding_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.Fragility_bulding_1.setGeometry(QtCore.QRect(140, 750, 120, 31))
        self.Fragility_bulding_1.setObjectName("Fragility_bulding_1")
        
        # Botón para generación de curvas de fragilidad de edificación 2
        self.Fragility_bulding_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_2)
        self.Fragility_bulding_2.setGeometry(QtCore.QRect(1470, 750, 120, 31))
        self.Fragility_bulding_2.setObjectName("Fragility_bulding_2")
        
        # ----------------------------------------------------------
        # GRAFICAS DE CURVAS DE FRAGILIDAD PRINCIPALES
        
        # ----------------------------------------------------------
        # TABWIDGET_1_1: SEC, FragilityCurves, PDFs of EDP
        
        # Frame para ubicación de los tabWidget_1_1
        self.frame_1_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frame_1_1.setGeometry(QtCore.QRect(280, 0, 1041, 391))
        self.frame_1_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1_1.setObjectName("frame_1_1")
        
        # Definición de la cinta de tabWidget_1_1
        self.tabWidget_1_1 = QtWidgets.QTabWidget(self.frame_1_1)
        self.tabWidget_1_1.setGeometry(QtCore.QRect(0, 20, 1041, 361))
        self.tabWidget_1_1.setObjectName("tabWidget_1_1")
        
        # Título de gráfica de la edificación 1
        self.label_curve1 = QtWidgets.QLabel(self.frame_1_1)
        self.label_curve1.setGeometry(QtCore.QRect(0, 0, 501, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_curve1.setFont(font)
        self.label_curve1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_curve1.setObjectName("label_curve1")
        
        # Título de gráfica de la edificación 2
        self.label_curve2 = QtWidgets.QLabel(self.frame_1_1)
        self.label_curve2.setGeometry(QtCore.QRect(520, 0, 501, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_curve2.setFont(font)
        self.label_curve2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_curve2.setObjectName("label_curve2")
        
        #----
        # tabWidget_1_1 SEC:
        
        # Apertura del tabWidget_1_1 de SEC
        self.SEC = QtWidgets.QWidget()
        self.SEC.setObjectName("SEC")
        
        # Frame de la gráfica de la edificación 1
        self.frame_fragilityD_1 = QtWidgets.QFrame(self.SEC)
        self.frame_fragilityD_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_fragilityD_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fragilityD_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fragilityD_1.setObjectName("frame_fragilityD_1")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.frame_fragilityD_1)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.graph_fragilityD_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.graph_fragilityD_1.setContentsMargins(0, 0, 0, 0)
        self.graph_fragilityD_1.setObjectName("graph_fragilityD_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_fragilityD_2 = QtWidgets.QFrame(self.SEC)
        self.frame_fragilityD_2.setGeometry(QtCore.QRect(510, -10, 511, 361))
        self.frame_fragilityD_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fragilityD_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fragilityD_2.setObjectName("frame_fragilityD_2")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.frame_fragilityD_2)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 501, 331))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.graph_fragilityD_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.graph_fragilityD_2.setContentsMargins(0, 0, 0, 0)
        self.graph_fragilityD_2.setObjectName("graph_fragilityD_2")
        
        # Cierre del Tab
        self.tabWidget_1_1.addTab(self.SEC, "")
        
        #----
        # tabWidget_1_1 FragilityCurves:
            
        # Apertura del tabWidget_1_1 de FragilityCurves
        self.FragilityCurves = QtWidgets.QWidget()
        self.FragilityCurves.setObjectName("FragilityCurves")
        
        # Frame de la gráfica de la edificación 1
        self.frame_fragilityP_1 = QtWidgets.QFrame(self.FragilityCurves)
        self.frame_fragilityP_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_fragilityP_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fragilityP_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fragilityP_1.setObjectName("frame_fragilityP_1")
        self.verticalLayoutWidget_7 = QtWidgets.QWidget(self.frame_fragilityP_1)
        self.verticalLayoutWidget_7.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_7.setObjectName("verticalLayoutWidget_7")
        self.graph_fragilityP_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_7)
        self.graph_fragilityP_1.setContentsMargins(0, 0, 0, 0)
        self.graph_fragilityP_1.setObjectName("graph_fragilityP_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_fragilityP_2 = QtWidgets.QFrame(self.FragilityCurves)
        self.frame_fragilityP_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_fragilityP_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_fragilityP_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_fragilityP_2.setObjectName("frame_fragilityP_2")
        self.verticalLayoutWidget_8 = QtWidgets.QWidget(self.frame_fragilityP_2)
        self.verticalLayoutWidget_8.setGeometry(QtCore.QRect(0, 10, 511, 331))
        self.verticalLayoutWidget_8.setObjectName("verticalLayoutWidget_8")
        self.graph_fragilityP_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_8)
        self.graph_fragilityP_2.setContentsMargins(0, 0, 0, 0)
        self.graph_fragilityP_2.setObjectName("graph_fragilityP_2")
        
        # Cierre del Tab
        self.tabWidget_1_1.addTab(self.FragilityCurves, "")
        
        #----
        # tabWidget_1_1 PDFs OF EDP:
        
        # Apertura del tabWidget_1_1 de PDFs of EDP
        self.pdf_EDPs = QtWidgets.QWidget()
        self.pdf_EDPs.setObjectName("pdf_EDPs")
        
        # Frame de la gráfica de pdfs de la edificación 1
        self.frame_PDF_1 = QtWidgets.QFrame(self.pdf_EDPs)
        self.frame_PDF_1.setGeometry(QtCore.QRect(0, -10, 471, 361))
        self.frame_PDF_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_PDF_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_PDF_1.setObjectName("frame_PDF_1")
        self.verticalLayoutWidget_12 = QtWidgets.QWidget(self.frame_PDF_1)
        self.verticalLayoutWidget_12.setGeometry(QtCore.QRect(0, 10, 471, 331))
        self.verticalLayoutWidget_12.setObjectName("verticalLayoutWidget_12")
        self.PDF_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_12)
        self.PDF_1.setContentsMargins(0, 0, 0, 0)
        self.PDF_1.setObjectName("PDF_1")
        
        # Frame de la gráfica de pdfs de la edificación 2
        self.frame_PDF_2 = QtWidgets.QFrame(self.pdf_EDPs)
        self.frame_PDF_2.setGeometry(QtCore.QRect(510, -10, 471, 361))
        self.frame_PDF_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_PDF_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_PDF_2.setObjectName("frame_PDF_2")
        self.verticalLayoutWidget_11 = QtWidgets.QWidget(self.frame_PDF_2)
        self.verticalLayoutWidget_11.setGeometry(QtCore.QRect(10, 10, 471, 331))
        self.verticalLayoutWidget_11.setObjectName("verticalLayoutWidget_11")
        self.PDF_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_11)
        self.PDF_2.setContentsMargins(0, 0, 0, 0)
        self.PDF_2.setObjectName("PDF_2")
        
        # Desplegables para selección de IMs de las pdfs de la edificación 1
        self.IM_1_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_1_1.setGeometry(QtCore.QRect(440, 40, 71, 22))
        self.IM_1_1.setObjectName("IM_1_1")
        self.IM_2_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_2_1.setGeometry(QtCore.QRect(440, 80, 71, 22))
        self.IM_2_1.setObjectName("IM_2_1")
        self.IM_3_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_3_1.setGeometry(QtCore.QRect(440, 120, 71, 22))
        self.IM_3_1.setObjectName("IM_3_1")
        self.IM_4_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_4_1.setGeometry(QtCore.QRect(440, 160, 71, 22))
        self.IM_4_1.setObjectName("IM_4_1")
        self.IM_5_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_5_1.setGeometry(QtCore.QRect(440, 200, 71, 22))
        self.IM_5_1.setObjectName("IM_5_1")
        self.IM_6_1 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_6_1.setGeometry(QtCore.QRect(440, 240, 71, 22))
        self.IM_6_1.setObjectName("IM_6_1")
        
        # Desplegables para selección de IMs de las pdfs de la edificación 2
        self.IM_1_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_1_2.setGeometry(QtCore.QRect(960, 40, 71, 22))
        self.IM_1_2.setObjectName("IM_1_2")
        self.IM_2_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_2_2.setGeometry(QtCore.QRect(960, 80, 71, 22))
        self.IM_2_2.setObjectName("IM_2_2")
        self.IM_3_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_3_2.setGeometry(QtCore.QRect(960, 120, 71, 22))
        self.IM_3_2.setObjectName("IM_3_2")
        self.IM_4_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_4_2.setGeometry(QtCore.QRect(960, 160, 71, 22))
        self.IM_4_2.setObjectName("IM_4_2")
        self.IM_5_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_5_2.setGeometry(QtCore.QRect(960, 200, 71, 22))
        self.IM_5_2.setObjectName("IM_5_2")
        self.IM_6_2 = QtWidgets.QComboBox(self.pdf_EDPs)
        self.IM_6_2.setGeometry(QtCore.QRect(960, 240, 71, 22))
        self.IM_6_2.setObjectName("IM_6_2")
        
        # Título de selección de IMs de la edificación 1
        self.IM_values_1 = QtWidgets.QLabel(self.pdf_EDPs)
        self.IM_values_1.setGeometry(QtCore.QRect(440, 0, 81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.IM_values_1.setFont(font)
        self.IM_values_1.setAlignment(QtCore.Qt.AlignCenter)
        self.IM_values_1.setObjectName("IM_values_1")
        
        # Título de selección de IMs de la edificación 2
        self.IM_values_2 = QtWidgets.QLabel(self.pdf_EDPs)
        self.IM_values_2.setGeometry(QtCore.QRect(960, 0, 81, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.IM_values_2.setFont(font)
        self.IM_values_2.setAlignment(QtCore.Qt.AlignCenter)
        self.IM_values_2.setObjectName("IM_values_2")
        
        # Botón para generación de pdfs de la edificación 1
        self.PDFs_button_1 = QtWidgets.QPushButton(self.pdf_EDPs)
        self.PDFs_button_1.setGeometry(QtCore.QRect(440, 287, 71, 41))
        self.PDFs_button_1.setObjectName("PDFs_button_1")
        
        # Botón para generación de pdfs de la edificación 2
        self.PDFs_button_2 = QtWidgets.QPushButton(self.pdf_EDPs)
        self.PDFs_button_2.setGeometry(QtCore.QRect(960, 287, 71, 41))
        self.PDFs_button_2.setObjectName("PDFs_button_2")
        
        # Cierre del Tab
        self.tabWidget_1_1.addTab(self.pdf_EDPs, "")
        
        # ----------------------------------------------------------
        # TABWIDGET_1_2: DISPERSION, Binning_SEC, Binning_FC, COMPARISON AND COMBINATION
        
        # Frame para ubicación de los tabWidget_1_2
        self.frame_1_2 = QtWidgets.QFrame(self.scrollAreaWidgetContents_2)
        self.frame_1_2.setGeometry(QtCore.QRect(280, 390, 1041, 431))
        self.frame_1_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1_2.setObjectName("frame_1_2")
        
        # Definición de la cinta de tabWidget_1_2
        self.tabWidget_1_2 = QtWidgets.QTabWidget(self.frame_1_2)
        self.tabWidget_1_2.setGeometry(QtCore.QRect(0, 0, 1041, 401))
        self.tabWidget_1_2.setObjectName("tabWidget_1_2")
        
        #----
        # tabWidget_1_2 DISPERSION: 
            
        # Apertura del tabWidget_1_2 de dispersión
        self.Dispersion = QtWidgets.QWidget()
        self.Dispersion.setObjectName("Dispersion")
        
        # Frame para gráfica de dispersión de la edificación 1
        self.frame_Dispersion_B1 = QtWidgets.QFrame(self.Dispersion)
        self.frame_Dispersion_B1.setGeometry(QtCore.QRect(0, 10, 501, 321))
        self.frame_Dispersion_B1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Dispersion_B1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Dispersion_B1.setObjectName("frame_Dispersion_B1")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.frame_Dispersion_B1)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.Dispersion_B1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.Dispersion_B1.setContentsMargins(0, 0, 0, 0)
        self.Dispersion_B1.setObjectName("Dispersion_B1")
        
        # Frame para gráfica de dispersión de la edificación 2
        self.frame_Dispersion_B2 = QtWidgets.QFrame(self.Dispersion)
        self.frame_Dispersion_B2.setGeometry(QtCore.QRect(520, 10, 501, 321))
        self.frame_Dispersion_B2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Dispersion_B2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Dispersion_B2.setObjectName("frame_Dispersion_B2")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.frame_Dispersion_B2)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.Dispersion_B2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.Dispersion_B2.setContentsMargins(0, 0, 0, 0)
        self.Dispersion_B2.setObjectName("Dispersion_B2")
        
        # Botón para generación de gráficas de dispersion 1
        self.refresh_dispersion_1 = QtWidgets.QPushButton(self.Dispersion)
        self.refresh_dispersion_1.setGeometry(QtCore.QRect(180, 340, 131, 31))
        self.refresh_dispersion_1.setObjectName("refresh_dispersion_1")
        
        # Botón para generación de gráficas de dispersion 2
        self.refresh_dispersion_2 = QtWidgets.QPushButton(self.Dispersion)
        self.refresh_dispersion_2.setGeometry(QtCore.QRect(710, 340, 131, 31))
        self.refresh_dispersion_2.setObjectName("refresh_dispersion_2")
        
        # Cierre del Tab
        self.tabWidget_1_2.addTab(self.Dispersion, "")
        
        #----
        # tabWidget_1_2 Binning_SEC:
            
        # Apertura del de tabWidget_1_2 de Binning_SEC  
        self.Binning_SEC  = QtWidgets.QWidget()
        self.Binning_SEC .setObjectName("Binning_SEC ")
        
        # Frame para gráfica de bineado de la edificación 1
        self.frame_BinD_1 = QtWidgets.QFrame(self.Binning_SEC )
        self.frame_BinD_1.setGeometry(QtCore.QRect(0, 10, 501, 321))
        self.frame_BinD_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BinD_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BinD_1.setObjectName("frame_BinD_1")
        self.verticalLayoutWidget_13 = QtWidgets.QWidget(self.frame_BinD_1)
        self.verticalLayoutWidget_13.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_13.setObjectName("verticalLayoutWidget_13")
        self.BinD_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_13)
        self.BinD_1.setContentsMargins(0, 0, 0, 0)
        self.BinD_1.setObjectName("BinD_1")
        
        # Frame para gráfica de bineado de la edificación 2
        self.frame_BinD_2 = QtWidgets.QFrame(self.Binning_SEC )
        self.frame_BinD_2.setGeometry(QtCore.QRect(520, 10, 501, 321))
        self.frame_BinD_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BinD_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BinD_2.setObjectName("frame_BinD_2")
        self.verticalLayoutWidget_14 = QtWidgets.QWidget(self.frame_BinD_2)
        self.verticalLayoutWidget_14.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_14.setObjectName("verticalLayoutWidget_14")
        self.BinD_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_14)
        self.BinD_2.setContentsMargins(0, 0, 0, 0)
        self.BinD_2.setObjectName("BinD_2")
        
        # Cierre del Tab
        self.tabWidget_1_2.addTab(self.Binning_SEC , "")
        
        #----
        # tabWidget_1_2 Binning_FC:
        
        # Apertura del de tabWidget_1_2 de Binning_Cens
        self.Binning_FC = QtWidgets.QWidget()
        self.Binning_FC.setObjectName("Binning_FC")
        
        # Frame para gráfica de bineado de la edificación 1
        self.frame_BinP_1 = QtWidgets.QFrame(self.Binning_FC)
        self.frame_BinP_1.setGeometry(QtCore.QRect(0, 10, 501, 321))
        self.frame_BinP_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BinP_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BinP_1.setObjectName("frame_BinP_1")
        self.verticalLayoutWidget_17 = QtWidgets.QWidget(self.frame_BinP_1)
        self.verticalLayoutWidget_17.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_17.setObjectName("verticalLayoutWidget_17")
        self.BinP_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_17)
        self.BinP_1.setContentsMargins(0, 0, 0, 0)
        self.BinP_1.setObjectName("BinP_1")
        
        # Frame para gráfica de bineado de la edificación 2
        self.frame_BinP_2 = QtWidgets.QFrame(self.Binning_FC)
        self.frame_BinP_2.setGeometry(QtCore.QRect(520, 10, 501, 321))
        self.frame_BinP_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_BinP_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_BinP_2.setObjectName("frame_BinP_2")
        self.verticalLayoutWidget_18 = QtWidgets.QWidget(self.frame_BinP_2)
        self.verticalLayoutWidget_18.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_18.setObjectName("verticalLayoutWidget_18")
        self.BinP_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_18)
        self.BinP_2.setContentsMargins(0, 0, 0, 0)
        self.BinP_2.setObjectName("BinP_2")
        
        # Cierre del Tab
        self.tabWidget_1_2.addTab(self.Binning_FC, "")
        
        #----
        # tabWidget_1_2 COMPARACIÓN Y COMBINACION:
        
        # Apertura del tabWidget_1_2 de comparación y dispersión
        self.Comparison_Combination = QtWidgets.QWidget()
        self.Comparison_Combination.setObjectName("Comparison_Combination")
        
        # Frame para gráfica de comparación de curvas   
        self.frame_comparison = QtWidgets.QFrame(self.Comparison_Combination)
        self.frame_comparison.setGeometry(QtCore.QRect(0, 10, 501, 321))
        self.frame_comparison.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comparison.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comparison.setObjectName("frame_comparison")
        self.verticalLayoutWidget_5 = QtWidgets.QWidget(self.frame_comparison)
        self.verticalLayoutWidget_5.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_5.setObjectName("verticalLayoutWidget_5")
        self.graph_comparison = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_5)
        self.graph_comparison.setContentsMargins(0, 0, 0, 0)
        self.graph_comparison.setObjectName("graph_comparison")   
        
        # Frame para gráfica de combinación de curvas
        self.frame_combine_curve = QtWidgets.QFrame(self.Comparison_Combination)
        self.frame_combine_curve.setGeometry(QtCore.QRect(520, 10, 501, 321))
        self.frame_combine_curve.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_combine_curve.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_combine_curve.setObjectName("frame_combine_curve")
        self.verticalLayoutWidget_6 = QtWidgets.QWidget(self.frame_combine_curve)
        self.verticalLayoutWidget_6.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_6.setObjectName("verticalLayoutWidget_6")
        self.graph_combine_curve = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_6)
        self.graph_combine_curve.setContentsMargins(0, 0, 0, 0)
        self.graph_combine_curve.setObjectName("graph_combine_curve")
        
        # Desplegable para seleccionar si la comparación de curvas será con curvas DET o PROB
        self.ComparisonType = QtWidgets.QComboBox(self.Comparison_Combination)
        self.ComparisonType.setGeometry(QtCore.QRect(440, 350, 151, 22))
        self.ComparisonType.setObjectName("ComparisonType")
        self.ComparisonType.addItem("SEC")    # Adiciona opción de desplegable
        self.ComparisonType.addItem("Fragility")    # Adiciona opción de desplegable
        
        # Botón para generación de grafica de comparación
        self.comparison_button = QtWidgets.QPushButton(self.Comparison_Combination)
        self.comparison_button.setGeometry(QtCore.QRect(180, 340, 131, 31))
        self.comparison_button.setObjectName("comparison_button")
        
        # Botón para generación de grafica de combinación
        self.combined_curve_button = QtWidgets.QPushButton(self.Comparison_Combination)
        self.combined_curve_button.setGeometry(QtCore.QRect(680, 340, 171, 31))
        self.combined_curve_button.setObjectName("combined_curve_button")
        
        # Cierre del Tab
        self.tabWidget_1_2.addTab(self.Comparison_Combination, "")
       
        # ----------------------------------------------------------
        # Otros
        
        # Scrolls
        self.verticalScrollBar_Structural = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.verticalScrollBar_Structural.setGeometry(QtCore.QRect(1630, 0, 16, 781))
        self.verticalScrollBar_Structural.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_Structural.setObjectName("verticalScrollBar_Structural")
        self.horizontalScrollBar_Structural = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_2)
        self.horizontalScrollBar_Structural.setGeometry(QtCore.QRect(0, 790, 1631, 16))
        self.horizontalScrollBar_Structural.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_Structural.setObjectName("horizontalScrollBar_Structural")
     
        self.scrollArea_Structural.setWidget(self.scrollAreaWidgetContents_2)
        
        # Cierre del Tab de Fragility Analysis
        self.tabWidget_General.addTab(self.FragilityAnalysis, "")
        
        
        # ################################################################
        # TABWIDGET FRAGILITY OF TAXONOMIES
        # ################################################################
        
        # Tab de fragilidad de taxonomias
        self.FragilityTaxonomy = QtWidgets.QWidget()
        self.FragilityTaxonomy.setObjectName("FragilityTaxonomy")
        
        # Area Scroll del Tab de rfagilidad de taxonomias
        self.scrollArea_taxonomy_1 = QtWidgets.QScrollArea(self.FragilityTaxonomy)
        self.scrollArea_taxonomy_1.setGeometry(QtCore.QRect(0, 0, 1651, 811))
        self.scrollArea_taxonomy_1.setWidgetResizable(True)
        self.scrollArea_taxonomy_1.setObjectName("scrollArea_taxonomy_1")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 1649, 809))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        
        # ----------------------------------------------------------
        ## INPUTS
        
        # Título
        self.input_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.input_label.setGeometry(QtCore.QRect(20, 5, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.input_label.setFont(font)
        self.input_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.input_label.setObjectName("input_label")
        
        
        # ----------------------
        # IM AND EDP DEFINITION
        
        # Título
        self.IM_EDP_selection_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IM_EDP_selection_3.setGeometry(QtCore.QRect(80, 60, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.IM_EDP_selection_3.setFont(font)
        self.IM_EDP_selection_3.setObjectName("IM_EDP_selection_3")
        
        # Etiqueta para introducir periodos
        self.PeriodoLabel_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.PeriodoLabel_3.setGeometry(QtCore.QRect(40, 90, 61, 21))
        self.PeriodoLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PeriodoLabel_3.setObjectName("PeriodoLabel_3")
        
        # Linea para introducir periodos
        self.periodo_value_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.periodo_value_3.setGeometry(QtCore.QRect(110, 90, 141, 21))
        self.periodo_value_3.setObjectName("periodo_value_3")
        self.periodo_value_3.setText("0.6,1")                       # Valor por defecto
        
        # Etiqueta para selección de tipo de IM
        self.IMType_Label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IMType_Label_3.setGeometry(QtCore.QRect(50, 115, 51, 20))
        self.IMType_Label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IMType_Label_3.setObjectName("IMType_Label_3")
        
        # Desplegable para seleccionar tipo de IM
        self.IMType_Value_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.IMType_Value_3.setGeometry(QtCore.QRect(110, 115, 73, 22))
        self.IMType_Value_3.setObjectName("IMType_Value_3")
        self.IMType_Value_3.addItem("Sa")            # Adiciona opción de desplegable
        self.IMType_Value_3.addItem("SaAVG")         # Adiciona opción de desplegable
        
        # Etiqueta para tipo de EDP
        self.EDPType_Label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.EDPType_Label_3.setGeometry(QtCore.QRect(40, 140, 61, 20))
        self.EDPType_Label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPType_Label_3.setObjectName("EDPType_Label_3")
        
        # Desplegable para introducir tipo de EDP
        self.EDPType_Value_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.EDPType_Value_3.setGeometry(QtCore.QRect(110, 140, 73, 22))
        self.EDPType_Value_3.setObjectName("EDPType_Value_3")
        self.EDPType_Value_3.addItem("SDR")         # Adiciona opción de desplegable
        self.EDPType_Value_3.addItem("RSDR")        # Adiciona opción de desplegable
        self.EDPType_Value_3.addItem("PFA")         # Adiciona opción de desplegable
        
        # Desplegable para introducir el piso del EDP considerado
        self.EDPType_ValueStory_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.EDPType_ValueStory_3.setGeometry(QtCore.QRect(190, 140, 61, 22))
        self.EDPType_ValueStory_3.setObjectName("EDPType_ValueStory_3")
        self.EDPType_ValueStory_3.addItem("max")         # Adiciona opción de desplegable

        
        # ----------------------
        # FRAGILITY PARAMETERS
        
        # Título
        self.FragilityTittle_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.FragilityTittle_3.setGeometry(QtCore.QRect(560, 60, 171, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.FragilityTittle_3.setFont(font)
        self.FragilityTittle_3.setObjectName("FragilityTittle_3")
        
        # Etiqueta para introducir porcentajes de curvas
        self.porc_fit_curves_Label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_Label_3.setGeometry(QtCore.QRect(340, 90, 111, 21))
        self.porc_fit_curves_Label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.porc_fit_curves_Label_3.setObjectName("porc_fit_curves_Label_3")
        
        # Linea para introducir porcentajes de curvas
        self.porc_fit_curves_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_3.setGeometry(QtCore.QRect(460, 90, 141, 21))
        self.porc_fit_curves_3.setObjectName("porc_fit_curves_3")
        self.porc_fit_curves_3.setText("1,1,1,1")                            # Valor por defecto
        
        # Etiqueta para introducir el tipo de bineado
        self.binLabel_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.binLabel_3.setGeometry(QtCore.QRect(380, 115, 71, 21))
        self.binLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binLabel_3.setObjectName("binLabel_3")
        
        # Desplegable para seleccionar tipo de bineado
        self.Bintype_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.Bintype_3.setGeometry(QtCore.QRect(460, 115, 141, 22))
        self.Bintype_3.setObjectName("Bintype_3")
        self.Bintype_3.addItem("Logspace")      # Adiciona opción de desplegable
        self.Bintype_3.addItem("Linespace")     # Adiciona opción de desplegable
        
        # Etiqueta para indicar si se incluye censura en el bineado
        self.include_cens_Label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.include_cens_Label_3.setGeometry(QtCore.QRect(350, 140, 101, 21))
        self.include_cens_Label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.include_cens_Label_3.setObjectName("include_cens_Label_3")
        
        # Desplegable para indicar si se incluye censura en el bineado
        self.includeCens_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.includeCens_3.setGeometry(QtCore.QRect(460, 140, 141, 22))
        self.includeCens_3.setObjectName("includeCens_3")
        self.includeCens_3.addItem("Yes")        # Adiciona opción de desplegable
        self.includeCens_3.addItem("No")         # Adiciona opción de desplegable
        
        # Etiqueta para indicar el metodo de colapso a utilizar
        self.collapseMethod_Label_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.collapseMethod_Label_3.setGeometry(QtCore.QRect(620, 90, 111, 21))
        self.collapseMethod_Label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.collapseMethod_Label_3.setObjectName("collapseMethod_Label_3")
        
        # Desplegable para indicar el metodo de colapso a utilizar
        self.collapseMethod_3 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.collapseMethod_3.setGeometry(QtCore.QRect(740, 90, 141, 22))
        self.collapseMethod_3.setObjectName("collapseMethod_3")
        self.collapseMethod_3.addItem("count")           # Adiciona opción de desplegable
        self.collapseMethod_3.addItem("count columns")   # Adiciona opción de desplegable
        self.collapseMethod_3.addItem("fit")             # Adiciona opción de desplegable
        
        # Etiqueta para introducir el minimo número de datos por bin
        self.binMinLabel_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.binMinLabel_3.setGeometry(QtCore.QRect(640, 115, 91, 21))
        self.binMinLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.binMinLabel_3.setObjectName("binMinLabel_3")
        
        # Línea para introducir el minimo número de datos por bin
        self.binminvalue_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.binminvalue_3.setGeometry(QtCore.QRect(740, 115, 141, 21))
        self.binminvalue_3.setObjectName("binminvalue_3")
        self.binminvalue_3.setText("15")        # Valor por defecto
        
        # Etiqueta para introducir el número de bines inicial
        self.initialBinLabel_3 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.initialBinLabel_3.setGeometry(QtCore.QRect(630, 140, 101, 21))
        self.initialBinLabel_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.initialBinLabel_3.setObjectName("initialBinLabel_3")
        
        # Línea para introducir el número de bines inicial
        self.bininitialvalue_3 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.bininitialvalue_3.setGeometry(QtCore.QRect(740, 140, 141, 21))
        self.bininitialvalue_3.setObjectName("bininitialvalue_3")
        self.bininitialvalue_3.setText("50")    # Valor por defecto
        
        # ----------------------
        # GROUPING OF BUILDINGS
        
        # Titulo
        self.Group_buildings = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.Group_buildings.setGeometry(QtCore.QRect(970, 40, 161, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.Group_buildings.setFont(font)
        self.Group_buildings.setObjectName("Group_buildings")
        
        # Etiqueta de criterio de agrupacion (columnas del excel guia)
        self.group_criteria_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.group_criteria_label.setGeometry(QtCore.QRect(920, 70, 111, 21))
        self.group_criteria_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.group_criteria_label.setObjectName("group_criteria_label")
        
        # Desplegable de criterio de agrupacion (columnas del excel guia)
        self.Group_Value = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.Group_Value.setGeometry(QtCore.QRect(1040, 70, 161, 22))
        self.Group_Value.setObjectName("Group_Value")
        
        # ----------------------
        # BUILDING RESULTS FOLDERS
        
        # Título
        self.Results_folders = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.Results_folders.setGeometry(QtCore.QRect(970, 110, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.Results_folders.setFont(font)
        self.Results_folders.setObjectName("Results_folders")
        
        # Etiqueta para seleccionar ubicacion de excel de resultados
        self.global_folder_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.global_folder_label.setGeometry(QtCore.QRect(920, 140, 111, 21))
        self.global_folder_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.global_folder_label.setObjectName("global_folder_label")
        
        # Boton para seleccionar ubicacion de excel de resultados
        self.global_folder_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.global_folder_button.setGeometry(QtCore.QRect(1040, 140, 161, 22))
        self.global_folder_button.setObjectName("global_folder_button")
        
        # ----------------------
        # DATABASE GENERATION
        
        # Título
        self.database_generation = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.database_generation.setGeometry(QtCore.QRect(1320, 40, 181, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.database_generation.setFont(font)
        self.database_generation.setObjectName("database_generation")
        
        # Etiqueta para introducir nombre de excel de resultados
        self.excel_name_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.excel_name_label.setGeometry(QtCore.QRect(1280, 70, 71, 21))
        self.excel_name_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.excel_name_label.setObjectName("excel_name_label")
        
        # Línea para introducir nombre de excel de resultados
        self.excel_name_value = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.excel_name_value.setGeometry(QtCore.QRect(1360, 70, 141, 21))
        self.excel_name_value.setObjectName("excel_name_value")
        self.excel_name_value.setText("Resultados")    # Valor por defecto
        
        # Texto que indica que el archivo se genera en .xlsx
        self.xlsx = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.xlsx.setGeometry(QtCore.QRect(1510, 70, 71, 21))
        self.xlsx.setObjectName("xlsx")
        
        # Etiqueta para seleccionar carpeta donde se guardará el excel de resultados
        self.excel_location_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.excel_location_label.setGeometry(QtCore.QRect(1230, 100, 121, 21))
        self.excel_location_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.excel_location_label.setObjectName("excel_location_label")
        
        # Botón para seleccionar carpeta donde se guardará el excel de resultados
        self.excel_folder_button = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.excel_folder_button.setGeometry(QtCore.QRect(1360, 100, 141, 22))
        self.excel_folder_button.setObjectName("excel_folder_button")
        
        # ----------------------
        # RUN BUTTON AND STATUTS
        
        # Boton para iniciar caluclos de taxonomias
        self.start_calculations = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.start_calculations.setGeometry(QtCore.QRect(960, 180, 161, 51))
        self.start_calculations.setObjectName("start_calculations")
        
        # Texto que indica status de generacion de tada T, TAX, Build
        self.status_taxonomy = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.status_taxonomy.setGeometry(QtCore.QRect(1150, 170, 431, 41))
        self.status_taxonomy.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.status_taxonomy.setAlignment(QtCore.Qt.AlignCenter)
        self.status_taxonomy.setObjectName("status_taxonomy")
        
        # Texto que indica status de excel: procesando o terminado
        self.processing_finishing_status = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.processing_finishing_status.setGeometry(QtCore.QRect(1150, 210, 431, 21))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.processing_finishing_status.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.processing_finishing_status.setFont(font)
        self.processing_finishing_status.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.processing_finishing_status.setAlignment(QtCore.Qt.AlignCenter)
        self.processing_finishing_status.setObjectName("processing_finishing_status")
        
        # ----------------------------------------------------------
        ## LINEAS DE SEPARACION DE INPUTS Y GRAPHICS
        
        # Linea 1
        self.line = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.line.setGeometry(QtCore.QRect(20, 230, 1561, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        
        # Linea 2
        self.line_3 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.line_3.setGeometry(QtCore.QRect(910, 160, 671, 20))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        
        # ----------------------------------------------------------
        ## GRAPHICS
        
        # Título
        self.graphics_label = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.graphics_label.setGeometry(QtCore.QRect(20, 250, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        self.graphics_label.setFont(font)
        self.graphics_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.graphics_label.setObjectName("graphics_label")
        
        # Boton para cargar archivo
        self.Load_Excel_Tax = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Load_Excel_Tax.setGeometry(QtCore.QRect(740, 250, 120, 31))
        self.Load_Excel_Tax.setObjectName("Load_Excel_Tax")
        
        # Etiqueta que dice el nombre del archivo del excel cargado
        self.excel_name_load = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.excel_name_load.setGeometry(QtCore.QRect(880, 250, 401, 31))
        self.excel_name_load.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.excel_name_load.setObjectName("excel_name_load")
        
        # ----------------------
        # GENERALIDADES PARA GRAFICAR
        
        # Título de taxonomia 1
        self.Taxonomy_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.Taxonomy_1.setGeometry(QtCore.QRect(30, 300, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.Taxonomy_1.setFont(font)
        self.Taxonomy_1.setObjectName("Taxonomy_1")
        
        # Título de taxonomia 2
        self.Taxonomy_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.Taxonomy_2.setGeometry(QtCore.QRect(1440, 300, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.Taxonomy_2.setFont(font)
        self.Taxonomy_2.setObjectName("Taxonomy_2")
        
        # Etiqueta de IM a utilizar para graficar la taxonomia 1
        self.IMLabelTax_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IMLabelTax_1.setGeometry(QtCore.QRect(0, 350, 61, 21))
        self.IMLabelTax_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IMLabelTax_1.setObjectName("IMLabelTax_1")
        
        # Etiqueta de IM a utilizar para graficar la taxonomia 2
        self.IMLabelTax_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IMLabelTax_2.setGeometry(QtCore.QRect(1400, 350, 61, 21))
        self.IMLabelTax_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IMLabelTax_2.setObjectName("IMLabelTax_2")
        
        # Desplegable para seleccionar IM a utilizar para graficar la taxonomia 1
        self.IMTax_value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.IMTax_value_1.setGeometry(QtCore.QRect(69, 350, 141, 22))
        self.IMTax_value_1.setObjectName("IMTax_value_1")
        
        # Desplegable para seleccionar IM a utilizar para graficar la taxonomia 2
        self.IMTax_value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.IMTax_value_2.setGeometry(QtCore.QRect(1469, 350, 141, 22))
        self.IMTax_value_2.setObjectName("IMTax_value_2")
        
        # Etiqueta de periodo a utilizar para graficar la taxonomia 1
        self.PeriodoLabelTax_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.PeriodoLabelTax_1.setGeometry(QtCore.QRect(0, 375, 61, 21))
        self.PeriodoLabelTax_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PeriodoLabelTax_1.setObjectName("PeriodoLabelTax_1")
        
        # Etiqueta de periodo a utilizar para graficar la taxonomia 2
        self.PeriodoLabelTax_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.PeriodoLabelTax_2.setGeometry(QtCore.QRect(1400, 375, 61, 21))
        self.PeriodoLabelTax_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PeriodoLabelTax_2.setObjectName("PeriodoLabelTax_2")
        
        # Desplegable para seleccionar periodo a utilizar para graficar la taxonomia 1
        self.PeriodoTax_value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.PeriodoTax_value_1.setGeometry(QtCore.QRect(69, 375, 141, 22))
        self.PeriodoTax_value_1.setObjectName("PeriodoTax_value_1")
        
        # Desplegable para seleccionar periodo a utilizar para graficar la taxonomia 2
        self.PeriodoTax_value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.PeriodoTax_value_2.setGeometry(QtCore.QRect(1469, 375, 141, 22))
        self.PeriodoTax_value_2.setObjectName("PeriodoTax_value_2")
        
        # Etiqueta para seleccionar taxonomia 1
        self.TaxonomyLabelTax_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.TaxonomyLabelTax_1.setGeometry(QtCore.QRect(-20, 400, 81, 21))
        self.TaxonomyLabelTax_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TaxonomyLabelTax_1.setObjectName("TaxonomyLabelTax_1")
        
        # Etiqueta para seleccionar taxonomia 2
        self.TaxonomyLabelTax_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.TaxonomyLabelTax_2.setGeometry(QtCore.QRect(1380, 400, 81, 21))
        self.TaxonomyLabelTax_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.TaxonomyLabelTax_2.setObjectName("TaxonomyLabelTax_2")
        
        # Desplegable para seleccionar taxonomia 1
        self.TaxonomyTax_value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.TaxonomyTax_value_1.setGeometry(QtCore.QRect(69, 400, 141, 22))
        self.TaxonomyTax_value_1.setObjectName("TaxonomyTax_value_1")
        
        # Desplegable para seleccionar taxonomia 2
        self.TaxonomyTax_value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.TaxonomyTax_value_2.setGeometry(QtCore.QRect(1469, 400, 141, 22))
        self.TaxonomyTax_value_2.setObjectName("TaxonomyTax_value_2")
        
        # Etiqueta para seleccionar parametro de graficas taxonomia 1
        self.ParamLabelTax_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.ParamLabelTax_1.setGeometry(QtCore.QRect(-20, 425, 81, 21))
        self.ParamLabelTax_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ParamLabelTax_1.setObjectName("ParamLabelTax_1")
        
        # Etiqueta para seleccionar parametro de graficas taxonomia 2
        self.ParamLabelTax_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.ParamLabelTax_2.setGeometry(QtCore.QRect(1380, 425, 81, 21))
        self.ParamLabelTax_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ParamLabelTax_2.setObjectName("ParamLabelTax_2")
        
        # Desplegable para seleccionar parametro de graficas taxonomia 1
        self.ParamTax_value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.ParamTax_value_1.setGeometry(QtCore.QRect(69, 425, 141, 22))
        self.ParamTax_value_1.setObjectName("ParamTax_value_1")
        self.ParamTax_value_1.addItem("Theta")        # Adiciona opción de desplegable
        self.ParamTax_value_1.addItem("Beta")         # Adiciona opción de desplegable
        
        # Desplegable para seleccionar parametro de graficas taxonomia 2
        self.ParamTax_value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.ParamTax_value_2.setGeometry(QtCore.QRect(1469, 425, 141, 22))
        self.ParamTax_value_2.setObjectName("ParamTax_value_2")
        self.ParamTax_value_2.addItem("Theta")        # Adiciona opción de desplegable
        self.ParamTax_value_2.addItem("Beta")         # Adiciona opción de desplegable
        
        # Boton para graficar taxonomia 1
        self.Graph_tax_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Graph_tax_1.setGeometry(QtCore.QRect(69, 455, 141, 31))
        self.Graph_tax_1.setObjectName("Graph_tax_1")
        
        # Boton para graficar taxonomia 2
        self.Graph_tax_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Graph_tax_2.setGeometry(QtCore.QRect(1469, 455, 141, 31))
        self.Graph_tax_2.setObjectName("Graph_tax_2")
        
        # ----------------------
        # MODIFICATIONS
        
        # Titulo de modificaciones de taxonomia 1
        self.modifications_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.modifications_Label_1.setGeometry(QtCore.QRect(60, 520, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.modifications_Label_1.setFont(font)
        self.modifications_Label_1.setObjectName("modifications_Label_1")
        
        # Titulo de modificaciones de taxonomia 2
        self.modifications_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.modifications_Label_2.setGeometry(QtCore.QRect(1460, 520, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.modifications_Label_2.setFont(font)
        self.modifications_Label_2.setObjectName("modifications_Label_2")
        
        # Etiqueta para tipo de cambio de la grafica de taxonomia 1
        self.changeType_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.changeType_Label_1.setGeometry(QtCore.QRect(0, 545, 101, 21))
        self.changeType_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.changeType_Label_1.setObjectName("changeType_Label_1")
        
        # Etiqueta para tipo de cambio de la grafica de taxonomia 2
        self.changeType_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.changeType_Label_2.setGeometry(QtCore.QRect(1400, 545, 101, 21))
        self.changeType_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.changeType_Label_2.setObjectName("changeType_Label_2")
        
        # Desplegable para tipo de cambio de la grafica de taxonomia 1
        self.changeType_value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.changeType_value_1.setGeometry(QtCore.QRect(110, 545, 100, 22))
        self.changeType_value_1.setObjectName("changeType_value_1")
        self.changeType_value_1.addItem("None")                 # Adiciona opción de desplegable
        self.changeType_value_1.addItem("Parameters")           # Adiciona opción de desplegable
        self.changeType_value_1.addItem("% Curves fitting")     # Adiciona opción de desplegable
        self.changeType_value_1.addItem("IM limits")            # Adiciona opción de desplegable
        
        # Desplegable para tipo de cambio de la grafica de taxonomia 2
        self.changeType_value_2 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_3)
        self.changeType_value_2.setGeometry(QtCore.QRect(1510, 545, 100, 22))
        self.changeType_value_2.setObjectName("changeType_value_2")
        self.changeType_value_2.addItem("None")                 # Adiciona opción de desplegable
        self.changeType_value_2.addItem("Parameters")           # Adiciona opción de desplegable
        self.changeType_value_2.addItem("% Curves fitting")     # Adiciona opción de desplegable
        self.changeType_value_2.addItem("IM limits")            # Adiciona opción de desplegable
        
        # Etiqueta para introducir nuevos valores theta de la taxonomia 1
        self.thetaTax_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.thetaTax_Label_1.setGeometry(QtCore.QRect(0, 570, 101, 21))
        self.thetaTax_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thetaTax_Label_1.setObjectName("thetaTax_Label_1")
        
        # Etiqueta para introducir nuevos valores theta de la taxonomia 2
        self.thetaTax_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.thetaTax_Label_2.setGeometry(QtCore.QRect(1400, 570, 101, 21))
        self.thetaTax_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.thetaTax_Label_2.setObjectName("thetaTax_Label_2")
        
        # Línea para introducir nuevos valores theta de la taxonomia 1
        self.thetaTax_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.thetaTax_value_1.setGeometry(QtCore.QRect(110, 570, 100, 21))
        self.thetaTax_value_1.setObjectName("thetaTax_value_1")
        
        # Línea para introducir nuevos valores theta de la taxonomia 2
        self.thetaTax_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.thetaTax_value_2.setGeometry(QtCore.QRect(1510, 570, 100, 21))
        self.thetaTax_value_2.setObjectName("thetaTax_value_2")
        
        # Etiqueta para introducir nuevos valores beta de la taxonomia 1
        self.sigmaTax_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.sigmaTax_Label_1.setGeometry(QtCore.QRect(0, 595, 101, 21))
        self.sigmaTax_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sigmaTax_Label_1.setObjectName("sigmaTax_Label_1")
        
        # Etiqueta para introducir nuevos valores beta de la taxonomia 2
        self.sigmaTax_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.sigmaTax_Label_2.setGeometry(QtCore.QRect(1400, 595, 101, 21))
        self.sigmaTax_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.sigmaTax_Label_2.setObjectName("sigmaTax_Label_2")
        
        # Línea para introducir nuevos valores beta de la taxonomia 1
        self.sigmaTax_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.sigmaTax_value_1.setGeometry(QtCore.QRect(110, 595, 100, 21))
        self.sigmaTax_value_1.setObjectName("sigmaTax_value_1")
        
        # Línea para introducir nuevos valores beta de la taxonomia 2
        self.sigmaTax_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.sigmaTax_value_2.setGeometry(QtCore.QRect(1510, 595, 100, 21))
        self.sigmaTax_value_2.setObjectName("sigmaTax_value_2")
        
        # Etiqueta para introducir % de curvas de ajuste de la taxonomia 1
        self.porc_fit_curves_changes_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_changes_Label_1.setGeometry(QtCore.QRect(0, 620, 101, 21))
        self.porc_fit_curves_changes_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.porc_fit_curves_changes_Label_1.setObjectName("porc_fit_curves_changes_Label_1")
        
        # Etiqueta para introducir % de curvas de ajuste de la taxonomia 2
        self.porc_fit_curves_changes_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_changes_Label_2.setGeometry(QtCore.QRect(1400, 620, 101, 21))
        self.porc_fit_curves_changes_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.porc_fit_curves_changes_Label_2.setObjectName("porc_fit_curves_changes_Label_2")
        
        # Linea para introducir % de curvas de ajuste de la taxonomia 1
        self.porc_fit_curves_changes_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_changes_value_1.setGeometry(QtCore.QRect(110, 620, 100, 21))
        self.porc_fit_curves_changes_value_1.setObjectName("porc_fit_curves_changes_value_1")
        
        # Linea para introducir % de curvas de ajuste de la taxonomia 2
        self.porc_fit_curves_changes_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.porc_fit_curves_changes_value_2.setGeometry(QtCore.QRect(1510, 620, 100, 21))
        self.porc_fit_curves_changes_value_2.setObjectName("porc_fit_curves_changes_value_2")
        
        # Etiqueta para introducir límite de valores IM que se tendrán en cuenta para el ajuste de la taxonomia 1
        self.IM_vals_changes_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IM_vals_changes_Label_1.setGeometry(QtCore.QRect(0, 645, 101, 21))
        self.IM_vals_changes_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IM_vals_changes_Label_1.setObjectName("IM_vals_changes_Label_1")
        
        # Etiqueta para introducir límite de valores IM que se tendrán en cuenta para el ajuste de la taxonomia 2
        self.IM_vals_changes_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.IM_vals_changes_value_1.setGeometry(QtCore.QRect(110, 645, 100, 21))
        self.IM_vals_changes_value_1.setObjectName("IM_vals_changes_value_1")
        
        # Linea para introducir límite de valores IM que se tendrán en cuenta para el ajuste de la taxonomia 1
        self.IM_vals_changes_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_3)
        self.IM_vals_changes_Label_2.setGeometry(QtCore.QRect(1400, 645, 101, 21))
        self.IM_vals_changes_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IM_vals_changes_Label_2.setObjectName("IM_vals_changes_Label_2")
        
        # Linea para introducir límite de valores IM que se tendrán en cuenta para el ajuste de la taxonomia 2
        self.IM_vals_changes_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_3)
        self.IM_vals_changes_value_2.setGeometry(QtCore.QRect(1510, 645, 100, 21))
        self.IM_vals_changes_value_2.setObjectName("IM_vals_changes_value_2")
        
        # Boton para graficar modificaciones de la taxonomia 1
        self.Graph_mod_tax_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Graph_mod_tax_1.setGeometry(QtCore.QRect(60, 680, 151, 31))
        self.Graph_mod_tax_1.setObjectName("Graph_mod_tax_1")
        
        # Boton para graficar modificaciones de la taxonomia 2
        self.Graph_mod_tax_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Graph_mod_tax_2.setGeometry(QtCore.QRect(1460, 680, 151, 31))
        self.Graph_mod_tax_2.setObjectName("Graph_mod_tax_2")
        
        # Boton para guardar nuevos parametros de la taxonomia 1
        self.Save_mod_tax_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Save_mod_tax_1.setGeometry(QtCore.QRect(430, 760, 181, 31))
        self.Save_mod_tax_1.setObjectName("Save_mod_tax_1")
        
        # Boton para guardar nuevos parametros de la taxonomia 2
        self.Save_mod_tax_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Save_mod_tax_2.setGeometry(QtCore.QRect(1010, 760, 181, 31))
        self.Save_mod_tax_2.setObjectName("Save_mod_tax_2")
        
        # Boton para exportar cambios de resultados en el excel
        self.Export_tax_mod_excel = QtWidgets.QPushButton(self.scrollAreaWidgetContents_3)
        self.Export_tax_mod_excel.setGeometry(QtCore.QRect(1440, 760, 181, 31))
        self.Export_tax_mod_excel.setObjectName("Export_tax_mod_excel")
        self.scrollArea_taxonomy_1.setWidget(self.scrollAreaWidgetContents_3)
        
        # ----------------------------------------------------------
        # GRAFICAS DE TAXONOMIAS
        
        # ----------------------------------------------------------
        # TABWIDGET_1_4: Dispersion, FragilityCurves, Fragility by DS, Parameter by DS,
        # Comparison by parameter, Comparison by typologies
        
        # Frame para ubicación de los tabWidget_1_4
        self.frame_1_4 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_1_4.setGeometry(QtCore.QRect(230, 280, 1171, 481))
        self.frame_1_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1_4.setObjectName("frame_1_4")
        
        # Definición de la cinta de tabWidget_1_4
        self.tabWidget_1_4 = QtWidgets.QTabWidget(self.frame_1_4)
        self.tabWidget_1_4.setGeometry(QtCore.QRect(0, 10, 1171, 471))
        self.tabWidget_1_4.setObjectName("tabWidget_1_4")
        
        #----
        # tabWidget_1_4 Dispersion:
            
        # Apertura del tabWidget_1_4 de Dispersion
        self.DispersionTax = QtWidgets.QWidget()
        self.DispersionTax.setObjectName("DispersionTax")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_dispe_tax_1 = QtWidgets.QFrame(self.DispersionTax)
        self.frame_dispe_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_dispe_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dispe_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dispe_tax_1.setObjectName("frame_dispe_tax_1")
        self.verticalLayoutWidget_35 = QtWidgets.QWidget(self.frame_dispe_tax_1)
        self.verticalLayoutWidget_35.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_35.setObjectName("verticalLayoutWidget_35")
        self.graph_dispe_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_35)
        self.graph_dispe_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_dispe_tax_1.setObjectName("graph_dispe_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_dispe_tax_2 = QtWidgets.QFrame(self.DispersionTax)
        self.frame_dispe_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_dispe_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_dispe_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_dispe_tax_2.setObjectName("frame_dispe_tax_2")
        self.verticalLayoutWidget_39 = QtWidgets.QWidget(self.frame_dispe_tax_2)
        self.verticalLayoutWidget_39.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_39.setObjectName("verticalLayoutWidget_39")
        self.graph_dispe_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_39)
        self.graph_dispe_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_dispe_tax_2.setObjectName("graph_dispe_tax_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.DispersionTax, "")
        
        #----
        # tabWidget_1_4 FragilityCurves:
            
        # Apertura del tabWidget_1_4 de FragilityCurves
        self.FragilityCurves_Tax = QtWidgets.QWidget()
        self.FragilityCurves_Tax.setObjectName("FragilityCurves_Tax")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_FC_tax_1 = QtWidgets.QFrame(self.FragilityCurves_Tax)
        self.frame_FC_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_FC_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_FC_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_FC_tax_1.setObjectName("frame_FC_tax_1")
        self.verticalLayoutWidget_41 = QtWidgets.QWidget(self.frame_FC_tax_1)
        self.verticalLayoutWidget_41.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_41.setObjectName("verticalLayoutWidget_41")
        self.graph_FC_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_41)
        self.graph_FC_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_FC_tax_1.setObjectName("graph_FC_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_FC_tax_2 = QtWidgets.QFrame(self.FragilityCurves_Tax)
        self.frame_FC_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_FC_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_FC_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_FC_tax_2.setObjectName("frame_FC_tax_2")
        self.verticalLayoutWidget_40 = QtWidgets.QWidget(self.frame_FC_tax_2)
        self.verticalLayoutWidget_40.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_40.setObjectName("verticalLayoutWidget_40")
        self.graph_FC_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_40)
        self.graph_FC_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_FC_tax_2.setObjectName("graph_FC_tax_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.FragilityCurves_Tax, "")
        
        #----
        # tabWidget_1_4 Fragility by DS:
            
        # Apertura del tabWidget_1_4 de Fragility by DS
        self.FragilityDS = QtWidgets.QWidget()
        self.FragilityDS.setObjectName("FragilityDS")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_FCS_tax_1 = QtWidgets.QFrame(self.FragilityDS)
        self.frame_FCS_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_FCS_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_FCS_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_FCS_tax_1.setObjectName("frame_FCS_tax_1")
        self.verticalLayoutWidget_43 = QtWidgets.QWidget(self.frame_FCS_tax_1)
        self.verticalLayoutWidget_43.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_43.setObjectName("verticalLayoutWidget_43")
        self.graph_FCS_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_43)
        self.graph_FCS_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_FCS_tax_1.setObjectName("graph_FCS_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_FCS_tax_2 = QtWidgets.QFrame(self.FragilityDS)
        self.frame_FCS_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_FCS_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_FCS_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_FCS_tax_2.setObjectName("frame_FCS_tax_2")
        self.verticalLayoutWidget_42 = QtWidgets.QWidget(self.frame_FCS_tax_2)
        self.verticalLayoutWidget_42.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_42.setObjectName("verticalLayoutWidget_42")
        self.graph_FCS_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_42)
        self.graph_FCS_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_FCS_tax_2.setObjectName("graph_FCS_tax_2")
        
        # Etiqueta de seleccion de DS para graficar de la taxonomia 1
        self.DS_graph_Label_1 = QtWidgets.QLabel(self.FragilityDS)
        self.DS_graph_Label_1.setGeometry(QtCore.QRect(360, 420, 101, 21))
        self.DS_graph_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DS_graph_Label_1.setObjectName("DS_graph_Label_1")
        
        # Etiqueta de seleccion de DS para graficar de la taxonomia 2
        self.DS_graph_Label_2 = QtWidgets.QLabel(self.FragilityDS)
        self.DS_graph_Label_2.setGeometry(QtCore.QRect(940, 420, 101, 21))
        self.DS_graph_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DS_graph_Label_2.setObjectName("DS_graph_Label_2")
        
        # Desplegable de seleccion de DS para graficar de la taxonomia 1
        self.DS_graph_Value_1 = QtWidgets.QComboBox(self.FragilityDS)
        self.DS_graph_Value_1.setGeometry(QtCore.QRect(470, 420, 100, 22))
        self.DS_graph_Value_1.setObjectName("DS_graph_Value_1")
        
        # Desplegable de seleccion de DS para graficar de la taxonomia 2
        self.DS_graph_Value_2 = QtWidgets.QComboBox(self.FragilityDS)
        self.DS_graph_Value_2.setGeometry(QtCore.QRect(1050, 420, 100, 22))
        self.DS_graph_Value_2.setObjectName("DS_graph_Value_2")
        
        # Boton para graficar DS de la taxonomia 1
        self.Graph_DS_1 = QtWidgets.QPushButton(self.FragilityDS)
        self.Graph_DS_1.setGeometry(QtCore.QRect(240, 420, 100, 22))
        self.Graph_DS_1.setObjectName("Graph_DS_1")
        
        # Boton para graficar DS de la taxonomia 2
        self.Graph_DS_2 = QtWidgets.QPushButton(self.FragilityDS)
        self.Graph_DS_2.setGeometry(QtCore.QRect(820, 420, 100, 22))
        self.Graph_DS_2.setObjectName("Graph_DS_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.FragilityDS, "")
        
        #----
        # tabWidget_1_4 Thetas or Betas by DS:
            
        # Apertura del tabWidget_1_4 de Parameter by DS
        self.ParametersDS = QtWidgets.QWidget()
        self.ParametersDS.setObjectName("ParametersDS")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_theta_tax_1 = QtWidgets.QFrame(self.ParametersDS)
        self.frame_theta_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_theta_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_theta_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_theta_tax_1.setObjectName("frame_theta_tax_1")
        self.verticalLayoutWidget_45 = QtWidgets.QWidget(self.frame_theta_tax_1)
        self.verticalLayoutWidget_45.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_45.setObjectName("verticalLayoutWidget_45")
        self.graph_theta_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_45)
        self.graph_theta_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_theta_tax_1.setObjectName("graph_theta_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_theta_tax_2 = QtWidgets.QFrame(self.ParametersDS)
        self.frame_theta_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_theta_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_theta_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_theta_tax_2.setObjectName("frame_theta_tax_2")
        self.verticalLayoutWidget_44 = QtWidgets.QWidget(self.frame_theta_tax_2)
        self.verticalLayoutWidget_44.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_44.setObjectName("verticalLayoutWidget_44")
        self.graph_theta_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_44)
        self.graph_theta_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_theta_tax_2.setObjectName("graph_theta_tax_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.ParametersDS, "")
        
        #----
        # tabWidget_1_4 Comparison by parameters or betas:
            
        # Apertura del tabWidget_1_4 Comparison by parameters
        self.comp_parameters = QtWidgets.QWidget()
        self.comp_parameters.setObjectName("comp_parameters")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_comp_theta_tax_1 = QtWidgets.QFrame(self.comp_parameters)
        self.frame_comp_theta_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_comp_theta_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_theta_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_theta_tax_1.setObjectName("frame_comp_theta_tax_1")
        self.verticalLayoutWidget_51 = QtWidgets.QWidget(self.frame_comp_theta_tax_1)
        self.verticalLayoutWidget_51.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_51.setObjectName("verticalLayoutWidget_51")
        self.graph_comp_theta_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_51)
        self.graph_comp_theta_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_theta_tax_1.setObjectName("graph_comp_theta_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_comp_theta_tax_2 = QtWidgets.QFrame(self.comp_parameters)
        self.frame_comp_theta_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_comp_theta_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_theta_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_theta_tax_2.setObjectName("frame_comp_theta_tax_2")
        self.verticalLayoutWidget_50 = QtWidgets.QWidget(self.frame_comp_theta_tax_2)
        self.verticalLayoutWidget_50.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_50.setObjectName("verticalLayoutWidget_50")
        self.graph_comp_theta_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_50)
        self.graph_comp_theta_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_theta_tax_2.setObjectName("graph_comp_theta_tax_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.comp_parameters, "")
            
        #----
        # tabWidget_1_4 Comparison by typologies:
        
        # Apertura del tabWidget_1_4 Comparison by typologies
        self.comp_typ = QtWidgets.QWidget()
        self.comp_typ.setObjectName("comp_typ")
        
        # Frame de la gráfica de la taxonomia 1
        self.frame_comp_typ_tax_1 = QtWidgets.QFrame(self.comp_typ)
        self.frame_comp_typ_tax_1.setGeometry(QtCore.QRect(0, -10, 571, 421))
        self.frame_comp_typ_tax_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_typ_tax_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_typ_tax_1.setObjectName("frame_comp_typ_tax_1")
        self.verticalLayoutWidget_49 = QtWidgets.QWidget(self.frame_comp_typ_tax_1)
        self.verticalLayoutWidget_49.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_49.setObjectName("verticalLayoutWidget_49")
        self.graph_comp_typ_tax_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_49)
        self.graph_comp_typ_tax_1.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_typ_tax_1.setObjectName("graph_comp_typ_tax_1")
        
        # Frame de la gráfica de la taxonomia 2
        self.frame_comp_typ_tax_2 = QtWidgets.QFrame(self.comp_typ)
        self.frame_comp_typ_tax_2.setGeometry(QtCore.QRect(580, -10, 571, 421))
        self.frame_comp_typ_tax_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_typ_tax_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_typ_tax_2.setObjectName("frame_comp_typ_tax_2")
        self.verticalLayoutWidget_48 = QtWidgets.QWidget(self.frame_comp_typ_tax_2)
        self.verticalLayoutWidget_48.setGeometry(QtCore.QRect(0, 10, 571, 411))
        self.verticalLayoutWidget_48.setObjectName("verticalLayoutWidget_48")
        self.graph_comp_typ_tax_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_48)
        self.graph_comp_typ_tax_2.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_typ_tax_2.setObjectName("graph_comp_typ_tax_2")
        
        # Etiqueta del tipo de comparación de la taxonomia 1
        self.Level_comparison_Label_1 = QtWidgets.QLabel(self.comp_typ)
        self.Level_comparison_Label_1.setGeometry(QtCore.QRect(0, 420, 141, 22))
        self.Level_comparison_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Level_comparison_Label_1.setObjectName("Level_comparison_Label_1")
        
        # Etiqueta del tipo de comparación de la taxonomia 2
        self.Level_comparison_Value_2 = QtWidgets.QComboBox(self.comp_typ)
        self.Level_comparison_Value_2.setGeometry(QtCore.QRect(730, 420, 161, 22))
        self.Level_comparison_Value_2.setObjectName("Level_comparison_Value_2")
        
        # Desplegable de selección del tipo de comparación de la taxonomia 1
        self.Level_comparison_Value_1 = QtWidgets.QComboBox(self.comp_typ)
        self.Level_comparison_Value_1.setGeometry(QtCore.QRect(150, 420, 161, 22))
        self.Level_comparison_Value_1.setObjectName("Level_comparison_Value_1")
        
        # Desplegable de selección del tipo de comparación de la taxonomia 2
        self.Level_comparison_Label_2 = QtWidgets.QLabel(self.comp_typ)
        self.Level_comparison_Label_2.setGeometry(QtCore.QRect(580, 420, 141, 22))
        self.Level_comparison_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Level_comparison_Label_2.setObjectName("Level_comparison_Label_2")
        
        # Etiqueta del DS a graficar de la taxonomia 1
        self.DS_graph_comp_Label_1 = QtWidgets.QLabel(self.comp_typ)
        self.DS_graph_comp_Label_1.setGeometry(QtCore.QRect(300, 420, 51, 21))
        self.DS_graph_comp_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DS_graph_comp_Label_1.setObjectName("DS_graph_comp_Label_1")
        
        # Etiqueta del DS a graficar de la taxonomia 2
        self.DS_graph_comp_Label_2 = QtWidgets.QLabel(self.comp_typ)
        self.DS_graph_comp_Label_2.setGeometry(QtCore.QRect(880, 420, 51, 21))
        self.DS_graph_comp_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.DS_graph_comp_Label_2.setObjectName("DS_graph_comp_Label_2")
        
        # Desplegable del DS a graficar de la taxonomia 1
        self.DS_graph_com_Value_1 = QtWidgets.QComboBox(self.comp_typ)
        self.DS_graph_com_Value_1.setGeometry(QtCore.QRect(360, 420, 100, 22))
        self.DS_graph_com_Value_1.setObjectName("DS_graph_com_Value_1")
        
        # Desplegable del DS a graficar de la taxonomia 2
        self.DS_graph_com_Value_2 = QtWidgets.QComboBox(self.comp_typ)
        self.DS_graph_com_Value_2.setGeometry(QtCore.QRect(940, 420, 100, 22))
        self.DS_graph_com_Value_2.setObjectName("DS_graph_com_Value_2")
        
        # Boton para graficar comparación de la taxonomia 1
        self.Graph_comp_1 = QtWidgets.QPushButton(self.comp_typ)
        self.Graph_comp_1.setGeometry(QtCore.QRect(460, 420, 100, 22))
        self.Graph_comp_1.setObjectName("Graph_comp_1")
        
        # Boton para graficar comparación de la taxonomia 2
        self.Graph_comp_2 = QtWidgets.QPushButton(self.comp_typ)
        self.Graph_comp_2.setGeometry(QtCore.QRect(1040, 420, 100, 22))
        self.Graph_comp_2.setObjectName("Graph_comp_2")
        
        # Cierre del Tab
        self.tabWidget_1_4.addTab(self.comp_typ, "")
        
        # ----------------
        
        # Scrolls
        self.verticalScrollBar_Taxonomy_1 = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_3)
        self.verticalScrollBar_Taxonomy_1.setGeometry(QtCore.QRect(1630, 0, 16, 781))
        self.verticalScrollBar_Taxonomy_1.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_Taxonomy_1.setObjectName("verticalScrollBar_Taxonomy_1")
        self.horizontalScrollBar_Taxonomy_1 = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_3)
        self.horizontalScrollBar_Taxonomy_1.setGeometry(QtCore.QRect(0, 790, 1631, 16))
        self.horizontalScrollBar_Taxonomy_1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_Taxonomy_1.setObjectName("horizontalScrollBar_Taxonomy_1")
        
        self.scrollArea_taxonomy_1.setWidget(self.scrollAreaWidgetContents_3)
        
        # Cierre del Tab de Fragility of Taxonomies
        self.tabWidget_General.addTab(self.FragilityTaxonomy, "")
        
        
        # ################################################################
        # TABWIDGET LOSS COMPONENT
        # ################################################################
        
        # Apertura del Tab de análisis de daño
        self.LossComponent = QtWidgets.QWidget()
        self.LossComponent.setObjectName("LossComponent")
        
        # Area Scroll del Tab de pérdida de componentes
        self.scrollArea_LossComponents = QtWidgets.QScrollArea(self.LossComponent)
        self.scrollArea_LossComponents.setGeometry(QtCore.QRect(0, 0, 1651, 811))
        self.scrollArea_LossComponents.setWidgetResizable(True)
        self.scrollArea_LossComponents.setObjectName("scrollArea_LossComponents")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1649, 809))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        
        # Título en el área principal del Tab de perdida por componentes
        self.label_damageLoss = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.label_damageLoss.setGeometry(QtCore.QRect(690, 10, 301, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_damageLoss.setFont(font)
        self.label_damageLoss.setAlignment(QtCore.Qt.AlignCenter)
        self.label_damageLoss.setObjectName("label_damageLoss")
        
        # Botón para cargar archivo guía de componentes
        self.load_compGuide = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.load_compGuide.setGeometry(QtCore.QRect(1090, 0, 131, 40))
        self.load_compGuide.setObjectName("load_compGuide")
        
        # Etiqueta de desplegable del tipo de costo utilizado
        self.CostType_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.CostType_label.setGeometry(QtCore.QRect(1300, 10, 121, 22))
        self.CostType_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CostType_label.setObjectName("CostType_label")
        
        # Desplegable del tipo de costo
        self.CostType_selection = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.CostType_selection.setGeometry(QtCore.QRect(1430, 10, 161, 22))
        self.CostType_selection.setObjectName("CostType_selection")
        self.CostType_selection.addItem("E'[L|Dsi]")         # Adiciona opción de desplegable
        self.CostType_selection.addItem("E[L|Dsi]")          # Adiciona opción de desplegable
        
        
        # ----------------------------------------------------------
        # TABWIDGET 2_1: COMPONENTS, COMPARISON OF COMPONENTS
        
        # Definición de la cinta de componentes individuales y de la edificación
        self.tabWidget_2_1 = QtWidgets.QTabWidget(self.scrollAreaWidgetContents)
        self.tabWidget_2_1.setGeometry(QtCore.QRect(10, 20, 1611, 761))
        self.tabWidget_2_1.setObjectName("tabWidget_2_1")
        
        #----
        # tabWidget_2_1 COMPONENTS:
        
        # Apertura del tabWidget de componentes
        self.Components = QtWidgets.QWidget()
        self.Components.setObjectName("Components")
        
        # Frame de la gráfica de POE del componente 1
        self.frame_POE_1 = QtWidgets.QFrame(self.Components)
        self.frame_POE_1.setGeometry(QtCore.QRect(20, 40, 501, 321))
        self.frame_POE_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_POE_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_POE_1.setObjectName("frame_POE_1")
        self.verticalLayoutWidget_21 = QtWidgets.QWidget(self.frame_POE_1)
        self.verticalLayoutWidget_21.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_21.setObjectName("verticalLayoutWidget_21")
        self.graph_POE_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_21)
        self.graph_POE_1.setContentsMargins(0, 0, 0, 0)
        self.graph_POE_1.setObjectName("graph_POE_1")
        
        # Frame de la gráfica de POE del componente 2
        self.frame_POE_2 = QtWidgets.QFrame(self.Components)
        self.frame_POE_2.setGeometry(QtCore.QRect(20, 410, 501, 321))
        self.frame_POE_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_POE_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_POE_2.setObjectName("frame_POE_2")
        self.verticalLayoutWidget_26 = QtWidgets.QWidget(self.frame_POE_2)
        self.verticalLayoutWidget_26.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_26.setObjectName("verticalLayoutWidget_26")
        self.graph_POE_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_26)
        self.graph_POE_2.setContentsMargins(0, 0, 0, 0)
        self.graph_POE_2.setObjectName("graph_POE_2")
        
        # Frame de la gráfica de la probabilidad de los estados de daño del componente 1
        self.frame_Prob_1 = QtWidgets.QFrame(self.Components)
        self.frame_Prob_1.setGeometry(QtCore.QRect(550, 40, 501, 321))
        self.frame_Prob_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Prob_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Prob_1.setObjectName("frame_Prob_1")
        self.verticalLayoutWidget_22 = QtWidgets.QWidget(self.frame_Prob_1)
        self.verticalLayoutWidget_22.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_22.setObjectName("verticalLayoutWidget_22")
        self.graph_Prob_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_22)
        self.graph_Prob_1.setContentsMargins(0, 0, 0, 0)
        self.graph_Prob_1.setObjectName("graph_Prob_1")
        
        # Frame de la gráfica de la probabilidad de los estados de daño del componente 2
        self.frame_Prob_2 = QtWidgets.QFrame(self.Components)
        self.frame_Prob_2.setGeometry(QtCore.QRect(550, 410, 501, 321))
        self.frame_Prob_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Prob_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Prob_2.setObjectName("frame_Prob_2")
        self.verticalLayoutWidget_27 = QtWidgets.QWidget(self.frame_Prob_2)
        self.verticalLayoutWidget_27.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_27.setObjectName("verticalLayoutWidget_27")
        self.graph_Prob_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_27)
        self.graph_Prob_3.setContentsMargins(0, 0, 0, 0)
        self.graph_Prob_3.setObjectName("graph_Prob_3")
        
        # Frame de la gráfica de valor esperado del componente 1
        self.frame_LossComp_1 = QtWidgets.QFrame(self.Components)
        self.frame_LossComp_1.setGeometry(QtCore.QRect(1080, 40, 501, 321))
        self.frame_LossComp_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_LossComp_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_LossComp_1.setObjectName("frame_LossComp_1")
        self.verticalLayoutWidget_24 = QtWidgets.QWidget(self.frame_LossComp_1)
        self.verticalLayoutWidget_24.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_24.setObjectName("verticalLayoutWidget_24")
        self.graph_LossComp_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_24)
        self.graph_LossComp_1.setContentsMargins(0, 0, 0, 0)
        self.graph_LossComp_1.setObjectName("graph_LossComp_1")
        
        # Frame de la gráfica de valor esperado del componente 2
        self.frame_LossComp_2 = QtWidgets.QFrame(self.Components)
        self.frame_LossComp_2.setGeometry(QtCore.QRect(1080, 410, 501, 321))
        self.frame_LossComp_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_LossComp_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_LossComp_2.setObjectName("frame_LossComp_2")
        self.verticalLayoutWidget_25 = QtWidgets.QWidget(self.frame_LossComp_2)
        self.verticalLayoutWidget_25.setGeometry(QtCore.QRect(0, 0, 501, 321))
        self.verticalLayoutWidget_25.setObjectName("verticalLayoutWidget_25")
        self.graph_LossComp_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_25)
        self.graph_LossComp_2.setContentsMargins(0, 0, 0, 0)
        self.graph_LossComp_2.setObjectName("graph_LossComp_2")
        
        # Etiqueta del componente 1
        self.fragilityGroup_Label_1 = QtWidgets.QLabel(self.Components)
        self.fragilityGroup_Label_1.setGeometry(QtCore.QRect(20, 10, 101, 20))
        self.fragilityGroup_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fragilityGroup_Label_1.setFont(font)
        self.fragilityGroup_Label_1.setObjectName("fragilityGroup_Label_1")
        
        # Etiqueta del componente 2
        self.fragilityGroup_Label_2 = QtWidgets.QLabel(self.Components)
        self.fragilityGroup_Label_2.setGeometry(QtCore.QRect(20, 380, 101, 20))
        self.fragilityGroup_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.fragilityGroup_Label_2.setFont(font)
        self.fragilityGroup_Label_2.setObjectName("fragilityGroup_Label_2")
        
        # Desplegable para selección del componente 1
        self.fragilityGroup_Value_1 = QtWidgets.QComboBox(self.Components)
        self.fragilityGroup_Value_1.setGeometry(QtCore.QRect(130, 10, 91, 22))
        self.fragilityGroup_Value_1.setObjectName("fragilityGroup_Value_1")
        
        # Desplegable para selección del componente 2
        self.fragilityGroup_Value_2 = QtWidgets.QComboBox(self.Components)
        self.fragilityGroup_Value_2.setGeometry(QtCore.QRect(130, 380, 91, 22))
        self.fragilityGroup_Value_2.setObjectName("fragilityGroup_Value_2")
        
        # Etiqueta del nombre del componente 1
        self.componentName_1 = QtWidgets.QLabel(self.Components)
        self.componentName_1.setGeometry(QtCore.QRect(240, 10, 301, 22))
        self.componentName_1.setObjectName("componentName_1")
        
        # Etiqueta del nombre del componente 2
        self.componentName_2 = QtWidgets.QLabel(self.Components)
        self.componentName_2.setGeometry(QtCore.QRect(240, 380, 301, 22))
        self.componentName_2.setObjectName("componentName_2")
        
        # Botón para calcular componente 1
        self.CalcComp_1 = QtWidgets.QPushButton(self.Components)
        self.CalcComp_1.setGeometry(QtCore.QRect(560, 10, 93, 22))
        self.CalcComp_1.setObjectName("CalcComp_1")
        
        # Botón para calcular componente 2
        self.CalcComp_2 = QtWidgets.QPushButton(self.Components)
        self.CalcComp_2.setGeometry(QtCore.QRect(560, 380, 93, 22))
        self.CalcComp_2.setObjectName("CalcComp_2")
        
        # Etiqueta para seleccion de EDP en el grafico de barras del componente 1
        self.EDPVal_label_comp_1 = QtWidgets.QLabel(self.Components)
        self.EDPVal_label_comp_1.setGeometry(QtCore.QRect(840, 10, 121, 22))
        self.EDPVal_label_comp_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPVal_label_comp_1.setObjectName("EDPVal_label_comp_1")
        
        # Etiqueta para seleccion de EDP en el grafico de barras del componente 2
        self.EDPVal_label_comp_2 = QtWidgets.QLabel(self.Components)
        self.EDPVal_label_comp_2.setGeometry(QtCore.QRect(840, 380, 121, 22))
        self.EDPVal_label_comp_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EDPVal_label_comp_2.setObjectName("EDPVal_label_comp_2")
        
        # Valor del EDP en el grafico de barras del componente 1
        self.EDPVal_value_comp_1 = QtWidgets.QLineEdit(self.Components)
        self.EDPVal_value_comp_1.setGeometry(QtCore.QRect(970, 5, 81, 31))
        self.EDPVal_value_comp_1.setObjectName("EDPVal_value_comp_1")
        self.EDPVal_value_comp_1.setText("0.03")       # Valor por defecto
        
        # Valor del EDP en el grafico de barras del componente 2
        self.EDPVal_value_comp_2 = QtWidgets.QLineEdit(self.Components)
        self.EDPVal_value_comp_2.setGeometry(QtCore.QRect(970, 375, 81, 31))
        self.EDPVal_value_comp_2.setObjectName("EDPVal_value_comp_2")
        self.EDPVal_value_comp_2.setText("0.03")       # Valor por defecto
        
        # Cierre del Tab
        self.tabWidget_2_1.addTab(self.Components, "")
        
        # ----------------------------------------------------------
        # TABWIDGET 2_1: COMPARISON COMPONENTS
        self.ComparisonComponents = QtWidgets.QWidget()
        self.ComparisonComponents.setObjectName("ComparisonComponents")
        self.tabWidget_2_1.addTab(self.ComparisonComponents, "")
        
        # Scrolls
        self.horizontalScrollBar_lossComponents = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.horizontalScrollBar_lossComponents.setGeometry(QtCore.QRect(0, 790, 1631, 16))
        self.horizontalScrollBar_lossComponents.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_lossComponents.setObjectName("horizontalScrollBar_lossComponents")
        self.verticalScrollBar__lossComponents = QtWidgets.QScrollBar(self.scrollAreaWidgetContents)
        self.verticalScrollBar__lossComponents.setGeometry(QtCore.QRect(1630, 0, 20, 791))
        self.verticalScrollBar__lossComponents.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar__lossComponents.setObjectName("verticalScrollBar__lossComponents")
        
        self.scrollArea_LossComponents.setWidget(self.scrollAreaWidgetContents)
        
        # Cierre del Tab de Loss Components
        self.tabWidget_General.addTab(self.LossComponent, "")
        
        
        # ################################################################
        # TABWIDGET LOSS OF BUILDINGS
        # ################################################################
        
        # Apertura del Tab de análisis de pérdidas
        self.LossStory = QtWidgets.QWidget()
        self.LossStory.setObjectName("LossStory")
        
        # Area Scroll del Tab de pérdida por piso
        self.scrollArea_LossStory = QtWidgets.QScrollArea(self.LossStory)
        self.scrollArea_LossStory.setGeometry(QtCore.QRect(0, 0, 1658, 843))
        self.scrollArea_LossStory.setWidgetResizable(True)
        self.scrollArea_LossStory.setObjectName("scrollArea_LossStory")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 1656, 841))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        
        # Subtítulo para introducir datos de la edificación 1
        self.BuildingTittle_Loss_1 = QtWidgets.QLabel(self.LossStory)
        self.BuildingTittle_Loss_1.setGeometry(QtCore.QRect(50, 10, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BuildingTittle_Loss_1.setFont(font)
        self.BuildingTittle_Loss_1.setObjectName("BuildingTittle_Loss_1")
        
        # Subtítulo para introducir datos de la edificación 2
        self.BuildingTittle_Loss_2 = QtWidgets.QLabel(self.LossStory)
        self.BuildingTittle_Loss_2.setGeometry(QtCore.QRect(1360, 10, 131, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BuildingTittle_Loss_2.setFont(font)
        self.BuildingTittle_Loss_2.setObjectName("BuildingTittle_Loss_2")
        
        # ----------------------------------------------------------
        ## LOAD FOLDERS
        
        # Subtítulo de sección para cargar archivos de la edificación 1
        self.LoadFiles_loss_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.LoadFiles_loss_1.setGeometry(QtCore.QRect(50, 40, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.LoadFiles_loss_1.setFont(font)
        self.LoadFiles_loss_1.setObjectName("LoadFiles_loss_1")
        
        # Subtítulo de sección para cargar archivos de la edificación 2
        self.LoadFiles_loss_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.LoadFiles_loss_2.setGeometry(QtCore.QRect(1370, 40, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.LoadFiles_loss_2.setFont(font)
        self.LoadFiles_loss_2.setObjectName("LoadFiles_loss_2")
        
        # Botón para seleccionar carpeta de edificación 1
        self.BuildingButton_Loss_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.BuildingButton_Loss_1.setGeometry(QtCore.QRect(20, 70, 131, 28))
        self.BuildingButton_Loss_1.setObjectName("BuildingButton_Loss_1")
        
        # Botón para seleccionar carpeta de edificación 2
        self.BuildingButton_Loss_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.BuildingButton_Loss_2.setGeometry(QtCore.QRect(1340, 70, 131, 28))
        self.BuildingButton_Loss_2.setObjectName("BuildingButton_Loss_2")
        
        # Texto que muestra el nombre la edificación seleccionada de la edificación 1
        self.Building_text_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Building_text_1.setGeometry(QtCore.QRect(160, 70, 121, 28))
        self.Building_text_1.setText("")
        self.Building_text_1.setObjectName("Building_text_1")
        self.Building_text_1.setText("CSS_277")      # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Texto que muestra el nombre la edificación seleccionada de la edificación 2
        self.Building_text_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Building_text_2.setGeometry(QtCore.QRect(1480, 70, 141, 28))
        self.Building_text_2.setText("")
        self.Building_text_2.setObjectName("Building_text_2")
        self.Building_text_2.setText("CSS_211")      # Texto por defecto !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        
        # ----------------------------------------------------------
        ## GRAPH OPTIONS: DV-EDP
        
        # Subtítulo de sección para cargar opciones del grafico de la edificación 1
        self.DV_EDP_options_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.DV_EDP_options_1.setGeometry(QtCore.QRect(50, 110, 161, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.DV_EDP_options_1.setFont(font)
        self.DV_EDP_options_1.setObjectName("DV_EDP_options_1")
        
        # Subtítulo de sección para cargar opciones del grafico de la edificación 2
        self.DV_EDP_options_2 = QtWidgets.QLabel(self.LossStory)
        self.DV_EDP_options_2.setGeometry(QtCore.QRect(1370, 110, 161, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.DV_EDP_options_2.setFont(font)
        self.DV_EDP_options_2.setObjectName("DV_EDP_options_2")
        
        # Etiqueta de selección de piso de la edificación 1
        self.Story_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Story_Label_1.setGeometry(QtCore.QRect(0, 150, 91, 20))
        self.Story_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Story_Label_1.setObjectName("Story_Label_1")
        
        # Etiqueta de selección de piso de la edificación 2
        self.Story_Label_2 = QtWidgets.QLabel(self.LossStory)
        self.Story_Label_2.setGeometry(QtCore.QRect(1320, 150, 91, 20))
        self.Story_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Story_Label_2.setObjectName("Story_Label_2")
        
        # Desplegable de selección de piso de la edificación 1
        self.Story_Value_1 = QtWidgets.QComboBox(self.scrollAreaWidgetContents_4)
        self.Story_Value_1.setGeometry(QtCore.QRect(100, 150, 161, 22))
        self.Story_Value_1.setObjectName("Story_Value_1")
        
        # Desplegable de selección de piso de la edificación 2
        self.Story_Value_2 = QtWidgets.QComboBox(self.LossStory)
        self.Story_Value_2.setGeometry(QtCore.QRect(1420, 150, 161, 22))
        self.Story_Value_2.setObjectName("Story_Value_2")
        
        # Etiqueta del input data a seleccionar de la edificación 1
        self.InputData_Label_1 = QtWidgets.QLabel(self.LossStory)
        self.InputData_Label_1.setGeometry(QtCore.QRect(0, 175, 91, 20))
        self.InputData_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.InputData_Label_1.setObjectName("InputData_Label_1")
        
        # Etiqueta del input data a seleccionar de la edificación 2
        self.InputData_Label_2 = QtWidgets.QLabel(self.LossStory)
        self.InputData_Label_2.setGeometry(QtCore.QRect(1320, 175, 91, 20))
        self.InputData_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.InputData_Label_2.setObjectName("InputData_Label_2")
        
        # Desplegable del input data a seleccionar de la edificación 1
        self.InputData_Value_1 = QtWidgets.QComboBox(self.LossStory)
        self.InputData_Value_1.setGeometry(QtCore.QRect(100, 175, 161, 22))
        self.InputData_Value_1.setObjectName("InputData_Value_1")
        
        # Desplegable del input data a seleccionar de la edificación 2
        self.InputData_Value_2 = QtWidgets.QComboBox(self.LossStory)
        self.InputData_Value_2.setGeometry(QtCore.QRect(1420, 175, 161, 22))
        self.InputData_Value_2.setObjectName("InputData_Value_2")
        
        # Etiqueta del elemento a seleccionar de la edificación 1
        self.Element_Label_1 = QtWidgets.QLabel(self.LossStory)
        self.Element_Label_1.setGeometry(QtCore.QRect(0, 225, 91, 20))
        self.Element_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Element_Label_1.setObjectName("Element_Label_1")
        
        # Etiqueta del elemento a seleccionar de la edificación 2
        self.Element_Label_2 = QtWidgets.QLabel(self.LossStory)
        self.Element_Label_2.setGeometry(QtCore.QRect(1320, 225, 91, 20))
        self.Element_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Element_Label_2.setObjectName("Element_Label_2")
        self.tabWidget_General.addTab(self.LossStory, "")
        
        # Desplegable del elemento a seleccionar de la edificación 1
        self.Element_Value_1 = QtWidgets.QComboBox(self.LossStory)
        self.Element_Value_1.setGeometry(QtCore.QRect(100, 225, 161, 22))
        self.Element_Value_1.setObjectName("Element_Value_1")
        
        # Desplegable del elemento a seleccionar de la edificación 2
        self.Element_Value_2 = QtWidgets.QComboBox(self.LossStory)
        self.Element_Value_2.setGeometry(QtCore.QRect(1420, 225, 161, 22))
        self.Element_Value_2.setObjectName("Element_Value_2")
        
        # Etiqueta de indicación de actualizar elementos de la edificación 1
        self.LoadElements_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.LoadElements_Label_1.setGeometry(QtCore.QRect(20, 200, 181, 20))
        self.LoadElements_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LoadElements_Label_1.setObjectName("LoadElements_Label_1")
        
        # Etiqueta de indicación de actualizar elementos de la edificación 2
        self.LoadElements_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.LoadElements_Label_2.setGeometry(QtCore.QRect(1340, 200, 181, 20))
        self.LoadElements_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LoadElements_Label_2.setObjectName("LoadElements_Label_2")
        
        # Botón para cargar archivos del desplegableme de elements de la edificación 1
        self.Element_activate_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Element_activate_1.setGeometry(QtCore.QRect(210, 200, 51, 22))
        self.Element_activate_1.setObjectName("Element_activate_1")
        
        # Botón para cargar archivos del desplegableme de elements de la edificación 2
        self.Element_activate_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Element_activate_2.setGeometry(QtCore.QRect(1530, 200, 51, 22))
        self.Element_activate_2.setObjectName("Element_activate_2")
        
        # Botón para graficar curvas de edificación 1
        self.Graph_button_DVEDP_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Graph_button_DVEDP_1.setGeometry(QtCore.QRect(100, 260, 161, 31))
        self.Graph_button_DVEDP_1.setObjectName("Graph_button_DVEDP_1")
        
        # Botón para graficar curvas de edificación 2
        self.Graph_button_DVEDP_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Graph_button_DVEDP_2.setGeometry(QtCore.QRect(1420, 260, 161, 31))
        self.Graph_button_DVEDP_2.setObjectName("Graph_button_DVEDP_2")
        
        # ----------------------------------------------------------
        ## GRAPH OPTIONS: DV-IM
        
        # Subtítulo de sección para cargar opciones del grafico de la edificación 1
        self.DV_IM_options_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.DV_IM_options_1.setGeometry(QtCore.QRect(50, 330, 161, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.DV_IM_options_1.setFont(font)
        self.DV_IM_options_1.setObjectName("DV_IM_options_1")
        
        # Subtítulo de sección para cargar opciones del grafico de la edificación 2
        self.DV_IM_options_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.DV_IM_options_2.setGeometry(QtCore.QRect(1370, 330, 161, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.DV_IM_options_2.setFont(font)
        self.DV_IM_options_2.setObjectName("DV_IM_options_2")
        
        # Etiqueta para definicion de SDR cens de la edificación 1
        self.SDRLoss_cens_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.SDRLoss_cens_Label_1.setGeometry(QtCore.QRect(30, 370, 111, 21))
        self.SDRLoss_cens_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SDRLoss_cens_Label_1.setObjectName("SDRLoss_cens_Label_1")
        
        # Etiqueta para definicion de SDR cens de la edificación 2
        self.SDRLoss_cens_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.SDRLoss_cens_Label_2.setGeometry(QtCore.QRect(1350, 370, 111, 21))
        self.SDRLoss_cens_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.SDRLoss_cens_Label_2.setObjectName("SDRLoss_cens_Label_2")
        
        # Linea para definicion de SDR cens de la edificación 1
        self.SDRLoss_cens_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.SDRLoss_cens_value_1.setGeometry(QtCore.QRect(150, 370, 110, 21))
        self.SDRLoss_cens_value_1.setObjectName("SDRLoss_cens_value_1")
        self.SDRLoss_cens_value_1.setText("0.1")     # Valor por defecto
        
        # Linea para definicion de SDR cens de la edificación 2
        self.SDRLoss_cens_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.SDRLoss_cens_value_2.setGeometry(QtCore.QRect(1470, 370, 110, 21))
        self.SDRLoss_cens_value_2.setObjectName("SDRLoss_cens_value_2")
        self.SDRLoss_cens_value_2.setText("0.1")     # Valor por defecto
        
        # Etiqueta para definicion de Theta de Colapso de la edificación 1
        self.Theta_collapse_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Theta_collapse_Label_1.setGeometry(QtCore.QRect(10, 410, 131, 21))
        self.Theta_collapse_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Theta_collapse_Label_1.setObjectName("Theta_collapse_Label_1")
        
        # Etiqueta para definicion de Theta de Colapso de la edificación 2
        self.Theta_collapse_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Theta_collapse_Label_2.setGeometry(QtCore.QRect(1330, 410, 131, 21))
        self.Theta_collapse_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Theta_collapse_Label_2.setObjectName("Theta_collapse_Label_2")
        
        # Linea para definicion de Theta de Colapso de la edificación 1
        self.Theta_collapse_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Theta_collapse_value_1.setGeometry(QtCore.QRect(150, 410, 110, 21))
        self.Theta_collapse_value_1.setObjectName("Theta_collapse_value_1")
        self.Theta_collapse_value_1.setText("1")     # Valor por defecto
        
        # Linea para definicion de Theta de Colapso cens de la edificación 2
        self.Theta_collapse_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Theta_collapse_value_2.setGeometry(QtCore.QRect(1470, 410, 110, 21))
        self.Theta_collapse_value_2.setObjectName("Theta_collapse_value_2")
        self.Theta_collapse_value_2.setText("1")     # Valor por defecto
        
        # Etiqueta para definicion de Sigma de Colapso de la edificación 1
        self.Sigma_collapse_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Sigma_collapse_Label_1.setGeometry(QtCore.QRect(10, 435, 131, 21))
        self.Sigma_collapse_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Sigma_collapse_Label_1.setObjectName("Sigma_collapse_Label_1")
        
        # Etiqueta para definicion de Sigma de Colapso de la edificación 2
        self.Sigma_collapse_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Sigma_collapse_Label_2.setGeometry(QtCore.QRect(1330, 435, 131, 21))
        self.Sigma_collapse_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Sigma_collapse_Label_2.setObjectName("Sigma_collapse_Label_2")
        
        # Linea para definicion de Sigma de Colapso de la edificación 1
        self.Sigma_collapse_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Sigma_collapse_value_1.setGeometry(QtCore.QRect(150, 435, 110, 21))
        self.Sigma_collapse_value_1.setObjectName("Sigma_collapse_value_1")
        self.Sigma_collapse_value_1.setText("0.4")     # Valor por defecto
        
        # Linea para definicion de Sigma de Colapso cens de la edificación 2
        self.Sigma_collapse_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Sigma_collapse_value_2.setGeometry(QtCore.QRect(1470, 435, 110, 21))
        self.Sigma_collapse_value_2.setObjectName("Sigma_collapse_value_2")
        self.Sigma_collapse_value_2.setText("0.4")     # Valor por defecto
        
        # Etiqueta para definicion de Theta de RSDR de la edificación 1
        self.Theta_rsdr_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Theta_rsdr_Label_1.setGeometry(QtCore.QRect(10, 480, 131, 21))
        self.Theta_rsdr_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Theta_rsdr_Label_1.setObjectName("Theta_rsdr_Label_1")
        
        # Etiqueta para definicion de Theta de RSDR de la edificación 2
        self.Theta_rsdr_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Theta_rsdr_Label_2.setGeometry(QtCore.QRect(1330, 480, 131, 21))
        self.Theta_rsdr_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Theta_rsdr_Label_2.setObjectName("Theta_rsdr_Label_2")
        
        # Linea para definicion de Theta de RSDR de la edificación 1
        self.Theta_rsdr_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Theta_rsdr_value_1.setGeometry(QtCore.QRect(150, 480, 110, 21))
        self.Theta_rsdr_value_1.setObjectName("Theta_rsdr_value_1")
        self.Theta_rsdr_value_1.setText("0.015")     # Valor por defecto
        
        # Linea para definicion de Theta de RSDR cens de la edificación 2
        self.Theta_rsdr_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Theta_rsdr_value_2.setGeometry(QtCore.QRect(1470, 480, 110, 21))
        self.Theta_rsdr_value_2.setObjectName("Theta_rsdr_value_2")
        self.Theta_rsdr_value_2.setText("0.015")     # Valor por defecto
        
        # Etiqueta para definicion de Sigma de RSDR de la edificación 1
        self.Sigma_rsdr_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Sigma_rsdr_Label_1.setGeometry(QtCore.QRect(10, 505, 131, 21))
        self.Sigma_rsdr_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Sigma_rsdr_Label_1.setObjectName("Sigma_rsdr_Label_1")
        
        # Etiqueta para definicion de Sigma de RSDR de la edificación 2
        self.Sigma_rsdr_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.Sigma_rsdr_Label_2.setGeometry(QtCore.QRect(1330, 505, 131, 21))
        self.Sigma_rsdr_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Sigma_rsdr_Label_2.setObjectName("Sigma_rsdr_Label_2")
        
        # Linea para definicion de Sigma de RSDR de la edificación 1
        self.Sigma_rsdr_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Sigma_rsdr_value_1.setGeometry(QtCore.QRect(150, 505, 110, 21))
        self.Sigma_rsdr_value_1.setObjectName("Sigma_rsdr_value_1")
        self.Sigma_rsdr_value_1.setText("0.3")     # Valor por defecto
        
        # Linea para definicion de Sigma de RSDR cens de la edificación 2
        self.Sigma_rsdr_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.Sigma_rsdr_value_2.setGeometry(QtCore.QRect(1470, 505, 110, 21))
        self.Sigma_rsdr_value_2.setObjectName("Sigma_rsdr_value_2")
        self.Sigma_rsdr_value_2.setText("0.3")     # Valor por defecto
        
        # Etiqueta para definicion de E[L|NC + D] de la edificación 1
        self.ED_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.ED_Label_1.setGeometry(QtCore.QRect(10, 550, 131, 21))
        self.ED_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ED_Label_1.setObjectName("ED_Label_1")
        
        # Etiqueta para definicion de E[L|NC + D] de la edificación 2
        self.ED_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.ED_Label_2.setGeometry(QtCore.QRect(1330, 550, 131, 21))
        self.ED_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ED_Label_2.setObjectName("ED_Label_2")
        
        # Linea para definicion de E[L|NC + D] de la edificación 1
        self.ED_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.ED_value_1.setGeometry(QtCore.QRect(150, 550, 110, 21))
        self.ED_value_1.setObjectName("ED_value_1")
        self.ED_value_1.setText("1.0")     # Valor por defecto
        
        # Linea para definicion de E[L|NC + D] cens de la edificación 2
        self.ED_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.ED_value_2.setGeometry(QtCore.QRect(1470, 550, 110, 21))
        self.ED_value_2.setObjectName("ED_value_2")
        self.ED_value_2.setText("1.0")     # Valor por defecto
        
        # Etiqueta para definicion de E[L|C] de la edificación 1
        self.EC_Label_1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.EC_Label_1.setGeometry(QtCore.QRect(10, 575, 131, 21))
        self.EC_Label_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EC_Label_1.setObjectName("EC_Label_1")
        
        # Etiqueta para definicion de E[L|C] de la edificación 2
        self.EC_Label_2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.EC_Label_2.setGeometry(QtCore.QRect(1330, 575, 131, 21))
        self.EC_Label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.EC_Label_2.setObjectName("EC_Label_2")
        
        # Linea para definicion de E[L|C] de la edificación 1
        self.EC_value_1 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.EC_value_1.setGeometry(QtCore.QRect(150, 575, 110, 21))
        self.EC_value_1.setObjectName("EC_value_1")
        self.EC_value_1.setText("1.0")     # Valor por defecto
        
        # Linea para definicion de E[L|C] cens de la edificación 2
        self.EC_value_2 = QtWidgets.QLineEdit(self.scrollAreaWidgetContents_4)
        self.EC_value_2.setGeometry(QtCore.QRect(1470, 575, 110, 21))
        self.EC_value_2.setObjectName("EC_value_2")
        self.EC_value_2.setText("1.0")     # Valor por defecto
        
        # Botón para graficar curvas de edificación 1
        self.Graph_button_DVIM_1 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Graph_button_DVIM_1.setGeometry(QtCore.QRect(100, 620, 161, 31))
        self.Graph_button_DVIM_1.setObjectName("Graph_button_DVIM_1")
        
        # Botón para graficar curvas de edificación 2
        self.Graph_button_DVIM_2 = QtWidgets.QPushButton(self.scrollAreaWidgetContents_4)
        self.Graph_button_DVIM_2.setGeometry(QtCore.QRect(1420, 620, 161, 31))
        self.Graph_button_DVIM_2.setObjectName("Graph_button_DVIM_2")
        
        # ----------------------------------------------------------
        # GRAFICAS DE CURVAS
        
        # Título de gráfica de la edificación 1
        self.label_curve_B1 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_curve_B1.setGeometry(QtCore.QRect(280, 0, 501, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_curve_B1.setFont(font)
        self.label_curve_B1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_curve_B1.setObjectName("label_curve_B1")
        
        # Título de gráfica de la edificación 2
        self.label_curve_B2 = QtWidgets.QLabel(self.scrollAreaWidgetContents_4)
        self.label_curve_B2.setGeometry(QtCore.QRect(800, 0, 501, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_curve_B2.setFont(font)
        self.label_curve_B2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_curve_B2.setObjectName("label_curve_B2")
        
        # ----------------------------------------------------------
        # TABWIDGET_3_1: DV-EDP, Expected Loss by story (NC+R), Expected Loss of building (NC+R), 
        # Expected Loss of building, Expected Loss of building by events, Probability of events
        
        # Definición de la cinta de gráficas de curvas de pérdidas
        self.tabWidget_3_1 = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_4)
        self.tabWidget_3_1.setGeometry(QtCore.QRect(280, 20, 1041, 361))
        self.tabWidget_3_1.setObjectName("tabWidget_3_1")
        
        #----
        # tabWidget_3_1 DV-EDP:
            
        # Apertura del tabWidget_3_1 de DV-EDP
        self.DV_EDP = QtWidgets.QWidget()
        self.DV_EDP.setObjectName("DV_EDP")
        
        # Frame de la gráfica de la edificación 1
        self.frame_DV_EDP_1 = QtWidgets.QFrame(self.DV_EDP)
        self.frame_DV_EDP_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_DV_EDP_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DV_EDP_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DV_EDP_1.setObjectName("frame_DV_EDP_1")
        self.verticalLayoutWidget_10 = QtWidgets.QWidget(self.frame_DV_EDP_1)
        self.verticalLayoutWidget_10.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_10.setObjectName("verticalLayoutWidget_10")
        self.graph_DV_EDP_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_10)
        self.graph_DV_EDP_1.setContentsMargins(0, 0, 0, 0)
        self.graph_DV_EDP_1.setObjectName("graph_DV_EDP_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_DV_EDP_2 = QtWidgets.QFrame(self.DV_EDP)
        self.frame_DV_EDP_2.setGeometry(QtCore.QRect(510, -10, 511, 361))
        self.frame_DV_EDP_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DV_EDP_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DV_EDP_2.setObjectName("frame_DV_EDP_2")
        self.verticalLayoutWidget_9 = QtWidgets.QWidget(self.frame_DV_EDP_2)
        self.verticalLayoutWidget_9.setGeometry(QtCore.QRect(10, 10, 501, 331))
        self.verticalLayoutWidget_9.setObjectName("verticalLayoutWidget_9")
        self.graph_DV_EDP_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_9)
        self.graph_DV_EDP_2.setContentsMargins(0, 0, 0, 0)
        self.graph_DV_EDP_2.setObjectName("graph_DV_EDP_2")
            
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.DV_EDP, "")
            
        #----
        # tabWidget_3_1 Expected Loss by story (NC+R):
            
        # Apertura del tabWidget_3_1 de Expected Loss by story (NC+R)
        self.E_L_Story = QtWidgets.QWidget()
        self.E_L_Story.setObjectName("E_L_Story")
        
        # Frame de la gráfica de la edificación 1
        self.frame_DV_IM_1 = QtWidgets.QFrame(self.E_L_Story)
        self.frame_DV_IM_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_DV_IM_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DV_IM_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DV_IM_1.setObjectName("frame_DV_IM_1")
        self.verticalLayoutWidget_16 = QtWidgets.QWidget(self.frame_DV_IM_1)
        self.verticalLayoutWidget_16.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_16.setObjectName("verticalLayoutWidget_16")
        self.graph_DV_IM_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_16)
        self.graph_DV_IM_1.setContentsMargins(0, 0, 0, 0)
        self.graph_DV_IM_1.setObjectName("graph_DV_IM_2")
        
        # Frame de la gráfica de la edificación 2
        self.frame_DV_IM_2 = QtWidgets.QFrame(self.E_L_Story)
        self.frame_DV_IM_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_DV_IM_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_DV_IM_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_DV_IM_2.setObjectName("frame_DV_IM_2")
        self.verticalLayoutWidget_15 = QtWidgets.QWidget(self.frame_DV_IM_2)
        self.verticalLayoutWidget_15.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_15.setObjectName("verticalLayoutWidget_15")
        self.graph_DV_IM_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_15)
        self.graph_DV_IM_2.setContentsMargins(0, 0, 0, 0)
        self.graph_DV_IM_2.setObjectName("graph_DV_IM_2")
        
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.E_L_Story, "")
        
        #----
        # tabWidget_3_1 Expected Loss of building (NC+R):
            
        # Apertura del tabWidget_3_1 de Expected Loss of building (NC+R)
        self.E_L_building_NC_R = QtWidgets.QWidget()
        self.E_L_building_NC_R.setObjectName("E_L_building_NC_R")
        
        # Frame de la gráfica de la edificación 1
        self.frame_Exp_NC_R_B_1 = QtWidgets.QFrame(self.E_L_building_NC_R)
        self.frame_Exp_NC_R_B_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_Exp_NC_R_B_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Exp_NC_R_B_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Exp_NC_R_B_1.setObjectName("frame_Exp_NC_R_B_1")
        self.verticalLayoutWidget_46 = QtWidgets.QWidget(self.frame_Exp_NC_R_B_1)
        self.verticalLayoutWidget_46.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_46.setObjectName("verticalLayoutWidget_46")
        self.graph_Exp_NC_R_B_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_46)
        self.graph_Exp_NC_R_B_1.setContentsMargins(0, 0, 0, 0)
        self.graph_Exp_NC_R_B_1.setObjectName("graph_Exp_NC_R_B_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_Exp_NC_R_B_2 = QtWidgets.QFrame(self.E_L_building_NC_R)
        self.frame_Exp_NC_R_B_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_Exp_NC_R_B_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Exp_NC_R_B_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Exp_NC_R_B_2.setObjectName("frame_Exp_NC_R_B_2")
        self.verticalLayoutWidget_47 = QtWidgets.QWidget(self.frame_Exp_NC_R_B_2)
        self.verticalLayoutWidget_47.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_47.setObjectName("verticalLayoutWidget_47")
        self.graph_Exp_NC_R_B_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_47)
        self.graph_Exp_NC_R_B_2.setContentsMargins(0, 0, 0, 0)
        self.graph_Exp_NC_R_B_2.setObjectName("graph_Exp_NC_R_B_2")
        
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.E_L_building_NC_R, "")
        
        #----
        # tabWidget_3_1 Expected Loss of building:
        
        # Apertura del tabWidget_3_1 de Expected Loss of building
        self.E_L_Building = QtWidgets.QWidget()
        self.E_L_Building.setObjectName("E_L_Building")
        
        # Frame de la gráfica de la edificación 1
        self.frame_Exp_B_1 = QtWidgets.QFrame(self.E_L_Building)
        self.frame_Exp_B_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_Exp_B_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Exp_B_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Exp_B_1.setObjectName("frame_Exp_B_1")
        self.verticalLayoutWidget_23 = QtWidgets.QWidget(self.frame_Exp_B_1)
        self.verticalLayoutWidget_23.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_23.setObjectName("verticalLayoutWidget_23")
        self.graph_Exp_B_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_23)
        self.graph_Exp_B_1.setContentsMargins(0, 0, 0, 0)
        self.graph_Exp_B_1.setObjectName("graph_Exp_B_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_Exp_B_2 = QtWidgets.QFrame(self.E_L_Building)
        self.frame_Exp_B_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_Exp_B_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Exp_B_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Exp_B_2.setObjectName("frame_Exp_B_2")
        self.verticalLayoutWidget_28 = QtWidgets.QWidget(self.frame_Exp_B_2)
        self.verticalLayoutWidget_28.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_28.setObjectName("verticalLayoutWidget_28")
        self.graph_Exp_B_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_28)
        self.graph_Exp_B_2.setContentsMargins(0, 0, 0, 0)
        self.graph_Exp_B_2.setObjectName("graph_Exp_B_2")
        
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.E_L_Building, "")
        
        #----
        # tabWidget_3_1 Expected Loss of building by events:
        
        # Apertura del tabWidget_3_1 de Expected Loss of building by events
        self.E_L_Building_events = QtWidgets.QWidget()
        self.E_L_Building_events.setObjectName("E_L_Building_events")
        
        # Frame de la gráfica de la edificación 1
        self.frame_ExpEvents_B_1 = QtWidgets.QFrame(self.E_L_Building_events)
        self.frame_ExpEvents_B_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_ExpEvents_B_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ExpEvents_B_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ExpEvents_B_1.setObjectName("frame_ExpEvents_B_1")
        self.verticalLayoutWidget_30 = QtWidgets.QWidget(self.frame_ExpEvents_B_1)
        self.verticalLayoutWidget_30.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_30.setObjectName("verticalLayoutWidget_30")
        self.graph_ExpEvents_B_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_30)
        self.graph_ExpEvents_B_1.setContentsMargins(0, 0, 0, 0)
        self.graph_ExpEvents_B_1.setObjectName("graph_ExpEvents_B_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_ExpEvents_B_2 = QtWidgets.QFrame(self.E_L_Building_events)
        self.frame_ExpEvents_B_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_ExpEvents_B_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ExpEvents_B_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ExpEvents_B_2.setObjectName("frame_ExpEvents_B_2")
        self.verticalLayoutWidget_29 = QtWidgets.QWidget(self.frame_ExpEvents_B_2)
        self.verticalLayoutWidget_29.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_29.setObjectName("verticalLayoutWidget_29")
        self.graph_ExpEvents_B_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_29)
        self.graph_ExpEvents_B_2.setContentsMargins(0, 0, 0, 0)
        self.graph_ExpEvents_B_2.setObjectName("graph_ExpEvents_B_2")
        
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.E_L_Building_events, "")
        
        #----
        # tabWidget_3_1 Probability of events:
        
        # Apertura del tabWidget_3_1 de Probability of events
        self.Prob_events = QtWidgets.QWidget()
        self.Prob_events.setObjectName("Prob_events")
        
        # Frame de la gráfica de la edificación 1
        self.frame_ProbEvent_B_1 = QtWidgets.QFrame(self.Prob_events)
        self.frame_ProbEvent_B_1.setGeometry(QtCore.QRect(0, -10, 501, 361))
        self.frame_ProbEvent_B_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ProbEvent_B_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ProbEvent_B_1.setObjectName("frame_ProbEvent_B_1")
        self.verticalLayoutWidget_32 = QtWidgets.QWidget(self.frame_ProbEvent_B_1)
        self.verticalLayoutWidget_32.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_32.setObjectName("verticalLayoutWidget_32")
        self.graph_ProbEvent_B_1 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_32)
        self.graph_ProbEvent_B_1.setContentsMargins(0, 0, 0, 0)
        self.graph_ProbEvent_B_1.setObjectName("graph_ProbEvent_B_1")
        
        # Frame de la gráfica de la edificación 2
        self.frame_ProbEvent_B_2 = QtWidgets.QFrame(self.Prob_events)
        self.frame_ProbEvent_B_2.setGeometry(QtCore.QRect(520, -10, 501, 361))
        self.frame_ProbEvent_B_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_ProbEvent_B_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_ProbEvent_B_2.setObjectName("frame_ProbEvent_B_2")
        self.verticalLayoutWidget_31 = QtWidgets.QWidget(self.frame_ProbEvent_B_2)
        self.verticalLayoutWidget_31.setGeometry(QtCore.QRect(0, 10, 501, 331))
        self.verticalLayoutWidget_31.setObjectName("verticalLayoutWidget_31")
        self.graph_ProbEvent_B_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_31)
        self.graph_ProbEvent_B_2.setContentsMargins(0, 0, 0, 0)
        self.graph_ProbEvent_B_2.setObjectName("graph_ProbEvent_B_2")
        
        # Cierre del Tab
        self.tabWidget_3_1.addTab(self.Prob_events, "")
        
        # ----------------------------------------------------------
        # TABWIDGET_3_2: Comp DV-EDP, Comp Expected Loss by story (NC+R), Comp Expected Loss of building (NC+R)
        # Comp Expected Loss of building, Comp Expected Loss of building by events, Comp Probability of events
        
        # Definición de la cinta de opciones del tab
        self.tabWidget_3_2 = QtWidgets.QTabWidget(self.scrollAreaWidgetContents_4)
        self.tabWidget_3_2.setGeometry(QtCore.QRect(280, 390, 1041, 401))
        self.tabWidget_3_2.setObjectName("tabWidget_3_2")
        
        #----
        # tabWidget_3_2 Comp DV-EDP:
        
        # Apertura del tabWidget_3_2 de Comp DV-EDP
        self.Comparison_LossStory = QtWidgets.QWidget()
        self.Comparison_LossStory.setObjectName("Comparison_LossStory")
        
        # Frame de la gráfica de la comparación
        self.frame_comparison_LossStory = QtWidgets.QFrame(self.Comparison_LossStory)
        self.frame_comparison_LossStory.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comparison_LossStory.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comparison_LossStory.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comparison_LossStory.setObjectName("frame_comparison_LossStory")
        self.verticalLayoutWidget_33 = QtWidgets.QWidget(self.frame_comparison_LossStory)
        self.verticalLayoutWidget_33.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_33.setObjectName("verticalLayoutWidget_33")
        self.graph_comparison_LossStory = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_33)
        self.graph_comparison_LossStory.setContentsMargins(0, 0, 0, 0)
        self.graph_comparison_LossStory.setObjectName("graph_comparison_LossStory")
        
        # Boton para comparaciones
        self.comparison_button_LossStory = QtWidgets.QPushButton(self.Comparison_LossStory)
        self.comparison_button_LossStory.setGeometry(QtCore.QRect(20, 330, 131, 31))
        self.comparison_button_LossStory.setObjectName("comparison_button_LossStory")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comparison_LossStory, "")
        
        #----
        # tabWidget_3_2 Comp Expected Loss by story (NC+R):
            
        # Apertura del tabWidget_3_2 de Comp Expected Loss by story (NC+R)
        self.Comp_E_L_Story = QtWidgets.QWidget()
        self.Comp_E_L_Story.setObjectName("Comp_E_L_Story")
            
        # Frame de la gráfica de la comparación
        self.frame_comp_exp_story = QtWidgets.QFrame(self.Comp_E_L_Story)
        self.frame_comp_exp_story.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comp_exp_story.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_exp_story.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_exp_story.setObjectName("frame_comp_exp_story")
        self.verticalLayoutWidget_34 = QtWidgets.QWidget(self.frame_comp_exp_story)
        self.verticalLayoutWidget_34.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_34.setObjectName("verticalLayoutWidget_34")
        self.graph_comp_exp_story = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_34)
        self.graph_comp_exp_story.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_exp_story.setObjectName("graph_comp_exp_story")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comp_E_L_Story, "")
        
        #----
        # tabWidget_3_2 Comp Expected Loss of building (NC+R):
            
        # Apertura del tabWidget_3_2 de Comp Expected Loss by story (NC+R)
        self.Comp_E_L_building_NC_R = QtWidgets.QWidget()
        self.Comp_E_L_building_NC_R.setObjectName("Comp_E_L_building_NC_R")
        
        # Frame de la gráfica de la comparación
        self.frame_comp_Exp_NC_R_B = QtWidgets.QFrame(self.Comp_E_L_building_NC_R)
        self.frame_comp_Exp_NC_R_B.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comp_Exp_NC_R_B.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_Exp_NC_R_B.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_Exp_NC_R_B.setObjectName("frame_comp_Exp_NC_R_B")
        self.verticalLayoutWidget_52 = QtWidgets.QWidget(self.frame_comp_Exp_NC_R_B)
        self.verticalLayoutWidget_52.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_52.setObjectName("verticalLayoutWidget_52")
        self.graph_comp_Exp_NC_R_B = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_52)
        self.graph_comp_Exp_NC_R_B.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_Exp_NC_R_B.setObjectName("graph_comp_Exp_NC_R_B")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comp_E_L_building_NC_R, "")
        
        
        #----
        # tabWidget_3_2 Comp Expected Loss of building:
            
        # Apertura del tabWidget_3_2 de Comp Expected Loss of building
        self.Comp_E_L_Building = QtWidgets.QWidget()
        self.Comp_E_L_Building.setObjectName("Comp_E_L_Building")
            
        # Frame de la gráfica de la comparación
        self.frame_comp_exp_building = QtWidgets.QFrame(self.Comp_E_L_Building)
        self.frame_comp_exp_building.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comp_exp_building.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_exp_building.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_exp_building.setObjectName("frame_comp_exp_building")
        self.verticalLayoutWidget_36 = QtWidgets.QWidget(self.frame_comp_exp_building)
        self.verticalLayoutWidget_36.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_36.setObjectName("verticalLayoutWidget_36")
        self.graph_comp_exp_building = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_36)
        self.graph_comp_exp_building.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_exp_building.setObjectName("graph_comp_exp_building")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comp_E_L_Building, "")
        
        #----
        # tabWidget_3_2 Comp Expected Loss of building by events:
            
        # Apertura del tabWidget_3_2 de Comp Expected Loss of building by events
        self.Comp_E_L_Building_events = QtWidgets.QWidget()
        self.Comp_E_L_Building_events.setObjectName("Comp_E_L_Building_events")
            
        # Frame de la gráfica de la comparación
        self.frame_comp_expEvent_building = QtWidgets.QFrame(self.Comp_E_L_Building_events)
        self.frame_comp_expEvent_building.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comp_expEvent_building.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_expEvent_building.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_expEvent_building.setObjectName("frame_comp_expEvent_building")
        self.verticalLayoutWidget_37 = QtWidgets.QWidget(self.frame_comp_expEvent_building)
        self.verticalLayoutWidget_37.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_37.setObjectName("verticalLayoutWidget_37")
        self.graph_comp_expEvent_building = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_37)
        self.graph_comp_expEvent_building.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_expEvent_building.setObjectName("graph_comp_expEvent_building")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comp_E_L_Building_events, "")
        
        #----
        # tabWidget_3_2 Comp Probability of events:
            
        # Apertura del tabWidget_3_2 de Comp Probability of events
        self.Comp_Prob_events = QtWidgets.QWidget()
        self.Comp_Prob_events.setObjectName("Comp_Prob_events")
            
        # Frame de la gráfica de la comparación
        self.frame_comp_prob = QtWidgets.QFrame(self.Comp_Prob_events)
        self.frame_comp_prob.setGeometry(QtCore.QRect(180, 10, 671, 351))
        self.frame_comp_prob.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_comp_prob.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_comp_prob.setObjectName("frame_comp_prob")
        self.verticalLayoutWidget_38 = QtWidgets.QWidget(self.frame_comp_prob)
        self.verticalLayoutWidget_38.setGeometry(QtCore.QRect(0, 0, 671, 351))
        self.verticalLayoutWidget_38.setObjectName("verticalLayoutWidget_38")
        self.graph_comp_prob = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_38)
        self.graph_comp_prob.setContentsMargins(0, 0, 0, 0)
        self.graph_comp_prob.setObjectName("graph_comp_prob")
        
        # Cierre del Tab
        self.tabWidget_3_2.addTab(self.Comp_Prob_events, "")
        
        # 
        # Cierre del Tab de Loss of Buildings
        self.tabWidget_General.addTab(self.LossStory, "")
        
        # Scrolls
        self.verticalScrollBar_lossStory = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_4)
        self.verticalScrollBar_lossStory.setGeometry(QtCore.QRect(1630, 0, 16, 791))
        self.verticalScrollBar_lossStory.setOrientation(QtCore.Qt.Vertical)
        self.verticalScrollBar_lossStory.setObjectName("verticalScrollBar_lossStory")
        self.horizontalScrollBar_lossStory = QtWidgets.QScrollBar(self.scrollAreaWidgetContents_4)
        self.horizontalScrollBar_lossStory.setGeometry(QtCore.QRect(0, 790, 1631, 16))
        self.horizontalScrollBar_lossStory.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalScrollBar_lossStory.setObjectName("horizontalScrollBar_lossStory")
        
        self.scrollArea_LossStory.setWidget(self.scrollAreaWidgetContents_4)
        
        # ################################################################
        # TABWIDGET LOSS OF TAXONOMIES
        # ################################################################
        
        # Tab de vulnerabilidad de taxonomias
        self.LossTax = QtWidgets.QWidget()
        self.LossTax.setObjectName("LossTax")
        
        #
        # Cierre del Tab de Loss of Buildings
        self.tabWidget_General.addTab(self.LossTax, "")
        
        
        
        
        
        # ################################################################
        # FINALIZACIÓN
        # ################################################################

        self.retranslateUi(FragilityCurvesTool)
        self.tabWidget_General.setCurrentIndex(0)
        self.tabWidget_1_1.setCurrentIndex(0)
        self.tabWidget_1_2.setCurrentIndex(0)
        self.tabWidget_2_1.setCurrentIndex(0)
        self.tabWidget_3_1.setCurrentIndex(0)
        self.tabWidget_3_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FragilityCurvesTool)


    def retranslateUi(self, FragilityCurvesTool):
        _translate = QtCore.QCoreApplication.translate
        
        FragilityCurvesTool.setWindowTitle(_translate("FragilityCurvesTool", "V-FAST: Vulnerability and Fragility Assessment Toolkit"))
        
        # ################################################################
        # TABWIDGET FRAGILITY OF BUILDINGS
        # ################################################################
        
        # Boton para cargar escel de edificaciones
        self.Load_Guide_Data.setText(_translate("FragilityCurvesTool", "LOAD BUILDING GUIDE"))
        
        # ----------------------------------------------------------
        # LOAD FOLDERS
        self.LoadFiles_1.setText(_translate("FragilityCurvesTool", "LOAD FOLDERS"))
        self.LoadFiles_2.setText(_translate("FragilityCurvesTool", "LOAD FOLDERS"))
        
        self.HazardLevelButton_1.setText(_translate("FragilityCurvesTool", "Hazard Levels Folder:"))
        self.HazardLevelButton_2.setText(_translate("FragilityCurvesTool", "Hazard Levels Folder:"))
        
        self.EDPButton_1.setText(_translate("FragilityCurvesTool", "Building Folder:"))
        self.EDPButton_2.setText(_translate("FragilityCurvesTool", "Building Folder:"))
        
        # ----------------------------------------------------------
        # TEST
        self.Test1.setText(_translate("FragilityCurvesTool", "TEST"))
        self.Test1_2.setText(_translate("FragilityCurvesTool", "TEST"))
        
        self.tminLabel_1.setText(_translate("FragilityCurvesTool", "tmin ="))
        self.tminLabel_2.setText(_translate("FragilityCurvesTool", "tmin ="))
        
        self.EDPlimLabel_1.setText(_translate("FragilityCurvesTool", "EDP lim ="))
        self.EDPlimLabel_2.setText(_translate("FragilityCurvesTool", "EDP lim ="))
        
        self.range_1.setText(_translate("FragilityCurvesTool", "range: [0-1]"))
        self.range_2.setText(_translate("FragilityCurvesTool", "range: [0-1]"))
        
        # self.porc_1.setText(_translate("FragilityCurvesTool", "[%]"))
        # self.porc_2.setText(_translate("FragilityCurvesTool", "[%]"))
        
        # ----------------------------------------------------------
        # IM AND EDP DEFINITION
        self.IM_EDP_selection_1.setText(_translate("FragilityCurvesTool", "IM AND EDP DEFINITION"))
        self.IM_EDP_selection_2.setText(_translate("FragilityCurvesTool", "IM AND EDP DEFINITION"))
        
        self.PeriodoLabel_1.setText(_translate("FragilityCurvesTool", "T ="))
        self.PeriodoLabel_2.setText(_translate("FragilityCurvesTool", "T ="))
        
        self.IMType_Label_1.setText(_translate("FragilityCurvesTool", "IM ="))
        self.IMType_Label_2.setText(_translate("FragilityCurvesTool", "IM ="))
        
        self.EDPType_Label_1.setText(_translate("FragilityCurvesTool", "EDP ="))
        self.EDPType_Label_2.setText(_translate("FragilityCurvesTool", "EDP ="))
        
        self.EDP_cens_Label_1.setText(_translate("FragilityCurvesTool", "EDP cens ="))
        self.EDP_cens_Label_2.setText(_translate("FragilityCurvesTool", "EDP cens ="))
        
        self.Hazard_Label_1.setText(_translate("FragilityCurvesTool", "Hazards ="))
        self.Hazard_Label_2.setText(_translate("FragilityCurvesTool", "Hazards ="))
   
        # ----------------------------------------------------------
        # FRAGILITY PARAMETERS
        self.FragilityTittle_1.setText(_translate("FragilityCurvesTool", "FRAGILITY PARAMETERS"))
        self.FragilityTittle_2.setText(_translate("FragilityCurvesTool", "FRAGILITY PARAMETERS"))
        
        self.j_Label_1.setText(_translate("FragilityCurvesTool", "Thresholds SEC =")) 
        self.j_Label_2.setText(_translate("FragilityCurvesTool", "Thresholds SEC ="))
        
        self.theta_Label_1.setText(_translate("FragilityCurvesTool", "θ DS-EDP ="))
        self.theta_Label_2.setText(_translate("FragilityCurvesTool", "θ DS-EDPS ="))
        
        self.sigma_Label_1.setText(_translate("FragilityCurvesTool", "β DS-EDP ="))
        self.sigma_Label_2.setText(_translate("FragilityCurvesTool", "β DS-EDP ="))
        
        self.EDPCollapse_Label_1.setText(_translate("FragilityCurvesTool", "EDP Collapse ="))
        self.EDPCollapse_Label_2.setText(_translate("FragilityCurvesTool", "EDP Collapse ="))
        
        self.DSTags_Label_1.setText(_translate("FragilityCurvesTool", "DS Tags ="))
        self.DSTags_Label_2.setText(_translate("FragilityCurvesTool", "DS Tags ="))
        
        self.porc_fit_curves_Label_1.setText(_translate("FragilityCurvesTool", "% Curves fitting ="))
        self.porc_fit_curves_Label_2.setText(_translate("FragilityCurvesTool", "% Curves fitting ="))
        
        self.binLabel_1.setText(_translate("FragilityCurvesTool", " Bin type ="))
        self.binLabel_2.setText(_translate("FragilityCurvesTool", "Bin type ="))
        
        self.collapseMethod_Label_1.setText(_translate("FragilityCurvesTool", "Collapse Method ="))
        self.collapseMethod_Label_2.setText(_translate("FragilityCurvesTool", "Collapse Method ="))
        
        self.binMinLabel_1.setText(_translate("FragilityCurvesTool", "MinData_Bin ="))
        self.binMinLabel_2.setText(_translate("FragilityCurvesTool", "MinData_Bin ="))
        
        self.initialBinLabel_1.setText(_translate("FragilityCurvesTool", "Initial_NumBins ="))
        self.initialBinLabel_2.setText(_translate("FragilityCurvesTool", "Initial_NumBins ="))
        
        # ----------------------------------------------------------
        # Autores
        # self.Authors.setText(_translate("FragilityCurvesTool", "(Abuchar & Arteta, 2023)"))
        
        # ----------------------------------------------------------
        # GRAFICAS Fragility Analysis
        
        # Curvas de fragilidad
        self.label_curve1.setText(_translate("FragilityCurvesTool", "BUILDING 1"))
        self.label_curve2.setText(_translate("FragilityCurvesTool", "BUILDING 2"))
        
        self.SEC_bulding_1.setText(_translate("FragilityCurvesTool", "Graph SEC 1"))
        self.SEC_bulding_2.setText(_translate("FragilityCurvesTool", "Graph SEC 2"))
        
        self.Fragility_bulding_1.setText(_translate("FragilityCurvesTool", "Graph Fragility 1"))
        self.Fragility_bulding_2.setText(_translate("FragilityCurvesTool", "Graph Fragility 2"))
        
        # ----
        # TABWIDGET_1_1 
        
        # Tab de SEC
        self.tabWidget_1_1.setTabText(self.tabWidget_1_1.indexOf(self.SEC), _translate("FragilityCurvesTool", "SEC"))
        
        # Tab de FragilityCurves
        self.tabWidget_1_1.setTabText(self.tabWidget_1_1.indexOf(self.FragilityCurves), _translate("FragilityCurvesTool", "FragilityCurves"))
        
        # Tab de PDFs of EDP
        self.IM_values_1.setText(_translate("FragilityCurvesTool", "IMs"))
        self.IM_values_2.setText(_translate("FragilityCurvesTool", "IMs"))
        self.PDFs_button_1.setText(_translate("FragilityCurvesTool", "Calc"))
        self.PDFs_button_2.setText(_translate("FragilityCurvesTool", "Calc"))
        self.tabWidget_1_1.setTabText(self.tabWidget_1_1.indexOf(self.pdf_EDPs), _translate("FragilityCurvesTool", "PDFs of EDP"))
        
        # ----
        # TABWIDGET_1_2
        
        # Tab de Dispersion
        self.refresh_dispersion_1.setText(_translate("FragilityCurvesTool", "Dispersion 1"))
        self.refresh_dispersion_2.setText(_translate("FragilityCurvesTool", "Dispersion 2"))
        self.tabWidget_1_2.setTabText(self.tabWidget_1_2.indexOf(self.Dispersion), _translate("FragilityCurvesTool", "Dispersion"))
        
        # Tab de Binning_SEC
        self.tabWidget_1_2.setTabText(self.tabWidget_1_2.indexOf(self.Binning_SEC), _translate("FragilityCurvesTool", "Binning_SEC"))
        
        # Tab de Binning_FC
        self.tabWidget_1_2.setTabText(self.tabWidget_1_2.indexOf(self.Binning_FC), _translate("FragilityCurvesTool", "Binning_FC"))
        
        # Tab de Comparison and Combination
        self.comparison_button.setText(_translate("FragilityCurvesTool", "Graph Comparison"))
        self.combined_curve_button.setText(_translate("FragilityCurvesTool", "Graph Combined Curves"))
        self.tabWidget_1_2.setTabText(self.tabWidget_1_2.indexOf(self.Comparison_Combination), _translate("FragilityCurvesTool", "Comparison and Combination"))
        
        # ################################################################
        # TABWIDGET FRAGILITY OF TAXONOMIES
        # ################################################################
        
        # ----------------------------------------------------------
        # INPUTS
        self.input_label.setText(_translate("FragilityCurvesTool", "INPUTS"))
        
        # ---------------------------
        # IM AND EDP DEFINITION
        self.IM_EDP_selection_3.setText(_translate("FragilityCurvesTool", "IM AND EDP DEFINITION"))
        self.PeriodoLabel_3.setText(_translate("FragilityCurvesTool", "T ="))
        self.IMType_Label_3.setText(_translate("FragilityCurvesTool", "IM ="))
        self.EDPType_Label_3.setText(_translate("FragilityCurvesTool", "EDP ="))
        
        # ---------------------------
        # FRAGILITY PARAMETERS
        self.FragilityTittle_3.setText(_translate("FragilityCurvesTool", "FRAGILITY PARAMETERS"))
        self.porc_fit_curves_Label_3.setText(_translate("FragilityCurvesTool", "% Curves fitting ="))
        self.binLabel_3.setText(_translate("FragilityCurvesTool", " Bin type ="))
        self.include_cens_Label_3.setText(_translate("FragilityCurvesTool", "Include Cens ="))
        self.collapseMethod_Label_3.setText(_translate("FragilityCurvesTool", "Collapse Method ="))
        self.binMinLabel_3.setText(_translate("FragilityCurvesTool", "MinData_Bin ="))
        self.initialBinLabel_3.setText(_translate("FragilityCurvesTool", "Initial_NumBins ="))
         
        # ---------------------------
        # GROUPING OF BUILDINGS
        self.Group_buildings.setText(_translate("FragilityCurvesTool", "GROUPING OF BUILDINGS"))
        self.group_criteria_label.setText(_translate("FragilityCurvesTool", "Grouping criteria ="))
        
        # ---------------------------
        # BUILDING RESULTS FOLDERS
        self.Results_folders.setText(_translate("FragilityCurvesTool", "BUILDING RESULTS FOLDERS"))
        self.global_folder_label.setText(_translate("FragilityCurvesTool", "Global folder ="))
        self.global_folder_button.setText(_translate("FragilityCurvesTool", "Load"))
        
        # ---------------------------
        # DATABASE GENERATION
        self.database_generation.setText(_translate("FragilityCurvesTool", "DATABASE GENERATION"))
        self.excel_name_label.setText(_translate("FragilityCurvesTool", "File name ="))
        self.xlsx.setText(_translate("FragilityCurvesTool", ".xlsx"))
        self.excel_location_label.setText(_translate("FragilityCurvesTool", "File location ="))
        self.excel_folder_button.setText(_translate("FragilityCurvesTool", "Search"))
        
        # ---------------------------
        # RUN
        self.status_taxonomy.setText(_translate("FragilityCurvesTool", "Status"))
        self.processing_finishing_status.setText(_translate("FragilityCurvesTool", "Clic to start button"))
        self.start_calculations.setText(_translate("FragilityCurvesTool", "Start  calculations"))
        
        
        # ----------------------------------------------------------
        # GRAPHICS
        self.graphics_label.setText(_translate("FragilityCurvesTool", "GRAPHICS"))
        self.Load_Excel_Tax.setText(_translate("FragilityCurvesTool", "Load File"))
        self.excel_name_load.setText(_translate("FragilityCurvesTool", "File Name"))
        
        # ---------------------------
        # GENERAL
        self.Taxonomy_1.setText(_translate("FragilityCurvesTool", "TAXONOMY 1"))
        self.Taxonomy_2.setText(_translate("FragilityCurvesTool", "TAXONOMY 2"))
        
        self.IMLabelTax_1.setText(_translate("FragilityCurvesTool", "IM ="))
        self.IMLabelTax_2.setText(_translate("FragilityCurvesTool", "IM ="))
        
        self.PeriodoLabelTax_1.setText(_translate("FragilityCurvesTool", "T ="))
        self.PeriodoLabelTax_2.setText(_translate("FragilityCurvesTool", "T ="))
        
        self.TaxonomyLabelTax_1.setText(_translate("FragilityCurvesTool", "Tax ="))
        self.TaxonomyLabelTax_2.setText(_translate("FragilityCurvesTool", "Tax ="))
        
        self.ParamLabelTax_1.setText(_translate("FragilityCurvesTool", "Param ="))
        self.ParamLabelTax_2.setText(_translate("FragilityCurvesTool", "Param ="))
        
        self.Graph_tax_1.setText(_translate("FragilityCurvesTool", "Graph Tax 1"))
        self.Graph_tax_2.setText(_translate("FragilityCurvesTool", "Graph Tax 2"))
        
        # ---------------------------
        # MODIFICATIONS
        self.modifications_Label_1.setText(_translate("FragilityCurvesTool", "MODIFICATIONS"))
        self.modifications_Label_2.setText(_translate("FragilityCurvesTool", "MODIFICATIONS"))
        
        self.changeType_Label_1.setText(_translate("FragilityCurvesTool", "Change Type ="))
        self.changeType_Label_2.setText(_translate("FragilityCurvesTool", "Change Type ="))
        
        self.thetaTax_Label_1.setText(_translate("FragilityCurvesTool", "θ DS-IM ="))
        self.thetaTax_Label_2.setText(_translate("FragilityCurvesTool", "θ DS-IM ="))
        
        self.sigmaTax_Label_1.setText(_translate("FragilityCurvesTool", "β DS-IM ="))
        self.sigmaTax_Label_2.setText(_translate("FragilityCurvesTool", "β DS-IMS ="))
        
        self.porc_fit_curves_changes_Label_1.setText(_translate("FragilityCurvesTool", "% Curves fitting ="))
        self.porc_fit_curves_changes_Label_2.setText(_translate("FragilityCurvesTool", "% Curves fitting ="))
        
        self.IM_vals_changes_Label_1.setText(_translate("FragilityCurvesTool", "IM limits ="))
        self.IM_vals_changes_Label_2.setText(_translate("FragilityCurvesTool", "IM limits ="))
        
        self.Graph_mod_tax_1.setText(_translate("FragilityCurvesTool", "Graph Modifications 1"))
        self.Graph_mod_tax_2.setText(_translate("FragilityCurvesTool", "Graph Modifications 2"))
        
        self.Save_mod_tax_1.setText(_translate("FragilityCurvesTool", "Save new parameters Tax 1"))
        self.Save_mod_tax_2.setText(_translate("FragilityCurvesTool", "Save new parameters Tax 2"))
        
        self.Export_tax_mod_excel.setText(_translate("FragilityCurvesTool", "Export Changes to Excel"))
        
        # ----------------------------------------------------------
        # GRAFICAS
        
        # ----
        # TABWIDGET_1_4
        
        # Tab de Dispersion
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.DispersionTax), _translate("FragilityCurvesTool", "Dispersion"))
        
        # Tab de FagilityCurves
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.FragilityCurves_Tax), _translate("FragilityCurvesTool", "FragilityCurves"))
        
        # Tab de Fragility by DS
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.FragilityDS), _translate("FragilityCurvesTool", "Fragility by DS"))
        
        self.DS_graph_Label_1.setText(_translate("FragilityCurvesTool", "DS ="))
        self.DS_graph_Label_2.setText(_translate("FragilityCurvesTool", "DS ="))
        
        self.Graph_DS_1.setText(_translate("FragilityCurvesTool", "Graph DS"))
        self.Graph_DS_2.setText(_translate("FragilityCurvesTool", "Graph DS"))
        
        # Tab de Parameter by DS
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.ParametersDS), _translate("FragilityCurvesTool", "Parameters by DS"))
        
        # Tab de Comparison by parameters
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.comp_parameters), _translate("FragilityCurvesTool", "Comparison by parameters"))
        
        # Comparison by typologies
        self.tabWidget_1_4.setTabText(self.tabWidget_1_4.indexOf(self.comp_typ), _translate("FragilityCurvesTool", "Comparison by typologies"))
        
        self.Level_comparison_Label_1.setText(_translate("FragilityCurvesTool", "Level of comparison ="))
        self.Level_comparison_Label_2.setText(_translate("FragilityCurvesTool", "Level of comparison ="))
        
        self.DS_graph_comp_Label_1.setText(_translate("FragilityCurvesTool", "DS ="))
        self.DS_graph_comp_Label_2.setText(_translate("FragilityCurvesTool", "DS ="))
        
        self.Graph_comp_1.setText(_translate("FragilityCurvesTool", "Graph"))
        self.Graph_comp_2.setText(_translate("FragilityCurvesTool", "Graph"))
               
        # ################################################################
        # TABWIDGET LOSS COMPONENT
        # ################################################################
        
        # ----------------------------------------------------------
        # GENERAL
        self.load_compGuide.setText(_translate("FragilityCurvesTool", "Load Components"))
        self.label_damageLoss.setText(_translate("FragilityCurvesTool", "DAMAGE TO LOSS"))
        self.CostType_label.setText(_translate("FragilityCurvesTool", "Cost Type ="))
        
        # ----
        # TABWIDGET_2_1
        
        # Tab components
        self.fragilityGroup_Label_1.setText(_translate("FragilityCurvesTool", "Frag. Group 1 ="))
        self.fragilityGroup_Label_2.setText(_translate("FragilityCurvesTool", "Frag. Group 2 ="))
        
        self.componentName_1.setText(_translate("FragilityCurvesTool", "Component name"))
        self.componentName_2.setText(_translate("FragilityCurvesTool", "Component name"))
        
        self.EDPVal_label_comp_1.setText(_translate("FragilityCurvesTool", "EDP Value ="))
        self.EDPVal_label_comp_2.setText(_translate("FragilityCurvesTool", "EDP Value ="))
        
        self.CalcComp_1.setText(_translate("FragilityCurvesTool", "Calculate"))
        self.CalcComp_2.setText(_translate("FragilityCurvesTool", "Calculate"))
        
        self.tabWidget_2_1.setTabText(self.tabWidget_2_1.indexOf(self.Components), _translate("FragilityCurvesTool", "Components"))
        
        # Tab comparison of components
        self.tabWidget_2_1.setTabText(self.tabWidget_2_1.indexOf(self.ComparisonComponents), _translate("FragilityCurvesTool", "Comparison of Components"))
        
        # ################################################################
        # TABWIDGET LOSS OF BUILDINGS
        # ################################################################
        
        # ----------------------------------------------------------
        # GENERAL
        self.BuildingTittle_Loss_1.setText(_translate("FragilityCurvesTool", "BUILDING 1"))
        self.BuildingTittle_Loss_2.setText(_translate("FragilityCurvesTool", "BUILDING 2"))
        
        self.label_curve_B1.setText(_translate("FragilityCurvesTool", "BUILDING 1"))
        self.label_curve_B2.setText(_translate("FragilityCurvesTool", "BUILDING 2"))
        
        # ----------------------------------------------------------
        # LOAD FOLDERS
        self.LoadFiles_loss_1.setText(_translate("FragilityCurvesTool", "LOAD DATA"))
        self.LoadFiles_loss_2.setText(_translate("FragilityCurvesTool", "LOAD DATA"))
        
        self.BuildingButton_Loss_1.setText(_translate("FragilityCurvesTool", "Load Data:"))
        self.BuildingButton_Loss_2.setText(_translate("FragilityCurvesTool", "Load Data:"))
        
        # ----------------------------------------------------------
        # GRAPH OPTIONS: DV-EDP
        self.DV_EDP_options_1.setText(_translate("FragilityCurvesTool", "GRAPH OPTIONS: DV-EDP"))
        self.DV_EDP_options_2.setText(_translate("FragilityCurvesTool", "GRAPH OPTIONS: DV-EDP"))
        
        self.Story_Label_1.setText(_translate("FragilityCurvesTool", "Story ="))
        self.Story_Label_2.setText(_translate("FragilityCurvesTool", "Story ="))
        
        self.InputData_Label_1.setText(_translate("FragilityCurvesTool", "Input Data ="))
        self.InputData_Label_2.setText(_translate("FragilityCurvesTool", "Input Data ="))
        
        self.Element_Label_1.setText(_translate("FragilityCurvesTool", "Element ="))
        self.Element_Label_2.setText(_translate("FragilityCurvesTool", "Element ="))
        
        self.LoadElements_Label_1.setText(_translate("FragilityCurvesTool", "Load elements selection"))
        self.LoadElements_Label_2.setText(_translate("FragilityCurvesTool", "Load elements selection"))
        
        self.Element_activate_1.setText(_translate("FragilityCurvesTool", "Load"))
        self.Element_activate_2.setText(_translate("FragilityCurvesTool", "Load"))
        
        self.Graph_button_DVEDP_1.setText(_translate("FragilityCurvesTool", "Graph DV-EDP B1"))
        self.Graph_button_DVEDP_2.setText(_translate("FragilityCurvesTool", "Graph DV-EDP B2"))
        
        # ----------------------------------------------------------
        # GRAPH OPTIONS: DV-IM
        
        self.DV_IM_options_1.setText(_translate("FragilityCurvesTool", "GRAPH OPTIONS: DV-IM"))
        self.DV_IM_options_2.setText(_translate("FragilityCurvesTool", "GRAPH OPTIONS: DV-IM"))
        
        self.SDRLoss_cens_Label_1.setText(_translate("FragilityCurvesTool", "SDR cens limit ="))
        self.SDRLoss_cens_Label_2.setText(_translate("FragilityCurvesTool", "SDR cens limit ="))
        
        self.Theta_collapse_Label_1.setText(_translate("FragilityCurvesTool", "θ collapse DS-IM ="))
        self.Theta_collapse_Label_2.setText(_translate("FragilityCurvesTool", "θ collapse DS-IM ="))
        
        self.Sigma_collapse_Label_1.setText(_translate("FragilityCurvesTool", "β collapse DS-IM ="))
        self.Sigma_collapse_Label_2.setText(_translate("FragilityCurvesTool", "β collapse DS-IM ="))
        
        self.Theta_rsdr_Label_1.setText(_translate("FragilityCurvesTool", "θ RSDR DS-EDP ="))
        self.Theta_rsdr_Label_2.setText(_translate("FragilityCurvesTool", "θ RSDR DS-EDP ="))
        
        self.Sigma_rsdr_Label_1.setText(_translate("FragilityCurvesTool", "β RSDR DS-EDP ="))
        self.Sigma_rsdr_Label_2.setText(_translate("FragilityCurvesTool", "β RSDR DS-EDP ="))
        
        self.ED_Label_1.setText(_translate("FragilityCurvesTool", "E[L|NC + D] ="))
        self.ED_Label_2.setText(_translate("FragilityCurvesTool", "E[L|NC + D] ="))
        
        self.EC_Label_1.setText(_translate("FragilityCurvesTool", "E[L|C] ="))
        self.EC_Label_2.setText(_translate("FragilityCurvesTool", "E[L|C] ="))
        
        self.Graph_button_DVIM_1.setText(_translate("FragilityCurvesTool", "Graph DV-IM B1"))
        self.Graph_button_DVIM_2.setText(_translate("FragilityCurvesTool", "Graph DV-IM B2"))
        
        # ----
        # TABWIDGET_3_1
        
        # Tab de DV-EDP
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.DV_EDP), _translate("FragilityCurvesTool", "DV-EDP"))
        
        # Tab de Expected Loss by story (NC+R)
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.E_L_Story), _translate("FragilityCurvesTool", "Expected Loss by story (NC+R)"))
        
        # Tab de Expected Loss of building (NC+R)
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.E_L_building_NC_R), _translate("FragilityCurvesTool", "Expected Loss of building (NC+R)"))
        
        # Tab de Expected Loss of building
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.E_L_Building), _translate("FragilityCurvesTool", "Expected Loss of building"))
        
        # Tab de Expected Loss of building by events
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.E_L_Building_events), _translate("FragilityCurvesTool", "Expected Loss of building by events"))
        
        # Tab de Probability of events
        self.tabWidget_3_1.setTabText(self.tabWidget_3_1.indexOf(self.Prob_events), _translate("FragilityCurvesTool", "Probability of events"))
        
        # ----
        # TABWIDGET_3_2
        
        # Tab de DV-EDP
        self.comparison_button_LossStory.setText(_translate("FragilityCurvesTool", "Graph Comparison"))
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comparison_LossStory), _translate("FragilityCurvesTool", "Comp DV-EDP"))
        
        # Tab de Comp Expected Loss by story (NC+R)
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comp_E_L_Story), _translate("FragilityCurvesTool", "Comp Expected Loss by story (NC+R)"))
        
        # Tab de Comp Expected Loss of building (NC+R)
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comp_E_L_building_NC_R), _translate("FragilityCurvesTool", "Comp Expected Loss of building (NC+R)"))
        
        # Tab de Comp Expected Loss of building
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comp_E_L_Building), _translate("FragilityCurvesTool", "Comp Expected Loss of building"))
        
        # Tab de Comp Expected Loss of building by events
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comp_E_L_Building_events), _translate("FragilityCurvesTool", "Comp Expected Loss of building by events"))
        
        # Tab de Comp Probability of events
        self.tabWidget_3_2.setTabText(self.tabWidget_3_2.indexOf(self.Comp_Prob_events), _translate("FragilityCurvesTool", "Comp Probability of events"))
        
        # ----------------------------------------------------------
        # Tabs principal
        self.tabWidget_General.setTabText(self.tabWidget_General.indexOf(self.FragilityAnalysis), _translate("FragilityCurvesTool", "Fragility of Buildings"))
        self.tabWidget_General.setTabText(self.tabWidget_General.indexOf(self.FragilityTaxonomy), _translate("FragilityCurvesTool", "Fragility of Taxonomies"))
        self.tabWidget_General.setTabText(self.tabWidget_General.indexOf(self.LossComponent), _translate("FragilityCurvesTool", "Loss Components"))
        self.tabWidget_General.setTabText(self.tabWidget_General.indexOf(self.LossStory), _translate("FragilityCurvesTool", "Loss of Buildings"))
        self.tabWidget_General.setTabText(self.tabWidget_General.indexOf(self.LossTax), _translate("FragilityCurvesTool", "Loss of Taxonomies"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    FragilityCurvesTool = QtWidgets.QDialog()
    ui = Ui_FragilityCurvesTool()
    ui.setupUi(FragilityCurvesTool)
    FragilityCurvesTool.show()
    sys.exit(app.exec_())

