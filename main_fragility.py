# -*- coding: utf-8 -*-
"""

V-FAST: VULNERABILITY AND FRAGILITY ASSESSMENT TOOLKIT
----------------------------------------------------------------------------------------
VERSION: VO1
AUTORES: ABUCHAR, V.J, ARTETA C.A. (2023)

"""

#%% IMPPORTE DE LIBRERIAS Y FUNCIONES
import sys
import os
import re
import glob
import time
from datetime import datetime

import numpy as np
import pandas as pd
import math
import statsmodels.api as sm
from scipy import stats
from scipy.stats import norm


import matplotlib
import matplotlib.pyplot as plt
from matplotlib import colors, colorbar
from matplotlib.ticker import MaxNLocator
#from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *

import shutil
from openpyxl import load_workbook

import warnings
warnings.simplefilter('ignore')

# IMPORTAR FUNCIONES
from exponente import exponente
from fragility_function_V7 import *
from Lectura_Archivos_V2 import *
from Definicion_IM_EDP import *
from Loss_functions import *
from GUIFragilityCurvesTool import * 
from Colores_Dispersion import *

#%% DEFINICIONES PRELIMINARES

# Colores de curvas
global color, color_py
color = ['green', 'yellow', 'orange', 'red', 'darkred','black', 'blue']
color2 = ['blue', 'green', 'yellow', 'orange', 'red', 'darkred','black']
color3 = ['blue', 'orange', 'green', 'red', 'blueviolet','black']
color_py = graphs_many_color()


# Datos de edps para plots de pérdidas
global delta_max_edp, EDPs_list
delta_max_edp = {}
delta_max_edp['SDR'] = {'edp_max': 0.3, 'd_edp': 0.001}
delta_max_edp['PFA'] = {'edp_max': 80, 'd_edp': 0.1}
delta_max_edp['RSDR'] = {'edp_max': 0.2, 'd_edp': 0.0001}
delta_max_edp['RDR'] = {'edp_max': 0.3, 'd_edp': 0.001}

EDPs_list = ['SDR', 'PFA', 'RSDR']


#%% DEFINICIÓN DE CLASE PARA GRÁFICAS

# Grafica de funciones de fragilidad de edificación 1
class Canvas_grafica(FigureCanvas):
    def __init__(self, parent=None):     
        self.fig , self.ax = plt.subplots(1, dpi=100, figsize=(4, 6), 
            sharey=True, facecolor='white')
        super().__init__(self.fig)
        
        self.toolbar = NavigationToolbar(self, self, coordinates=False)
        self.toolbar.setMinimumWidth(300)
        self.toolbar.setStyleSheet("QToolBar { border: 0px }")
        self.toolbar.setIconSize(QtCore.QSize(15, 15))
        
class Canvas_grafica_2(FigureCanvas):
    def __init__(self, parent=None):  
        
        self.fig, (self.ax1, self.ax2) = plt.subplots(nrows=2, ncols=1, dpi=100, figsize=(8,5), sharex=True,
                                      gridspec_kw={'height_ratios': [1, 3]}, facecolor='white')
    
        super().__init__(self.fig)
        
        self.toolbar = NavigationToolbar(self, self, coordinates=False)
        self.toolbar.setMinimumWidth(300)
        self.toolbar.setStyleSheet("QToolBar { border: 0px }")
        self.toolbar.setIconSize(QtCore.QSize(15, 15))

#%% APP PRINCIPAL

###################################################################################
# DEFINICIÓN DE APP PRINCIPAL PARA GENERACIÓN DE CURVAS      
###################################################################################   
    
class MiApp(QtWidgets.QMainWindow):

#%% BOTONES
    
###################################################################################
# CONEXIÓN DE BOTONES
###################################################################################
    
    def __init__(self):
        super().__init__()
        self.ui = Ui_FragilityCurvesTool() 
        self.ui.setupUi(self)
        
        #-----------------------------------------------------------------------------
        # Conecta los botones de la ui con las funciones definidas abajo
        
        # Tabwidget Fragility of Buildings
        self.ui.SEC_bulding_1.clicked.connect(self.SEC_b1)
        self.ui.SEC_bulding_2.clicked.connect(self.SEC_b2)
        self.ui.Fragility_bulding_1.clicked.connect(self.Fragility_b1)
        self.ui.Fragility_bulding_2.clicked.connect(self.Fragility_b2)
        self.ui.comparison_button.clicked.connect(self.fragility_comparison)
        self.ui.combined_curve_button.clicked.connect(self.fragility_combined)
        self.ui.refresh_dispersion_1.clicked.connect(self.dispersion_b1)
        self.ui.refresh_dispersion_2.clicked.connect(self.dispersion_b2)
        self.ui.PDFs_button_1.clicked.connect(self.pdfs_b1)
        self.ui.PDFs_button_2.clicked.connect(self.pdfs_b2)
        
        # Tabwidget Fragility of Taxonomies
        self.ui.start_calculations.clicked.connect(self.excel_generator_taxonomies)
        self.ui.Graph_tax_1.clicked.connect(self.graph_tax_T1)
        self.ui.Graph_DS_1.clicked.connect(self.graph_specific_DS_tax_T1)
        self.ui.Graph_tax_2.clicked.connect(self.graph_tax_T2)
        self.ui.Graph_DS_2.clicked.connect(self.graph_specific_DS_tax_T2)
        self.ui.Graph_comp_1.clicked.connect(self.graph_comp_typologies_T1)
        self.ui.Graph_comp_2.clicked.connect(self.graph_comp_typologies_T2)
        self.ui.Graph_mod_tax_1.clicked.connect(self.graph_mod_typologies_T1)
        self.ui.Graph_mod_tax_2.clicked.connect(self.graph_mod_typologies_T2)
        self.ui.Save_mod_tax_1.clicked.connect(self.save_change_T1)
        self.ui.Save_mod_tax_2.clicked.connect(self.save_change_T2)
        self.ui.Export_tax_mod_excel.clicked.connect(self.export_changes_to_excel)
        
        # Tabwidget Loss Components
        self.ui.CalcComp_1.clicked.connect(self.fragility_group_1)
        self.ui.CalcComp_2.clicked.connect(self.fragility_group_2)
        
        # Tabwidget Loss of Buildings
        self.ui.BuildingButton_Loss_1.clicked.connect(self.load_Building_1_Loss)
        self.ui.BuildingButton_Loss_2.clicked.connect(self.load_Building_2_Loss)
        self.ui.Element_activate_1.clicked.connect(self.elements_options_1)
        self.ui.Element_activate_2.clicked.connect(self.elements_options_2)
        self.ui.Graph_button_DVEDP_1.clicked.connect(self.loss_story_1)
        self.ui.Graph_button_DVEDP_2.clicked.connect(self.loss_story_2)
        self.ui.Graph_button_DVIM_1.clicked.connect(self.loss_DV_IM_1)
        self.ui.Graph_button_DVIM_2.clicked.connect(self.loss_DV_IM_2)
        self.ui.comparison_button_LossStory.clicked.connect(self.loss_story_comparison)
        
        #-----------------------------------------------------------------------------
        # Definición de los widgets de busqueda de archivos o carpetas
        
        # Tabwidget Fragility of Buildings
        self.button_1 = self.findChild(QPushButton, "HazardLevelButton_1")
        self.label_HzB1 = self.findChild(QLabel, "Hazard_text_1")
        self.button_2 = self.findChild(QPushButton, "HazardLevelButton_2")
        self.label_HzB2 = self.findChild(QLabel, "Hazard_text_2")
        self.button_3 = self.findChild(QPushButton, "EDPButton_1")
        self.label_EdpB1 = self.findChild(QLabel, "EDP_text_1")
        self.button_4 = self.findChild(QPushButton, "EDPButton_2")
        self.label_EdpB2 = self.findChild(QLabel, "EDP_text_2")
        
        # Tabwidget de Fragility of Taxonomies
        self.button_loadGuideData = self.findChild(QPushButton, "Load_Guide_Data")
        self.button_resultBuildingsFolder = self.findChild(QPushButton, "global_folder_button")
        self.button_location_file_result_tax = self.findChild(QPushButton, "excel_folder_button")
        self.button_load_excel_results_tax_to_graph = self.findChild(QPushButton, "Load_Excel_Tax")
        
        # Tabwidget Loss Components
        self.button_5 = self.findChild(QPushButton, "load_compGuide")

        #-----------------------------------------------------------------------------
        # Click los Dropdown Box
        
        # Tabwidget Fragility of Buildings
        self.button_1.clicked.connect(self.clicker_Hz_1)
        self.button_2.clicked.connect(self.clicker_Hz_2)
        self.button_3.clicked.connect(self.clicker_EDP_1)
        self.button_4.clicked.connect(self.clicker_EDP_2)
        
        # Tabwidget de Fragility of Taxonomies
        self.button_loadGuideData.clicked.connect(self.clicker_global_guide)
        self.button_resultBuildingsFolder.clicked.connect(self.clicker_resultBuildingsFolder)
        self.button_location_file_result_tax.clicked.connect(self.clicker_location_file_result)
        self.button_load_excel_results_tax_to_graph.clicked.connect(self.clicker_open_excel_results)
        
        # Tabwidget Loss Components
        self.button_5.clicked.connect(self.clicker_load_component_guide)

        
        
        # Show the APP
        #self.show()
#%%  CLICKERS  

###################################################################################
# FUNCIONES CLICKERS PARA APERTURA DE CARPETAS, ARCHIVOS Y GUARDADO DE DIRECCIONES
###################################################################################

    # ----------------------------------------------------------------------------
    # Explorador de archivos para excel general de edificaciones
    # ----------------------------------------------------------------------------
    def clicker_global_guide(self):
        global fname_guide_b, building_guide_original
        
        # ------------------------------------------------------------------------
        # Lectura de archivo general de edificaciones
        # ------------------------------------------------------------------------
        
        # Apertura de base de datos de edificaciones
        current_dir = os.getcwd()
        fname_guide_b = QFileDialog.getOpenFileName(self, "Open Excel Guide of Buildings", current_dir, "(*.xlsx *.xls)")
        fname_guide_b = fname_guide_b[0]
        
        # Hoja de Excel
        sheet_principal = 'Guide'
        
        # DataFrame con lista de edificaciones
        building_guide_original = pd.read_excel(fname_guide_b, sheet_name = sheet_principal)
        
        # ------------------------------------------------------------------------
        # Adicion de desplegable para seleccionar columna de taxonomias en la pestaña de Fragility of Taxonomies
        # ------------------------------------------------------------------------
        # Se llama a la matriz general donde estan todas las edificaciones y se guarda unicamente  
        # la data que tenga la columna de 'Included in Frag?' = 1
        
        # La matriz se limpia de los nan
        columnas_matriz_guia = building_guide_original.columns.tolist()
        columnas_matriz_guia = pd.Series(columnas_matriz_guia)
        columnas_matriz_guia = sorted(columnas_matriz_guia.dropna().tolist())
        
        # Adicion de desplegable de columnas disponibles
        try:
            self.ui.Group_Value.clear()
        except:
            pass
        
        self.ui.Group_Value.addItems(columnas_matriz_guia)
        
    # ----------------------------------------------------------------------------
    # Explorador de archivos para carpetas Hazard de la edificación 1
    # ----------------------------------------------------------------------------
    def clicker_Hz_1(self):
        global fname_HzB1
        
        fname_HzB1 = str(QFileDialog.getExistingDirectory(self, "Open Hazard Folder Building 1" ))
        NameFolder = os.path.basename(fname_HzB1)
        self.label_HzB1.setText(NameFolder)
            
    # ----------------------------------------------------------------------------
    # Explorador de archivos para carpetas Hazard de la edificación 2
    # ----------------------------------------------------------------------------
    def clicker_Hz_2(self):
        global fname_HzB2
        
        fname_HzB2 = str(QFileDialog.getExistingDirectory(self, "Open Hazard Folder Building 2" ))
        NameFolder = os.path.basename(fname_HzB2)
        self.label_HzB2.setText(NameFolder)
    
    # ----------------------------------------------------------------------------        
    # Explorador de archivos para carpetas de resultados de corridas de la edificación 1  
    # ----------------------------------------------------------------------------     
    def clicker_EDP_1(self):
        global fname_EdpB1, fname_HzB1
        
        fname_EdpB1 = str(QFileDialog.getExistingDirectory(self, "Open EDP Folder Building 1" ))
        NameFolder = os.path.basename(fname_EdpB1)
        self.label_EdpB1.setText(NameFolder)
        
        # ------------------------------------------------------------------------
        # Definición de numero de pisos para desplegable
        # ------------------------------------------------------------------------
        
        os.chdir(fname_EdpB1)
        current_file = glob.glob('*_SDR.txt*')
        n_story = pd.read_csv(current_file[0], sep = " ")
        
        try:
            self.ui.EDPType_ValueStory_1.clear()
        except:
            pass
        
        self.ui.EDPType_ValueStory_1.addItem("Max")
        for i in range (len(n_story.columns)):
            self.ui.EDPType_ValueStory_1.addItem(str(i+1))
        
        # ------------------------------------------------------------------------
        # Definición de carpeta de hazards cuando no se selecciona
        # ------------------------------------------------------------------------
        try:
            # Seleccion de CSS y Description Name asociado al edificio escogido
            ind = building_guide_original.loc[building_guide_original['Building Folder Name'] == NameFolder]
            CSS_name = ind['CSS'].tolist()[0]
            BuildingType = ind['Description Name'].tolist()[0]
            
            # Modificación de título para describir edificación
            title_g_1 = "BUILDING 1: " + BuildingType
            self.ui.label_curve1.setText(title_g_1)
            
            # Carpeta de Hz
            fname_HzB1 = os.path.join(os.path.dirname(os.path.dirname(fname_EdpB1)),CSS_name)
            self.ui.Hazard_text_1.setText(CSS_name)   
            
        except NameError:
            print('Error with the function that asign automatically CSS hazard')
            
    # ----------------------------------------------------------------------------       
    # Explorador de archivos para carpetas de resultados de corridas de la edificación 2
    # ----------------------------------------------------------------------------             
    def clicker_EDP_2(self):
        global fname_EdpB2, fname_HzB2
        
        fname_EdpB2 = str(QFileDialog.getExistingDirectory(self, "Open EDP Folder Building 2" ))
        NameFolder = os.path.basename(fname_EdpB2)
        self.label_EdpB2.setText(NameFolder)
        
        # ------------------------------------------------------------------------
        # Definición de numero de pisos para desplegable
        # ------------------------------------------------------------------------
        
        os.chdir(fname_EdpB2)
        current_file = glob.glob('*_SDR.txt*')
        n_story = pd.read_csv(current_file[0], sep = " ")
        
        try:
            self.ui.EDPType_ValueStory_2.clear()
        except:
            pass
        
        self.ui.EDPType_ValueStory_2.addItem("Max")
        for i in range (len(n_story.columns)):
            self.ui.EDPType_ValueStory_2.addItem(str(i+1))
            
        # ------------------------------------------------------------------------
        # Definición de carpeta de hazards cuando no se selecciona
        # ------------------------------------------------------------------------
        try:
            # Seleccion de CSS y Description Name asociado al edificio escogido
            ind = building_guide_original.loc[building_guide_original['Building Folder Name'] == NameFolder]
            CSS_name = ind['CSS'].tolist()[0]
            BuildingType = ind['Description Name'].tolist()[0]
            
            # Modificación de título para describir edificación
            title_g_2 = "BUILDING 2: " + BuildingType
            self.ui.label_curve2.setText(title_g_2)
            
            # Carpeta de Hz
            fname_HzB2 = os.path.join(os.path.dirname(os.path.dirname(fname_EdpB2)),CSS_name)
            self.ui.Hazard_text_2.setText(CSS_name)   
            
        except NameError:
            print('Error with the function that asign automatically CSS hazard')
    
    # ----------------------------------------------------------------------------
    # Explorador de archivos para abrir carpeta general donde estaran subcarpetas de grupos de resultados
    # ----------------------------------------------------------------------------
    def clicker_resultBuildingsFolder(self):
        global fname_resultsBuildings
        fname_resultsBuildings = str(QFileDialog.getExistingDirectory(self, "Open Global Folder"))
        
    # ----------------------------------------------------------------------------
    # Explorador de archivos para abrir carpeta donde se guarda excel resultado de taxonomias
    # ----------------------------------------------------------------------------
    def clicker_location_file_result(self):
        global fname_file_result
        fname_file_result = str(QFileDialog.getExistingDirectory(self, "Search Folder to Save File Result"))
        
    # ----------------------------------------------------------------------------
    # Explorador de archivos para abrir excel de resultados de taxonomia si no fue generado en la corrida actual
    # ----------------------------------------------------------------------------
    def clicker_open_excel_results(self):
        global fname_location_excel_tax, dict_data_IM_EDP_HzLv, dict_param_buildings, \
                dict_param_taxonomy, dict_points_fragility, separation_tax_name, dataF_excel_tax
        
        # Path del excel de resultados de taxonomías
        current_dir = os.getcwd()
        fname_location_excel_tax = QFileDialog.getOpenFileName(self, "Search Excel Result of Taxonomies", current_dir, "(*.xlsx *.xls)")
        fname_location_excel_tax = fname_location_excel_tax[0]
        
        # ------------------------------------------------------------------------
        # Lectura de archivo de excel que contiene los datos de la taxonomia para generacion de desplegables
        # ------------------------------------------------------------------------
        
        # DataFrame de resultados de taxonomias
        dataF_excel_tax = pd.read_excel(fname_location_excel_tax, sheet_name = 'Taxonomies')
        
        # Listas de interés
        IM_list = dataF_excel_tax['IM'].unique()
        T_list = dataF_excel_tax['T'].unique()
        taxonomy_list = dataF_excel_tax['Taxonomy'].unique()
        
        # ----------------------
        # IM del Excel
        # ----------------------
        try:
            self.ui.IMTax_value_1.clear()
            self.ui.IMTax_value_2.clear()
        except:
            pass
        
        self.ui.IMTax_value_1.addItems(IM_list)
        self.ui.IMTax_value_2.addItems(IM_list)
        
        # ----------------------
        # Periodos del Excel
        # ----------------------
        try:
            self.ui.PeriodoTax_value_1.clear()
            self.ui.PeriodoTax_value_2.clear()
        except:
            pass
        
        for current_T in T_list:
            self.ui.PeriodoTax_value_1.addItem(str(current_T))
            self.ui.PeriodoTax_value_2.addItem(str(current_T))
        
        # ----------------------
        # Taxonomias
        # ----------------------
        try:
            self.ui.TaxonomyTax_value_1.clear()
            self.ui.TaxonomyTax_value_2.clear()
        except:
            pass
        
        self.ui.TaxonomyTax_value_1.addItems(taxonomy_list)
        self.ui.TaxonomyTax_value_2.addItems(taxonomy_list)
            
        # ------------------------------------------------------------------------
        # Creacion de variables de diccionarios de taxonomias como lo hace la funcion excel_generator_taxonomies
        # ------------------------------------------------------------------------
        
        # Diccionarios donde se guarda la informacion de resultados
        dict_data_IM_EDP_HzLv = {}
        dict_param_buildings = {}
        dict_param_taxonomy = {}
        dict_points_fragility = {}
        
        # Loop de periodos de interés
        for current_T in T_list:
            
            # Diccionarios y DataFrames para current_T
            current_data_IM_EDP_HzLv = {}
            current_points_fragility = {}
            current_param_buildings = pd.DataFrame()
            current_param_taxonomy = pd.DataFrame()
            
            # Loop de taxonomias
            for current_tax in taxonomy_list:
                
                # ---------------------------
                # Para dict_IM_EDP_HzLv
                # ---------------------------
                
                # Con este diccionario leemos la data para graficar disperisones
                current_sheet_name = 'Disp - ' + current_tax.replace('/','-')
                data_aux = pd.read_excel(fname_location_excel_tax, sheet_name = current_sheet_name)
                data_aux = data_aux.loc[data_aux['T'] == current_T]
                current_data_IM_EDP_HzLv[current_tax] = data_aux
                
                # ---------------------------
                # Para dict_points_fragility
                # ---------------------------
                
                # Con este diccionario se tienen los puntos con los que se ajustan las curvas
                current_sheet_name = current_tax.replace('/','-')
                data_aux = pd.read_excel(fname_location_excel_tax, sheet_name = current_sheet_name)
                data_aux = data_aux.loc[data_aux['T'] == current_T]
                current_points_fragility[current_tax] = data_aux
                
            # Guardado de diccionarios de un periodo especifico
            dict_data_IM_EDP_HzLv[str(current_T)] = current_data_IM_EDP_HzLv
            dict_points_fragility[str(current_T)] = current_points_fragility
            
            # ---------------------------
            # Para dict_param_buildings
            # ---------------------------
            
            # Con este diccionario se pueden graficar las curvas de cualquier edificacion
            current_sheet_name = 'Buildings'
            data_aux = pd.read_excel(fname_location_excel_tax, sheet_name = current_sheet_name)
            data_aux = data_aux.loc[data_aux['T'] == current_T]
            dict_param_buildings[str(current_T)] = data_aux
            
            # ---------------------------
            # Para dict_param_taxonomy
            # ---------------------------
            
            # Con este diccionario se pueden graficar las curvas de cualquier taxonomia
            current_sheet_name = 'Taxonomies'
            data_aux = pd.read_excel(fname_location_excel_tax, sheet_name = current_sheet_name)
            data_aux = data_aux.loc[data_aux['T'] == current_T]
            dict_param_taxonomy[str(current_T)] = data_aux
            
        # ------------------------------------------------------------------------
        # Generacion de desplegables de estados de daños para graficas
        # ------------------------------------------------------------------------
        
        # Numero de estados de daño
        data_aux = dict_param_taxonomy[str(current_T)]
        num_ds = sum(cols.startswith('Theta') for cols in data_aux.columns)
        
        # Limpieza de desplegables de estados de daño
        try:
            self.ui.DS_graph_Value_1.clear()
        except:
            pass
        try:
            self.ui.DS_graph_Value_2.clear()
        except:
            pass
        try:
            self.ui.DS_graph_com_Value_1.clear()
        except:
            pass
        try:
            self.ui.DS_graph_com_Value_2.clear()
        except:
            pass
        
        # Adicion de estados de daño al desplegable
        for i in range(num_ds):
            self.ui.DS_graph_Value_1.addItem(str(i+1))
            self.ui.DS_graph_Value_2.addItem(str(i+1))
            self.ui.DS_graph_com_Value_1.addItem(str(i+1))
            self.ui.DS_graph_com_Value_2.addItem(str(i+1))
        
        # ------------------------------------------------------------------------
        # Nombre del excel cargado
        # ------------------------------------------------------------------------
        
        file_loaded_name = os.path.basename(fname_location_excel_tax)
        self.ui.excel_name_load.setText(file_loaded_name)
        
        # ------------------------------------------------------------------------
        # Generación de matriz de taxonomias separando componentes 
        # para generar en la funcion de graficas el Nivel de comparacion
        # ------------------------------------------------------------------------
        
        # Data Frame con nombres de taxonomias separadas
        separation_tax_name = pd.DataFrame()
        
        all_tax_list = pd.DataFrame()
        
        # Se buscan todas las taxonomias de cada IM porque puede que unas tengan otras que otros no
        for curr_key_dict in list(dict_param_taxonomy.keys()):
            all_tax_list = pd.concat([all_tax_list,dict_param_taxonomy[curr_key_dict]['Taxonomy']],axis = 0, ignore_index = True) 
        all_tax_list = all_tax_list[0].unique()
        
        separation_tax_name['Taxonomy'] = all_tax_list
        list_tax = separation_tax_name['Taxonomy'].unique()
        
        # Creacion de columnas de acuerdo con la cantidad de componentes
        num_taxs = len(separation_tax_name['Taxonomy'].unique()[0].split('/'))
        
        # Columnas a asignar
        cols_asignar = []
        
        # Creación de columna de taxonomia sin numero de pisos
        separation_tax_name['Tax_No_stories'] = None
        
        # Llenado de las columnas separando los componentes de la cadena
        for i in range(num_taxs):
            # Crea columnas por cada componente separado
            separation_tax_name['C'+str(i+1)] = None
            
            # Agrega a la lista los nombres de las columnas creadas
            cols_asignar.append('C'+str(i+1))
            
        # Llenado de columna de cadena sin numero de piso
        for i in range (len(list_tax)):
            current_tax = list_tax[i]
            components_tax = current_tax.split('/')
            separation_tax_name.loc[i, cols_asignar] = components_tax
            
            # Nombre de taxonomia sin el ultimo dato de la cadena, es decir, el piso
            tax_no_s = components_tax[0]
            for j in range(1, num_taxs-1):
                tax_no_s = tax_no_s + '/' + str(components_tax[j])
            
            # Guardado de la taxonomía sin piso
            separation_tax_name.at[i,'Tax_No_stories'] = tax_no_s
        
    # ----------------------------------------------------------------------------
    # Explorador de archivos para cargar archivo excel de componentes
    # ----------------------------------------------------------------------------
    def clicker_load_component_guide(self):
        global fname_compGuide, guide_component
        
        # Path de excel de componentes
        current_dir = os.getcwd()
        fname_compGuide = QFileDialog.getOpenFileName(self, "Open Component File", current_dir, "All Files (*)")
        fname_compGuide = fname_compGuide[0]
        
        # Hoja de Excel
        sheet_principal = 'Guide'
        
        # DataFrame con hoja principal de los componentes disponibles
        guide_component = pd.read_excel(fname_compGuide, sheet_name = sheet_principal)
        
        # ------------------------------------------------------------------------
        # Definición de componentes para desplegable dentro del Tab Components
        # ------------------------------------------------------------------------
        
        # Fragility Group 1
        try:
            self.ui.fragilityGroup_Value_1.clear()
        except:
            pass
        
        self.ui.fragilityGroup_Value_1.addItems(guide_component['Fragility Group'])
        
        # Fragility Group 2
        try:
            self.ui.fragilityGroup_Value_2.clear()
        except:
            pass
        self.ui.fragilityGroup_Value_2.addItems(guide_component['Fragility Group'])
    
#%% 

###################################################################################
# FUNCIONES PARA BOTONES DEL TABWIDGET DE FRAGILITY OF BUILDINGS
###################################################################################   
 
#%% FUNCIÓN DE LECTURA DE DATOS DE LA EDIFICACION 1

    def read_input_data_b1(self):
        global timeOK_E1,EDP_limit_E1, T_E1, IM_name_graph_E1, EDP_method_E1, EDP_name_graph_E1, story_E1, EDP_cens_E1, \
            Hzlv_curves_E1, j_E1, thetas_DS_E1, betas_DS_E1, EDP_collapse_E1, ds_tags_E1, porc_curves_E1, \
            tipo_bin_E1, include_cens_E1, collapse_method_E1, min_datos_bin_E1, num_bins_inicial_E1, IM_max_graph_E1, \
            IM_delta_graph_E1, num_DS_E1
        
        # --------------------------
        # Test
        # --------------------------
        
        # Tiempo de limite de evaluacion
        timeOK_E1 = float(self.ui.tmin_value_1.text())
        
        # Lectura del EDP límite
        EDP_limit_E1 = float(self.ui.EDP_value_1.text()) # Esto no será necesariamiento SDR, sino el EDP seleccionado
        
        # --------------------------
        # IM and EDP definition
        # --------------------------
        
        # Periodo
        T_E1 = np.round(float(self.ui.periodo_value_1.text()),2)
        
        # IM
        IM_name_graph_E1 = self.ui.IMType_Value_1.currentText()

        # EDP de interés
        EDP_name_graph_E1 = self.ui.EDPType_Value_1.currentText()
        
        story_E1 = "S"+self.ui.EDPType_ValueStory_1.currentText()
        if story_E1 == "SMax":
            story_E1 = "max"
        
        # Valor de EDP de censura
        EDP_cens_E1 = float(self.ui.EDPcens_value_1.text())
        
        # Hazard Levels
        Hzlv_curves_E1 = self.ui.hazard_value_1.text()
        Hzlv_curves_E1 = np.asarray(Hzlv_curves_E1.split(",")).astype(int)
        
        # --------------------------
        # Fragility Parameters
        # --------------------------
        
        # Thresholds de excedencia estructrual (SEC)
        j_E1 = self.ui.j_value_1.text()
        j_E1 = np.asarray(j_E1.split(",")).astype(float)
        
        # Thetas de curvas de fragilidad DS vs EDP
        thetas_DS_E1 = self.ui.theta_value_1.text()
        thetas_DS_E1 = np.asarray(thetas_DS_E1.split(",")).astype(float)
        
        # Betas o sigmas de curvas de fragilidad DS vs EDP
        betas_DS_E1 = self.ui.sigma_value_1.text()
        betas_DS_E1 = np.asarray(betas_DS_E1.split(",")).astype(float)
        
        # Valor de EDP de colapso
        EDP_collapse_E1 = float(self.ui.EDPCollapse_value_1.text())
        
        # Tags de curvas de fragilidad DS vs EDP
        ds_tags_E1 = self.ui.DSTags_value_1.text()
        ds_tags_E1 = ds_tags_E1.split(",")
        
        # Porcentajes de ajustes de curvas
        porc_curves_E1 = self.ui.porc_fit_curves_1.text()
        porc_curves_E1 = np.asarray(porc_curves_E1.split(",")).astype(float)
        
        # Tipo de bineado
        tipo_bin_E1 = self.ui.Bintype_1.currentText()
        if tipo_bin_E1 == "Linespace":
            tipo_bin_E1 = 1
        elif tipo_bin_E1 == "Logspace":
            tipo_bin_E1 = 2
            
        # Inclusión de censura en la bineo de fragilidad (OJO: No de excedencia)
        include_cens_E1 = self.ui.includeCens_1.currentText()
        if include_cens_E1 == "Yes":
            include_cens_E1 = 1
        elif include_cens_E1 == "No":
            include_cens_E1 = 0
            
        # Definición de metodologia de colapso para fragilidad
        collapse_method_E1 = self.ui.collapseMethod_1.currentText()
        
        # Número mínimo de datos por bin y número inicial de bines
        min_datos_bin_E1 = int(self.ui.binminvalue_1.text())
        num_bins_inicial_E1 = int(self.ui.bininitialvalue_1.text())
        
        # IM maximo de gráficos, las curvas de fragilidad se estimaran hasta este valor
        IM_max_graph_E1 = 10
        
        # Delta de graficos, las curvas de fragilidad se calcularan cada valor delta
        IM_delta_graph_E1 = 0.001
        
        # Cantidad de estados de daño considerados
        if collapse_method_E1 == 'fit':
            num_DS_E1 = len(thetas_DS_E1)
        elif collapse_method_E1 == 'count' or collapse_method_E1 =='count columns':
            num_DS_E1 = len(thetas_DS_E1)+1
            
#%% FUNCIÓN DE LECTURA DE DATOS DE LA EDIFICACION 2

    def read_input_data_b2(self):
        global timeOK_E2,EDP_limit_E2, T_E2, IM_name_graph_E2, EDP_method_E2, EDP_name_graph_E2, story_E2, EDP_cens_E2, \
            Hzlv_curves_E2, j_E2, thetas_DS_E2, betas_DS_E2, EDP_collapse_E2, ds_tags_E2, porc_curves_E2, \
            tipo_bin_E2, include_cens_E2, collapse_method_E2, min_datos_bin_E2, num_bins_inicial_E2, IM_max_graph_E2, \
            IM_delta_graph_E2, num_DS_E2
        
        # --------------------------
        # Test
        # --------------------------
        
        # Tiempo de limite de evaluacion
        timeOK_E2 = float(self.ui.tmin_value_2.text())
        
        # Lectura del EDP límite
        EDP_limit_E2 = float(self.ui.EDP_value_2.text()) # Esto no será necesariamiento SDR, sino el EDP seleccionado
        
        # --------------------------
        # IM and EDP definition
        # --------------------------
        
        # Periodo
        T_E2 = np.round(float(self.ui.periodo_value_2.text()),2)
        
        # IM
        IM_name_graph_E2 = self.ui.IMType_Value_2.currentText()

        # EDP de interés
        EDP_name_graph_E2 = self.ui.EDPType_Value_2.currentText()
        
        story_E2 = "S"+self.ui.EDPType_ValueStory_2.currentText()
        if story_E2 == "SMax":
            story_E2 = "max"
        
        # Valor de EDP de censura
        EDP_cens_E2 = float(self.ui.EDPcens_value_2.text())
        
        # Hazard Levels
        Hzlv_curves_E2 = self.ui.hazard_value_2.text()
        Hzlv_curves_E2 = np.asarray(Hzlv_curves_E2.split(",")).astype(int)
        
        # --------------------------
        # Fragility Parameters
        # --------------------------
        
        # Thresholds de excedencia estructrual (SEC)
        j_E2 = self.ui.j_value_2.text()
        j_E2 = np.asarray(j_E2.split(",")).astype(float)
        
        # Thetas de curvas de fragilidad DS vs EDP
        thetas_DS_E2 = self.ui.theta_value_2.text()
        thetas_DS_E2 = np.asarray(thetas_DS_E2.split(",")).astype(float)
        
        # Betas o sigmas de curvas de fragilidad DS vs EDP
        betas_DS_E2 = self.ui.sigma_value_2.text()
        betas_DS_E2 = np.asarray(betas_DS_E2.split(",")).astype(float)
        
        # Valor de EDP de colapso
        EDP_collapse_E2 = float(self.ui.EDPCollapse_value_2.text())
        
        # Tags de curvas de fragilidad DS vs EDP
        ds_tags_E2 = self.ui.DSTags_value_2.text()
        ds_tags_E2 = ds_tags_E2.split(",")
        
        # Porcentajes de ajustes de curvas
        porc_curves_E2 = self.ui.porc_fit_curves_2.text()
        porc_curves_E2 = np.asarray(porc_curves_E2.split(",")).astype(float)
        
        # Tipo de bineado
        tipo_bin_E2 = self.ui.Bintype_2.currentText()
        if tipo_bin_E2 == "Linespace":
            tipo_bin_E2 = 1
        elif tipo_bin_E2 == "Logspace":
            tipo_bin_E2 = 2
            
        # Inclusión de censura en la bineo de fragilidad (OJO: No de excedencia)
        include_cens_E2 = self.ui.includeCens_2.currentText()
        if include_cens_E2 == "Yes":
            include_cens_E2 = 1
        elif include_cens_E2 == "No":
            include_cens_E2 = 0
            
        # Definición de metodologia de colapso para fragilidad
        collapse_method_E2 = self.ui.collapseMethod_2.currentText()
        
        # Número mínimo de datos por bin y número inicial de bines
        min_datos_bin_E2 = int(self.ui.binminvalue_2.text())
        num_bins_inicial_E2 = int(self.ui.bininitialvalue_2.text())
        
        # IM maximo de gráficos, las curvas de fragilidad se estimaran hasta este valor
        IM_max_graph_E2 = 10
        
        # Delta de graficos, las curvas de fragilidad se calcularan cada valor delta
        IM_delta_graph_E2 = 0.001
        
        # Cantidad de estados de daño considerados
        if collapse_method_E2 == 'fit':
            num_DS_E2 = len(thetas_DS_E2)
        elif collapse_method_E2 == 'count' or collapse_method_E2 =='count columns':
            num_DS_E2 = len(thetas_DS_E2)+1        

#%% # FUNCIÓN PARA GRAFICAR DISPERSIÓN DEL EDIFICIO 1
    # ---------------------------------------------------------------------------- 

    def dispersion_b1(self):
        global dict_all_EDPs_E1, dict_EDPs_Original_E1, IM_curva_E1, EDP_curva_E1
        
        print('New run of dispersion of SEC building 1')
        
        ######################################################################  
        # CARGAR DATOS DE ENTRADA
        
        self.read_input_data_b1()
        
        ######################################################################  
        # LECTURA DE DATOS
        
        [Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, Hazard_All_E1] = RSP_total(fname_HzB1)
        dict_all_EDPs_E1 = lectura_EDPs(fname_EdpB1, Hazard_All_E1)
        test_E1 = testRun(fname_EdpB1, timeOK_E1, EDP_limit_E1, EDP_name_graph_E1, dict_all_EDPs_E1)
        [Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, dict_all_EDPs_E1] = correccion_test (Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, dict_all_EDPs_E1, test_E1)
        
        ######################################################################  
        # DATOS PARA CONSTRUCCIÓN DE CURVAS
        
        # Se define si es Sa o SaAVG
        if IM_name_graph_E1 == "Sa":
            IM_data_E1 = Sa_All_HzLVLs_E1
        elif IM_name_graph_E1 == "SaAVG":
            IM_data_E1 = SaAVG_All_HzLVLs_E1
        
        # Se define el EDP de interés
        EDP_data_E1 = dict_all_EDPs_E1[EDP_name_graph_E1]
        
        # Se filtra el IM y el EDP de interés
        IM_curva_E1 = lista_IM(T_E1, Hzlv_curves_E1, IM_data_E1)
        EDP_curva_E1 = lista_EDP(story_E1, Hzlv_curves_E1, EDP_data_E1)
        
        # Diccionario de IM y EDPS originales (será usado en código de pérdidas)
        dict_EDPs_Original_E1 = {}
        dict_EDPs_Original_E1['IM'] = IM_data_E1
        dict_EDPs_Original_E1['SDR'] = dict_all_EDPs_E1['SDR']
        try:
            dict_EDPs_Original_E1['RSDR'] = dict_all_EDPs_E1['RSDR']
        except:
            pass
        dict_EDPs_Original_E1['PFA'] = dict_all_EDPs_E1['PFA']

        ######################################################################  
        # GRAFICAS
        
        try:
            self.grafica_dispersion_1.close()
        except AttributeError:
            pass
            
        self.grafica_dispersion_1 = Canvas_grafica()      
        self.grafica_dispersion_1.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E1 = Hzlv_curves_E1.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E1)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico
        for HL in Hzlv_curves_E1:
            IM_aux = IM_curva_E1[IM_curva_E1['Hz Lv']==HL][T_E1]
            EDP_aux = EDP_curva_E1[EDP_curva_E1['Hz Lv']==HL][story_E1]
            self.grafica_dispersion_1.ax.loglog(IM_aux, EDP_aux, marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        self.grafica_dispersion_1.ax.set_xlim(0.01, 10)        
        if EDP_name_graph_E1 == "PFA":
            self.grafica_dispersion_1.ax.set_ylim(0, 200)
        else:
            self.grafica_dispersion_1.ax.set_ylim(0.0001, 100)
            
        self.grafica_dispersion_1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's) [g]', size = 10)
        self.grafica_dispersion_1.ax.set_ylabel(EDP_name_graph_E1 + r'$_{'+story_E1+'}$', size = 10)
        self.grafica_dispersion_1.ax.grid(which="both", alpha = 0.5)
        self.grafica_dispersion_1.ax.legend(fontsize=7)

        self.ui.Dispersion_B1.addWidget(self.grafica_dispersion_1)
        
        ###################################################################### 
        # CIERRE DE GRAFICAS
        
        # Curvas de pdfs
        try:
            self.grafica_pdf_1.close()
        except AttributeError:
            pass
        
        # Curvas de comparación
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        # Curvas de combinacion
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
  
#%% # FUNCIÓN PARA GRAFICAR DISPERSIÓN DEL EDIFICIO 2
    # ---------------------------------------------------------------------------- 
    
    def dispersion_b2(self):
        global dict_all_EDPs_E2, dict_EDPs_Original_E2, IM_curva_E2, EDP_curva_E2
        
        print('New run of dispersion of SEC building 2')
        
        ######################################################################  
        # CARGAR DATOS DE ENTRADA
        
        self.read_input_data_b2()
        
        ######################################################################  
        # LECTURA DE DATOS
        
        [Sa_All_HzLVLs_E2, SaAVG_All_HzLVLs_E2, Hazard_All_E2] = RSP_total(fname_HzB2)
        dict_all_EDPs_E2 = lectura_EDPs(fname_EdpB2, Hazard_All_E2)
        test_E2 = testRun(fname_EdpB2, timeOK_E2, EDP_limit_E2, EDP_name_graph_E2, dict_all_EDPs_E2)
        [Sa_All_HzLVLs_E2, SaAVG_All_HzLVLs_E2, dict_all_EDPs_E2] = correccion_test (Sa_All_HzLVLs_E2, SaAVG_All_HzLVLs_E2, dict_all_EDPs_E2, test_E2)
        
        ######################################################################  
        # DATOS PARA CONSTRUCCIÓN DE CURVAS
        
        # Se define si es Sa o SaAVG
        if IM_name_graph_E2 == "Sa":
            IM_data_E2 = Sa_All_HzLVLs_E2
        elif IM_name_graph_E2 == "SaAVG":
            IM_data_E2 = SaAVG_All_HzLVLs_E2
        
        # Se define el EDP de interés
        EDP_data_E2 = dict_all_EDPs_E2[EDP_name_graph_E2]
        
        # Se filtra el IM y el EDP de interés
        IM_curva_E2 = lista_IM(T_E2, Hzlv_curves_E2, IM_data_E2)
        EDP_curva_E2 = lista_EDP(story_E2, Hzlv_curves_E2, EDP_data_E2)
        
        # Diccionario de IM y EDPS originales (será usado en código de pérdidas)
        dict_EDPs_Original_E2 = {}
        dict_EDPs_Original_E2['IM'] = IM_data_E2
        dict_EDPs_Original_E2['SDR'] = dict_all_EDPs_E2['SDR']
        try:
            dict_EDPs_Original_E2['RSDR'] = dict_all_EDPs_E2['RSDR']
        except:
            pass
        dict_EDPs_Original_E2['PFA'] = dict_all_EDPs_E2['PFA']

        ######################################################################  
        # GRAFICAS
        
        try:
            self.grafica_dispersion_2.close()
        except AttributeError:
            pass
            
        self.grafica_dispersion_2 = Canvas_grafica()      
        self.grafica_dispersion_2.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E2 = Hzlv_curves_E2.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E2)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico
        for HL in Hzlv_curves_E2:
            IM_aux = IM_curva_E2[IM_curva_E2['Hz Lv']==HL][T_E2]
            EDP_aux = EDP_curva_E2[EDP_curva_E2['Hz Lv']==HL][story_E2]
            self.grafica_dispersion_2.ax.loglog(IM_aux, EDP_aux, marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        self.grafica_dispersion_2.ax.set_xlim(0.01, 10)        
        if EDP_name_graph_E2 == "PFA":
            self.grafica_dispersion_2.ax.set_ylim(0, 200)
        else:
            self.grafica_dispersion_2.ax.set_ylim(0.0001, 100)
            
        self.grafica_dispersion_2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's) [g]', size = 10)
        self.grafica_dispersion_2.ax.set_ylabel(EDP_name_graph_E2 + r'$_{'+story_E2+'}$', size = 10)
        self.grafica_dispersion_2.ax.grid(which="both", alpha = 0.5)
        self.grafica_dispersion_2.ax.legend(fontsize=7)

        self.ui.Dispersion_B2.addWidget(self.grafica_dispersion_2)
        
        ###################################################################### 
        # CIERRE DE GRAFICAS
        
        # Curvas de pdfs
        try:
            self.grafica_pdf_2.close()
        except AttributeError:
            pass
        
        # Curvas de comparación
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        # Curvas de combinacion
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
   
#%% # FUNCIÓN PARA GRAFICAR CURVAS DE EXCEDENCIA DE EDIFICACIÓN 1      
    # ----------------------------------------------------------------------------
    def SEC_b1(self):
        global parameters_D_E1, matriz_plot_D_E1, fragility_D_E1, matriz_IM_EDP_D_E1, dataF_IM_EDP_Hz_E1
        
        print('New run of SEC building 1')
        
        ######################################################################  
        # CARGAR DATOS Y CORRER DISPERSION
        
        self.dispersion_b1()
        
        ######################################################################  
        # GENERACIÓN DE DATOS PARA CURVAS DE EXCEDENCIA
        
        # Definición de DataFrame de entrada para curvas de la forma: IM - EDP - HzL
        dataF_IM_EDP_Hz_E1 = pd.DataFrame()
        dataF_IM_EDP_Hz_E1['IM'] = IM_curva_E1[T_E1]
        dataF_IM_EDP_Hz_E1['EDP'] = EDP_curva_E1[story_E1]
        dataF_IM_EDP_Hz_E1['Hz Lv'] = IM_curva_E1['Hz Lv']
        
        # Generación de parámetros
        [parameters_D_E1, matriz_plot_D_E1, fragility_D_E1, matriz_IM_EDP_D_E1] = fragility_function_det(dataF_IM_EDP_Hz_E1, j_E1, tipo_bin_E1, min_datos_bin_E1, 
                                                                                                         num_bins_inicial_E1, IM_max_graph_E1, IM_delta_graph_E1)
        
        ######################################################################  
        # GRAFICAS DE BINEADO CON DATA DE EXCEDENCIA ESTRUCTURAL
        
        try:
            self.grafica_bineado_DET_1.close()
        except AttributeError:
            pass
        
        self.grafica_bineado_DET_1 = Canvas_grafica()      
        self.grafica_bineado_DET_1.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E1 = Hzlv_curves_E1.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E1)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico   
        for HL in Hzlv_curves_E1:
            IM_aux = matriz_IM_EDP_D_E1.loc[matriz_IM_EDP_D_E1['Hz Lv']==HL]['IM_bin']
            EDP_aux = matriz_IM_EDP_D_E1.loc[matriz_IM_EDP_D_E1['Hz Lv']==HL]['EDP']
  
            self.grafica_bineado_DET_1.ax.loglog(IM_aux, EDP_aux, marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        if EDP_name_graph_E1 == "PFA":
            self.grafica_bineado_DET_1.ax.set_ylim(0.5, 200)
        else:
            self.grafica_bineado_DET_1.ax.set_ylim(0.0001, 100)
        
        self.grafica_bineado_DET_1.ax.set_xlim(0.01,10)
        self.grafica_bineado_DET_1.ax.set_yscale("log")
        self.grafica_bineado_DET_1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's) [g]', size = 10)
        self.grafica_bineado_DET_1.ax.set_ylabel(EDP_name_graph_E1 + r'$_{'+story_E1+'}$', size = 10)
        self.grafica_bineado_DET_1.ax.grid(which="both", alpha = 0.5)
        self.grafica_bineado_DET_1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.BinD_1.addWidget(self.grafica_bineado_DET_1)
        
        ######################################################################   
        # GRAFICAS DE CURVAS DE EXCEDENCIA ESTRUCTURAL
                
        try:
            self.grafica_SEOC_DET_1.close()
        except AttributeError:
            pass
                
        self.grafica_SEOC_DET_1 = Canvas_grafica()      
        self.grafica_SEOC_DET_1.ax.clear()
        
        if EDP_name_graph_E1 == "PFA":
            for i in range (len(j_E1)):
                
                # Curvas
                self.grafica_SEOC_DET_1.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i], linestyle = '-', 
                          label = 'j =' + str(round(j_E1[i],2)) + ' - ' + r"$\theta$" +' = ' + str(round(parameters_D_E1.at[i,'theta'],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_D_E1.at[i,'sigma'],3)))
                
                # Puntos de ajuste
                self.grafica_SEOC_DET_1.ax.plot(fragility_D_E1['IM_bin'], fragility_D_E1['Zi - j = ' + str(j_E1[i])]/fragility_D_E1['N'], color = color[i], 
                          marker = 'o', linestyle='', markersize = 3)
        else:
            for i in range (len(j_E1)):
                # Curvas
                self.grafica_SEOC_DET_1.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i], linestyle = '-',  
                          label = 'j =' + str(round(j_E1[i]*100,2)) + '% - ' + r"$\theta$" +' = ' + str(round(parameters_D_E1.at[i,'theta'],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_D_E1.at[i,'sigma'],3)))
                
                # Puntos de ajuste
                self.grafica_SEOC_DET_1.ax.plot(fragility_D_E1['IM_bin'], fragility_D_E1['Zi - j = ' + str(j_E1[i])]/fragility_D_E1['N'], color = color[i], 
                          marker = 'o', linestyle='', markersize = 3)
                       
        self.grafica_SEOC_DET_1.ax.set_xlim(0, 2.5)
        self.grafica_SEOC_DET_1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)  [g]', size = 10)
        self.grafica_SEOC_DET_1.ax.set_ylabel('P(' + EDP_name_graph_E1 + r'$_{'+story_E1+'}$' + ' ' +'> j)', size = 10)
        self.grafica_SEOC_DET_1.ax.grid(which="both")
        self.grafica_SEOC_DET_1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_fragilityD_1.addWidget(self.grafica_SEOC_DET_1)
        
        ######################################################################  
        # CIERRE DE GRAFICAS
        
        # Curvas de pdfs
        try:
            self.grafica_pdf_2.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
        
#%% # FUNCIÓN PARA GRAFICAR CURVAS DE EXCEDENCIA DE EDIFICACIÓN 2
    # ----------------------------------------------------------------------------
    def SEC_b2(self):
        global parameters_D_E2, matriz_plot_D_E2, fragility_D_E2, matriz_IM_EDP_D_E2, dataF_IM_EDP_Hz_E2
        
        print('New run of SEC building 2')
        
        ######################################################################  
        # CARGAR DATOS Y CORRER DISPERSION
        
        self.dispersion_b2()
        
        ######################################################################  
        # GENERACIÓN DE DATOS PARA CURVAS DE EXCEDENCIA
        
        # Definición de DataFrame de entrada para curvas de la forma: IM - EDP - HzL
        dataF_IM_EDP_Hz_E2 = pd.DataFrame()
        dataF_IM_EDP_Hz_E2['IM'] = IM_curva_E2[T_E2]
        dataF_IM_EDP_Hz_E2['EDP'] = EDP_curva_E2[story_E2]
        dataF_IM_EDP_Hz_E2['Hz Lv'] = IM_curva_E2['Hz Lv']
        
        # Generación de parámetros
        [parameters_D_E2, matriz_plot_D_E2, fragility_D_E2, matriz_IM_EDP_D_E2] = fragility_function_det(dataF_IM_EDP_Hz_E2, j_E2, tipo_bin_E2, min_datos_bin_E2, 
                                                                                                         num_bins_inicial_E2, IM_max_graph_E2, IM_delta_graph_E2)
        
        ######################################################################  
        # GRAFICAS DE BINEADO CON DATA DE EXCEDENCIA ESTRUCTURAL
        
        try:
            self.grafica_bineado_DET_2.close()
        except AttributeError:
            pass
        
        self.grafica_bineado_DET_2 = Canvas_grafica()      
        self.grafica_bineado_DET_2.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E2 = Hzlv_curves_E2.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E2)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico   
        for HL in Hzlv_curves_E2:
            IM_aux = matriz_IM_EDP_D_E2.loc[matriz_IM_EDP_D_E2['Hz Lv']==HL]['IM_bin']
            EDP_aux = matriz_IM_EDP_D_E2.loc[matriz_IM_EDP_D_E2['Hz Lv']==HL]['EDP']
  
            self.grafica_bineado_DET_2.ax.loglog(IM_aux, EDP_aux, marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        if EDP_name_graph_E2 == "PFA":
            self.grafica_bineado_DET_2.ax.set_ylim(0.5, 200)
        elif EDP_name_graph_E2 == "SDR" or EDP_name_graph_E2 == "RSDR":
            self.grafica_bineado_DET_2.ax.set_ylim(0.0001, 100)
        
        self.grafica_bineado_DET_2.ax.set_xlim(0.01,10)
        self.grafica_bineado_DET_2.ax.set_yscale("log")
        self.grafica_bineado_DET_2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)  [g]', size = 10)
        self.grafica_bineado_DET_2.ax.set_ylabel(EDP_name_graph_E2 + r'$_{'+story_E2+'}$', size = 10)
        self.grafica_bineado_DET_2.ax.grid(which="both", alpha = 0.5)
        self.grafica_bineado_DET_2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.BinD_2.addWidget(self.grafica_bineado_DET_2)
        
        ######################################################################   
        # GRAFICAS DE CURVAS DE EXCEDENCIA ESTRUCTURAL
                
        try:
            self.grafica_SEOC_DET_2.close()
        except AttributeError:
            pass
                
        self.grafica_SEOC_DET_2 = Canvas_grafica()      
        self.grafica_SEOC_DET_2.ax.clear()
        
        if EDP_name_graph_E2 == "PFA":
            for i in range (len(j_E2)):
                
                # Curvas
                self.grafica_SEOC_DET_2.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = '--', 
                          label = 'j =' + str(round(j_E2[i],2)) + ' - ' + r"$\theta$" +' = ' + str(round(parameters_D_E2.at[i,'theta'],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_D_E2.at[i,'sigma'],3)))
                
                # Puntos de ajuste
                self.grafica_SEOC_DET_2.ax.plot(fragility_D_E2['IM_bin'], fragility_D_E2['Zi - j = ' + str(j_E2[i])]/fragility_D_E2['N'], color = color[i], 
                          marker = '^', linestyle='', markersize = 3)
        else:
            for i in range (len(j_E2)):
                # Curvas
                self.grafica_SEOC_DET_2.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = '--',  
                          label = 'j =' + str(round(j_E2[i]*100,2)) + '% - ' + r"$\theta$" +' = ' + str(round(parameters_D_E2.at[i,'theta'],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_D_E2.at[i,'sigma'],3)))
                
                # Puntos de ajuste
                self.grafica_SEOC_DET_2.ax.plot(fragility_D_E2['IM_bin'], fragility_D_E2['Zi - j = ' + str(j_E2[i])]/fragility_D_E2['N'], color = color[i], 
                          marker = '^', linestyle='', markersize = 3)
                       
        self.grafica_SEOC_DET_2.ax.set_xlim(0, 2.5)
        self.grafica_SEOC_DET_2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)  [g]', size = 10)
        self.grafica_SEOC_DET_2.ax.set_ylabel('P(' + EDP_name_graph_E2 + r'$_{'+story_E2+'}$' + ' ' +'> j)', size = 10)
        self.grafica_SEOC_DET_2.ax.grid(which="both")
        self.grafica_SEOC_DET_2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_fragilityD_2.addWidget(self.grafica_SEOC_DET_2)
        
        ######################################################################  
        # CIERRE DE GRAFICAS
        
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
    
    
#%% # FUNCIÓN PARA GRAFICAR CURVAS DE FRAGILIDAD DE EDIFICACIÓN 1        
    # ---------------------------------------------------------------------------- 

    def Fragility_b1(self):
        global parameters_P_E1, matriz_plot_P_E1, fragility_P_E1, matriz_IM_EDP_P_E1, dataF_IM_EDP_Hz_E1, \
        dict_count_colap_E1, count_colap_columns_E1
        
        print('New run of Fragility building 1')
        
        ######################################################################  
        # CARGAR DATOS Y CORRER DISPERSION
        
        self.dispersion_b1()
        
        ###################################################################### 
        # GENERACIÓN DE CURVAS DE FRAGILIDAD
        
        # Definición de DataFrame de entrada para curvas de la forma: IM - EDP - HzL
        dataF_IM_EDP_Hz_E1 = pd.DataFrame()
        dataF_IM_EDP_Hz_E1['IM'] = IM_curva_E1[T_E1]
        dataF_IM_EDP_Hz_E1['EDP'] = EDP_curva_E1[story_E1]
        dataF_IM_EDP_Hz_E1['Hz Lv'] = IM_curva_E1['Hz Lv']
                  
        # Definición de delta y edp_max
        d_edp = delta_max_edp[EDP_name_graph_E1]['d_edp']
        edp_max = delta_max_edp[EDP_name_graph_E1]['edp_max']
        
        # Intenta crear una data frame para el conteo de columnas cuando sea el caso, si no lo encuentra lo crea vacío
        if collapse_method_E1 =='count columns':
            count_colap_columns_E1 = input_colum_count(fname_HzB1, fname_EdpB1, T_E1, IM_name_graph_E1, EDP_name_graph_E1, story_E1, EDP_collapse_E1, timeOK_E1, SDR_limit_E1)
            count_colap_columns_E1 = count_colap_columns_E1.loc[count_colap_columns_E1['Hz Lv'].isin(Hzlv_curves_E1)]
        else:
            count_colap_columns_E1 = {}
        
        # Generación de parámetros
        [parameters_P_E1, matriz_plot_P_E1, fragility_P_E1, matriz_IM_EDP_P_E1] = fragility_function_prob_collapseOptions(dataF_IM_EDP_Hz_E1, EDP_cens_E1, thetas_DS_E1, betas_DS_E1, tipo_bin_E1, min_datos_bin_E1, 
                                                                                                                              num_bins_inicial_E1, IM_max_graph_E1, d_edp, edp_max, include_cens_E1, porc_curves_E1,
                                                                                                                              collapse_method_E1, EDP_collapse_E1, IM_delta_graph_E1, count_colap_columns_E1)
        ######################################################################  
        # GRAFICAS DE BINEADO CON DATA DE CURVAS DE FRAGILIDAD
        
        try:
            self.grafica_bineado_PROB_1.close()
        except AttributeError:
            pass
        
        self.grafica_bineado_PROB_1 = Canvas_grafica()      
        self.grafica_bineado_PROB_1.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E1 = Hzlv_curves_E1.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E1)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
            
        # Gráfico   
        for HL in Hzlv_curves_E1:
            IM_aux = matriz_IM_EDP_P_E1.loc[matriz_IM_EDP_P_E1['Hz Lv']==HL]['IM_bin']
            EDP_aux = matriz_IM_EDP_P_E1.loc[matriz_IM_EDP_P_E1['Hz Lv']==HL]['EDP']
            
            self.grafica_bineado_PROB_1.ax.loglog(IM_aux, EDP_aux , marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        if EDP_name_graph_E1 == "PFA":
            self.grafica_bineado_PROB_1.ax.set_ylim(0.5, 200)
        else:
            self.grafica_bineado_PROB_1.ax.set_ylim(0.0001, 100)

        self.grafica_bineado_PROB_1.ax.set_xlim(0.01,10)
        self.grafica_bineado_PROB_1.ax.set_yscale("log")
        self.grafica_bineado_PROB_1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's) [g]', size = 10)
        self.grafica_bineado_PROB_1.ax.set_ylabel(EDP_name_graph_E1 + r'$_{'+story_E1+'}$', size = 10)
        self.grafica_bineado_PROB_1.ax.legend(fontsize=7, loc = 'best')
        self.grafica_bineado_PROB_1.ax.grid(which="both", alpha = 0.5)
        
        self.ui.BinP_1.addWidget(self.grafica_bineado_PROB_1)
        
        ######################################################################   
        # GRAFICAS DE CURVAS DE FRAGILIDAD DS VS IM
        
        try:
            self.grafica_SEOC_PROB_1.close()
        except AttributeError:
            pass
                
        self.grafica_SEOC_PROB_1 = Canvas_grafica()      
        self.grafica_SEOC_PROB_1.ax.clear()
        
        for i in range (num_DS_E1):
            # Curva
            self.grafica_SEOC_PROB_1.ax.plot(matriz_plot_P_E1['IM'], matriz_plot_P_E1['DS'+str(i+1)], color = color[i], linestyle = '-',
                      label = ds_tags_E1[i] + ' - ' + r"$\theta$" +' = ' + str(round(parameters_P_E1.at[i,'theta'],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(parameters_P_E1.at[i,'sigma'],3)))
            
            # Puntos
            self.grafica_SEOC_PROB_1.ax.plot(fragility_P_E1['IM_bin'], fragility_P_E1['Zi - DS' + str(i+1)]/fragility_P_E1['N'], color = color[i], 
                      marker = 'o', linestyle='', markersize = 3)

        self.grafica_SEOC_PROB_1.ax.set_xlim(0, 2.5)
        self.grafica_SEOC_PROB_1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's) [g]', size = 10)
        self.grafica_SEOC_PROB_1.ax.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_SEOC_PROB_1.ax.grid(which="both")
        self.grafica_SEOC_PROB_1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_fragilityP_1.addWidget(self.grafica_SEOC_PROB_1)
        
        ###################################################################### 
        # ASIGNACIÓN DE DESPLEGABLES DE PDFS
        
        IM_bin_E1 = matriz_IM_EDP_P_E1['IM_bin'].unique()
        
        try:
            self.ui.IM_1_1.clear()
            self.ui.IM_2_1.clear()
            self.ui.IM_3_1.clear()
            self.ui.IM_4_1.clear()
            self.ui.IM_5_1.clear()
            self.ui.IM_6_1.clear()
        except:
            pass
        
        self.ui.IM_1_1.addItem('None')
        self.ui.IM_2_1.addItem('None')
        self.ui.IM_3_1.addItem('None')
        self.ui.IM_4_1.addItem('None')
        self.ui.IM_5_1.addItem('None')
        self.ui.IM_6_1.addItem('None')
        
        for i in range(len(IM_bin_E1)):
            
            if IM_bin_E1[len(IM_bin_E1)-i-1] < 0.1:
                digit_round = 3
            else:
                digit_round = 2
                
            self.ui.IM_1_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            self.ui.IM_2_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            self.ui.IM_3_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            self.ui.IM_4_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            self.ui.IM_5_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            self.ui.IM_6_1.addItem(str(round(IM_bin_E1[len(IM_bin_E1)-i-1],digit_round)))
            
        ###################################################################### 
        # ASIGNACIÓN DE PARÁMETROS DE COLAPSO PARA PESTAÑA DE LOSS OF BUILDINGS 
        self.ui.Theta_collapse_value_1.setText(str(round(parameters_P_E1.iloc[-1,1],3)))
        self.ui.Sigma_collapse_value_1.setText(str(round(parameters_P_E1.iloc[-1,2],3)))
           
        ###################################################################### 
        # CIERRE DE GRAFICAS
        
        # Cierra graficas para que no se confunda que hay que presionar botones
        try:
            self.grafica_pdf_1.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
        
#%% # FUNCIÓN PARA GRAFICAR CURVAS DE FRAGILIDAD DE EDIFICACIÓN 2   
    # ---------------------------------------------------------------------------- 

    def Fragility_b2(self):
        global parameters_P_E2, matriz_plot_P_E2, fragility_P_E2, matriz_IM_EDP_P_E2, dataF_IM_EDP_Hz_E2, \
        dict_count_colap_E2, count_colap_columns_E2
        
        print('New run of Fragility building _2')
        
        ######################################################################  
        # CARGAR DATOS Y CORRER DISPERSION
        
        self.dispersion_b2()
        
        ####################################################################### 
        # GENERACIÓN DE CURVAS DE FRAGILIDAD
        
        # Definición de DataFrame de entrada para curvas de la forma: IM - EDP - HzL
        dataF_IM_EDP_Hz_E2 = pd.DataFrame()
        dataF_IM_EDP_Hz_E2['IM'] = IM_curva_E2[T_E2]
        dataF_IM_EDP_Hz_E2['EDP'] = EDP_curva_E2[story_E2]
        dataF_IM_EDP_Hz_E2['Hz Lv'] = IM_curva_E2['Hz Lv']
                  
        # Definición de delta y edp_max
        d_edp = delta_max_edp[EDP_name_graph_E2]['d_edp']
        edp_max = delta_max_edp[EDP_name_graph_E2]['edp_max']
        
        # Intenta crear una data frame para el conteo de columnas cuando sea el caso, si no lo encuentra lo crea vacío
        if collapse_method_E2 =='count columns':
            count_colap_columns_E2 = input_colum_count(fname_HzB_2, fname_EdpB_2, T_E2, IM_name_graph_E2, EDP_name_graph_E2, story_E2, EDP_collapse_E2, timeOK_E2, SDR_limit_E2)
            count_colap_columns_E2 = count_colap_columns_E2.loc[count_colap_columns_E2['Hz Lv'].isin(Hzlv_curves_E2)]
        else:
            count_colap_columns_E2 = {}
        
        # Generación de parámetros
        [parameters_P_E2, matriz_plot_P_E2, fragility_P_E2, matriz_IM_EDP_P_E2] = fragility_function_prob_collapseOptions(dataF_IM_EDP_Hz_E2, EDP_cens_E2, thetas_DS_E2, betas_DS_E2, tipo_bin_E2, min_datos_bin_E2, 
                                                                                                                              num_bins_inicial_E2, IM_max_graph_E2, d_edp, edp_max, include_cens_E2, porc_curves_E2,
                                                                                                                              collapse_method_E2, EDP_collapse_E2, IM_delta_graph_E2, count_colap_columns_E2)
        ######################################################################  
        # GRAFICAS DE BINEADO CON DATA DE CURVAS DE FRAGILIDAD
        
        try:
            self.grafica_bineado_PROB_2.close()
        except AttributeError:
            pass
        
        self.grafica_bineado_PROB_2 = Canvas_grafica()      
        self.grafica_bineado_PROB_2.ax.clear()
        
        # Total de hazard evaluados
        total_num_hazard_E2 = Hzlv_curves_E2.max()
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(total_num_hazard_E2)
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
            
        # Gráfico   
        for HL in Hzlv_curves_E2:
            IM_aux = matriz_IM_EDP_P_E2.loc[matriz_IM_EDP_P_E2['Hz Lv']==HL]['IM_bin']
            EDP_aux = matriz_IM_EDP_P_E2.loc[matriz_IM_EDP_P_E2['Hz Lv']==HL]['EDP']
            
            self.grafica_bineado_PROB_2.ax.loglog(IM_aux, EDP_aux , marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        if EDP_name_graph_E2 == "PFA":
            self.grafica_bineado_PROB_2.ax.set_ylim(0.5, 200)
        else:
            self.grafica_bineado_PROB_2.ax.set_ylim(0.0001, 100)

        self.grafica_bineado_PROB_2.ax.set_xlim(0.01,10)
        self.grafica_bineado_PROB_2.ax.set_yscale("log")
        self.grafica_bineado_PROB_2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's) [g]', size = 10)
        self.grafica_bineado_PROB_2.ax.set_ylabel(EDP_name_graph_E2 + r'$_{'+story_E2+'}$', size = 10)
        self.grafica_bineado_PROB_2.ax.legend(fontsize=7, loc = 'best')
        self.grafica_bineado_PROB_2.ax.grid(which="both", alpha = 0.5)
        
        self.ui.BinP_2.addWidget(self.grafica_bineado_PROB_2)
        
        ######################################################################   
        # GRAFICAS DE CURVAS DE FRAGILIDAD DS VS IM
        
        try:
            self.grafica_SEOC_PROB_2.close()
        except AttributeError:
            pass
                
        self.grafica_SEOC_PROB_2 = Canvas_grafica()      
        self.grafica_SEOC_PROB_2.ax.clear()
        
        for i in range (num_DS_E2):
            # Curva
            self.grafica_SEOC_PROB_2.ax.plot(matriz_plot_P_E2['IM'], matriz_plot_P_E2['DS'+str(i+1)], color = color[i], linestyle = '--',
                      label = ds_tags_E2[i] + ' - ' + r"$\theta$" +' = ' + str(round(parameters_P_E2.at[i,'theta'],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(parameters_P_E2.at[i,'sigma'],3)))
            
            # Puntos
            self.grafica_SEOC_PROB_2.ax.plot(fragility_P_E2['IM_bin'], fragility_P_E2['Zi - DS' + str(i+1)]/fragility_P_E2['N'], color = color[i], 
                      marker = '^', linestyle='', markersize = 3)

        self.grafica_SEOC_PROB_2.ax.set_xlim(0, 2.5)
        self.grafica_SEOC_PROB_2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's) [g]', size = 10)
        self.grafica_SEOC_PROB_2.ax.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_SEOC_PROB_2.ax.grid(which="both")
        self.grafica_SEOC_PROB_2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_fragilityP_2.addWidget(self.grafica_SEOC_PROB_2)
        
        ###################################################################### 
        # ASIGNACIÓN DE DESPLEGABLES DE PDFS
        
        IM_bin_E2 = matriz_IM_EDP_P_E2['IM_bin'].unique()
        
        try:
            self.ui.IM_1_2.clear()
            self.ui.IM_2_2.clear()
            self.ui.IM_3_2.clear()
            self.ui.IM_4_2.clear()
            self.ui.IM_5_2.clear()
            self.ui.IM_6_2.clear()
        except:
            pass
        
        self.ui.IM_1_2.addItem('None')
        self.ui.IM_2_2.addItem('None')
        self.ui.IM_3_2.addItem('None')
        self.ui.IM_4_2.addItem('None')
        self.ui.IM_5_2.addItem('None')
        self.ui.IM_6_2.addItem('None')
        
        for i in range(len(IM_bin_E2)):
            
            if IM_bin_E2[len(IM_bin_E2)-i-1] < 0.1:
                digit_round = 3
            else:
                digit_round = 2
                
            self.ui.IM_1_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            self.ui.IM_2_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            self.ui.IM_3_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            self.ui.IM_4_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            self.ui.IM_5_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            self.ui.IM_6_2.addItem(str(round(IM_bin_E2[len(IM_bin_E2)-i-1],digit_round)))
            
        ###################################################################### 
        # ASIGNACIÓN DE PARÁMETROS DE COLAPSO PARA PESTAÑA DE LOSS OF BUILDINGS 
        self.ui.Theta_collapse_value_2.setText(str(round(parameters_P_E2.iloc[-1,1],3)))
        self.ui.Sigma_collapse_value_2.setText(str(round(parameters_P_E2.iloc[-1,2],3)))
           
        ###################################################################### 
        # CIERRE DE GRAFICAS
        
        # Cierra graficas para que no se confunda que hay que presionar botones
        try:
            self.grafica_pdf_2.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
        
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
            
#%% # FUNCIÓN PARA GRAFICAR COMBPARACIÓN DE CURVAS DE FRAGILIDAD
    # ---------------------------------------------------------------------------- 

    def fragility_comparison(self):
        
        # Definición del tipo de curva a utilizar
        CurveType = self.ui.ComparisonType.currentText()
        
        # Gráfica
        try:
            self.grafica_comparison.close()
        except AttributeError:
            pass
            
        self.grafica_comparison = Canvas_grafica()
        self.grafica_comparison.ax.clear()
        
        if CurveType == 'SEC':
            
            # EDIFICIO 1
            if EDP_name_graph_E1 == "SDR" or EDP_name_graph_E1 == "RSDR":
                for i in range (len(j_E1)):
                    self.grafica_comparison.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i], 
                              label = 'j =' + str(round(j_E1[i]*100,2)) + '% - ' + r"$\theta$" +' = ' + str(round(parameters_D_E1.iloc[i,1],3)) + '  ' +
                              r"$\beta$"+' = ' + str(round(parameters_D_E1.iloc[i,2],3)))
                    self.grafica_comparison.ax.plot(fragility_D_E1['IM_bin'], fragility_D_E1['Zi - j = ' + str(j_E1[i])]/fragility_D_E1['N'], color = color[i], 
                              marker = 'o', linestyle='', markersize = 3)
                
            elif EDP_name_graph_E1 == "PFA":
                for i in range (len(j_E1)):
                    self.grafica_comparison.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i], 
                              label = 'j =' + str(round(j_E1[i],2)) + ' - ' + r"$\theta$" +' = ' + str(round(parameters_D_E1.iloc[i,1],3)) + '  ' +
                              r"$\beta$"+' = ' + str(round(parameters_D_E1.iloc[i,2],3)))
                    self.grafica_comparison.ax.plot(fragility_D_E1['IM_bin'], fragility_D_E1['Zi - j = ' + str(j_E1[i])]/fragility_D_E1['N'], color = color[i], 
                              marker = 'o', linestyle='', markersize = 3)
                    
            # EDIFICIO 2
            if EDP_name_graph_E2 == "SDR" or EDP_name_graph_E2 == "RSDR":
                for i in range (len(j_E2)):
                    self.grafica_comparison.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = 'dashed',
                             label = 'j =' + str(round(j_E2[i]*100,2)) + '% - ' + r"$\theta$" +' = ' + str(round(parameters_D_E2.iloc[i,1],3)) + '  ' +
                             r"$\beta$"+' = ' + str(round(parameters_D_E2.iloc[i,2],3)))
                    self.grafica_comparison.ax.plot(fragility_D_E2['IM_bin'], fragility_D_E2['Zi - j = ' + str(j_E2[i])]/fragility_D_E2['N'], color = color[i], 
                             marker = '^', linestyle='', markersize = 3)
                
            elif EDP_name_graph_E2 == "PFA":
                for i in range (len(j_E2)):
                    self.grafica_comparison.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = 'dashed',
                             label = 'j =' + str(round(j_E2[i],2)) + ' - ' + r"$\theta$" +' = ' + str(round(parameters_D_E2.iloc[i,1],3)) + '  ' +
                             r"$\beta$"+' = ' + str(round(parameters_D_E2.iloc[i,2],3)))
                    self.grafica_comparison.ax.plot(fragility_D_E2['IM_bin'], fragility_D_E2['Zi - j = ' + str(j_E2[i])]/fragility_D_E2['N'], color = color[i], 
                             marker = '^', linestyle='', markersize = 3)
                    
                
        elif CurveType == 'Fragility':
            
            # EDIFICIO 1
            for i in range (num_DS_E1):
                self.grafica_comparison.ax.plot(matriz_plot_P_E1['IM'], matriz_plot_P_E1['DS'+str(i+1)], color = color[i], 
                          label = ds_tags_E1[i] + ' - ' + r"$\theta$" +' = ' + str(round(parameters_P_E1.iloc[i,1],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_P_E1.iloc[i,2],3)))
                self.grafica_comparison.ax.plot(fragility_P_E1['IM_bin'], fragility_P_E1['Zi - DS' + str(i+1)]/fragility_P_E1['N'], color = color[i], 
                          marker = 'o', linestyle='', markersize = 3)
            
            # EDIFICIO 2
            for i in range (num_DS_E2):
                self.grafica_comparison.ax.plot(matriz_plot_P_E2['IM'], matriz_plot_P_E2['DS'+str(i+1)], color = color[i], linestyle = 'dashed',
                          label = ds_tags_E2[i] + ' - ' + r"$\theta$" +' = ' + str(round(parameters_P_E2.iloc[i,1],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_P_E2.iloc[i,2],3)))
                self.grafica_comparison.ax.plot(fragility_P_E2['IM_bin'], fragility_P_E2['Zi - DS' + str(i+1)]/fragility_P_E2['N'], color = color[i], 
                          marker = '^', linestyle='', markersize = 3)

    
        self.grafica_comparison.ax.set_xlim(0, 2.5)
        self.grafica_comparison.ax.set_xlabel('IM', size = 10)
        self.grafica_comparison.ax.set_ylabel('EDP', size = 10)
        self.grafica_comparison.ax.grid(which="both")
        self.grafica_comparison.ax.legend(fontsize=5.5, loc = 'best')
        self.ui.graph_comparison.addWidget(self.grafica_comparison)  
    
#%% # FUNCIÓN PARA GRAFICAR COMBINACIÓN DE CURVAS DE FRAGILIDAD   
    # ---------------------------------------------------------------------------- 

    def fragility_combined(self):
        global IM_comb, EDP_comb
        
        
        # Definición del tipo de curva a utilizar
        CurveType = self.ui.ComparisonType.currentText()
        
        ################################### 
        #  ORGANIZAR DATOS
        
        # Combinación de DataFrames
        dataF_IM_EDP_comb = pd.DataFrame()
        dataF_IM_EDP_comb = pd.concat([dataF_IM_EDP_comb, dataF_IM_EDP_Hz_E1], axis = 0, ignore_index = True)
        dataF_IM_EDP_comb = pd.concat([dataF_IM_EDP_comb, dataF_IM_EDP_Hz_E2], axis = 0, ignore_index = True)
        
        if CurveType == 'SEC':
            [parameters_comb, matriz_plot_comb, fragility_comb, matriz_IM_EDP_comb] = fragility_function_det(dataF_IM_EDP_comb, j_E1, tipo_bin_E1, min_datos_bin_E1, 
                                                                                                             num_bins_inicial_E1, IM_max_graph_E1, IM_delta_graph_E1)

        
        elif CurveType == 'Fragility':
            
            d_edp = delta_max_edp[EDP_name_graph_E1]['d_edp']
            edp_max = delta_max_edp[EDP_name_graph_E1]['edp_max']
            
            
            # Intenta crear una data frame para el conteo de columnas cuando sea el caso, si no lo encuentra lo crea vacío
            count_colap_columns_comb = {}
            
            # Generación de parámetros
            [parameters_comb, matriz_plot_comb, fragility_comb, matriz_IM_EDP_comb] = fragility_function_prob_collapseOptions(dataF_IM_EDP_comb, EDP_cens_E1, thetas_DS_E1, betas_DS_E1, tipo_bin_E1, min_datos_bin_E1, 
                                                                                                                              num_bins_inicial_E1, IM_max_graph_E1, d_edp, edp_max, include_cens_E1, porc_curves_E1,
                                                                                                                              collapse_method_E1, EDP_collapse_E1, IM_delta_graph_E1, count_colap_columns_comb)

        if (len(j_E1) != len(j_E2)) or (num_DS_E1 != num_DS_E2):
            print('WARNING: There are many damage states in one building than in the another, you may to receive an error trying combining')
        
        ################################### 
        # GRAFICA
      
        try:
            self.grafica_combination.close()
        except AttributeError:
            pass
        
        self.grafica_combination = Canvas_grafica()
        self.grafica_combination.ax.clear()
        
        if CurveType == 'SEC':
        
            if EDP_name_graph_E1 == "SDR" or EDP_name_graph_E1 == "RSDR":
                    
                for i in range (len(j_E1)):
                    
                    # Grafica combinada
                    self.grafica_combination.ax.plot(matriz_plot_comb['IM'], matriz_plot_comb['j = ' + str(j_E1[i])], color = color[i], linestyle = 'dashdot',
                            label = 'j =' + str(round(j_E1[i]*100,2)) + '% - ' + r"$\theta$" +' = ' + str(round(parameters_comb.iloc[i,1],3)) + '  ' +
                            r"$\beta$"+' = ' + str(round(parameters_comb.iloc[i,2],3)))
                    self.grafica_combination.ax.plot(fragility_comb['IM_bin'], fragility_comb['Zi - j = ' + str(j_E1[i])]/fragility_comb['N'], color = color[i], 
                            marker = 'X', linestyle='', markersize = 3)
                  
                    # Grafica de las otras dos curvas
                    self.grafica_combination.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i],alpha=0.3)
                    self.grafica_combination.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = 'dashed',alpha=0.3)
                    
            elif EDP_name_graph_E1 == "PFA":
                
                for i in range (len(j_E1)):
                    
                    # Grafica combinada
                    self.grafica_combination.ax.plot(matriz_plot_comb['IM'], matriz_plot_comb['j = ' + str(j_E1[i])], color = color[i], linestyle = 'dashdot',
                            label = 'j =' + str(round(j_E1[i],2)) + ' - ' + r"$\theta$" +' = ' + str(round(parameters_comb.iloc[i,1],3)) + '  ' +
                            r"$\beta$"+' = ' + str(round(parameters_comb.iloc[i,2],3)))
                    self.grafica_combination.ax.plot(fragility_comb['IM_bin'], fragility_comb['Zi - j = ' + str(j_E1[i])]/fragility_comb['N'], color = color[i], 
                            marker = 'X', linestyle='', markersize = 3)
                    
                    # Grafica de las otras dos curvas
                    self.grafica_combination.ax.plot(matriz_plot_D_E1['IM'], matriz_plot_D_E1['j = ' + str(j_E1[i])], color = color[i],alpha=0.3)
                    self.grafica_combination.ax.plot(matriz_plot_D_E2['IM'], matriz_plot_D_E2['j = ' + str(j_E2[i])], color = color[i], linestyle = 'dashed',alpha=0.3)
        
        if CurveType == 'Fragility':
                
            for i in range (num_DS_E1):
                
                # Grafica combinada
                self.grafica_combination.ax.plot(matriz_plot_comb['IM'], matriz_plot_comb['DS'+str(i+1)], color = color[i], 
                          label = ds_tags_E1[i] + ' - ' + r"$\theta$" +' = ' + str(round(parameters_comb.iloc[i,1],3)) + '  ' +
                          r"$\beta$"+' = ' + str(round(parameters_comb.iloc[i,2],3)))
                self.grafica_combination.ax.plot(fragility_comb['IM_bin'], fragility_comb['Zi - DS' + str(i+1)]/fragility_comb['N'], color = color[i], 
                          marker = 'X', linestyle='', markersize = 3)
                
                # Grafica de las otras dos curvas
                self.grafica_combination.ax.plot(matriz_plot_P_E1['IM'], matriz_plot_P_E1['DS'+str(i+1)], color = color[i],alpha=0.3)
                self.grafica_combination.ax.plot(matriz_plot_P_E2['IM'], matriz_plot_P_E2['DS'+str(i+1)], color = color[i], linestyle = 'dashed',alpha=0.3)
            
                    
  
        self.grafica_combination.ax.set_xlim(0, 2.5)
        self.grafica_combination.ax.set_xlabel('IM', size = 10)
        self.grafica_combination.ax.set_ylabel('EDP', size = 10)

        self.grafica_combination.ax.grid(which="both")
        self.grafica_combination.ax.legend(fontsize=7, loc = 'lower right')
        self.ui.graph_combine_curve.addWidget(self.grafica_combination)
        
#%% # FUNCIÓN PARA GRAFICAR PDFS DE LA EDIFICACION 1       
    # ---------------------------------------------------------------------------- 

    def pdfs_b1(self):
        
        IM_name_graph_E1 = self.ui.IMType_Value_1.currentText()
        EDP_name_graph_E1 = self.ui.EDPType_Value_1.currentText()
        
        # Redondeo de IM_bin
        for i in range(len(matriz_IM_EDP_P_E1)):
            # Redondedo de IMs bineados
            if matriz_IM_EDP_P_E1.at[i,'IM_bin'] < 0.1:
                digit_round = 3
            else:
                digit_round = 2
                
            matriz_IM_EDP_P_E1.at[i,'IM_bin'] = round(matriz_IM_EDP_P_E1.at[i,'IM_bin'],digit_round)
            
        ################################### 
        # GRAFICA
        try:
            self.grafica_pdf_1.close()
        except AttributeError:
            pass
        
        self.grafica_pdf_1 = Canvas_grafica()
        self.grafica_pdf_1.ax.clear()
        
        # Valores de PDFs seleccionados
        try:
            IM_1 = float(self.ui.IM_1_1.currentText())
        except ValueError:
            pass
        try:
            IM_2 = float(self.ui.IM_2_1.currentText())
        except ValueError:
            pass
        try:
            IM_3 = float(self.ui.IM_3_1.currentText())
        except ValueError:
            pass
        try:
            IM_4 = float(self.ui.IM_4_1.currentText())
        except ValueError:
            pass
        try:
            IM_5 = float(self.ui.IM_5_1.currentText())
        except ValueError:
            pass
        try:
            IM_6 = float(self.ui.IM_6_1.currentText())
        except ValueError:
            pass
        
        # Creacion de vector de valores con IMs de interés
        IMS_graph = np.asarray([])
        try:
            IMS_graph = np.append(IMS_graph, IM_1)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_2)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_3)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_4)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_5)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_6)
        except UnboundLocalError:
            pass
        
        # Generación de datos para la gráfica
        for i in range(len(IMS_graph)):
            
            IM_bin_graph = IMS_graph[i]
            
            ind = matriz_IM_EDP_P_E1.loc[matriz_IM_EDP_P_E1['IM_bin'] == IM_bin_graph]
            ind.reset_index(drop = True, inplace=True)
            # print(ind)
            
            shape, loc, scale = stats.lognorm.fit(ind['EDP'], floc=0)
            mu = np.log(scale)
            sigma = shape
            
            edp_max = delta_max_edp[EDP_name_graph_E1]['edp_max']
            d_edp = delta_max_edp[EDP_name_graph_E1]['d_edp']
            x = np.arange(d_edp/10, edp_max + d_edp/10, d_edp/10)
                
            data_plot = stats.lognorm.pdf(x = x, scale = np.exp(mu), s = sigma) 
            self.grafica_pdf_1.ax.plot(x,data_plot, label = IM_name_graph_E1 + '(T=' + str(T_E1) + 's)' + ' = ' + str(IM_bin_graph) + 'g')

        if EDP_name_graph_E1 == "PFA":
            self.grafica_pdf_1.ax.set_xlim(0, 20)
        else:
            self.grafica_pdf_1.ax.set_xlim(0, 0.10)
        
        self.grafica_pdf_1.ax.set_xlabel(EDP_name_graph_E1 + r'$_{'+story_E1+'}$', size = 10)
        self.grafica_pdf_1.ax.set_ylabel('p(' + EDP_name_graph_E1 + r'$_{'+story_E1+'}$' + '|' + IM_name_graph_E1 + '(T=' + str(T_E1) + r'$s)_{m})$', size = 10)
        self.grafica_pdf_1.ax.grid(which="both")
        self.grafica_pdf_1.ax.legend(fontsize=7, loc = 'upper right')
        self.ui.PDF_1.addWidget(self.grafica_pdf_1)
        
#%% # FUNCIÓN PARA GRAFICAR PDFS DE LA EDIFICACION 2        
    # ----------------------------------------------------------------------------    

    def pdfs_b2(self):
        
        IM_name_graph_E2 = self.ui.IMType_Value_2.currentText()
        EDP_name_graph_E2 = self.ui.EDPType_Value_2.currentText()
        
        # Redondeo de IM_bin
        for i in range(len(matriz_IM_EDP_P_E2)):
            # Redondedo de IMs bineados
            if matriz_IM_EDP_P_E2.at[i,'IM_bin'] < 0.1:
                digit_round = 3
            else:
                digit_round = 2
                
            matriz_IM_EDP_P_E2.at[i,'IM_bin'] = round(matriz_IM_EDP_P_E2.at[i,'IM_bin'],digit_round)
            
        ################################### 
        # GRAFICA
        try:
            self.grafica_pdf_2.close()
        except AttributeError:
            pass
        
        self.grafica_pdf_2 = Canvas_grafica()
        self.grafica_pdf_2.ax.clear()
        
        # Valores de PDFs seleccionados
        try:
            IM_1 = float(self.ui.IM_1_2.currentText())
        except ValueError:
            pass
        try:
            IM_2 = float(self.ui.IM_2_2.currentText())
        except ValueError:
            pass
        try:
            IM_3 = float(self.ui.IM_3_2.currentText())
        except ValueError:
            pass
        try:
            IM_4 = float(self.ui.IM_4_2.currentText())
        except ValueError:
            pass
        try:
            IM_5 = float(self.ui.IM_5_2.currentText())
        except ValueError:
            pass
        try:
            IM_6 = float(self.ui.IM_6_2.currentText())
        except ValueError:
            pass
        
        # Creacion de vector de valores con IMs de interés
        IMS_graph = np.asarray([])
        try:
            IMS_graph = np.append(IMS_graph, IM_1)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_2)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_3)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_4)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_5)
        except UnboundLocalError:
            pass
        try:
            IMS_graph = np.append(IMS_graph, IM_6)
        except UnboundLocalError:
            pass
        
        # Generación de datos para la gráfica
        for i in range(len(IMS_graph)):
            
            IM_bin_graph = IMS_graph[i]
            
            ind = matriz_IM_EDP_P_E2.loc[matriz_IM_EDP_P_E2['IM_bin'] == IM_bin_graph]
            ind.reset_index(drop = True, inplace=True)
            
            shape, loc, scale = stats.lognorm.fit(ind['EDP'], floc=0)
            mu = np.log(scale)
            sigma = shape
            
            edp_max = delta_max_edp[EDP_name_graph_E2]['edp_max']
            d_edp = delta_max_edp[EDP_name_graph_E2]['d_edp']
            x = np.arange(d_edp/10, edp_max + d_edp/10, d_edp/10)
                
            data_plot = stats.lognorm.pdf(x = x, scale = np.exp(mu), s = sigma) 
            self.grafica_pdf_2.ax.plot(x,data_plot, label = IM_name_graph_E2 + '(T=' + str(T_E2) + 's)' + ' = ' + str(IM_bin_graph) + 'g')

       
        if EDP_name_graph_E2 == "PFA":
            self.grafica_pdf_2.ax.set_xlim(0, 20) 
        else:
            self.grafica_pdf_2.ax.set_xlim(0, 0.10)
        
        
        self.grafica_pdf_2.ax.set_xlabel(EDP_name_graph_E2 + r'$_{'+story_E2+'}$', size = 10)
        self.grafica_pdf_2.ax.set_ylabel('p(' + EDP_name_graph_E2 + r'$_{'+story_E2+'}$' + '|' + IM_name_graph_E2 + '(T=' + str(T_E2) + r'$s)_{m})$', size = 10)
        self.grafica_pdf_2.ax.grid(which="both")
        self.grafica_pdf_2.ax.legend(fontsize=7, loc = 'upper right')
        self.ui.PDF_2.addWidget(self.grafica_pdf_2)

#%%   
     
###################################################################################
# FUNCIONES PARA BOTONES DEL TABWIDGET DE FRAGILITY OF TAXONOMIES
###################################################################################
  
#%% # FUNCIÓN PARA GRAFICAR GENERA ARCHIVO DE EXCEL DE TAXONOMIAS  
    # ---------------------------------------------------------------------------- 
    
    def excel_generator_taxonomies(self):
        global dict_param_buildings, dict_param_taxonomy, dict_points_fragility, dict_data_IM_EDP_HzLv, num_ds, \
                separation_tax_name
        
        ######################################################################  
        # LECTURA DE PARAMETROS GENERALES
        
        # Revisión de corridas
        timeOK = float(self.ui.tmin_value_3.text())
        EDP_limit = float(self.ui.EDP_value_3.text())
        
        # Periodos de interes 
        T = self.ui.periodo_value_3.text()
        T = np.asarray(T.split(",")).astype(float)
        
        # IM de interés
        IM_name_graph = self.ui.IMType_Value_3.currentText()
        
        # EDP de interés
        EDP_name_graph = self.ui.EDPType_Value_3.currentText()
        story = self.ui.EDPType_ValueStory_3.currentText()
        
        # Porcentajes de ajustes de curvas
        porc_curves = self.ui.porc_fit_curves_3.text()
        porc_curves = np.asarray(porc_curves.split(",")).astype(float)
        
        # Bin Type
        tipo_bin = self.ui.Bintype_3.currentText()
        if tipo_bin == "Linespace":
            tipo_bin = 1
        elif tipo_bin == "Logspace":
            tipo_bin = 2
            
        # Inclusión de censura en la bineado
        include_cens = self.ui.includeCens_3.currentText()
        if include_cens == "Yes":
            include_cens = 1
        elif include_cens == "No":
            include_cens = 0
        
        # Definición de metodologia de colapso para fragilidad
        collapse_method = self.ui.collapseMethod_3.currentText()
        
        # Número mínimo de datos por bin y número inicial de bines
        min_datos_bin = int(self.ui.binminvalue_3.text())
        num_bins_inicial = int(self.ui.bininitialvalue_3.text())
        
        # IM maximo de gráficos, las curvas de fragilidad se estimaran hasta este valor
        IM_max_graph = 10
        
        # Delta de graficos, las curvas de fragilidad se calcularan cada valor delta
        IM_delta_graph = 0.001
        
        ######################################################################  
        # GENERACION DE RESULTADOS
        
        self.ui.processing_finishing_status.setText('Estimating curve parameters...')
        
        # Matriz que incluye ls edificaciones que se utilziaran para elaborar taxonomia
        matriz_filter_tax = building_guide_original.loc[building_guide_original['Included in Frag?']==1]
        
        # Lista de taxonomias
        col_name_tax = self.ui.Group_Value.currentText()
        taxonomy_list = matriz_filter_tax[col_name_tax].unique()
        
        # Conversion de taxonomylist en str (aunque ya lo sea) para cuando encuentre una taxonomia nan y pueda eliminarla
        taxonomy_list = taxonomy_list.astype(str)
        taxonomy_list = list(filter(lambda x: x!='nan', taxonomy_list))
        
        # Carpeta donde se buscan los subgrupos de carpetas de resultados
        results_path = fname_resultsBuildings
        
        # Llamado de función que genera taxonomias
        [dict_param_buildings, dict_param_taxonomy, dict_points_fragility, dict_data_IM_EDP_HzLv] = taxonomy_calculation(fname_resultsBuildings, T, taxonomy_list, matriz_filter_tax, 
                                                                                                                         results_path, IM_name_graph, EDP_name_graph, story, timeOK, 
                                                                                                                         EDP_limit, include_cens, porc_curves, collapse_method, tipo_bin, 
                                                                                                                         min_datos_bin, num_bins_inicial, IM_max_graph, self.ui, col_name_tax, 
                                                                                                                         delta_max_edp)
        ################################### 
        # CREACIÓN DE EXCEL DE RESULTADOS
        
        self.ui.processing_finishing_status.setText('Generating excel results...')
        QApplication.processEvents() # Forzar la actualización de la interfaz gráfica en cada iteración
        
        file_name = self.ui.excel_name_value.text()
        
        results_excel_path = os.path.join(fname_file_result, file_name + '.xlsx')
        
        # Escribir sobre excel
        writer = pd.ExcelWriter(results_excel_path)

        # ------------------------------------------
        # Guardado de resultado de parámetros de las taxonomias

        # Lista de IMs
        IM_T_list = list(dict_param_taxonomy.keys())

        current_sheet_name = 'Taxonomies'

        data_aux = pd.DataFrame()
        for i in range(len(IM_T_list)):
            data_aux = data_aux.append(dict_param_taxonomy[IM_T_list[i]], ignore_index=True)

        data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)

        # ------------------------------------------
        # Guardado de resultado de parámetros de las edificaciones

        # Lista de IMs
        IM_T_list = list(dict_param_buildings.keys())

        current_sheet_name = 'Buildings'

        data_aux = pd.DataFrame()
        for i in range(len(IM_T_list)):
            data_aux = data_aux.append(dict_param_buildings[IM_T_list[i]], ignore_index=True)
            
        data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)
        
        # ------------------------------------------
        # Guardado de resultado de los puntos con los que se ajustan las curvas de los DS de cada taxonomia para cada T
        
        # Lista de IMs
        IM_T_list = list(dict_points_fragility.keys())
        
        # Loop de las taxonomias
        for j in range(len(taxonomy_list)):
            
            data_aux = pd.DataFrame()
            
            for i in range(len(IM_T_list)):
                
                # En caso de que hay habido error generando la taxonmia
                try:
                    # Nombre de la hoja
                    current_sheet_name = taxonomy_list[j].replace('/','-')
                    
                    current_data = dict_points_fragility[IM_T_list[i]][taxonomy_list[j]]
                    current_data['IM_Type'] = IM_name_graph
                    current_data['T'] = IM_T_list[i]
                    data_aux = data_aux.append(current_data, ignore_index=True)
                    
                    data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)
                except KeyError:
                    pass
                
        # ------------------------------------------
        # Guardado de los datos de cada taxonomia para graficar dispersion
        
        # Lista de IMs
        IM_T_list = list(dict_data_IM_EDP_HzLv.keys())
        
        # Loop de las taxonomias
        for j in range(len(taxonomy_list)):
            
            data_aux = pd.DataFrame()
            
            for i in range(len(IM_T_list)):
                
                # En caso de que hay habido error generando la taxonmia
                try:
                    # Nombre de la hoja
                    current_sheet_name = 'Disp - ' + taxonomy_list[j].replace('/','-')
                    
                    current_data = dict_data_IM_EDP_HzLv[IM_T_list[i]][taxonomy_list[j]]
                    current_data['IM_Type'] = IM_name_graph
                    current_data['T'] = IM_T_list[i]
                    data_aux = data_aux.append(current_data, ignore_index=True)
                    
                    data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)
                    
                except KeyError:
                    pass

        writer.save()
        writer.close() 
        
        self.ui.processing_finishing_status.setText('Process completed successfully!')
        
        ################################### 
        # GENERACION DE DESPLEGABLES PARA LAS GRAFICAS
        
        #---------------------------------------------------
        # IM del Excel
        try:
            self.ui.IMTax_value_1.clear()
            self.ui.IMTax_value_2.clear()
        except:
            pass
        IM_T1 = self.ui.IMTax_value_1.addItem(IM_name_graph)
        IM_T2 = self.ui.IMTax_value_2.addItem(IM_name_graph)
        
        # Periodos del Excel
        try:
            self.ui.PeriodoTax_value_1.clear()
            self.ui.PeriodoTax_value_2.clear()
        except:
            pass
        
        for current_T in T:
            T_T1 = self.ui.PeriodoTax_value_1.addItem(str(current_T))
            T_T2 = self.ui.PeriodoTax_value_2.addItem(str(current_T))
        
        # Taxonomias
        try:
            self.ui.TaxonomyTax_value_1.clear()
            self.ui.TaxonomyTax_value_2.clear()
        except:
            pass
        
        for current_tax in taxonomy_list:
            tax_T1 = self.ui.TaxonomyTax_value_1.addItem(current_tax)
            tax_T2 = self.ui.TaxonomyTax_value_2.addItem(current_tax)
            
        #---------------------------------------------------
        # Damage states para graficas
        data_aux = dict_param_taxonomy[str(current_T)]
        num_ds = sum(cols.startswith('Theta') for cols in data_aux.columns)
        
        try:
            self.ui.DS_graph_Value_1.clear()
        except:
            pass
        
        try:
            self.ui.DS_graph_Value_2.clear()
        except:
            pass
        
        try:
            self.ui.DS_graph_com_Value_1.clear()
        except:
            pass
        
        try:
            self.ui.DS_graph_com_Value_2.clear()
        except:
            pass
        
        for i in range(num_ds):
            self.ui.DS_graph_Value_1.addItem(str(i+1))
            self.ui.DS_graph_Value_2.addItem(str(i+1))
            self.ui.DS_graph_com_Value_1.addItem(str(i+1))
            self.ui.DS_graph_com_Value_2.addItem(str(i+1))
            
        #---------------------------------------------------
        # Generación de matriz de taxonomias separando componentes 
        # para generar en la funcion de graficas el Nivel de comparacion
        
        # Data Frame con nombres de taxonomias separadas
        separation_tax_name = pd.DataFrame()
        
        all_tax_list = pd.DataFrame()
        # Se buscan todas las taxonomias de cada IM porque puede que unas tengan otras que otros no
        for curr_key_dict in list(dict_param_taxonomy.keys()):
            all_tax_list = pd.concat([all_tax_list,dict_param_taxonomy[curr_key_dict]['Taxonomy']],axis = 0, ignore_index = True) 
        all_tax_list = all_tax_list[0].unique()
        
        separation_tax_name['Taxonomy'] = all_tax_list
        list_tax = separation_tax_name['Taxonomy'].unique()
        
        # Creacion de columnas de acuerdo con la cantidad de componentes
        num_taxs = len(separation_tax_name['Taxonomy'].unique()[0].split('/'))
        
        # Columnas a asignar
        cols_asignar = []
        
        # Columna de taxonomia sin numero de pisos
        separation_tax_name['Tax_No_stories'] = None
        
        for i in range(num_taxs):
            separation_tax_name['C'+str(i+1)] = None
            cols_asignar.append('C'+str(i+1))
            
        # Llenado de dataframe de los componentes que conforman la taxonomia
        for i in range (len(list_tax)):
            current_tax = list_tax[i]
            components_tax = current_tax.split('/')
            separation_tax_name.loc[i, cols_asignar] = components_tax
            
            tax_no_s = components_tax[0]
            for j in range(1, num_taxs-1):
                tax_no_s = tax_no_s + '/' + str(components_tax[j])
            
            separation_tax_name.at[i,'Tax_No_stories'] = tax_no_s

#%% # FUNCIÓN PARA GRAFICAR TAXONOMIA 1        
    # ---------------------------------------------------------------------------- 
    
    def graph_tax_T1(self):
        global IM_T1, T_T1, Tax_T1, current_param_Tax_data_T1, current_param_Build_data_T1, \
                thetas_tax_T1, betas_tax_T1, num_ds
        
        # Lectura de desplegables
        IM_T1 = self.ui.IMTax_value_1.currentText()
        T_T1 = self.ui.PeriodoTax_value_1.currentText()
        Tax_T1 = self.ui.TaxonomyTax_value_1.currentText()
        parameter_T1 = self.ui.ParamTax_value_1.currentText()
        
        self.ui.porc_fit_curves_changes_value_1.setText("1,1,1,1")
        self.ui.IM_vals_changes_value_1.setText("5,5,5,5")
        
        IM_max_graph = 10
        
        ################################### 
        # GRAFICAS DE DISPERSIÓN
        
        try:
            self.grafica_dipsersion_T1.close()
        except AttributeError:
            pass
        
        self.grafica_dipsersion_T1 = Canvas_grafica()      
        self.grafica_dipsersion_T1.ax.clear()
        
        # Data de taxonomia
        current_data = dict_data_IM_EDP_HzLv[str(T_T1)][Tax_T1]
        
        # Hazard levels
        Hzlv_curves = dict_data_IM_EDP_HzLv[str(T_T1)][Tax_T1]['Hz Lv'].unique().astype(int)
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(len(Hzlv_curves))
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico   
        for HL in Hzlv_curves:
            data_aux = current_data.loc[current_data['Hz Lv'].astype(int) == HL]
            # print(data_aux)
            
            self.grafica_dipsersion_T1.ax.loglog(data_aux['IM'], data_aux['EDP'], marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        self.grafica_dipsersion_T1.ax.set_title(Tax_T1)
        self.grafica_dipsersion_T1.ax.set_ylim(0.0001, 100)
        self.grafica_dipsersion_T1.ax.set_xlim(0.01,10)
        self.grafica_dipsersion_T1.ax.set_yscale("log")
        self.grafica_dipsersion_T1.ax.set_xlabel(IM_T1 + '(T = ' + str(T_T1) + 's)', size = 10)
        self.grafica_dipsersion_T1.ax.set_ylabel('EDP', size = 10)
        self.grafica_dipsersion_T1.ax.legend(fontsize=7, loc = 'upper left')
        self.grafica_dipsersion_T1.ax.grid(which="both", alpha = 0.5)

        self.ui.graph_dispe_tax_1.addWidget(self.grafica_dipsersion_T1)
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA TODOS LOS ESTADOS DE DAÑO
        
        try:
            self.grafica_all_FC_tax_T1.close()
        except AttributeError:
            pass
        
        self.grafica_all_FC_tax_T1 = Canvas_grafica()      
        self.grafica_all_FC_tax_T1.ax.clear()
        
        
        # Data de taxonomia
        current_param_Tax_data_T1 = dict_param_taxonomy[str(T_T1)]
        current_param_Tax_data_T1 = current_param_Tax_data_T1.loc[current_param_Tax_data_T1['Taxonomy'] == Tax_T1]
        
        # Cantidad de estados de daño
        num_ds = sum(cols.startswith('Theta') for cols in current_param_Tax_data_T1.columns)
        
        # Guardado de parámetros theta y beta
        thetas_tax_T1 = []
        betas_tax_T1 = []
        
        for i in range (num_ds):
            thetas_tax_T1.append(current_param_Tax_data_T1['Theta'+str(i+1)].tolist()[0])
            betas_tax_T1.append(current_param_Tax_data_T1['Beta'+str(i+1)].tolist()[0])
            
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
        
        for i in range(num_ds):
            matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_tax_T1[i]), betas_tax_T1[i])
            
        # Puntos de ajustes de curvas
        current_points = dict_points_fragility[str(T_T1)][Tax_T1]
        
        # Grafica
        for i in range (num_ds):
            self.grafica_all_FC_tax_T1.ax.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = color[i], 
                      label = 'DS' + str(i+1) + ' - ' + r"$\theta$" +' = ' + str(round(thetas_tax_T1[i],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(betas_tax_T1[i],3)))
            self.grafica_all_FC_tax_T1.ax.plot(current_points['IM_bin'], current_points['DS' + str(i+1)], color = color[i], 
                      marker = 'o', linestyle='', markersize = 3)

        self.grafica_all_FC_tax_T1.ax.set_xlim(0, 4)
        self.grafica_all_FC_tax_T1.ax.set_xlabel(IM_T1 + '(T = ' + str(T_T1) + 's)', size = 10)
        self.grafica_all_FC_tax_T1.ax.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_all_FC_tax_T1.ax.set_title(Tax_T1)
        self.grafica_all_FC_tax_T1.ax.grid(which="both")
        self.grafica_all_FC_tax_T1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_FC_tax_1.addWidget(self.grafica_all_FC_tax_T1)
        
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        self.graph_specific_DS_tax_T1()
        
        # Data de edificaciones
        current_param_Build_data_T1 = dict_param_buildings[str(T_T1)]
        current_param_Build_data_T1 = current_param_Build_data_T1.loc[current_param_Build_data_T1['Taxonomy'] == Tax_T1]
        current_param_Build_data_T1.reset_index(level=None, drop=True, inplace=True)
        
        # buildings_list = current_param_Build_data_T1['Building'].tolist()
        
        # Vector de posiciones para boxplots
        DS_names = []
        positions_boxplot = []
        
        for i in range (num_ds):
            DS_names.append('DS'+str(i+1))
            positions_boxplot.append(str(i+1))
        positions_boxplot = np.asarray(positions_boxplot).astype(int).tolist()
        
        ################################### 
        # GRAFICA DE THETAS O BETAS
        
        try:
            self.grafica_boxplot_thetas_T1.close()
        except AttributeError:
            pass
        
        self.grafica_boxplot_thetas_T1 = Canvas_grafica()      
        self.grafica_boxplot_thetas_T1.ax.clear()
        
        # Organizacion de data en un array para introducir en boxplot
        box_plot_data = {}
        for i in range(num_ds):
            box_plot_data[parameter_T1+str(i+1)] = current_param_Build_data_T1[parameter_T1+str(i+1)]
        # Convertir los datos en una matriz y transponerla
        box_plot_data_array = np.array(list(box_plot_data.values())).T
        
        # Creacion de boxplots por taxonomia
        bp = self.grafica_boxplot_thetas_T1.ax.boxplot(box_plot_data_array, positions = positions_boxplot, patch_artist=True)
        
        # Marca el valor de beta dentro la taxonomia dentro del boxplot
        for current_index in range (num_ds):
            
            if parameter_T1 == 'Theta':
                current_parameter = thetas_tax_T1
            elif parameter_T1 == 'Beta':
                current_parameter = betas_tax_T1
                
            self.grafica_boxplot_thetas_T1.ax.scatter(current_index+1, current_parameter[current_index], marker='*', s = 100, 
                                                      color='white', edgecolor = 'k', lw = 1.2, zorder = 100)
        
        # Asignacion de colores a los boxplots
        for patch, color_i in zip(bp['boxes'], color):
            patch.set_facecolor(color_i)
            bp['medians'][color.index(color_i)].set_color('black')
        
        # Configuracion de ejes
        self.grafica_boxplot_thetas_T1.ax.set_ylim(bottom=-0.05)
        self.grafica_boxplot_thetas_T1.ax.set_title(Tax_T1)
        self.grafica_boxplot_thetas_T1.ax.set_xticks(positions_boxplot)
        self.grafica_boxplot_thetas_T1.ax.set_xticklabels(DS_names)
        if parameter_T1 == 'Theta':
            self.grafica_boxplot_thetas_T1.ax.set_ylabel(r"$\theta$")
        elif parameter_T1 == 'Beta':
            self.grafica_boxplot_thetas_T1.ax.set_ylabel(r"$\beta$")
        self.grafica_boxplot_thetas_T1.ax.grid(which="both", alpha = 0.5)
        
        self.ui.graph_theta_tax_1.addWidget(self.grafica_boxplot_thetas_T1)
        
        
        ################################### 
        # GRAFICA DE COMPARACION DE PARAMETROS
        
        try:
            self.grafica_param_bystory_T1.close()
        except AttributeError:
            pass
        
        self.grafica_param_bystory_T1 = Canvas_grafica()      
        self.grafica_param_bystory_T1.ax.clear()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T1 = dict_param_taxonomy[str(T_T1)]
        
        # Cantidad de elementos separados
        num_sep_comp = len(separation_tax_name['Taxonomy'].unique()[0].split('/'))
        
        # Taxonomia actual
        ind_current_tax = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T1]
        
        # Nombre de la taxonomia sin pisos a graficar
        filt_name = ind_current_tax['C1'].tolist()[0]
        for i in range(1, num_sep_comp - 1):
            filt_name = filt_name + '/' + str(ind_current_tax['C'+str(i+1)].tolist()[0])
            
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{filt_name}')
        
        # Data Frame filtrado para thetas y betas de taxonomia
        filt_verification = current_param_Tax_data_T1['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        taxs_to_plot = current_param_Tax_data_T1[filt_verification]
        taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        # Para cuando en el IM actual hay menos taxonomias de todas las disponibles
        separation_to_plot = separation_to_plot.loc[separation_to_plot['Taxonomy'].isin(taxs_to_plot['Taxonomy'])]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conversion de columna de pisos en enteros
        separation_to_plot.iloc[:,-1] = separation_to_plot.iloc[:,-1].astype(int)
 
        # Ordenar separation por # de pisos y ordenar tax_to_plot tambien
        separation_to_plot = separation_to_plot.sort_values(by=separation_to_plot.columns[-1])
        taxs_to_plot = taxs_to_plot.set_index('Taxonomy').loc[separation_to_plot['Taxonomy']].reset_index()
        
        num_stories = separation_to_plot.iloc[:,-1].astype(int).to_numpy()
        for i in range(num_ds):
            parameters_aux = taxs_to_plot[parameter_T1+str(i+1)]
            self.grafica_param_bystory_T1.ax.plot(num_stories, parameters_aux, 'o-', color = color[i], markersize = 3, label = "DS" + str(i+1))
        
        # self.grafica_param_bystory_T1.ax.set_ylim(bottom=-0.05)
        self.grafica_param_bystory_T1.ax.set_title(filt_name)
        self.grafica_param_bystory_T1.ax.set_xlabel('N Stories', size = 10)
        if parameter_T1 == 'Theta':
            self.grafica_param_bystory_T1.ax.set_ylabel(r"$\theta$", size = 10)
        elif parameter_T1 == 'Beta':
            self.grafica_param_bystory_T1.ax.set_ylabel(r"$\beta$", size = 10)
        self.grafica_param_bystory_T1.ax.grid(which="both", alpha = 0.5)
        self.grafica_param_bystory_T1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_theta_tax_1.addWidget(self.grafica_param_bystory_T1)
        
        
        ################################### 
        # GRAFICA DE COMPARACION DE TIPOLOGIAS
        
        # -----------------------------------------------------
        # Generación de desplegable del nivel de comparacion
        
        # Taxonomia actual
        ind_T1 = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T1]
        
        # Generación de desplegables
        try:
            self.ui.Level_comparison_Value_1.clear()
        except:
            pass
        
        num_cols_tax_comp = len(separation_tax_name.columns) - 2
        
        for i in range(num_cols_tax_comp - 1):
            try:
                variable = variable + '/' + str(ind_T1['C'+str(i+1)].tolist()[0])
            except NameError or TypeError:
                variable = str(ind_T1['C'+str(i+1)].tolist()[0])
                
            self.ui.Level_comparison_Value_1.addItem(variable)

        # Se borra para que no haya error en la siguiente iteracion
        del variable
        
        # -----------------------------------------------------
        # Generación de grafica
        
        self.graph_comp_typologies_T1()
        
        ################################### 
        # ADICIÓN DE THETAS Y BETAS EN LA SECCIÓN DE MODIFICACION
        
        theta_list = str(round(thetas_tax_T1[0],4))
        beta_list = str(round(betas_tax_T1[0],4))
        
        for i in range(1,num_ds):
            theta_list = theta_list + ',' + str(round(thetas_tax_T1[i],4))
            beta_list = beta_list + ',' + str(round(betas_tax_T1[i],4))
            
        
        self.ui.thetaTax_value_1.setText(theta_list)
        self.ui.sigmaTax_value_1.setText(beta_list)  
            
#%% # FUNCIÓN PARA GRAFICAR TAXONOMIA 2
    # ---------------------------------------------------------------------------- 
    
    def graph_tax_T2(self):
        global IM_T2, T_T2, Tax_T2, current_param_Tax_data_T2, current_param_Build_data_T2, \
                thetas_tax_T2, betas_tax_T2, num_ds
        
        # Lectura de desplegables
        IM_T2 = self.ui.IMTax_value_2.currentText()
        T_T2 = self.ui.PeriodoTax_value_2.currentText()
        Tax_T2 = self.ui.TaxonomyTax_value_2.currentText()
        parameter_T2 = self.ui.ParamTax_value_2.currentText()
        
        self.ui.porc_fit_curves_changes_value_2.setText("1,1,1,1")
        self.ui.IM_vals_changes_value_2.setText("5,5,5,5")
        
        IM_max_graph = 10
        
        ################################### 
        # GRAFICAS DE DISPERSIÓN
        
        try:
            self.grafica_dipsersion_T2.close()
        except AttributeError:
            pass
        
        self.grafica_dipsersion_T2 = Canvas_grafica()      
        self.grafica_dipsersion_T2.ax.clear()
        
        # Data de taxonomia
        current_data = dict_data_IM_EDP_HzLv[str(T_T2)][Tax_T2]
        
        # Hazard levels
        Hzlv_curves = dict_data_IM_EDP_HzLv[str(T_T2)][Tax_T2]['Hz Lv'].unique().astype(int)
        
        # Definición de paleta de colores
        try:
            color_graphs = color_dispersion_hazard(len(Hzlv_curves))
        except UnboundLocalError:
            print('WARNING: Add more colors in the file called: Colores_Dispersion')
        
        # Gráfico   
        for HL in Hzlv_curves:
            data_aux = current_data.loc[current_data['Hz Lv'].astype(int) == HL]
            # print(data_aux)
            
            self.grafica_dipsersion_T2.ax.loglog(data_aux['IM'], data_aux['EDP'], marker = 'o', mfc = 'none',
                     mec = color_graphs[HL-1], linestyle='', label = 'Hz Lev '+ str(HL), markersize = 4)
        
        self.grafica_dipsersion_T2.ax.set_title(Tax_T2)
        self.grafica_dipsersion_T2.ax.set_ylim(0.0001, 100)
        self.grafica_dipsersion_T2.ax.set_xlim(0.01,10)
        self.grafica_dipsersion_T2.ax.set_yscale("log")
        self.grafica_dipsersion_T2.ax.set_xlabel(IM_T2 + '(T = ' + str(T_T2) + 's)', size = 10)
        self.grafica_dipsersion_T2.ax.set_ylabel('EDP', size = 10)
        self.grafica_dipsersion_T2.ax.legend(fontsize=7, loc = 'upper left')
        self.grafica_dipsersion_T2.ax.grid(which="both", alpha = 0.5)

        self.ui.graph_dispe_tax_2.addWidget(self.grafica_dipsersion_T2)
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA TODOS LOS ESTADOS DE DAÑO
        
        try:
            self.grafica_all_FC_tax_T2.close()
        except AttributeError:
            pass
        
        self.grafica_all_FC_tax_T2 = Canvas_grafica()      
        self.grafica_all_FC_tax_T2.ax.clear()
        
        
        # Data de taxonomia
        current_param_Tax_data_T2 = dict_param_taxonomy[str(T_T2)]
        current_param_Tax_data_T2 = current_param_Tax_data_T2.loc[current_param_Tax_data_T2['Taxonomy'] == Tax_T2]
        
        # Cantidad de estados de daño
        num_ds = sum(cols.startswith('Theta') for cols in current_param_Tax_data_T2.columns)
        
        # Guardado de parámetros theta y beta
        thetas_tax_T2 = []
        betas_tax_T2 = []
        
        for i in range (num_ds):
            thetas_tax_T2.append(current_param_Tax_data_T2['Theta'+str(i+1)].tolist()[0])
            betas_tax_T2.append(current_param_Tax_data_T2['Beta'+str(i+1)].tolist()[0])
            
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
        
        for i in range(num_ds):
            matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_tax_T2[i]), betas_tax_T2[i])
            
        # Puntos de ajustes de curvas
        current_points = dict_points_fragility[str(T_T2)][Tax_T2]
        
        # Grafica
        for i in range (num_ds):
            self.grafica_all_FC_tax_T2.ax.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = color[i], 
                      label = 'DS' + str(i+1) + ' - ' + r"$\theta$" +' = ' + str(round(thetas_tax_T2[i],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(betas_tax_T2[i],3)))
            self.grafica_all_FC_tax_T2.ax.plot(current_points['IM_bin'], current_points['DS' + str(i+1)], color = color[i], 
                      marker = 'o', linestyle='', markersize = 3)

        self.grafica_all_FC_tax_T2.ax.set_xlim(0, 4)
        self.grafica_all_FC_tax_T2.ax.set_xlabel(IM_T2 + '(T = ' + str(T_T2) + 's)', size = 10)
        self.grafica_all_FC_tax_T2.ax.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_all_FC_tax_T2.ax.set_title(Tax_T2)
        self.grafica_all_FC_tax_T2.ax.grid(which="both")
        self.grafica_all_FC_tax_T2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_FC_tax_2.addWidget(self.grafica_all_FC_tax_T2)
        
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        self.graph_specific_DS_tax_T2()
        
        # Data de edificaciones
        current_param_Build_data_T2 = dict_param_buildings[str(T_T2)]
        current_param_Build_data_T2 = current_param_Build_data_T2.loc[current_param_Build_data_T2['Taxonomy'] == Tax_T2]
        current_param_Build_data_T2.reset_index(level=None, drop=True, inplace=True)
        
        # buildings_list = current_param_Build_data_T2['Building'].tolist()
        
        # Vector de posiciones para boxplots
        DS_names = []
        positions_boxplot = []
        
        for i in range (num_ds):
            DS_names.append('DS'+str(i+1))
            positions_boxplot.append(str(i+1))
        positions_boxplot = np.asarray(positions_boxplot).astype(int).tolist()
        
        ################################### 
        # GRAFICA DE THETAS O BETAS
        
        try:
            self.grafica_boxplot_thetas_T2.close()
        except AttributeError:
            pass
        
        self.grafica_boxplot_thetas_T2 = Canvas_grafica()      
        self.grafica_boxplot_thetas_T2.ax.clear()
        
        # Organizacion de data en un array para introducir en boxplot
        box_plot_data = {}
        for i in range(num_ds):
            box_plot_data[parameter_T2+str(i+1)] = current_param_Build_data_T2[parameter_T2+str(i+1)]
        # Convertir los datos en una matriz y transponerla
        box_plot_data_array = np.array(list(box_plot_data.values())).T
        
        # Creacion de boxplots por taxonomia
        bp = self.grafica_boxplot_thetas_T2.ax.boxplot(box_plot_data_array, positions = positions_boxplot, patch_artist=True)
        
        # Marca el valor de beta dentro la taxonomia dentro del boxplot
        for current_index in range (num_ds):
            
            if parameter_T2 == 'Theta':
                current_parameter = thetas_tax_T2
            elif parameter_T2 == 'Beta':
                current_parameter = betas_tax_T2
                
            self.grafica_boxplot_thetas_T2.ax.scatter(current_index+1, current_parameter[current_index], marker='*', s = 100, 
                                                      color='white', edgecolor = 'k', lw = 1.2, zorder = 100)
        
        # Asignacion de colores a los boxplots
        for patch, color_i in zip(bp['boxes'], color):
            patch.set_facecolor(color_i)
            bp['medians'][color.index(color_i)].set_color('black')
        
        # Configuracion de ejes
        self.grafica_boxplot_thetas_T2.ax.set_ylim(bottom=-0.05)
        self.grafica_boxplot_thetas_T2.ax.set_title(Tax_T2)
        self.grafica_boxplot_thetas_T2.ax.set_xticks(positions_boxplot)
        self.grafica_boxplot_thetas_T2.ax.set_xticklabels(DS_names)
        if parameter_T2 == 'Theta':
            self.grafica_boxplot_thetas_T2.ax.set_ylabel(r"$\theta$")
        elif parameter_T2 == 'Beta':
            self.grafica_boxplot_thetas_T2.ax.set_ylabel(r"$\beta$")
        self.grafica_boxplot_thetas_T2.ax.grid(which="both", alpha = 0.5)
        
        self.ui.graph_theta_tax_2.addWidget(self.grafica_boxplot_thetas_T2)
        
        
        ################################### 
        # GRAFICA DE COMPARACION DE PARAMETROS
        
        try:
            self.grafica_param_bystory_T2.close()
        except AttributeError:
            pass
        
        self.grafica_param_bystory_T2 = Canvas_grafica()      
        self.grafica_param_bystory_T2.ax.clear()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T2 = dict_param_taxonomy[str(T_T2)]
        
        # Cantidad de elementos separados
        num_sep_comp = len(separation_tax_name['Taxonomy'].unique()[0].split('/'))
        
        # Taxonomia actual
        ind_current_tax = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T2]
        
        # Nombre de la taxonomia sin pisos a graficar
        filt_name = ind_current_tax['C1'].tolist()[0]
        for i in range(1, num_sep_comp - 1):
            filt_name = filt_name + '/' + str(ind_current_tax['C'+str(i+1)].tolist()[0])
            
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{filt_name}')
        
        # Data Frame filtrado para thetas y betas de taxonomia
        filt_verification = current_param_Tax_data_T2['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        taxs_to_plot = current_param_Tax_data_T2[filt_verification]
        taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        # Para cuando en el IM actual hay menos taxonomias de todas las disponibles
        separation_to_plot = separation_to_plot.loc[separation_to_plot['Taxonomy'].isin(taxs_to_plot['Taxonomy'])]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conversion de columna de pisos en enteros
        separation_to_plot.iloc[:,-1] = separation_to_plot.iloc[:,-1].astype(int)
 
        # Ordenar separation por # de pisos y ordenar tax_to_plot tambien
        separation_to_plot = separation_to_plot.sort_values(by=separation_to_plot.columns[-1])
        taxs_to_plot = taxs_to_plot.set_index('Taxonomy').loc[separation_to_plot['Taxonomy']].reset_index()
        
        num_stories = separation_to_plot.iloc[:,-1].astype(int).to_numpy()
        for i in range(num_ds):
            parameters_aux = taxs_to_plot[parameter_T2+str(i+1)]
            self.grafica_param_bystory_T2.ax.plot(num_stories, parameters_aux, 'o-', color = color[i], markersize = 3, label = "DS" + str(i+1))
        
        # self.grafica_param_bystory_T2.ax.set_ylim(bottom=-0.05)
        self.grafica_param_bystory_T2.ax.set_title(filt_name)
        self.grafica_param_bystory_T2.ax.set_xlabel('N Stories', size = 10)
        if parameter_T2 == 'Theta':
            self.grafica_param_bystory_T2.ax.set_ylabel(r"$\theta$", size = 10)
        elif parameter_T2 == 'Beta':
            self.grafica_param_bystory_T2.ax.set_ylabel(r"$\beta$", size = 10)
        self.grafica_param_bystory_T2.ax.grid(which="both", alpha = 0.5)
        self.grafica_param_bystory_T2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_theta_tax_2.addWidget(self.grafica_param_bystory_T2)
        
        
        ################################### 
        # GRAFICA DE COMPARACION DE TIPOLOGIAS
        
        # -----------------------------------------------------
        # Generación de desplegable del nivel de comparacion
        
        # Taxonomia actual
        ind_T2 = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T2]
        
        # Generación de desplegables
        try:
            self.ui.Level_comparison_Value_2.clear()
        except:
            pass
        
        num_cols_tax_comp = len(separation_tax_name.columns) - 2
        
        for i in range(num_cols_tax_comp - 1):
            try:
                variable = variable + '/' + str(ind_T2['C'+str(i+1)].tolist()[0])
            except NameError or TypeError:
                variable = str(ind_T2['C'+str(i+1)].tolist()[0])
                
            self.ui.Level_comparison_Value_2.addItem(variable)

        # Se borra para que no haya error en la siguiente iteracion
        del variable
        
        # -----------------------------------------------------
        # Generación de grafica
        
        self.graph_comp_typologies_T2()
        
        ################################### 
        # ADICIÓN DE THETAS Y BETAS EN LA SECCIÓN DE MODIFICACION
        
        theta_list = str(round(thetas_tax_T2[0],4))
        beta_list = str(round(betas_tax_T2[0],4))
        
        for i in range(1,num_ds):
            theta_list = theta_list + ',' + str(round(thetas_tax_T2[i],4))
            beta_list = beta_list + ',' + str(round(betas_tax_T2[i],4))
            
        
        self.ui.thetaTax_value_2.setText(theta_list)
        self.ui.sigmaTax_value_2.setText(beta_list)
           
#%% # FUNCIÓN PARA GRAFICAR DS ESPECIFICOS DE TAXONOMIA 1         
    # ---------------------------------------------------------------------------- 
    
    def graph_specific_DS_tax_T1(self):
        
        IM_max_graph = 10
        
        # DS actual
        current_DS = int(self.ui.DS_graph_Value_1.currentText())
        current_index = current_DS - 1
        
        # Cantidad de estados de daño
        num_ds = sum(cols.startswith('Theta') for cols in current_param_Tax_data_T1.columns)
        
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
        
        for i in range(num_ds):
            matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_tax_T1[i]), betas_tax_T1[i])
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        # En esta funcion se grafica solo el primer damage state, pero con el boton pertinente se pueden
        # cargar los demás DS
        
        try:
            self.grafica_one_FC_tax_T1.close()
        except AttributeError:
            pass
        
        self.grafica_one_FC_tax_T1 = Canvas_grafica_2()  
        self.grafica_one_FC_tax_T1.ax1.clear()
        self.grafica_one_FC_tax_T1.ax2.clear()
        
        # Data de edificaciones
        current_param_Build_data_T1 = dict_param_buildings[str(T_T1)]
        current_param_Build_data_T1 = current_param_Build_data_T1.loc[current_param_Build_data_T1['Taxonomy'] == Tax_T1]
        current_param_Build_data_T1.reset_index(level=None, drop=True, inplace=True)
        
        # ----------------------
        # Grafica de boxplots
        
        self.grafica_one_FC_tax_T1.ax1.boxplot(current_param_Build_data_T1['Theta'+str(current_index+1)], vert=False, 
                      patch_artist=True, boxprops=dict(facecolor=color[current_index], color='black'),
                      medianprops=dict(color='black'))
        self.grafica_one_FC_tax_T1.ax1.grid(which="both", alpha = 0.5)
        
        # Marca el valor de theta de la taxonomia dentro del boxplot
        self.grafica_one_FC_tax_T1.ax1.scatter(thetas_tax_T1[current_index], 1, marker='*', s = 50, color='white', edgecolor = 'k', lw = 0.75, 
                      zorder = 100, label = r"$\theta$ Taxonomy") 
        self.grafica_one_FC_tax_T1.ax1.legend(fontsize=7, loc = 'lower right')
        
        # ----------------------
        # Grafica la curva de fragilidad de la taxonomia
        self.grafica_one_FC_tax_T1.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(current_index+1)], color = color[current_index], 
                  label = 'DS' + str(current_index+1) + ' - ' + r"$\theta$ = " + str(round(thetas_tax_T1[current_index],3)) + '  ' + 
                  r"$\beta$"+' = ' + str(round(betas_tax_T1[current_index],3)))
        
        self.grafica_one_FC_tax_T1.ax2.set_xlim(0, 2.5)
        self.grafica_one_FC_tax_T1.ax2.set_ylim(-0.05, 1.05)
        self.grafica_one_FC_tax_T1.ax2.set_title(Tax_T1)
        self.grafica_one_FC_tax_T1.ax2.set_xlabel(IM_T1 + '(T = ' + str(T_T1) + 's)', size = 10)
        self.grafica_one_FC_tax_T1.ax2.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_one_FC_tax_T1.ax2.grid(which="both", alpha = 0.5)
        self.grafica_one_FC_tax_T1.ax2.legend(fontsize=7, loc = 'lower right')
        
        # ----------------------
        # Grafica la curva de fragilidad de cada edificacion
        
        buildings_list = current_param_Build_data_T1['Building'].tolist()
        
        # Vector de posiciones para boxplots
        DS_names = []
        positions_boxplot = []
        
        for i in range (num_ds):
            DS_names.append('DS'+str(i+1))
            positions_boxplot.append(str(i+1))
        positions_boxplot = np.asarray(positions_boxplot).astype(int).tolist()
        
        # Loop para edifciaciones dentro de una misma taxonomia
        for current_building in buildings_list:
            
            current_building = current_param_Build_data_T1.loc[current_param_Build_data_T1['Building'] == current_building]
            
            # Guardado de parámetros theta y beta
            thetas_build = []
            betas_build = []
            
            for i in range (num_ds):
                thetas_build.append(current_building['Theta'+str(i+1)].tolist()[0])
                betas_build.append(current_building['Beta'+str(i+1)].tolist()[0])
            
            # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
            delta_im = 0.001 # Delta para graficar
            matriz_plot = pd.DataFrame()
            IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
            matriz_plot['IM'] =  IM_plot
            
            for i in range(num_ds):
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_build[i]), betas_build[i])
                
            self.grafica_one_FC_tax_T1.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(current_index+1)], color = color[current_index], alpha = 0.2)
        
        self.ui.graph_FCS_tax_1.addWidget(self.grafica_one_FC_tax_T1)

#%% # FUNCIÓN PARA GRAFICAR DS ESPECIFICOS DE TAXONOMIA 2        
    # ---------------------------------------------------------------------------- 
    
    def graph_specific_DS_tax_T2(self):
        
        IM_max_graph = 10
        
        # DS actual
        current_DS = int(self.ui.DS_graph_Value_2.currentText())
        current_index = current_DS - 1
        
        # Cantidad de estados de daño
        num_ds = sum(cols.startswith('Theta') for cols in current_param_Tax_data_T2.columns)
        
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
        
        for i in range(num_ds):
            matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_tax_T2[i]), betas_tax_T2[i])
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        # En esta funcion se grafica solo el primer damage state, pero con el boton pertinente se pueden
        # cargar los demás DS
        
        try:
            self.grafica_one_FC_tax_T2.close()
        except AttributeError:
            pass
        
        self.grafica_one_FC_tax_T2 = Canvas_grafica_2()  
        self.grafica_one_FC_tax_T2.ax1.clear()
        self.grafica_one_FC_tax_T2.ax2.clear()
        
        # Data de edificaciones
        current_param_Build_data_T2 = dict_param_buildings[str(T_T2)]
        current_param_Build_data_T2 = current_param_Build_data_T2.loc[current_param_Build_data_T2['Taxonomy'] == Tax_T2]
        current_param_Build_data_T2.reset_index(level=None, drop=True, inplace=True)
        
        # ----------------------
        # Grafica de boxplots
        
        self.grafica_one_FC_tax_T2.ax1.boxplot(current_param_Build_data_T2['Theta'+str(current_index+1)], vert=False, 
                      patch_artist=True, boxprops=dict(facecolor=color[current_index], color='black'),
                      medianprops=dict(color='black'))
        self.grafica_one_FC_tax_T2.ax1.grid(which="both", alpha = 0.5)
        
        # Marca el valor de theta de la taxonomia dentro del boxplot
        self.grafica_one_FC_tax_T2.ax1.scatter(thetas_tax_T2[current_index], 1, marker='*', s = 50, color='white', edgecolor = 'k', lw = 0.75, 
                      zorder = 100, label = r"$\theta$ Taxonomy") 
        self.grafica_one_FC_tax_T2.ax1.legend(fontsize=7, loc = 'lower right')
        
        # ----------------------
        # Grafica la curva de fragilidad de la taxonomia
        self.grafica_one_FC_tax_T2.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(current_index+1)], color = color[current_index], 
                  label = 'DS' + str(current_index+1) + ' - ' + r"$\theta$ = " + str(round(thetas_tax_T2[current_index],3)) + '  ' + 
                  r"$\beta$"+' = ' + str(round(betas_tax_T2[current_index],3)))
        
        self.grafica_one_FC_tax_T2.ax2.set_xlim(0, 2.5)
        self.grafica_one_FC_tax_T2.ax2.set_ylim(-0.05, 1.05)
        self.grafica_one_FC_tax_T2.ax2.set_title(Tax_T2)
        self.grafica_one_FC_tax_T2.ax2.set_xlabel(IM_T2 + '(T = ' + str(T_T2) + 's)', size = 10)
        self.grafica_one_FC_tax_T2.ax2.set_ylabel('P(DS >= ds)', size = 10)
        self.grafica_one_FC_tax_T2.ax2.grid(which="both", alpha = 0.5)
        self.grafica_one_FC_tax_T2.ax2.legend(fontsize=7, loc = 'lower right')
        
        # ----------------------
        # Grafica la curva de fragilidad de cada edificacion
        
        buildings_list = current_param_Build_data_T2['Building'].tolist()
        
        # Vector de posiciones para boxplots
        DS_names = []
        positions_boxplot = []
        
        for i in range (num_ds):
            DS_names.append('DS'+str(i+1))
            positions_boxplot.append(str(i+1))
        positions_boxplot = np.asarray(positions_boxplot).astype(int).tolist()
        
        # Loop para edifciaciones dentro de una misma taxonomia
        for current_building in buildings_list:
            
            current_building = current_param_Build_data_T2.loc[current_param_Build_data_T2['Building'] == current_building]
            
            # Guardado de parámetros theta y beta
            thetas_build = []
            betas_build = []

            for i in range (num_ds):
                thetas_build.append(current_building['Theta'+str(i+1)].tolist()[0])
                betas_build.append(current_building['Beta'+str(i+1)].tolist()[0])
            
            # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
            delta_im = 0.001 # Delta para graficar
            matriz_plot = pd.DataFrame()
            IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
            matriz_plot['IM'] =  IM_plot
            
            for i in range(num_ds):
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(thetas_build[i]), betas_build[i])
                
            self.grafica_one_FC_tax_T2.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(current_index+1)], color = color[current_index], alpha = 0.2)
        
        self.ui.graph_FCS_tax_2.addWidget(self.grafica_one_FC_tax_T2)
        
#%% # FUNCIÓN PARA GRAFICAR COMPARACIÓN DE TIPOLOGIAS DE TAXONOMIA 1        
    # ----------------------------------------------------------------------------
    
    def graph_comp_typologies_T1(self):
        
        # Lectura de desplegables
        level_comp_T1 = self.ui.Level_comparison_Value_1.currentText()
        current_DS_T1 = self.ui.DS_graph_com_Value_1.currentText()
        parameter_T1 = self.ui.ParamTax_value_1.currentText()
        
        # Inicializacion de la grafica
        try:
            self.grafica_param_bytyp_T1.close()
        except AttributeError:
            pass
        
        self.grafica_param_bytyp_T1 = Canvas_grafica()      
        self.grafica_param_bytyp_T1.ax.clear()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T1 = dict_param_taxonomy[str(T_T1)]
        
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{level_comp_T1}')
        
        # Data Frame filtrado para thetas y betas de taxonomia
        filt_verification = current_param_Tax_data_T1['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        taxs_to_plot = current_param_Tax_data_T1[filt_verification]
        taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conteo de la cantidad de tipologias (taxonomias sin tener en cuenta num de pisos)
        list_typology = separation_to_plot['Tax_No_stories'].unique().tolist()
        
        for i in range(len(list_typology)):
            
            # Se realiza la busqueda de una sola tipologia para todos los pisos
            current_patron = re.compile(rf'{list_typology[i]}')
            
            # thetas y betas
            filt_verification = current_param_Tax_data_T1['Taxonomy'].apply(lambda x: bool(current_patron.search(x)))
            current_taxs_to_plot = current_param_Tax_data_T1[filt_verification]
            current_taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
            
            # separacion de taxonomias
            filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(current_patron.search(x)))
            current_separation_to_plot = separation_tax_name[filt_verification_2]
            # Para cuando en el IM actual hay menos taxonomias de todas las disponibles
            current_separation_to_plot = current_separation_to_plot.loc[current_separation_to_plot['Taxonomy'].isin( current_taxs_to_plot['Taxonomy'])]
            current_separation_to_plot.reset_index(level=None, drop=True, inplace=True)
            
            # Conversion de columna de pisos en enteros
            current_separation_to_plot.iloc[:,-1] = current_separation_to_plot.iloc[:,-1].astype(int)
            
            # Ordenar current_separation por # de pisos y ordenar current_tax_to_plot tambien
            current_separation_to_plot = current_separation_to_plot.sort_values(by=current_separation_to_plot.columns[-1])
            current_taxs_to_plot = current_taxs_to_plot.set_index('Taxonomy').loc[current_separation_to_plot['Taxonomy']].reset_index()
            
            # numero de pisos
            num_stories = current_separation_to_plot.iloc[:,-1].astype(int).to_numpy()
            parameters_aux = current_taxs_to_plot[parameter_T1+str(current_DS_T1)]
            
            self.grafica_param_bytyp_T1.ax.plot(num_stories, parameters_aux, 'o-', color = color_py[i], markersize = 3, label = list_typology[i])
        
        # self.grafica_param_bytyp_T1.ax.set_ylim(bottom=-0.05)
        self.grafica_param_bytyp_T1.ax.set_title(level_comp_T1)
        self.grafica_param_bytyp_T1.ax.set_xlabel('N Stories', size = 10)
        if parameter_T1 == 'Theta':
            self.grafica_param_bytyp_T1.ax.set_ylabel(r"$\theta$"+str(current_DS_T1), size = 10)
        elif parameter_T1 == 'Beta':
            self.grafica_param_bytyp_T1.ax.set_ylabel(r"$\beta$"+str(current_DS_T1), size = 10)
        self.grafica_param_bytyp_T1.ax.grid(which="both", alpha = 0.5)
        self.grafica_param_bytyp_T1.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_typ_tax_1.addWidget(self.grafica_param_bytyp_T1)

#%% # FUNCIÓN PARA GRAFICAR COMPARACIÓN DE TIPOLOGIAS DE TAXONOMIA 2   
    
    def graph_comp_typologies_T2(self):
        
        # Lectura de desplegables
        level_comp_T2 = self.ui.Level_comparison_Value_2.currentText()
        current_DS_T2 = self.ui.DS_graph_com_Value_2.currentText()
        parameter_T2 = self.ui.ParamTax_value_2.currentText()
        
        # Inicializacion de la grafica
        try:
            self.grafica_param_bytyp_T2.close()
        except AttributeError:
            pass
        
        self.grafica_param_bytyp_T2 = Canvas_grafica()      
        self.grafica_param_bytyp_T2.ax.clear()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T2 = dict_param_taxonomy[str(T_T2)]
        
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{level_comp_T2}')
        
        # Data Frame filtrado para thetas y betas de taxonomia
        filt_verification = current_param_Tax_data_T2['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        taxs_to_plot = current_param_Tax_data_T2[filt_verification]
        taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conteo de la cantidad de tipologias (taxonomias sin tener en cuenta num de pisos)
        list_typology = separation_to_plot['Tax_No_stories'].unique().tolist()
        
        for i in range(len(list_typology)):
            
            # Se realiza la busqueda de una sola tipologia para todos los pisos
            current_patron = re.compile(rf'{list_typology[i]}')
            
            # thetas y betas
            filt_verification = current_param_Tax_data_T2['Taxonomy'].apply(lambda x: bool(current_patron.search(x)))
            current_taxs_to_plot = current_param_Tax_data_T2[filt_verification]
            current_taxs_to_plot.reset_index(level=None, drop=True, inplace=True)
            
            # separacion de taxonomias
            filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(current_patron.search(x)))
            current_separation_to_plot = separation_tax_name[filt_verification_2]
            # Para cuando en el IM actual hay menos taxonomias de todas las disponibles
            current_separation_to_plot = current_separation_to_plot.loc[current_separation_to_plot['Taxonomy'].isin( current_taxs_to_plot['Taxonomy'])]
            current_separation_to_plot.reset_index(level=None, drop=True, inplace=True)
            
            # Conversion de columna de pisos en enteros
            current_separation_to_plot.iloc[:,-1] = current_separation_to_plot.iloc[:,-1].astype(int)
            
            # Ordenar current_separation por # de pisos y ordenar current_tax_to_plot tambien
            current_separation_to_plot = current_separation_to_plot.sort_values(by=current_separation_to_plot.columns[-1])
            current_taxs_to_plot = current_taxs_to_plot.set_index('Taxonomy').loc[current_separation_to_plot['Taxonomy']].reset_index()
            
            # numero de pisos
            num_stories = current_separation_to_plot.iloc[:,-1].astype(int).to_numpy()
            parameters_aux = current_taxs_to_plot[parameter_T2+str(current_DS_T2)]
            
            self.grafica_param_bytyp_T2.ax.plot(num_stories, parameters_aux, 'o-', color = color_py[i], markersize = 3, label = list_typology[i])
        
        # self.grafica_param_bytyp_T2.ax.set_ylim(bottom=-0.05)
        self.grafica_param_bytyp_T2.ax.set_title(level_comp_T2)
        self.grafica_param_bytyp_T2.ax.set_xlabel('N Stories', size = 10)
        if parameter_T2 == 'Theta':
            self.grafica_param_bytyp_T2.ax.set_ylabel(r"$\theta$"+str(current_DS_T2), size = 10)
        elif parameter_T2 == 'Beta':
            self.grafica_param_bytyp_T2.ax.set_ylabel(r"$\beta$"+str(current_DS_T2), size = 10)
        self.grafica_param_bytyp_T2.ax.grid(which="both", alpha = 0.5)
        self.grafica_param_bytyp_T2.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_typ_tax_2.addWidget(self.grafica_param_bytyp_T2)
        
#%% # FUNCIÓN PARA HACER MODIFICACIONES DE TAXONOMIA 1   
    # ---------------------------------------------------------------------------- 
    
    def graph_mod_typologies_T1(self):
        global new_thetas_T1, new_betas_T1
        
        # Lectura de inputs
        change_type_T1 = self.ui.changeType_value_1.currentText()
        parameter_T1 = self.ui.ParamTax_value_1.currentText()
        level_comp_T1 = self.ui.Level_comparison_Value_1.currentText()
        current_DS_T1 = self.ui.DS_graph_com_Value_1.currentText()
        
        if change_type_T1 == 'Parameters':
        
            new_thetas_T1 = self.ui.thetaTax_value_1.text()
            new_thetas_T1 = np.asarray(new_thetas_T1.split(",")).astype(float)
            
            new_betas_T1 = self.ui.sigmaTax_value_1.text()
            new_betas_T1 = np.asarray(new_betas_T1.split(",")).astype(float)
            
            num_ds = len(new_thetas_T1)
        
        elif change_type_T1 == '% curves fitting':
            
            new_porc_fit = self.ui.porc_fit_curves_changes_value_1.text()
            new_porc_fit = np.asarray(new_porc_fit.split(",")).astype(float)
            
            num_ds = len(new_porc_fit)
            
        elif change_type_T1 == 'IM limits':
            
            new_IM_limits = self.ui.IM_vals_changes_value_1.text()
            new_IM_limits = np.asarray(new_IM_limits.split(",")).astype(float)
            
            num_ds = len(new_IM_limits)
        
        IM_max_graph = 10
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA TODOS LOS ESTADOS DE DAÑO
        
        # Puntos de ajustes de curvas
        current_points = dict_points_fragility[str(T_T1)][Tax_T1]
        
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
              
       
        if change_type_T1 == 'Parameters':
            
            for i in range(num_ds):
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(new_thetas_T1[i]), new_betas_T1[i])
            
        elif change_type_T1 == '% curves fitting' or change_type_T1 == 'IM limits':
            
            # Puntos que generan los DS
            DS_IM_data = dict_points_fragility[str(T_T1)][Tax_T1]
            
            # Generacion de vedctor de parámetros
            new_thetas_T1 = np.array([])
            new_betas_T1 = np.array([])
            
            # ---------------------------------------------------------------
            # Creación de la matriz fragility de la forma IM_BIN - N - Zi
            fragility = pd.DataFrame()
            fragility['IM_bin'] =  current_points['IM_bin']
            fragility['N'] = 100

            # Estimación de Zi
            for k in range(num_ds):
                fragility['Zi - DS' + str(k+1)] =  round(DS_IM_data['DS' + str(k+1)]*100)
                
            # ---------------------------------------------------------------
            # Cálculo de parámetros de curvas de fragilidad
    
            for i in range(num_ds):
                
                # Data a ajustar
                Y = pd.DataFrame()
                Y['Zi'] = fragility['Zi - DS' + str(i+1)]
                Y['N-Zi'] = fragility['N'] - fragility['Zi - DS' + str(i+1)]
                Y['IM_bin'] = fragility['IM_bin']
                
                # --------------------------------------------------------------------
                # Determinación de los valores de los puntos que se tendrán en cuenta para estimar los parámetros
                
                Y2 = Y.copy()
                fragility2 = fragility.copy()
                
                # Selección de data que no se tendrá en cuenta dependiendo del tipo de ajuste
                if change_type_T1 == '% curves fitting':
                
                    current_porc = new_porc_fit[i]
                    
                    ind = Y.loc[Y['Zi'] <= current_porc*100]
                    lista_index = list(ind.index)
                            
                elif change_type_T1 == 'IM limits':
                    
                    current_IM_limit = new_IM_limits[i]
                    
                    ind = Y.loc[Y['IM_bin'] <= current_IM_limit]
                    lista_index = list(ind.index)
                
                # Eliminación de data que no se tendrá en cuenta
                for k in Y.index.tolist():
                    if k in lista_index:
                        pass
                    else:
                        Y2.drop(k, axis=0, inplace=True)
                        fragility2.drop(k, axis=0, inplace=True)
                        
                # Se borra la columna de IM_bin de Y2 para poder usar la funcion glm_binom
                Y2 = Y2.drop('IM_bin', axis = 1)
                
                # --------------------------------------------------------------------
                # Ajuste de curvas
                sm_probit_Link = sm.genmod.families.links.probit
                x = np.log(fragility2['IM_bin'])
                glm_binom = sm.GLM(Y2, sm.add_constant(x), family=sm.families.Binomial(link=sm_probit_Link()))
                
                glm_result = glm_binom.fit()
                weights_py = glm_result.params
                
                # Conversion de coeficientes probit a parámetros de la distribucion lognormal
                sigma_ln = 1/weights_py[1]
                mu_ln = -weights_py[0]/weights_py[1]
                
                # Guardado de los parámetros
                new_thetas_T1 = np.append(new_thetas_T1, np.exp(mu_ln))
                new_betas_T1 = np.append(new_betas_T1, sigma_ln)
                
                # Matriz de graficas
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), mu_ln, sigma_ln)
                
            # --------------------------------------------------------------------
            # Modificacion del texto de thetas y betas
            
            theta_list = str(round(new_thetas_T1[0],4))
            beta_list = str(round(new_betas_T1[0],4))
            
            for i in range(1,num_ds):
                
                theta_list = theta_list + ',' + str(round(new_thetas_T1[i],4))
                beta_list = beta_list + ',' + str(round(new_betas_T1[i],4))
                
            self.ui.thetaTax_value_1.setText(theta_list)
            self.ui.sigmaTax_value_1.setText(beta_list)
                        
        # Grafica
        for i in range (num_ds):
            self.grafica_all_FC_tax_T1.ax.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = color[i], linestyle = 'dashed',
                      label = 'DS_Mod' + str(i+1) + ' - ' + r"$\theta$" +' = ' + str(round(new_thetas_T1[i],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(new_betas_T1[i],3)))
            
        # self.grafica_all_FC_tax_T1.ax.legend()
        
        # Actualizar la gráfica en tu GUI
        self.grafica_all_FC_tax_T1.draw()
        
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        # Se corre inicialmente la funcion para que lea la selección del ds
        self.graph_specific_DS_tax_T1()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T1 = dict_param_taxonomy[str(T_T1)]
        current_param_Tax_data_T1 = current_param_Tax_data_T1.loc[current_param_Tax_data_T1['Taxonomy'] == Tax_T1]
        
        # DS actual de la figura
        current_DS = int(self.ui.DS_graph_Value_1.currentText())
        current_index = current_DS - 1
        
        for i in range(num_ds):
            
            original_param_i = current_param_Tax_data_T1['Theta'+str(i+1)].tolist()[0]      # Parametro original
            cur_param_i = new_thetas_T1[i]                                                  # Parametro nuevo
            
            
            if round(original_param_i,2) != round(cur_param_i,2) and current_DS == i+1:
                
                # ----------------------
                # Grafica de boxplots: Marca el valor de theta de la taxonomia
                self.grafica_one_FC_tax_T1.ax1.scatter(cur_param_i, 1, marker='D', s = 30, color='white', edgecolor = 'k', lw = 0.75, 
                              zorder = 101, label = r"$\theta$Mod Taxonomy") 
                self.grafica_one_FC_tax_T1.ax1.legend(fontsize='small')
            
                # ----------------------
                # Grafica la curva de fragilidad de la taxonomia
                self.grafica_one_FC_tax_T1.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = 'black', linestyle = 'dashed', 
                          label = 'DS_Mod' + str(i+1) + ' - ' + r"$\theta$ = " + str(round(new_thetas_T1[i],3)) + '  ' + 
                          r"$\beta$"+' = ' + str(round(new_betas_T1[i],3)))
                self.grafica_one_FC_tax_T1.ax2.legend(fontsize='small')
        
        # Actualizar la gráfica en tu GUI
        self.grafica_one_FC_tax_T1.draw()
        
        
        ################################### 
        # GRAFICA DE THETAS O BETAS
        
        for i in range(num_ds):
            
            if parameter_T1 == 'Theta':
                original_param_i = current_param_Tax_data_T1['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T1[i]                                                  # Parametro nuevo
                
            elif parameter_T1 == 'Beta':
                original_param_i = current_param_Tax_data_T1['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T1[i]                                                  # Parametro nuevo
            
            if round(original_param_i,2) != round(cur_param_i,2):
                self.grafica_boxplot_thetas_T1.ax.scatter(i+1, cur_param_i, marker='D', s = 30, 
                                                  color='white', edgecolor = 'k', lw = 1.2, zorder = 101)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_boxplot_thetas_T1.draw()
        
        ################################### 
        # GRAFICA DE COMPARACION DE PARAMETROS
        
        # Taxonomia actual
        ind_current_tax = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T1]
        current_story = ind_current_tax.iloc[:,-1].astype(int).to_numpy()
        
        for i in range(num_ds):
            
            if parameter_T1 == 'Theta':
                original_param_i = current_param_Tax_data_T1['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T1[i]                                                  # Parametro nuevo
                
            elif parameter_T1 == 'Beta':
                original_param_i = current_param_Tax_data_T1['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T1[i]                                                   # Parametro nuevo
            
            if round(original_param_i,2) != round(cur_param_i,2):
                self.grafica_param_bystory_T1.ax.plot(current_story, cur_param_i, 'o', color = color[i], markersize = 5)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_param_bystory_T1.draw()
        
        ################################### 
        # GRAFICA DE COMPARACION DE TIPOLOGIAS
        
        # Se corre inicialmente la funcion para que lea la selección del ds
        self.graph_comp_typologies_T1()
        
        # DS actual de la grafica
        current_DS = int(self.ui.DS_graph_com_Value_1.currentText())
        
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{level_comp_T1}')
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conteo de la cantidad de tipologias (taxonomias sin tener en cuenta num de pisos)
        list_typology = separation_to_plot['Tax_No_stories'].unique().tolist()
        
        # Taxonomia sin piso actual
        current_sep = ind_current_tax['Tax_No_stories'].tolist()[0]
        
        for i in range(len(list_typology)):
            
            if current_sep == list_typology[i]:
                # Color de la gráfica
                current_color = color_py[i]
        
        for i in range(num_ds):
                
            if parameter_T1 == 'Theta':
                original_param_i = current_param_Tax_data_T1['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T1[i]                                                  # Parametro nuevo
                
            elif parameter_T1 == 'Beta':
                original_param_i = current_param_Tax_data_T1['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T1[i]                                               # Parametro nuevo
        
            if round(original_param_i,2) != round(cur_param_i,2) and current_DS == i+1:
                self.grafica_param_bytyp_T1.ax.plot(current_story, cur_param_i, 'o', color = current_color, markersize = 5)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_param_bytyp_T1.draw()
        
#%% # FUNCIÓN PARA HACER MODIFICACIONES DE TAXONOMIA 2
    # ---------------------------------------------------------------------------- 
    
    def graph_mod_typologies_T2(self):
        global new_thetas_T2, new_betas_T2
        
        # Lectura de inputs
        change_type_T2 = self.ui.changeType_value_2.currentText()
        parameter_T2 = self.ui.ParamTax_value_2.currentText()
        level_comp_T2 = self.ui.Level_comparison_Value_2.currentText()
        current_DS_T2 = self.ui.DS_graph_com_Value_2.currentText()
        
        if change_type_T2 == 'Parameters':
        
            new_thetas_T2 = self.ui.thetaTax_value_2.text()
            new_thetas_T2 = np.asarray(new_thetas_T2.split(",")).astype(float)
            
            new_betas_T2 = self.ui.sigmaTax_value_2.text()
            new_betas_T2 = np.asarray(new_betas_T2.split(",")).astype(float)
            
            num_ds = len(new_thetas_T2)
        
        elif change_type_T2 == '% curves fitting':
            
            new_porc_fit = self.ui.porc_fit_curves_changes_value_2.text()
            new_porc_fit = np.asarray(new_porc_fit.split(",")).astype(float)
            
            num_ds = len(new_porc_fit)
            
        elif change_type_T2 == 'IM limits':
            
            new_IM_limits = self.ui.IM_vals_changes_value_2.text()
            new_IM_limits = np.asarray(new_IM_limits.split(",")).astype(float)
            
            num_ds = len(new_IM_limits)
        
        IM_max_graph = 10
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA TODOS LOS ESTADOS DE DAÑO
        
        # Puntos de ajustes de curvas
        current_points = dict_points_fragility[str(T_T2)][Tax_T2]
        
        # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva
        delta_im = 0.001 # Delta para graficar
        matriz_plot = pd.DataFrame()
        IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)
        matriz_plot['IM'] =  IM_plot
              
       
        if change_type_T2 == 'Parameters':
            
            for i in range(num_ds):
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), np.log(new_thetas_T2[i]), new_betas_T2[i])
            
        elif change_type_T2 == '% curves fitting' or change_type_T2 == 'IM limits':
            
            # Puntos que generan los DS
            DS_IM_data = dict_points_fragility[str(T_T2)][Tax_T2]
            
            # Generacion de vedctor de parámetros
            new_thetas_T2 = np.array([])
            new_betas_T2 = np.array([])
            
            # ---------------------------------------------------------------
            # Creación de la matriz fragility de la forma IM_BIN - N - Zi
            fragility = pd.DataFrame()
            fragility['IM_bin'] =  current_points['IM_bin']
            fragility['N'] = 100

            # Estimación de Zi
            for k in range(num_ds):
                fragility['Zi - DS' + str(k+1)] =  round(DS_IM_data['DS' + str(k+1)]*100)
                
            # ---------------------------------------------------------------
            # Cálculo de parámetros de curvas de fragilidad
    
            for i in range(num_ds):
                
                # Data a ajustar
                Y = pd.DataFrame()
                Y['Zi'] = fragility['Zi - DS' + str(i+1)]
                Y['N-Zi'] = fragility['N'] - fragility['Zi - DS' + str(i+1)]
                Y['IM_bin'] = fragility['IM_bin']
                
                # --------------------------------------------------------------------
                # Determinación de los valores de los puntos que se tendrán en cuenta para estimar los parámetros
                
                Y2 = Y.copy()
                fragility2 = fragility.copy()
                
                # Selección de data que no se tendrá en cuenta dependiendo del tipo de ajuste
                if change_type_T2 == '% curves fitting':
                
                    current_porc = new_porc_fit[i]
                    
                    ind = Y.loc[Y['Zi'] <= current_porc*100]
                    lista_index = list(ind.index)
                            
                elif change_type_T2 == 'IM limits':
                    
                    current_IM_limit = new_IM_limits[i]
                    
                    ind = Y.loc[Y['IM_bin'] <= current_IM_limit]
                    lista_index = list(ind.index)
                
                # Eliminación de data que no se tendrá en cuenta
                for k in Y.index.tolist():
                    if k in lista_index:
                        pass
                    else:
                        Y2.drop(k, axis=0, inplace=True)
                        fragility2.drop(k, axis=0, inplace=True)
                        
                # Se borra la columna de IM_bin de Y2 para poder usar la funcion glm_binom
                Y2 = Y2.drop('IM_bin', axis = 1)
                
                # --------------------------------------------------------------------
                # Ajuste de curvas
                sm_probit_Link = sm.genmod.families.links.probit
                x = np.log(fragility2['IM_bin'])
                glm_binom = sm.GLM(Y2, sm.add_constant(x), family=sm.families.Binomial(link=sm_probit_Link()))
                
                glm_result = glm_binom.fit()
                weights_py = glm_result.params
                
                # Conversion de coeficientes probit a parámetros de la distribucion lognormal
                sigma_ln = 1/weights_py[1]
                mu_ln = -weights_py[0]/weights_py[1]
                
                # Guardado de los parámetros
                new_thetas_T2 = np.append(new_thetas_T2, np.exp(mu_ln))
                new_betas_T2 = np.append(new_betas_T2, sigma_ln)
                
                # Matriz de graficas
                matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), mu_ln, sigma_ln)
                
            # --------------------------------------------------------------------
            # Modificacion del texto de thetas y betas
            
            theta_list = str(round(new_thetas_T2[0],4))
            beta_list = str(round(new_betas_T2[0],4))
            
            for i in range(1,num_ds):
                
                theta_list = theta_list + ',' + str(round(new_thetas_T2[i],4))
                beta_list = beta_list + ',' + str(round(new_betas_T2[i],4))
                
            self.ui.thetaTax_value_1.setText(theta_list)
            self.ui.sigmaTax_value_1.setText(beta_list)
                        
        # Grafica
        for i in range (num_ds):
            self.grafica_all_FC_tax_T2.ax.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = color[i], linestyle = 'dashed',
                      label = 'DS_Mod' + str(i+1) + ' - ' + r"$\theta$" +' = ' + str(round(new_thetas_T2[i],3)) + '  ' +
                      r"$\beta$"+' = ' + str(round(new_betas_T2[i],3)))
            
        # self.grafica_all_FC_tax_T2.ax.legend()
        
        # Actualizar la gráfica en tu GUI
        self.grafica_all_FC_tax_T2.draw()
        
        
        ################################### 
        # CURVAS DE FRAGILIDAD PARA CADA ESTADO DE DAÑO
        
        # Se corre inicialmente la funcion para que lea la selección del ds
        self.graph_specific_DS_tax_T2()
        
        # Data Frame con las taxonomias del periodo seleccionado
        current_param_Tax_data_T2 = dict_param_taxonomy[str(T_T2)]
        current_param_Tax_data_T2 = current_param_Tax_data_T2.loc[current_param_Tax_data_T2['Taxonomy'] == Tax_T2]
        
        # DS actual de la figura
        current_DS = int(self.ui.DS_graph_Value_2.currentText())
        current_index = current_DS - 1
        
        for i in range(num_ds):
            
            original_param_i = current_param_Tax_data_T2['Theta'+str(i+1)].tolist()[0]      # Parametro original
            cur_param_i = new_thetas_T2[i]                                                  # Parametro nuevo
            
            
            if round(original_param_i,2) != round(cur_param_i,2) and current_DS == i+1:
                
                # ----------------------
                # Grafica de boxplots: Marca el valor de theta de la taxonomia
                self.grafica_one_FC_tax_T2.ax1.scatter(cur_param_i, 1, marker='D', s = 30, color='white', edgecolor = 'k', lw = 0.75, 
                              zorder = 101, label = r"$\theta$Mod Taxonomy") 
                self.grafica_one_FC_tax_T2.ax1.legend(fontsize='small')
            
                # ----------------------
                # Grafica la curva de fragilidad de la taxonomia
                self.grafica_one_FC_tax_T2.ax2.plot(matriz_plot['IM'], matriz_plot['DS'+str(i+1)], color = 'black', linestyle = 'dashed', 
                          label = 'DS_Mod' + str(i+1) + ' - ' + r"$\theta$ = " + str(round(new_thetas_T2[i],3)) + '  ' + 
                          r"$\beta$"+' = ' + str(round(new_betas_T2[i],3)))
                self.grafica_one_FC_tax_T2.ax2.legend(fontsize='small')
        
        # Actualizar la gráfica en tu GUI
        self.grafica_one_FC_tax_T2.draw()
        
        
        ################################### 
        # GRAFICA DE THETAS O BETAS
        
        for i in range(num_ds):
            
            if parameter_T2 == 'Theta':
                original_param_i = current_param_Tax_data_T2['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T2[i]                                                  # Parametro nuevo
                
            elif parameter_T2 == 'Beta':
                original_param_i = current_param_Tax_data_T2['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T2[i]                                                  # Parametro nuevo
            
            if round(original_param_i,2) != round(cur_param_i,2):
                self.grafica_boxplot_thetas_T2.ax.scatter(i+1, cur_param_i, marker='D', s = 30, 
                                                  color='white', edgecolor = 'k', lw = 1.2, zorder = 101)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_boxplot_thetas_T2.draw()
        
        ################################### 
        # GRAFICA DE COMPARACION DE PARAMETROS
        
        # Taxonomia actual
        ind_current_tax = separation_tax_name.loc[separation_tax_name['Taxonomy'] == Tax_T2]
        current_story = ind_current_tax.iloc[:,-1].astype(int).to_numpy()
        
        for i in range(num_ds):
            
            if parameter_T2 == 'Theta':
                original_param_i = current_param_Tax_data_T2['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T2[i]                                                  # Parametro nuevo
                
            elif parameter_T2 == 'Beta':
                original_param_i = current_param_Tax_data_T2['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T2[i]                                                   # Parametro nuevo
            
            if round(original_param_i,2) != round(cur_param_i,2):
                self.grafica_param_bystory_T2.ax.plot(current_story, cur_param_i, 'o', color = color[i], markersize = 5)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_param_bystory_T2.draw()
        
        ################################### 
        # GRAFICA DE COMPARACION DE TIPOLOGIAS
        
        # Se corre inicialmente la funcion para que lea la selección del ds
        self.graph_comp_typologies_T2()
        
        # DS actual de la grafica
        current_DS = int(self.ui.DS_graph_com_Value_2.currentText())
        
        # Patron de filtrado
        patron_busqueda = re.compile(rf'{level_comp_T2}')
        
        # Data Frame filtrado para separacion que contiene numero de pisos
        filt_verification_2 = separation_tax_name['Taxonomy'].apply(lambda x: bool(patron_busqueda.search(x)))
        separation_to_plot = separation_tax_name[filt_verification_2]
        separation_to_plot.reset_index(level=None, drop=True, inplace=True)
        
        # Conteo de la cantidad de tipologias (taxonomias sin tener en cuenta num de pisos)
        list_typology = separation_to_plot['Tax_No_stories'].unique().tolist()
        
        # Taxonomia sin piso actual
        current_sep = ind_current_tax['Tax_No_stories'].tolist()[0]
        
        for i in range(len(list_typology)):
            
            if current_sep == list_typology[i]:
                # Color de la gráfica
                current_color = color_py[i]
        
        for i in range(num_ds):
                
            if parameter_T2 == 'Theta':
                original_param_i = current_param_Tax_data_T2['Theta'+str(i+1)].tolist()[0]      # Parametro original
                cur_param_i = new_thetas_T2[i]                                                  # Parametro nuevo
                
            elif parameter_T2 == 'Beta':
                original_param_i = current_param_Tax_data_T2['Beta'+str(i+1)].tolist()[0]       # Parametro original
                cur_param_i = new_betas_T2[i]                                               # Parametro nuevo
        
            if round(original_param_i,2) != round(cur_param_i,2) and current_DS == i+1:
                self.grafica_param_bytyp_T2.ax.plot(current_story, cur_param_i, 'o', color = current_color, markersize = 5)
        
        # Actualizar la gráfica en tu GUI
        self.grafica_param_bytyp_T2.draw()

#%% # FUNCIÓN PARA GUARDAR MODIFICACIONES DENTRO DE TAXONOMIA 1   
    # ---------------------------------------------------------------------------- 
    
    def save_change_T1(self):
        
        # Acceder a diccionario
        current_data_frame = dict_param_taxonomy[str(T_T1)]
        
        # Modificación de parámetros
        for i in range(num_ds):
            current_data_frame.loc[current_data_frame['Taxonomy'] == Tax_T1, 'Theta' + str(i+1)] = new_thetas_T1[i]
            current_data_frame.loc[current_data_frame['Taxonomy'] == Tax_T1, 'Beta' + str(i+1)] = new_betas_T1[i]

#%% # FUNCIÓN PARA GUARDAR MODIFICACIONES DENTRO DE TAXONOMIA 2   
    # ---------------------------------------------------------------------------- 
    
    def save_change_T2(self):
        
        # Acceder a diccionario
        current_data_frame = dict_param_taxonomy[str(T_T2)]
        
        # Modificación de parámetros
        for i in range(num_ds):
            current_data_frame.loc[current_data_frame['Taxonomy'] == Tax_T2, 'Theta' + str(i+1)] = new_thetas_T2[i]
            current_data_frame.loc[current_data_frame['Taxonomy'] == Tax_T2, 'Beta' + str(i+1)] = new_betas_T2[i]
    
#%% # FUNCIÓN PARA EXPORTAR RESULTADOS A UN NUEVO EXCEL   
    # ---------------------------------------------------------------------------- 
    
    def export_changes_to_excel(self):
        
        # ----------------------------------------------------
        # Carga de listas de interés
        taxonomy_list = dataF_excel_tax['Taxonomy'].unique()
        
        # ------------------------------------------
        # Generación de nuevo DataFrame de resultados para guardar en excel

        # Lista de IMs
        IM_T_list = list(dict_param_taxonomy.keys())

        data_to_export = pd.DataFrame()
        for i in range(len(IM_T_list)):
            data_to_export = data_to_export.append(dict_param_taxonomy[IM_T_list[i]], ignore_index=True)
        
        # ---------------------------------------------------- 
        # Definición de ubicacion y nombres de archivos
        
        # Datos de tiempo para adicionar al nombre
        c_time = datetime.now()
        name_add = str(c_time.year) + '-' + str(c_time.month) + '-' + str(c_time.day) + '-' + str(c_time.hour) + \
                    '-' + str(c_time.minute) + '-' + str(c_time.second)
           
        # Definición de path y nombre de excel de resultados
        if fname_location_excel_tax:
            excel_file_name = os.path.basename(fname_location_excel_tax)
            excel_file_path = fname_location_excel_tax
            
        elif fname_file_result:
            excel_file_name = self.ui.excel_name_value.text()
            excel_file_path = os.path.join(fname_file_result, excel_file_name + '.xlsx')
            
        # Nombre del nuevo archivo y ruta
        new_excel_file_name = os.path.splitext(excel_file_name)[0] + '_MOD_' + name_add + '.xlsx'
        new_excel_file_path  =  os.path.join(os.path.dirname(excel_file_path), new_excel_file_name)
        
        
        # ----------------------------------------------------
        # Inicio de escritura en excel
        
        # Escribir sobre excel
        writer = pd.ExcelWriter(new_excel_file_path)

        # ------
        # Guardado de resultado de parámetros de las taxonomias

        # Lista de IMs
        IM_T_list = list(dict_param_taxonomy.keys())

        current_sheet_name = 'Taxonomies'

        data_aux = pd.DataFrame()
        for i in range(len(IM_T_list)):
            data_aux = data_aux.append(dict_param_taxonomy[IM_T_list[i]], ignore_index=True)

        data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)

        # ------
        # Guardado de resultado de parámetros de las edificaciones

        # Lista de IMs
        IM_T_list = list(dict_param_buildings.keys())

        current_sheet_name = 'Buildings'

        data_aux = pd.DataFrame()
        for i in range(len(IM_T_list)):
            data_aux = data_aux.append(dict_param_buildings[IM_T_list[i]], ignore_index=True)
            
        data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)
        
        # ------
        # Guardado de resultado de los puntos con los que se ajustan las curvas de los DS de cada taxonomia para cada T
        
        # Lista de IMs
        IM_T_list = list(dict_points_fragility.keys())
        
        # Loop de las taxonomias
        for j in range(len(taxonomy_list)):
            
            data_aux = pd.DataFrame()
            
            for i in range(len(IM_T_list)):
                
                # Nombre de la hoja
                current_sheet_name = taxonomy_list[j].replace('/','-')
                
                current_data = dict_points_fragility[IM_T_list[i]][taxonomy_list[j]]
                data_aux = data_aux.append(current_data, ignore_index=True)
                
                data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)
                
        # ------
        # Guardado de los datos de cada taxonomia para graficar dispersion
        
        # Lista de IMs
        IM_T_list = list(dict_data_IM_EDP_HzLv.keys())
        
        # Loop de las taxonomias
        for j in range(len(taxonomy_list)):
            
            data_aux = pd.DataFrame()
            
            for i in range(len(IM_T_list)):
                
                # Nombre de la hoja
                current_sheet_name = 'Disp - ' + taxonomy_list[j].replace('/','-')
                
                current_data = dict_data_IM_EDP_HzLv[IM_T_list[i]][taxonomy_list[j]]
                data_aux = data_aux.append(current_data, ignore_index=True)
                
                data_aux.to_excel(writer, sheet_name = current_sheet_name , index = False)

        writer.save()
        writer.close() 
        
              
#%%    

###################################################################################
# FUNCIONES PARA BOTONES DEL TABWIDGET DE LOSS COMPONENTS
###################################################################################    

#%% # FUNCIÓN PARA GRAFICAR GRUPO DE FRAGILIDAD 1      
    # ----------------------------------------------------------------------------    
    
    def fragility_group_1(self):
        global costType
         
        ################################### 
        # GENERAL
        
        # Tipo de costo de la hoja de excel
        costType = self.ui.CostType_selection.currentText()
        
        # Apertura de la descripción del componente
        comp1 = self.ui.fragilityGroup_Value_1.currentText()
        comp1_name = guide_component.loc[guide_component['Fragility Group'] == comp1]['Description']
        comp1_name.reset_index(drop = True, inplace=True)
        comp1_name = comp1_name[0]
        self.ui.componentName_1.setText(comp1_name)
        
        # Definición de EDP asociado al componente
        EDP_comp1 = guide_component.loc[guide_component['Fragility Group'] == comp1]['EDP_Associated']
        EDP_comp1.reset_index(drop = True, inplace=True)
        EDP_comp1 = EDP_comp1[0]
        
        # Valor de EDP para gráfica de probabilidades de estados de daño
        EDPval_1 =  float(self.ui.EDPVal_value_comp_1.text())
        
        # Carga estados de daño del componente
        data_ds_comp1 = pd.read_excel(fname_compGuide, sheet_name = comp1)
        
        # Definición del delta de EDP de acuerdo con el tipo de EDP
        edp_max = delta_max_edp[EDP_comp1]['edp_max']
        d_edp = delta_max_edp[EDP_comp1]['d_edp']
        expon = abs(exponente(d_edp)) # para aproximar a ese número
        
        # Función que genera la matriz plot
        plot_ds_c1 = Expected_loss_one_component(data_ds_comp1, d_edp, edp_max, costType)
        
        ################################### 
        # GRAFICA DE ESTADOS DE DAÑO EN FUNCIÓN DE EDP
        
        try:
            self.graficaPOE_comp_1.close()
        except AttributeError:
            pass
        
        self.graficaPOE_comp_1 = Canvas_grafica()
        self.graficaPOE_comp_1.ax.clear()
        
        for ds_k in range (len(data_ds_comp1)):
            self.graficaPOE_comp_1.ax.plot(plot_ds_c1['EDP'], plot_ds_c1[data_ds_comp1.iloc[ds_k]['Damage State']], label = data_ds_comp1.iloc[ds_k]['Damage State'] + 
                     '=' + r'$\theta$ = ' + str(round(data_ds_comp1['θ'][ds_k],3)) + '  ' + r'$\beta$ = ' +str(round(data_ds_comp1['β'][ds_k],3)), color = color[ds_k])

        if EDP_comp1 == 'SDR':
            self.graficaPOE_comp_1.ax.set_xlim(0, 0.1)
        elif EDP_comp1 == 'PFA':
            self.graficaPOE_comp_1.ax.set_xlim(0, 60)
            
        self.graficaPOE_comp_1.ax.set_xlabel(EDP_comp1, size = 10)
        self.graficaPOE_comp_1.ax.set_ylabel('P(DS > ds$_{k}$ |' + EDP_comp1 +')', size = 10)
        self.graficaPOE_comp_1.ax.grid(which="both")
        self.graficaPOE_comp_1.ax.legend(fontsize=7, loc = 'lower right')
        self.ui.graph_POE_1.addWidget(self.graficaPOE_comp_1)
        
        ################################### 
        # GRAFICA DE PROBABILIDAD DE ESTADOS DE DAÑO
        
        p_ds_c1 = pd.DataFrame()
        p_ds_c1['DS'] = np.zeros(len(data_ds_comp1) + 1)
        p_ds_c1['DS'][0]  = 'DS0'
        p_ds_c1['DS'][1::] = data_ds_comp1['Damage State']

        p_ds_c1['P(DS)'] = np.zeros(len(data_ds_comp1) + 1)
        

        ind = plot_ds_c1.loc[round(plot_ds_c1['EDP'], expon) == round(EDPval_1, expon)]
        ind.reset_index(drop = True, inplace=True)

        for i in range(len(p_ds_c1)):
            DS_num = len(p_ds_c1)-1-i
            if i == 0:
                p_ds_c1['P(DS)'][DS_num] = ind['DS' + str(DS_num)][0]
            elif DS_num > 0:
                p_ds_c1['P(DS)'][DS_num] = ind['DS' + str(DS_num)][0] - ind['DS' + str(DS_num+1)][0]
            else:
                p_ds_c1['P(DS)'][DS_num] = 1 - ind['DS' + str(DS_num+1)][0]
                
        try:
            self.graficaProb_comp_1.close()
        except AttributeError:
            pass
        
        self.graficaProb_comp_1 = Canvas_grafica()
        self.graficaProb_comp_1.ax.clear()
        
        bars = self.graficaProb_comp_1.ax.bar(p_ds_c1['DS'],p_ds_c1['P(DS)'], color = color2)
        for bar in bars:
            height = bar.get_height()
            self.graficaProb_comp_1.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')
        self.graficaProb_comp_1.ax.set_ylim(0, 1)
        self.graficaProb_comp_1.ax.set_xlabel('Damage States - ' + EDP_comp1 + ' = ' + str(round(EDPval_1, expon)), size = 10)
        self.graficaProb_comp_1.ax.set_ylabel('P(DS = ds$_{k}$ |' + EDP_comp1 +')', size = 10)
        self.ui.graph_Prob_1.addWidget(self.graficaProb_comp_1)
        
        ################################### 
        # GRAFICA DE PROBABILIDAD DE PÉRDIDA NORMALIZADA DEL COMPONENTE
        
        try:
            self.graficaPerdNorm_comp_1.close()
        except AttributeError:
            pass
       
        self.graficaPerdNorm_comp_1 = Canvas_grafica()
        self.graficaPerdNorm_comp_1.ax.clear()
        
        self.graficaPerdNorm_comp_1.ax.plot(plot_ds_c1['EDP'], plot_ds_c1["E'[L|EDP]"], linewidth = 3)
        self.graficaPerdNorm_comp_1.ax.set_xlabel(EDP_comp1, size = 10)
        self.graficaPerdNorm_comp_1.ax.set_ylabel("E'[L = " + comp1 + '|' + EDP_comp1+ ']', size = 10)
        self.graficaPerdNorm_comp_1.ax.grid(which="both")
        self.ui.graph_LossComp_1.addWidget(self.graficaPerdNorm_comp_1)
     
#%% # FUNCIÓN PARA GRAFICAR GRUPO DE FRAGILIDAD 2       
    # ----------------------------------------------------------------------------    

    def fragility_group_2(self):
        global costType
         
        ################################### 
        # GENERAL
        
        # Tipo de costo de la hoja de excel
        costType = self.ui.CostType_selection.currentText()
        
        # Apertura de la descripción del componente
        comp2 = self.ui.fragilityGroup_Value_2.currentText()
        comp2_name = guide_component.loc[guide_component['Fragility Group'] == comp2]['Description']
        comp2_name.reset_index(drop = True, inplace=True)
        comp2_name = comp2_name[0]
        self.ui.componentName_2.setText(comp2_name)
        
        # Definición de EDP asociado al componente
        EDP_comp2 = guide_component.loc[guide_component['Fragility Group'] == comp2]['EDP_Associated']
        EDP_comp2.reset_index(drop = True, inplace=True)
        EDP_comp2 = EDP_comp2[0]
        
        # Valor de EDP para gráfica de probabilidades de estados de daño
        EDPval_2 =  float(self.ui.EDPVal_value_comp_2.text())
        
        # Carga estados de daño del componente
        data_ds_comp2 = pd.read_excel(fname_compGuide, sheet_name = comp2)
        
        # Definición del delta de EDP de acuerdo con el tipo de EDP
        edp_max = delta_max_edp[EDP_comp2]['edp_max']
        d_edp = delta_max_edp[EDP_comp2]['d_edp']
        expon = abs(exponente(d_edp)) # para aproximar a ese número
        
        # Función que genera la matriz plot
        plot_ds_c2 = Expected_loss_one_component(data_ds_comp2, d_edp, edp_max, costType)
        
        ################################### 
        # GRAFICA DE ESTADOS DE DAÑO EN FUNCIÓN DE EDP
        
        try:
            self.graficaPOE_comp_2.close()
        except AttributeError:
            pass
        
        self.graficaPOE_comp_2 = Canvas_grafica()
        self.graficaPOE_comp_2.ax.clear()
        
        for ds_k in range (len(data_ds_comp2)):
            self.graficaPOE_comp_2.ax.plot(plot_ds_c2['EDP'], plot_ds_c2[data_ds_comp2.iloc[ds_k]['Damage State']], label = data_ds_comp2.iloc[ds_k]['Damage State'] + 
                     '=' + r'$\theta$ = ' + str(round(data_ds_comp2['θ'][ds_k],3)) + '  ' + r'$\beta$ = ' +str(round(data_ds_comp2['β'][ds_k],3)), color = color[ds_k])

        if EDP_comp2 == 'SDR':
            self.graficaPOE_comp_2.ax.set_xlim(0, 0.1)
        elif EDP_comp2 == 'PFA':
            self.graficaPOE_comp_2.ax.set_xlim(0, 60)
            
        self.graficaPOE_comp_2.ax.set_xlabel(EDP_comp2, size = 10)
        self.graficaPOE_comp_2.ax.set_ylabel('P(DS > ds$_{k}$ |' + EDP_comp2 +')', size = 10)
        self.graficaPOE_comp_2.ax.grid(which="both")
        self.graficaPOE_comp_2.ax.legend(fontsize=7, loc = 'lower right')
        self.ui.graph_POE_2.addWidget(self.graficaPOE_comp_2)
        
        ################################### 
        # GRAFICA DE PROBABILIDAD DE ESTADOS DE DAÑO
        
        p_ds_c2 = pd.DataFrame()
        p_ds_c2['DS'] = np.zeros(len(data_ds_comp2) + 1)
        p_ds_c2['DS'][0]  = 'DS0'
        p_ds_c2['DS'][1::] = data_ds_comp2['Damage State']

        p_ds_c2['P(DS)'] = np.zeros(len(data_ds_comp2) + 1)
        

        ind = plot_ds_c2.loc[round(plot_ds_c2['EDP'], expon) == round(EDPval_2, expon)]
        ind.reset_index(drop = True, inplace=True)

        for i in range(len(p_ds_c2)):
            DS_num = len(p_ds_c2)-1-i
            if i == 0:
                p_ds_c2['P(DS)'][DS_num] = ind['DS' + str(DS_num)][0]
            elif DS_num > 0:
                p_ds_c2['P(DS)'][DS_num] = ind['DS' + str(DS_num)][0] - ind['DS' + str(DS_num+1)][0]
            else:
                p_ds_c2['P(DS)'][DS_num] = 1 - ind['DS' + str(DS_num+1)][0]
                
        try:
            self.graficaProb_comp_2.close()
        except AttributeError:
            pass
        
        self.graficaProb_comp_2 = Canvas_grafica()
        self.graficaProb_comp_2.ax.clear()
        
        bars = self.graficaProb_comp_2.ax.bar(p_ds_c2['DS'],p_ds_c2['P(DS)'], color = color2)
        for bar in bars:
            height = bar.get_height()
            self.graficaProb_comp_2.ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')
        self.graficaProb_comp_2.ax.set_ylim(0, 1)
        self.graficaProb_comp_2.ax.set_xlabel('Damage States - ' + EDP_comp2 + ' = ' + str(round(EDPval_2, expon)), size = 10)
        self.graficaProb_comp_2.ax.set_ylabel('P(DS = ds$_{k}$ |' + EDP_comp2 +')', size = 10)
        self.ui.graph_Prob_3.addWidget(self.graficaProb_comp_2)
        
        ################################### 
        # GRAFICA DE PROBABILIDAD DE PÉRDIDA NORMALIZADA DEL COMPONENTE
        
        try:
            self.graficaPerdNorm_comp_2.close()
        except AttributeError:
            pass
       
        self.graficaPerdNorm_comp_2 = Canvas_grafica()
        self.graficaPerdNorm_comp_2.ax.clear()
        
        self.graficaPerdNorm_comp_2.ax.plot(plot_ds_c2['EDP'], plot_ds_c2["E'[L|EDP]"], linewidth = 3)
        self.graficaPerdNorm_comp_2.ax.set_xlabel(EDP_comp2, size = 10)
        self.graficaPerdNorm_comp_2.ax.set_ylabel("E'[L = "  + comp2 + '|' + EDP_comp2+ ']', size = 10)
        self.graficaPerdNorm_comp_2.ax.grid(which="both")
        self.ui.graph_LossComp_2.addWidget(self.graficaPerdNorm_comp_2)
        
#%% # FUNCIÓN PARA CARGAR DESPLEGABLES DE ELEMENTOS DE LA EDIFICACIÓN 1   
    # ---------------------------------------------------------------------------- 

    def elements_options_1(self):
        
        # Columnas de interés a seleccionar
        inputdata_E1 = self.ui.InputData_Value_1.currentText()
        Element_options = data_story_E1[inputdata_E1].unique()
        
        # Desplegaable de opciones
        try:
            self.ui.Element_Value_1.clear()
        except:
            pass
        
        for i in range (len(Element_options)):
            self.ui.Element_Value_1.addItem(Element_options[i])
            
#%% # FUNCIÓN PARA CARGAR DESPLEGABLES DE ELEMENTOS DE LA EDIFICACIÓN 2           
    # ----------------------------------------------------------------------------       

    def elements_options_2(self):
        
        # Columnas de interés a seleccionar
        inputdata_E2 = self.ui.InputData_Value_2.currentText()
        Element_options = data_story_E2[inputdata_E2].unique()
        
        # Desplegaable de opciones
        try:
            self.ui.Element_Value_2.clear()
        except:
            pass
        
        for i in range (len(Element_options)):
            self.ui.Element_Value_2.addItem(Element_options[i])
#%%  
          
###################################################################################
# FUNCIONES PARA BOTONES DEL TABWIDGET DE LOSS STORY
###################################################################################   

#%% # CALCULA PÉRDIDAS DE TODOS LOS COMPONENTES DE LA EDIFICACIÓN 1     
    # ----------------------------------------------------------------------------        
     
    def load_Building_1_Loss(self):
        global fname_EdpB1, data_StoryTypes_E1, data_story_E1, curve_options, \
                costType, dictionary_loss_E1
        
        
        NameFolder = os.path.basename(fname_EdpB1)
        self.ui.Building_text_1.setText(NameFolder)
        
        # --------------------------------------------------------------------
        # Definición de desplegables del tipo de piso
        
        # Importante: ya se debe haber presionado el boton Load Components para cargar componentes
        
        # Apertura de excel guia con numero de pisos
        os.chdir(fname_EdpB1)

        file_name = glob.glob('*Loss_distribution*')
        sheet_principal = 'Guide'     

        data_StoryTypes_E1 = pd.read_excel(os.path.join(fname_EdpB1, file_name[0]), sheet_name = sheet_principal)

        # Desplegable para adicionar opciones del piso
        try:
            self.ui.Story_Value_1.clear()
        except:
            pass
        
        self.ui.Story_Value_1.addItem('All')
        for i in range (len(data_StoryTypes_E1['Story Type'].unique())):
            self.ui.Story_Value_1.addItem(data_StoryTypes_E1['Story Type'].unique()[i])
            
        # --------------------------------------------------------------------
        # Definición de desplegables de que elemento se quiere graficar
        
        # Lectura de piso
        current_story = self.ui.Story_Value_1.currentText()
        # Si es all, no hay una hoja con ese nombre asi que le asignamos cualquier piso suponiendo
        # que todas las hojas tienen los mismos elementos
        if current_story == 'All':
            current_story = data_StoryTypes_E1['Story Type'].unique()[0]

        # Datos de pérdidas del piso
        data_story_E1 = pd.read_excel(os.path.join(fname_EdpB1, file_name[0]), sheet_name = current_story)
        data_story_E1['Component + Fragility Group'] = data_story_E1['Component'] + ' (' + data_story_E1['Fragility Group'] + ')'
        
        # Desplegaable de opciones
        try:
            self.ui.InputData_Value_1.clear()
        except:
            pass
        
        # Columnas de interés a seleccionar
        curve_options = [data_story_E1.columns[3], data_story_E1.columns[4], data_story_E1.columns[6]]
        
        for i in range (len(curve_options)):
            self.ui.InputData_Value_1.addItem(curve_options[i])
            
        # --------------------------------------------------------------------
        # Generación de data de pérdidas para todos los pisos para graficar pérdidas DV-EDP
        
        costType = self.ui.CostType_selection.currentText()
        
        print('\n')
        print('################### BUILDING 1 ###################')
        dictionary_loss_E1 = loss_all_stories_allElements (costType, fname_EdpB1, delta_max_edp, fname_compGuide, guide_component)
        print('############## BUILDING 1 FINISHED ###############')
        
        # --------------------------------------------------------------------
        # Definición de nombre de edificación
        try:
            # Seleccion de CSS y Description Name asociado al edificio escogido
            ind = building_guide_original.loc[building_guide_original['Building Folder Name'] == NameFolder]
            CSS_name = ind['CSS'].tolist()[0]
            BuildingType = ind['Description Name'].tolist()[0]
            
            title_g_1 = "BUILDING 1: " + BuildingType
            self.ui.label_curve_B1.setText(title_g_1)
            
        except NameError:
            pass
#%% # CALCULA PÉRDIDAS DE TODOS LOS COMPONENTES DE LA EDIFICACIÓN 2        
    # ----------------------------------------------------------------------------    
        
    def load_Building_2_Loss(self):
        global fname_EdpB2, data_StoryTypes_E2, data_story_E2, curve_options, \
                costType, dictionary_loss_E2
        
        
        NameFolder = os.path.basename(fname_EdpB2)
        self.ui.Building_text_2.setText(NameFolder)
        
        # --------------------------------------------------------------------
        # Definición de desplegables del tipo de piso
        
        # Importante: ya se debe haber presionado el boton Load Components para cargar componentes
        
        # Apertura de excel guia con numero de pisos
        os.chdir(fname_EdpB2)

        file_name = glob.glob('*Loss_distribution*')
        sheet_principal = 'Guide'     

        data_StoryTypes_E2 = pd.read_excel(os.path.join(fname_EdpB2, file_name[0]), sheet_name = sheet_principal)

        # Desplegable para adicionar opciones del piso
        # col_name = data_StoryTypes_E2.columns[0]
        try:
            self.ui.Story_Value_2.clear()
        except:
            pass
        
        self.ui.Story_Value_2.addItem('All')
        for i in range (len(data_StoryTypes_E2['Story Type'].unique())):
            self.ui.Story_Value_2.addItem(data_StoryTypes_E2['Story Type'].unique()[i])
    
            
        # --------------------------------------------------------------------
        # Definición de desplegables de que elemento se quiere graficar
        
        # Lectura de piso
        current_story = self.ui.Story_Value_2.currentText()
        # Si es all, no hay una hoja con ese nombre asi que le asignamos cualquier piso suponiendo
        # que todas las hojas tienen los mismos elementos
        if current_story == 'All':
            current_story = data_StoryTypes_E2['Story Type'].unique()[0]

        # Datos de pérdidas del piso
        data_story_E2 = pd.read_excel(os.path.join(fname_EdpB2, file_name[0]), sheet_name = current_story)
        data_story_E2['Component + Fragility Group'] = data_story_E2['Component'] + ' (' + data_story_E2['Fragility Group'] + ')'
        
        # Desplegaable de opciones
        try:
            self.ui.InputData_Value_2.clear()
        except:
            pass
        
        # Columnas de interés a seleccionar
        curve_options = [data_story_E2.columns[3], data_story_E2.columns[4], data_story_E2.columns[6]]
        
        for i in range (len(curve_options)):
            self.ui.InputData_Value_2.addItem(curve_options[i])
            
        # --------------------------------------------------------------------
        # Generación de data de pérdidas para todos los pisos para graficar pérdidas DV-EDP
        
        costType = self.ui.CostType_selection.currentText()
        
        print('\n')
        print('################### BUILDING 2 ###################')
        dictionary_loss_E2 = loss_all_stories_allElements (costType, fname_EdpB2, delta_max_edp, fname_compGuide, guide_component)
        print('############## BUILDING 2 FINISHED ###############')
        
        # --------------------------------------------------------------------
        # Definición de nombre de edificación
        try:
            # Seleccion de CSS y Description Name asociado al edificio escogido
            ind = building_guide_original.loc[building_guide_original['Building Folder Name'] == NameFolder]
            CSS_name = ind['CSS'].tolist()[0]
            BuildingType = ind['Description Name'].tolist()[0]
            
            title_g_2 = "BUILDING 2: " + BuildingType
            self.ui.label_curve_B2.setText(title_g_2)
            
        except NameError:
            pass


#%% # FUNCIÓN PARA CURVAS DE PÉRDIDAS DV-EDP DE LA EDIFICACIÓN 1    
    # ----------------------------------------------------------------------------         

    def loss_story_1(self):
        
        global dictionary_plot_E1, current_story_E1, current_element_E1, data_StoryTypes_E1, EDP_assoc_E1
        
        # Opciones seleccionadas
        current_story_E1 = self.ui.Story_Value_1.currentText()
        current_inputdata_E1 = self.ui.InputData_Value_1.currentText()
        current_element_E1 = self.ui.Element_Value_1.currentText()
        
        # Cargado de diccionario para los elementos de interés
        [dictionary_plot_E1, EDP_assoc_E1] = plot_loss_groups(current_inputdata_E1, current_element_E1, dictionary_loss_E1, fname_EdpB1, guide_component)
        
        ################################### 
        # GRAFICAS DE CURVAS DE PÉRDIDAS
        
        try:
            self.grafica_LossStory_1.close()
        except AttributeError:
            pass
                
        self.grafica_LossStory_1 = Canvas_grafica()      
        self.grafica_LossStory_1.ax.clear()
        
        if current_story_E1 != 'All':
            if EDP_assoc_E1 == 'SDR':
                aux = dictionary_plot_E1['Loss_data_plot_'  +  current_story_E1]
                self.grafica_LossStory_1.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3,
                                                 label = current_story_E1 + ' - ' + current_element_E1, color = color3[0])
                
            elif EDP_assoc_E1 == 'PFA':
                aux = dictionary_plot_E1['Loss_data_plot_'  +  current_story_E1]
                self.grafica_LossStory_1.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3,
                                                 label = current_story_E1 + ' - ' + current_element_E1, color = color3[0])
        else:
            
            if EDP_assoc_E1 == 'SDR':
                
                for i in range(len(data_StoryTypes_E1['Story Type'].unique())):
                    aux = dictionary_plot_E1['Loss_data_plot_'  +  data_StoryTypes_E1['Story Type'].unique()[i]]
                
                    self.grafica_LossStory_1.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3,
                                                 label = data_StoryTypes_E1['Story Type'].unique()[i] + ' - ' + current_element_E1, color = color3[i])
                
            elif EDP_assoc_E1 == 'PFA':
                for i in range(len(data_StoryTypes_E1['Story Type'].unique())):
                    aux = dictionary_plot_E1['Loss_data_plot_'  +  data_StoryTypes_E1['Story Type'].unique()[i]]
                    
                    self.grafica_LossStory_1.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3,
                                                 label = data_StoryTypes_E1['Story Type'].unique()[i] + ' - ' + current_element_E1, color = color3[i])
            
                
        self.grafica_LossStory_1.ax.set_xlabel(EDP_assoc_E1, size = 10)   
        self.grafica_LossStory_1.ax.set_ylabel("E'[L = " + current_element_E1 + " | " + EDP_assoc_E1 + "]", size = 10)
        self.grafica_LossStory_1.ax.set_ylim(0, 1.05)
        self.grafica_LossStory_1.ax.grid(which="both")
        self.grafica_LossStory_1.ax.legend(fontsize=7, loc = 'best')
        self.ui.graph_DV_EDP_1.addWidget(self.grafica_LossStory_1)
        
#%% # FUNCIÓN PARA CURVAS DE PÉRDIDAS DV-EDP DE LA EDIFICACIÓN 2    
    # ----------------------------------------------------------------------------         

    def loss_story_2(self):
        
        global dictionary_plot_E2, current_story_E2, current_element_E2, data_StoryTypes_E2, EDP_assoc_E2
        
        # Opciones seleccionadas
        current_story_E2 = self.ui.Story_Value_2.currentText()
        current_inputdata_E2 = self.ui.InputData_Value_2.currentText()
        current_element_E2 = self.ui.Element_Value_2.currentText()
        
        # Cargado de diccionario para los elementos de interés
        [dictionary_plot_E2, EDP_assoc_E2] = plot_loss_groups(current_inputdata_E2, current_element_E2, dictionary_loss_E2, fname_EdpB2, guide_component)
        
        ################################### 
        # GRAFICAS DE CURVAS DE PÉRDIDAS
        
        try:
            self.grafica_LossStory_2.close()
        except AttributeError:
            pass
                
        self.grafica_LossStory_2 = Canvas_grafica()      
        self.grafica_LossStory_2.ax.clear()
        
        if current_story_E2 != 'All':
            if EDP_assoc_E2 == 'SDR':
                aux = dictionary_plot_E2['Loss_data_plot_'  +  current_story_E2]
                self.grafica_LossStory_2.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = current_story_E2 + ' - ' + current_element_E2, color = color3[0])
                
            elif EDP_assoc_E2 == 'PFA':
                aux = dictionary_plot_E2['Loss_data_plot_'  +  current_story_E2]
                self.grafica_LossStory_2.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = current_story_E2 + ' - ' + current_element_E2, color = color3[0])
        else:
            
            if EDP_assoc_E2 == 'SDR':
                
                for i in range(len(data_StoryTypes_E2['Story Type'].unique())):
                    aux = dictionary_plot_E2['Loss_data_plot_'  +  data_StoryTypes_E2['Story Type'].unique()[i]]
                
                    self.grafica_LossStory_2.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = data_StoryTypes_E2['Story Type'].unique()[i] + ' - ' + current_element_E2, color = color3[i])
                
            elif EDP_assoc_E2 == 'PFA':
                for i in range(len(data_StoryTypes_E2['Story Type'].unique())):
                    aux = dictionary_plot_E2['Loss_data_plot_'  +  data_StoryTypes_E2['Story Type'].unique()[i]]
                    
                    self.grafica_LossStory_2.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = data_StoryTypes_E2['Story Type'].unique()[i] + ' - ' + current_element_E2, color = color3[i])
            
                
        self.grafica_LossStory_2.ax.set_xlabel(EDP_assoc_E2, size = 10)   
        self.grafica_LossStory_2.ax.set_ylabel("E'[L = " + current_element_E2 + " | " + EDP_assoc_E2 + "]", size = 10)
        self.grafica_LossStory_2.ax.set_ylim(0, 1.05)
        self.grafica_LossStory_2.ax.grid(which="both")
        self.grafica_LossStory_2.ax.legend(fontsize=7, loc = 'best')
        self.ui.graph_DV_EDP_2.addWidget(self.grafica_LossStory_2)
        
#%% # FUNCIÓN PARA CURVAS DE PÉRDIDAS DV-IM DE LA EDIFICACIÓN 1    
    # ----------------------------------------------------------------------------  
    
    def loss_DV_IM_1(self):
        global dict_PG_NC_loss_E1, dict_DV_IM_NC_E1, POC_E1, POD_E1, EL_NC_ND_E1, \
               EL_NC_D_E1, EL_C_E1, EL_total_E1, IM_bin_data_E1
        
        ################################### 
        # CARGAR DATOS
    
        SDR_cens = float(self.ui.SDRLoss_cens_value_1.text())
        
        theta_colapse = float(self.ui.Theta_collapse_value_1.text())
        beta_colapse = float(self.ui.Sigma_collapse_value_1.text())

        theta_rsdr_lim = float(self.ui.Theta_rsdr_value_1.text())
        beta_rsdr_lim = float(self.ui.Sigma_rsdr_value_1.text())

        # Valores eperados de demolición y colapso
        E_D = float(self.ui.ED_value_1.text())
        E_C = float(self.ui.EC_value_1.text())
        
        # Tipo de IM (Viene de la pestaña de Fragility of Buildings)
        IM_name_graph_E1 = self.ui.IMType_Value_1.currentText()
        
        ######################################################################
        # PÉRDIDAS ESPERADAS PARA NO COLAPSO
        
        # Censurar datos
        type_cens = 'lower'
        dict_EDPs_Cens_E1 = EDP_censor_data (SDR_cens, type_cens, dict_EDPs_Original_E1)
        
        # Bineado de datos Y parámetros de curvas pdfs
        EDPs_list = ['SDR', 'PFA', 'RSDR']
        [dict_EDPs_bin_E1, dict_params_log_E1] = binning_and_pdfs_bystory(dict_EDPs_Cens_E1, EDPs_list, T_E1, tipo_bin_E1, min_datos_bin_E1, num_bins_inicial_E1)
        stories = list(dict_params_log_E1[EDPs_list[0]].keys())
        IM_bin_data_E1 = dict_params_log_E1[EDPs_list[0]][stories[0]]['IM_bin']
        
        #------------------------------------------------------
        # PÉRDIDAS ESPERADAS DV vs EDP
        
        # Diccionario de los primary groups (PG) para cada piso: contiene valores de EDPs y péridas asociadas a cada valor
        dict_PG_NC_loss_E1 = data_plot_primaryGroups (fname_EdpB1, guide_component, dictionary_loss_E1)
        
        #------------------------------------------------------
        # PÉRDIDAS ESPERADAS DV VS IM para No Colapso ni Demolicion
        
        # Diccionario con los datos par graficar pérdidas DV vs IM para no colapso
        dict_DV_IM_NC_E1 = DV_IM_curves_NC(dict_params_log_E1, dict_PG_NC_loss_E1, data_StoryTypes_E1)
        
        ######################################################################
        # ESTIMACIÓN DE PROBABILIDAD DE COLAPSO
        
        POC_E1 = norm.cdf(np.log(IM_bin_data_E1), np.log(theta_colapse), beta_colapse)
        
        ######################################################################
        # ESTIMACIÓN DE PROBABILIDAD DE DEMOLICIÓN
        
        # Parámetros de curvas pdf RSDR para cada IM_bin
        parameters_RSDR_E1 = binning_and_pdfs_RSDRmax(dict_EDPs_Cens_E1, T_E1, tipo_bin_E1, min_datos_bin_E1, num_bins_inicial_E1)

        # Probabilidad de demolición
        edp_max_RSDR = delta_max_edp['RSDR']['edp_max']
        d_edp_RSDR = delta_max_edp['RSDR']['d_edp']
        POD_E1 = function_POD(parameters_RSDR_E1, theta_rsdr_lim, beta_rsdr_lim, edp_max_RSDR, d_edp_RSDR)
        
        ######################################################################
        # PERDIDAS ESPERADAS DE TODA LA EDIFICACIÓN
        
        EL_NC_ND_E1 = dict_DV_IM_NC_E1['Building']['Loss_building_NC']*(1-POC_E1)*(1-POD_E1['Prob'])
        EL_NC_D_E1 = E_D*(1-POC_E1)*POD_E1['Prob']
        EL_C_E1 = E_C*POC_E1
        
        EL_total_E1 = EL_NC_ND_E1 + EL_NC_D_E1 + EL_C_E1
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA NO COLAPSO DE CADA PISO
        
        try:
            self.grafica_Loss_by_Story_E1.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_by_Story_E1 = Canvas_grafica()      
        self.grafica_Loss_by_Story_E1.ax.clear()
        
        for i in range(len(stories)):
            im_graph = dict_DV_IM_NC_E1[stories[i]]['IM_bin']
            loss_graph = dict_DV_IM_NC_E1[stories[i]]['All_PG']
            
            self.grafica_Loss_by_Story_E1.ax.plot(im_graph, loss_graph, 'o-', color = color_py[i], markersize = 4, label = stories[i])

        self.grafica_Loss_by_Story_E1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
        self.grafica_Loss_by_Story_E1.ax.set_ylabel("E'[L$_{Story}$ "  + " | NC+R, IM = " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
        self.grafica_Loss_by_Story_E1.ax.set_ylim(0, 1.05)
        self.grafica_Loss_by_Story_E1.ax.grid(which="both")
        self.grafica_Loss_by_Story_E1.ax.legend(fontsize=10, loc = 'best')
        
        self.ui.graph_DV_IM_1.addWidget(self.grafica_Loss_by_Story_E1)
        
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO PARA NO COLAPSO
        
        try:
            self.grafica_Loss_all_NC_Building_E1.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_all_NC_Building_E1 = Canvas_grafica()      
        self.grafica_Loss_all_NC_Building_E1.ax.clear()

        self.grafica_Loss_all_NC_Building_E1.ax.plot(dict_DV_IM_NC_E1['Building']['IM_bin'], dict_DV_IM_NC_E1['Building']['Loss_building_NC'], 'o-',
                                                  color = color_py[0], markersize = 4, linewidth = 2)
        self.grafica_Loss_all_NC_Building_E1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
        self.grafica_Loss_all_NC_Building_E1.ax.set_ylabel("E'[L$_{Building}$ "  + " | NC+R, IM = " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
        self.grafica_Loss_all_NC_Building_E1.ax.set_ylim(0, 1.05)
        self.grafica_Loss_all_NC_Building_E1.ax.grid(which="both")
        
        self.ui.graph_Exp_NC_R_B_1.addWidget(self.grafica_Loss_all_NC_Building_E1)
    
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO (INCLUYE COLPASO, NO COLAPSO, DEMOLICIÓN)
        
        try:
            self.grafica_Loss_all_Building_E1.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_all_Building_E1 = Canvas_grafica()      
        self.grafica_Loss_all_Building_E1.ax.clear()
        
        self.grafica_Loss_all_Building_E1.ax.plot(IM_bin_data_E1, EL_total_E1, 'o-', color = color_py[0], markersize = 4, linewidth = 2)
        self.grafica_Loss_all_Building_E1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
        self.grafica_Loss_all_Building_E1.ax.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
        self.grafica_Loss_all_Building_E1.ax.set_ylim(0, 1.05)
        self.grafica_Loss_all_Building_E1.ax.grid(which="both")
        
        self.ui.graph_Exp_B_1.addWidget(self.grafica_Loss_all_Building_E1)
        
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO POR EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_Loss_byEvents_Building_E1.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_byEvents_Building_E1 = Canvas_grafica()      
        self.grafica_Loss_byEvents_Building_E1.ax.clear()
        
        self.grafica_Loss_byEvents_Building_E1.ax.plot(IM_bin_data_E1, EL_NC_ND_E1, 'o-', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND')
        self.grafica_Loss_byEvents_Building_E1.ax.plot(IM_bin_data_E1, EL_NC_D_E1, 'o-', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D')
        self.grafica_Loss_byEvents_Building_E1.ax.plot(IM_bin_data_E1, EL_C_E1, 'o-', linewidth = 2, markersize = 4, color = 'red', label ='C')

        self.grafica_Loss_byEvents_Building_E1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
        self.grafica_Loss_byEvents_Building_E1.ax.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
        self.grafica_Loss_byEvents_Building_E1.ax.set_ylim(0, 1.05)
        self.grafica_Loss_byEvents_Building_E1.ax.legend(fontsize=10, loc = 'best')
        self.grafica_Loss_byEvents_Building_E1.ax.grid(which="both")
        
        self.ui.graph_ExpEvents_B_1.addWidget(self.grafica_Loss_byEvents_Building_E1)
        
        ######################################################################
        # GRAFICA DE PROBABILIDADES DE EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_prob_events_E1.close()
        except AttributeError:
            pass
                
        self.grafica_prob_events_E1 = Canvas_grafica()      
        self.grafica_prob_events_E1.ax.clear()
        
        self.grafica_prob_events_E1.ax.plot(IM_bin_data_E1, (1-POC_E1)*(1-POD_E1['Prob']), 'o-', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND')
        self.grafica_prob_events_E1.ax.plot(IM_bin_data_E1, (1-POC_E1)*POD_E1['Prob'], 'o-', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D')
        self.grafica_prob_events_E1.ax.plot(IM_bin_data_E1, POC_E1, 'o-', linewidth = 2, markersize = 4, color = 'red', label ='C')

        self.grafica_prob_events_E1.ax.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
        self.grafica_prob_events_E1.ax.set_ylabel("Probability", size = 10)
        self.grafica_prob_events_E1.ax.set_ylim(0, 1.05)
        self.grafica_prob_events_E1.ax.legend(fontsize=10, loc = 'best')
        self.grafica_prob_events_E1.ax.grid(which="both")
        
        self.ui.graph_ProbEvent_B_1.addWidget(self.grafica_prob_events_E1)
        
#%% # FUNCIÓN PARA CURVAS DE PÉRDIDAS DV-IM DE LA EDIFICACIÓN 2    
    # ----------------------------------------------------------------------------  
    
    def loss_DV_IM_2(self):
        global dict_PG_NC_loss_E2, dict_DV_IM_NC_E2, POC_E2, POD_E2, EL_NC_ND_E2, \
               EL_NC_D_E2, EL_C_E2, EL_total_E2, IM_bin_data_E2
        
        ################################### 
        # CARGAR DATOS
    
        SDR_cens = float(self.ui.SDRLoss_cens_value_2.text())
        
        theta_colapse = float(self.ui.Theta_collapse_value_2.text())
        beta_colapse = float(self.ui.Sigma_collapse_value_2.text())

        theta_rsdr_lim = float(self.ui.Theta_rsdr_value_2.text())
        beta_rsdr_lim = float(self.ui.Sigma_rsdr_value_2.text())

        # Valores eperados de demolición y colapso
        E_D = float(self.ui.ED_value_2.text())
        E_C = float(self.ui.EC_value_2.text())
        
        # Tipo de IM (Viene de la pestaña de Fragility of Buildings)
        IM_name_graph_E2 = self.ui.IMType_Value_2.currentText()
        
        ######################################################################
        # PÉRDIDAS ESPERADAS PARA NO COLAPSO
        
        # Censurar datos
        type_cens = 'lower'
        dict_EDPs_Cens_E2 = EDP_censor_data (SDR_cens, type_cens, dict_EDPs_Original_E2)
        
        # Bineado de datos Y parámetros de curvas pdfs
        EDPs_list = ['SDR', 'PFA', 'RSDR']
        [dict_EDPs_bin_E2, dict_params_log_E2] = binning_and_pdfs_bystory(dict_EDPs_Cens_E2, EDPs_list, T_E2, tipo_bin_E2, min_datos_bin_E2, num_bins_inicial_E2)
        stories = list(dict_params_log_E2[EDPs_list[0]].keys())
        IM_bin_data_E2 = dict_params_log_E2[EDPs_list[0]][stories[0]]['IM_bin']
        
        #------------------------------------------------------
        # PÉRDIDAS ESPERADAS DV vs EDP
        
        # Diccionario de los primary groups (PG) para cada piso: contiene valores de EDPs y péridas asociadas a cada valor
        dict_PG_NC_loss_E2 = data_plot_primaryGroups (fname_EdpB2, guide_component, dictionary_loss_E2)
        
        #------------------------------------------------------
        # PÉRDIDAS ESPERADAS DV VS IM para No Colapso ni Demolicion
        
        # Diccionario con los datos par graficar pérdidas DV vs IM para no colapso
        dict_DV_IM_NC_E2 = DV_IM_curves_NC(dict_params_log_E2, dict_PG_NC_loss_E2, data_StoryTypes_E2)
        
        ######################################################################
        # ESTIMACIÓN DE PROBABILIDAD DE COLAPSO
        
        POC_E2 = norm.cdf(np.log(IM_bin_data_E2), np.log(theta_colapse), beta_colapse)
        
        ######################################################################
        # ESTIMACIÓN DE PROBABILIDAD DE DEMOLICIÓN
        
        # Parámetros de curvas pdf RSDR para cada IM_bin
        parameters_RSDR_E2 = binning_and_pdfs_RSDRmax(dict_EDPs_Cens_E2, T_E2, tipo_bin_E2, min_datos_bin_E2, num_bins_inicial_E2)

        # Probabilidad de demolición
        edp_max_RSDR = delta_max_edp['RSDR']['edp_max']
        d_edp_RSDR = delta_max_edp['RSDR']['d_edp']
        POD_E2 = function_POD(parameters_RSDR_E2, theta_rsdr_lim, beta_rsdr_lim, edp_max_RSDR, d_edp_RSDR)
        
        ######################################################################
        # PERDIDAS ESPERADAS DE TODA LA EDIFICACIÓN
        
        EL_NC_ND_E2 = dict_DV_IM_NC_E2['Building']['Loss_building_NC']*(1-POC_E2)*(1-POD_E2['Prob'])
        EL_NC_D_E2 = E_D*(1-POC_E2)*POD_E2['Prob']
        EL_C_E2 = E_C*POC_E2
        
        EL_total_E2 = EL_NC_ND_E2 + EL_NC_D_E2 + EL_C_E2
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA NO COLAPSO DE CADA PISO
        
        try:
            self.grafica_Loss_by_Story_E2.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_by_Story_E2 = Canvas_grafica()      
        self.grafica_Loss_by_Story_E2.ax.clear()
        
        for i in range(len(stories)):
            im_graph = dict_DV_IM_NC_E2[stories[i]]['IM_bin']
            loss_graph = dict_DV_IM_NC_E2[stories[i]]['All_PG']
            
            self.grafica_Loss_by_Story_E2.ax.plot(im_graph, loss_graph, '^--', color = color_py[i], markersize = 4, label = stories[i])

        self.grafica_Loss_by_Story_E2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)', size = 10)   
        self.grafica_Loss_by_Story_E2.ax.set_ylabel("E'[L$_{Story}$ "  + " | NC+R, IM = " + IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)]', size = 10)
        self.grafica_Loss_by_Story_E2.ax.set_ylim(0, 1.05)
        self.grafica_Loss_by_Story_E2.ax.grid(which="both")
        self.grafica_Loss_by_Story_E2.ax.legend(fontsize=10, loc = 'best')
        
        self.ui.graph_DV_IM_2.addWidget(self.grafica_Loss_by_Story_E2)
        
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO PARA NO COLAPSO
        
        try:
            self.grafica_Loss_all_NC_Building_E2.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_all_NC_Building_E2 = Canvas_grafica()      
        self.grafica_Loss_all_NC_Building_E2.ax.clear()

        self.grafica_Loss_all_NC_Building_E2.ax.plot(dict_DV_IM_NC_E2['Building']['IM_bin'], dict_DV_IM_NC_E2['Building']['Loss_building_NC'], '^--',
                                                  color = color_py[0], markersize = 4, linewidth = 2)
        self.grafica_Loss_all_NC_Building_E2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)', size = 10)   
        self.grafica_Loss_all_NC_Building_E2.ax.set_ylabel("E'[L$_{Building}$ "  + " | NC+R, IM = " + IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)]', size = 10)
        self.grafica_Loss_all_NC_Building_E2.ax.set_ylim(0, 1.05)
        self.grafica_Loss_all_NC_Building_E2.ax.grid(which="both")
        
        self.ui.graph_Exp_NC_R_B_2.addWidget(self.grafica_Loss_all_NC_Building_E2)
    
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO (INCLUYE COLPASO, NO COLAPSO, DEMOLICIÓN)
        
        try:
            self.grafica_Loss_all_Building_E2.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_all_Building_E2 = Canvas_grafica()      
        self.grafica_Loss_all_Building_E2.ax.clear()
        
        self.grafica_Loss_all_Building_E2.ax.plot(IM_bin_data_E2, EL_total_E2, '^--', color = color_py[0], markersize = 4, linewidth = 2)
        self.grafica_Loss_all_Building_E2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)', size = 10)   
        self.grafica_Loss_all_Building_E2.ax.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)]', size = 10)
        self.grafica_Loss_all_Building_E2.ax.set_ylim(0, 1.05)
        self.grafica_Loss_all_Building_E2.ax.grid(which="both")
        
        self.ui.graph_Exp_B_2.addWidget(self.grafica_Loss_all_Building_E2)
        
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO POR EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_Loss_byEvents_Building_E2.close()
        except AttributeError:
            pass
                
        self.grafica_Loss_byEvents_Building_E2 = Canvas_grafica()      
        self.grafica_Loss_byEvents_Building_E2.ax.clear()
        
        self.grafica_Loss_byEvents_Building_E2.ax.plot(IM_bin_data_E2, EL_NC_ND_E2, '^--', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND')
        self.grafica_Loss_byEvents_Building_E2.ax.plot(IM_bin_data_E2, EL_NC_D_E2, '^--', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D')
        self.grafica_Loss_byEvents_Building_E2.ax.plot(IM_bin_data_E2, EL_C_E2, '^--', linewidth = 2, markersize = 4, color = 'red', label ='C')

        self.grafica_Loss_byEvents_Building_E2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)', size = 10)   
        self.grafica_Loss_byEvents_Building_E2.ax.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)]', size = 10)
        self.grafica_Loss_byEvents_Building_E2.ax.set_ylim(0, 1.05)
        self.grafica_Loss_byEvents_Building_E2.ax.legend(fontsize=10, loc = 'best')
        self.grafica_Loss_byEvents_Building_E2.ax.grid(which="both")
        
        self.ui.graph_ExpEvents_B_2.addWidget(self.grafica_Loss_byEvents_Building_E2)
        
        ######################################################################
        # GRAFICA DE PROBABILIDADES DE EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_prob_events_E2.close()
        except AttributeError:
            pass
                
        self.grafica_prob_events_E2 = Canvas_grafica()      
        self.grafica_prob_events_E2.ax.clear()
        
        self.grafica_prob_events_E2.ax.plot(IM_bin_data_E2, (1-POC_E2)*(1-POD_E2['Prob']), '^--', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND')
        self.grafica_prob_events_E2.ax.plot(IM_bin_data_E2, (1-POC_E2)*POD_E2['Prob'], '^--', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D')
        self.grafica_prob_events_E2.ax.plot(IM_bin_data_E2, POC_E2, '^--', linewidth = 2, markersize = 4, color = 'red', label ='C')

        self.grafica_prob_events_E2.ax.set_xlabel(IM_name_graph_E2 + '(T = ' + str(T_E2) + 's)', size = 10)   
        self.grafica_prob_events_E2.ax.set_ylabel("Probability", size = 10)
        self.grafica_prob_events_E2.ax.set_ylim(0, 1.05)
        self.grafica_prob_events_E2.ax.legend(fontsize=10, loc = 'best')
        self.grafica_prob_events_E2.ax.grid(which="both")
        
        self.ui.graph_ProbEvent_B_2.addWidget(self.grafica_prob_events_E2)        
      
    
#%% # FUNCIÓN PARA COMBINACIÓN DE CURVAS DE PÉRDIDAS DV-EDP DE LAS EDIFICACIONES 1 Y 2    
    # ----------------------------------------------------------------------------         
    
    def loss_story_comparison(self):
        
        ######################################################################
        # CARGAR DATOS
        
        # Tipo de IM (Viene de la pestaña de Fragility of Buildings)
        IM_name_graph_E1 = self.ui.IMType_Value_1.currentText()
        IM_name_graph_E2 = self.ui.IMType_Value_2.currentText()
        
        if IM_name_graph_E1 == IM_name_graph_E2:
            current_IM_graph = IM_name_graph_E1
        else:
            current_IM_graph = 'im'
        
        ######################################################################
        # GRAFICA DE DV VS EDP

        try:
            self.grafica_LossStory_comparison.close()
        except AttributeError:
            pass
                
        self.grafica_LossStory_comparison = Canvas_grafica()      
        self.grafica_LossStory_comparison.ax.clear()
       
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        
        if current_story_E1 != 'All':
            if EDP_assoc_E1 == 'SDR':
                aux = dictionary_plot_E1['Loss_data_plot_'  +  current_story_E1]
                self.grafica_LossStory_comparison.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3,
                                                 label = current_story_E1 + ' - ' + current_element_E1 + ' - B1', color = color3[0])
                
            elif EDP_assoc_E1 == 'PFA':
                aux = dictionary_plot_E1['Loss_data_plot_'  +  current_story_E1]
                self.grafica_LossStory_comparison.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3,
                                                 label = current_story_E1 + ' - ' + current_element_E1 + ' - B1', color = color3[0])
        else:
            
            if EDP_assoc_E1 == 'SDR':
                
                for i in range(len(data_StoryTypes_E1['Story Type'].unique())):
                    aux = dictionary_plot_E1['Loss_data_plot_'  +  data_StoryTypes_E1['Story Type'].unique()[i]]
                
                    self.grafica_LossStory_comparison.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3,
                                                 label = data_StoryTypes_E1['Story Type'].unique()[i] + ' - ' + current_element_E1 + ' - B1', color = color3[i])
                
            elif EDP_assoc_E1 == 'PFA':
                for i in range(len(data_StoryTypes_E1['Story Type'].unique())):
                    aux = dictionary_plot_E1['Loss_data_plot_'  +  data_StoryTypes_E1['Story Type'].unique()[i]]
                    
                    self.grafica_LossStory_comparison.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3,
                                                 label = data_StoryTypes_E1['Story Type'].unique()[i] + ' - ' + current_element_E1 + ' - B1', color = color3[i])
                    
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        
        if current_story_E2 != 'All':
            if EDP_assoc_E2 == 'SDR':
                aux = dictionary_plot_E2['Loss_data_plot_'  +  current_story_E2]
                self.grafica_LossStory_comparison.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = current_story_E2 + ' - ' + current_element_E2 + ' - B2', color = color3[0])
                
            elif EDP_assoc_E2 == 'PFA':
                aux = dictionary_plot_E2['Loss_data_plot_'  +  current_story_E2]
                self.grafica_LossStory_comparison.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = current_story_E2 + ' - ' + current_element_E2 + ' - B2', color = color3[0])
        else:
            
            if EDP_assoc_E2 == 'SDR':
                
                for i in range(len(data_StoryTypes_E2['Story Type'].unique())):
                    aux = dictionary_plot_E2['Loss_data_plot_'  +  data_StoryTypes_E2['Story Type'].unique()[i]]
                
                    self.grafica_LossStory_comparison.ax.plot(aux['SDR'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = data_StoryTypes_E2['Story Type'].unique()[i] + ' - ' + current_element_E2 + ' - B2', color = color3[i])
                
            elif EDP_assoc_E2 == 'PFA':
                for i in range(len(data_StoryTypes_E2['Story Type'].unique())):
                    aux = dictionary_plot_E2['Loss_data_plot_'  +  data_StoryTypes_E2['Story Type'].unique()[i]]
                    
                    self.grafica_LossStory_comparison.ax.plot(aux['PFA'], aux['Loss'], linewidth = 3, linestyle = 'dashed',
                                                 label = data_StoryTypes_E2['Story Type'].unique()[i] + ' - ' + current_element_E2 + ' - B2', color = color3[i])
        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS
        
        self.grafica_LossStory_comparison.ax.set_xlabel('EDP', size = 10)   
        self.grafica_LossStory_comparison.ax.set_ylabel("E'[Lj | EDP]", size = 10)
        self.grafica_LossStory_comparison.ax.set_ylim(0, 1.05)
        self.grafica_LossStory_comparison.ax.grid(which="both")
        self.grafica_LossStory_comparison.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comparison_LossStory.addWidget(self.grafica_LossStory_comparison)
        
        
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA NO COLAPSO DE CADA PISO
        
        try:
            self.grafica_Comp_Loss_by_Story.close()
        except AttributeError:
            pass
                
        self.grafica_Comp_Loss_by_Story = Canvas_grafica()      
        self.grafica_Comp_Loss_by_Story.ax.clear()
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        
        stories = list(dict_DV_IM_NC_E1.keys())[:-1]
        
        for i in range(len(stories)):
            im_graph = dict_DV_IM_NC_E1[stories[i]]['IM_bin']
            loss_graph = dict_DV_IM_NC_E1[stories[i]]['All_PG']
            
            self.grafica_Comp_Loss_by_Story.ax.plot(im_graph, loss_graph, 'o-', color = color_py[i], 
                                                       markersize = 4, label = stories[i] + '- B1')
            
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        
        stories = list(dict_DV_IM_NC_E2.keys())[:-1]
        
        for i in range(len(stories)):
            im_graph = dict_DV_IM_NC_E2[stories[i]]['IM_bin']
            loss_graph = dict_DV_IM_NC_E2[stories[i]]['All_PG']
            
            self.grafica_Comp_Loss_by_Story.ax.plot(im_graph, loss_graph, '^--', color = color_py[i],
                                                       markersize = 4, label = stories[i] + '- B2')
        
        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS

        self.grafica_Comp_Loss_by_Story.ax.set_xlabel(current_IM_graph + '(T)', size = 10)   
        self.grafica_Comp_Loss_by_Story.ax.set_ylabel("E'[L$_{Story}$ "  + " | NC+R, IM = " + current_IM_graph + '(T)', size = 10)
        self.grafica_Comp_Loss_by_Story.ax.set_ylim(0, 1.05)
        self.grafica_Comp_Loss_by_Story.ax.grid(which="both")
        self.grafica_Comp_Loss_by_Story.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_exp_story.addWidget(self.grafica_Comp_Loss_by_Story)
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO PARA NO COLAPSO
        
        try:
            self.grafica_Comp_Loss_all_NC_Building.close()
        except AttributeError:
            pass
                
        self.grafica_Comp_Loss_all_NC_Building = Canvas_grafica()      
        self.grafica_Comp_Loss_all_NC_Building.ax.clear()
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        
        self.grafica_Comp_Loss_all_NC_Building.ax.plot(dict_DV_IM_NC_E1['Building']['IM_bin'], dict_DV_IM_NC_E1['Building']['Loss_building_NC'], 
                                                       'o-', color = color_py[0], markersize = 4, linewidth = 2, label = 'B1')
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        
        self.grafica_Comp_Loss_all_NC_Building.ax.plot(dict_DV_IM_NC_E2['Building']['IM_bin'], dict_DV_IM_NC_E2['Building']['Loss_building_NC'], 
                                                       '^--', color = color_py[0], markersize = 4, linewidth = 2, label = 'B2')
        
        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS
        
        self.grafica_Comp_Loss_all_NC_Building.ax.set_xlabel(current_IM_graph + '(T)', size = 10)   
        self.grafica_Comp_Loss_all_NC_Building.ax.set_ylabel("E'[L$_{Building}$ "  + " | NC+R, IM = " + current_IM_graph + '(T)', size = 10)
        self.grafica_Comp_Loss_all_NC_Building.ax.set_ylim(0, 1.05)
        self.grafica_Comp_Loss_all_NC_Building.ax.grid(which="both")
        self.grafica_Comp_Loss_all_NC_Building.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_Exp_NC_R_B.addWidget(self.grafica_Comp_Loss_all_NC_Building)
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO (INCLUYE COLPASO, NO COLAPSO, DEMOLICIÓN)
        
        try:
            self.grafica_Comp_Loss_all_Building.close()
        except AttributeError:
            pass
                
        self.grafica_Comp_Loss_all_Building = Canvas_grafica()      
        self.grafica_Comp_Loss_all_Building.ax.clear()
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        
        self.grafica_Comp_Loss_all_Building.ax.plot(IM_bin_data_E1, EL_total_E1, 'o-', color = color_py[0], 
                                                    markersize = 4, linewidth = 2, label = 'B1')
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        
        self.grafica_Comp_Loss_all_Building.ax.plot(IM_bin_data_E2, EL_total_E2, '^--', color = color_py[0], 
                                                    markersize = 4, linewidth = 2, label = 'B2')
        
        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS
        
        self.grafica_Comp_Loss_all_Building.ax.set_xlabel(current_IM_graph + '(T)', size = 10)   
        self.grafica_Comp_Loss_all_Building.ax.set_ylabel("E'[L$_{Building}$ | " + current_IM_graph + '(T)', size = 10)
        self.grafica_Comp_Loss_all_Building.ax.set_ylim(0, 1.05)
        self.grafica_Comp_Loss_all_Building.ax.grid(which="both")
        self.grafica_Comp_Loss_all_Building.ax.legend(fontsize=7, loc = 'best')
        
        self.ui.graph_comp_exp_building.addWidget(self.grafica_Comp_Loss_all_Building)
        
        ######################################################################
        # GRAFICA DE PÉRDIDAS ESPERADAS PARA TODO EL EDIFICIO POR EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_Comp_Loss_byEvents_Building.close()
        except AttributeError:
            pass
                
        self.grafica_Comp_Loss_byEvents_Building = Canvas_grafica()      
        self.grafica_Comp_Loss_byEvents_Building.ax.clear()
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E1, EL_NC_ND_E1, 'o-', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND - B1')
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E1, EL_NC_D_E1, 'o-', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D - B1')
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E1, EL_C_E1, 'o-', linewidth = 2, markersize = 4, color = 'red', label ='C - B1')

        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E2, EL_NC_ND_E2, '^--', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND - B2')
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E2, EL_NC_D_E2, '^--', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D - B2')
        self.grafica_Comp_Loss_byEvents_Building.ax.plot(IM_bin_data_E2, EL_C_E2, '^--', linewidth = 2, markersize = 4, color = 'red', label ='C - B2')
        
        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS
        
        self.grafica_Comp_Loss_byEvents_Building.ax.set_xlabel(current_IM_graph + '(T)', size = 10)   
        self.grafica_Comp_Loss_byEvents_Building.ax.set_ylabel("E'[L$_{Building}$ | " + current_IM_graph + '(T)', size = 10)
        self.grafica_Comp_Loss_byEvents_Building.ax.set_ylim(0, 1.05)
        self.grafica_Comp_Loss_byEvents_Building.ax.legend(fontsize=7, loc = 'best')
        self.grafica_Comp_Loss_byEvents_Building.ax.grid(which="both")
        
        self.ui.graph_comp_expEvent_building.addWidget(self.grafica_Comp_Loss_byEvents_Building)
        
        ######################################################################
        # GRAFICA DE PROBABILIDADES DE EVENTOS: NC+ND, NC+D, Y C
        
        try:
            self.grafica_Comp_prob_events.close()
        except AttributeError:
            pass
                
        self.grafica_Comp_prob_events = Canvas_grafica()      
        self.grafica_Comp_prob_events.ax.clear()
        
        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 1
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E1, (1-POC_E1)*(1-POD_E1['Prob']), 'o-', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND - B1')
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E1, (1-POC_E1)*POD_E1['Prob'], 'o-', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D - B1')
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E1, POC_E1, 'o-', linewidth = 2, markersize = 4, color = 'red', label ='C - B1')

        #-----------------------------------------------
        # GRAFICA DE EDIFICACIÓN 2
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E2, (1-POC_E2)*(1-POD_E2['Prob']), '^--', linewidth = 2, markersize = 4, color = 'blue', label ='NC + ND - B2')
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E2, (1-POC_E2)*POD_E2['Prob'], '^--', linewidth = 2, markersize = 4, color = 'orange', label ='NC + D - B2')
        self.grafica_Comp_prob_events.ax.plot(IM_bin_data_E2, POC_E2, '^--', linewidth = 2, markersize = 4, color = 'red', label ='C - B2')

        #-----------------------------------------------
        # ESPECIFICACIONES GENERALES PARA AMBAS
        
        self.grafica_Comp_prob_events.ax.set_xlabel(current_IM_graph + '(T)', size = 10)   
        self.grafica_Comp_prob_events.ax.set_ylabel("Probability", size = 10)
        self.grafica_Comp_prob_events.ax.set_ylim(0, 1.05)
        self.grafica_Comp_prob_events.ax.legend(fontsize=7, loc = 'best')
        self.grafica_Comp_prob_events.ax.grid(which="both")
        
        self.ui.graph_comp_prob.addWidget(self.grafica_Comp_prob_events)
        
    
    
#%%        

if __name__ == "__main__":
    #import sys
    app = QtWidgets.QApplication(sys.argv)
    FragilityCurvesTool = QtWidgets.QMainWindow()
    ui = Ui_FragilityCurvesTool()
    ui.setupUi(FragilityCurvesTool)
    #FragilityCurvesTool.show()
    mi_app = MiApp()
    mi_app.show()    
    sys.exit(app.exec_())
    
    

