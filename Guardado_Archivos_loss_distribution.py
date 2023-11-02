# -*- coding: utf-8 -*-
"""
Created on Wed Sep  6 11:49:38 2023

@author: vabuchar
"""

#%% Librería

import os
import shutil
import pandas as pd
import re
import glob

#%% RUTAS Y ARCHIVOS PRINCIPALES

# ---------------------------------------------------------
# CARPETAS DE RESULTADOS DE LAS EDIFICACIONES Y LOS CSS

results_path = 'C:\\Users\\vabuchar\\OneDrive - Universidad del Norte\\+Informes Uninorte MNRS\\++CORRIDAS\\CSS'

# folders_results_list = ['Resultados-post98-L', 'Resultados-post98-T', 'Resultados-84-L','Resultados-84-T', 'Resultados Pre85']

folders_results_list = ['+Resultados_FI_ultimo']
# ---------------------------------------------------------
# EDIFICACIONES Y TAXONOMIAS CON LA INFO REQUERIDA PARA PERDIDAS

# Ubicacion de Excel
data_tax_EL_path = 'C:\\Users\\vabuchar\\OneDrive - Universidad del Norte\Migrado\\+++ GUI\\Prueba1\\GUI_FRAGILITY_V09.2 - Verion 1EDP\\Ejemplo Input\\Guide_for_buildings_for_ExpectedLoss.xlsx'

# Hoja de Excel
sheet_principal = 'Data'

# Matriz general
guide_EL_buildings = pd.read_excel(data_tax_EL_path, sheet_name = sheet_principal)

# ---------------------------------------------------------
# MATRIZ GUIA

# Path de matriz guia de resultados
matriz_path = 'C:\\Users\\vabuchar\\OneDrive - Universidad del Norte\\+Informes Uninorte MNRS\\++CORRIDAS\\Matriz_Edificaciones_Indicativas.xlsx'

# Hoja de Excel
sheet_principal = 'Matriz'

guide_general_buildings = pd.read_excel(matriz_path, sheet_name = sheet_principal)

# Asignacion de nombres a las columnas
for i in range(len(guide_general_buildings.columns)):
    guide_general_buildings.columns.values[i] = guide_general_buildings.iloc[2,i]

# Eliminación de primeras 3 filas porque no contienen data
guide_general_buildings.drop([0,1,2], axis = 0, inplace = True)

# Nos quedamos solo con las versiones finales VF
guide_general_buildings = guide_general_buildings.loc[guide_general_buildings['Version']=='VF']
guide_general_buildings.reset_index(level=None, drop=True, inplace=True)

# ---------------------------------------------------------
# INPUTS EXCELEES GENERALES PARA CADA EDIFICIO

# De esta carpeta se copian los archivos

# Path
inputs_EL_copy_path = 'C:\\Users\\vabuchar\\OneDrive - Universidad del Norte\\+Informes Uninorte MNRS\\Vulnerabilidad - Presupuesto\\Inputs'


#%% BORRAR ARCHIVOS LOSS DISTRIBUTION ACTUALES

for current_folder_result in folders_results_list:
    
    # Path de la actual carpeta de resultados
    current_groupbuilding_path = os.path.join(results_path, current_folder_result)
    
    # Ubicacion en la actual dirección de de carpeta de reultados
    os.chdir(current_groupbuilding_path)
    
    # Lista actual de edificaciones
    current_list_of_building = os.listdir(current_groupbuilding_path)
    
    for current_building in current_list_of_building:
        
        try:
            del name_file_interest
        except NameError:
            pass
        
        try:
            # Ruta de la edificación que se está revisando
            current_building_path = os.path.join(current_groupbuilding_path, current_building)
            
            # Ubicación en la actual direccion
            os.chdir(current_building_path)
        except:
            continue
        
        # Fraccion del nombre
        name_file_interest = glob.glob('*Loss_distribution*')
        
        if name_file_interest:
            
            # print('Archivo encontrado')
            
            # Elimina archivo
            os.remove(os.path.join(current_building_path, name_file_interest[0]))
            
        else:
            print('Archivo NO encontrado para '+current_building)
                

#%% COPIAR ARCHIVOS

for current_folder_result in folders_results_list:
    
    # Path de la actual carpeta de resultados
    current_groupbuilding_path = os.path.join(results_path, current_folder_result)
    
    # Ubicacion en la actual dirección de de carpeta de reultados
    os.chdir(current_groupbuilding_path)
    
    # Lista actual de edificaciones
    current_list_of_building = os.listdir(current_groupbuilding_path)
    
    # Loop que entra de edificio a edificio
    for current_building in current_list_of_building:
        
        try:
            # Path de la edificacion
            current_building_path = os.path.join(current_groupbuilding_path, current_building)
        
            # En matriz general se busca el nombre del loss distribution que se pega
            file_LossDistribution_name = guide_general_buildings.loc[guide_general_buildings['Output CSS']==current_building]['Loss_file']
            file_LossDistribution_name = file_LossDistribution_name.values[0] + '.xlsx'
        except:
            print(current_building + ' was not generated')
            continue
        
        # ruta de excel
        current_loss_file = os.path.join(inputs_EL_copy_path,file_LossDistribution_name)
        
        # Se copia el archivo de Excel a la carpeta de destino
        shutil.copy(current_loss_file, current_building_path)

