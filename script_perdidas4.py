# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:00:30 2023

@author: vabuchar
"""

#%% Librería
import sys
import os
import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import pandas as pd
import math
import statsmodels.api as sm
from scipy import stats
from scipy.stats import norm, weibull_min
from scipy.optimize import curve_fit
from scipy.optimize import minimize, NonlinearConstraint
import glob

# IMPORTAR FUNCIONES
from exponente import exponente
from fragility_function_V7 import *
from Lectura_Archivos_V2 import *
from Definicion_IM_EDP import *
from Loss_functions import *
from GUIFragilityCurvesTool import * 
from Colores_Dispersion import *

######################################################################
# DEFINCIONES PRELIMINARES
######################################################################

color = ['green', 'yellow', 'orange', 'red', 'darkred','black']
color2 = ['blue', 'green', 'yellow', 'orange', 'red', 'darkred','black']
color3 = ['blue', 'orange', 'green', 'red', 'blueviolet','black']

delta_max_edp = {}
delta_max_edp['SDR'] = {'edp_max': 0.3, 'd_edp': 0.001}
delta_max_edp['PFA'] = {'edp_max': 80, 'd_edp': 0.1}
delta_max_edp['RSDR'] = {'edp_max': 0.2, 'd_edp': 0.0001}
delta_max_edp['RDR'] = {'edp_max': 0.3, 'd_edp': 0.001}



# # Datos de edps para plots de pérdidas
# edp_max_SDR = 0.3
# edp_max_PFA = 80
# edp_max_RSDR = 0.25
# d_edp_SDR = 0.001
# d_edp_PFA = 0.1
# d_edp_RSDR = 0.0005

#%% IM vs EDP

######################################################################
#DATOS DE ENTRADA
######################################################################

ruta_principal = os.getcwd()

# --------------------------
# CASO 1
# CSS = 'CSS_205'
# Hz = 'CSS_BAQ_Soil_T1s'

# CASO 2
# CSS = 'CSS_187'
# Hz = 'CSS_BAQ_Soil_T07s'

# CASO 3
# CSS = 'CSS_333'
# Hz = 'CSS_CLO_Soil_T07s'

# CASO 4
CSS = 'CSS_223'
Hz = 'CSS_BAQ_Soil_T1s'

# Rutas de carpetas de IMs y EDPs
fname_HzB1 = ruta_principal + '\\Ejemplo Input\\CSS+Resultados' + '\\' + Hz
fname_EdpB1 = ruta_principal + '\\Ejemplo Input\\CSS+Resultados\\Resultados' + '\\' + CSS

# Revisión de corridas
timeOK_E1 = 0.90
SDR_limit_E1 = 0.04
EDP_cens_E1 = 0.1
SDR_cens_E1 = 0.1

# Especificaciones para las curvas
T_E1 = 1
Hzlv_curves_E1 = [1,2,3,4,5,6,7,8,9,10]
story_E1 = 'max' # Desplegable con opciones. Evaluar con el len el numero de pisos

tipo_bin_E1 = 2 
min_datos_bin_E1 = 15
num_bins_inicial_E1 = 50  
IM_delta_graph_E1 = 0.001
IM_max_graph_E1 = 10

# Parámetros para curvas deterministas
j_E1 = [0.005, 0.01, 0.02, 0.04]

# Parámetros para curvas probabilistas
thetas_DS_E1 = [0.005, 0.01, 0.02, 0.04]
betas_DS_E1 = [0.3, 0.3, 0.3, 0.3]
EDP_collapse_E1 = 0.1
porc_curves_E1 = [1,1,1,1]
num_DS_E1 = len(thetas_DS_E1)

include_cens_E1 = 1
collapse_method_E1 = 'fit'

IM_name_graph_E1 = 'Sa'
EDP_name_graph_E1 = 'SDR'

EDPs_list = ['SDR', 'PFA', 'RSDR']

######################################################################  
# LECTURA DE DATOS

[Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, Hazard_All_E1] = RSP_total(fname_HzB1)
dict_all_EDPs_E1 = lectura_EDPs(fname_EdpB1, Hazard_All_E1)
test_E1 = testRun(fname_EdpB1, timeOK_E1, SDR_limit_E1, EDP_name_graph_E1, dict_all_EDPs_E1)
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

#%% PÉRDIDA DE COMPONENTES

######################################################################
# DATOS DE ENTRADA
######################################################################

costType = "E'[L|Dsi]"
sheet_principal = 'Guide'


# Carga de componentes
excel_name_comp = 'Loss_components_guide.xlsx'
fname_compGuide = ruta_principal + '\\Ejemplo Input' + '\\' + excel_name_comp

######################################################################
# LECTURA DE ARCHIVOS
######################################################################
guide_component = pd.read_excel(fname_compGuide, sheet_name = sheet_principal)

######################################################################
# ESTIMACIÓN DE PÉRDIDAS DE COMPONENTES
######################################################################
# Carga de diccionario con todos los datos de todos los pisos para las dos EDPs
dictionary_loss_E1 = loss_all_stories_allElements (costType, fname_EdpB1, delta_max_edp, fname_compGuide, guide_component)



#%% ESTIMACIÓN DE PÉRDIDAS DE LA FORMA DS VS EDP

######################################################################
# DATOS DE ENTRADA
######################################################################
# Opciones seleccionadas
current_story_E1 = 'All'
current_inputdata_E1 = 'Primary Group'
current_element_E1 = 'NSTR_D'

######################################################################
# ESTIMACIÓN DE PÉRDIDAS DE PISO
######################################################################
# Cargado de diccionario para los elementos de interés
file_name = glob.glob('*Loss_distribution*')
sheet_principal = 'Guide'  
data_StoryTypes_E1 = pd.read_excel(fname_EdpB1 + '\\' + file_name[0], sheet_name = sheet_principal)

[dictionary_plot_E1, EDP_assoc_E1] = plot_loss_groups(current_inputdata_E1, current_element_E1, dictionary_loss_E1, fname_EdpB1, guide_component)

######################################################################    
# GRAFICA DE PÉRIDAS DE PISO DS VS EDP
######################################################################

# fig5, ax5 = plt.subplots(figsize=(8,5))

# if current_story_E1 != 'All':
#     aux = dictionary_plot_E1['Loss_data_plot_'  +  current_story_E1]
#     ax5.plot(aux[EDP_assoc_E1], aux['Loss'], linewidth = 3,
#                                      label = current_story_E1 + ' - ' + current_element_E1, color = color3[0])  
# else:   
#     for i in range(len(data_StoryTypes_E1['Story Type'].unique())):
#         aux = dictionary_plot_E1['Loss_data_plot_'  +  data_StoryTypes_E1['Story Type'].unique()[i]]
#         ax5.plot(aux[EDP_assoc_E1], aux['Loss'], linewidth = 3,
#                                      label = data_StoryTypes_E1['Story Type'].unique()[i] + ' - ' + current_element_E1, color = color3[i])
                
# ax5.set_xlabel(EDP_assoc_E1, size = 10)   
# ax5.set_ylabel("E'[L = " + current_element_E1 + " | " + EDP_assoc_E1 + "]", size = 10)
# ax5.set_ylim(0, 1.05)
# ax5.grid(which="both")
# ax5.legend(fontsize=7, loc = 'best')

#%% ESTIMACIÓN DE PÉRDIDAS DE LA FORMA DS VS IM

######################################################################
# DATOS DE ENTRADA
######################################################################

theta_colapse = 0.97
beta_colapse = 0.40

theta_rsdr_lim = 0.015
beta_rsdr_lim = 0.30

# Valores eperados de demolición y colapso
E_D = 1.0
E_C = 1.0

######################################################################
# PÉRDIDAS ESPERADAS PARA NO COLAPSO
######################################################################

#------------------------------------------------------
# EDP vs IM
#------------------------------------------------------

# # Data de SDR, RSDR, PFA
# [Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, Hazard_All_E1] = RSP_total(fname_HzB1)
# [PFA_All_E1, SDR_All_E1, RSDR_All_E1] = lectura_EDPs(fname_EdpB1, Hazard_All_E1)
# test_E1 = testRun(fname_EdpB1, timeOK_E1, SDR_limit_E1)
# [Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, PFA_All_E1, SDR_All_E1, RSDR_All_E1] = correccion_test (Sa_All_HzLVLs_E1, SaAVG_All_HzLVLs_E1, PFA_All_E1, SDR_All_E1, RSDR_All_E1, test_E1)

# Censurar datos
type_cens = 'lower'
dict_EDPs_Cens_E1 = EDP_censor_data (SDR_cens_E1, type_cens, dict_EDPs_Original_E1)

# Bineado de datos Y parámetros de curvas pdfs
EDPs_list = ['SDR', 'PFA', 'RSDR']
[dict_EDPs_bin_E1, dict_params_log_E1] = binning_and_pdfs_bystory(dict_EDPs_Cens_E1, EDPs_list, T_E1, tipo_bin_E1, min_datos_bin_E1, num_bins_inicial_E1)
stories = list(dict_params_log_E1[EDPs_list[0]].keys())
IM_bin_data = dict_params_log_E1[EDPs_list[0]][stories[0]]['IM_bin']

#------------------------------------------------------
# DV vs EDP
#------------------------------------------------------
# Lectura de todos los pisos los valores de pérdidas STR, NSTR_D y NSTR_A

# Diccionario de los primary groups (PG) para cada piso: contiene valores de EDPs y péridas asociadas a cada valor
dict_PG_NC_loss_E1 = data_plot_primaryGroups (fname_EdpB1, guide_component, dictionary_loss_E1)

#------------------------------------------------------
# ESTIMACIÓN DE PÉRDIDAS ESPERADAS DV VS IM para No Colapso ni Demolicion
#------------------------------------------------------
# Diccionario con los datos par graficar pérdidas DV vs IM para no colapso
dict_DV_IM_NC_E1 = DV_IM_curves_NC(dict_params_log_E1, dict_PG_NC_loss_E1, data_StoryTypes_E1)


#------------------------------------------------------   
# GRAFICA DE PÉRDIDAS ESPERADAS PARA NO COLAPSO DE CADA PISO 
#------------------------------------------------------
fig6, ax6 = plt.subplots(figsize=(8,5))

for i in range(len(stories)):
    im_graph = dict_DV_IM_NC_E1[stories[i]]['IM_bin']
    loss_graph = dict_DV_IM_NC_E1[stories[i]]['All_PG']
    
    ax6.plot(im_graph, loss_graph, 'o-', label = stories[i])

ax6.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax6.set_ylabel("E'[L$_{Story}$ "  + " | NC, IM = " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
# ax6.set_ylim(0, 1.05)
ax6.grid(which="both")
ax6.legend(fontsize=10, loc = 'best')

#--------------------------------------------------------------------- 
# GRAFICA DE PÉRDIDAS ESPERADAS PARA NO COLAPSO DE TODO EL EDIFICIO
#---------------------------------------------------------------------
fig7, ax7 = plt.subplots(figsize=(8,5))

ax7.plot(dict_DV_IM_NC_E1['Building']['IM_bin'], dict_DV_IM_NC_E1['Building']['Loss_building_NC'], 'o-', linewidth = 3)
ax7.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax7.set_ylabel("E'[L$_{Building}$ "  + " | NC, IM = " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
ax7.grid(which="both")

######################################################################
# ESTIMACIÓN DE PROBABILIDAD DE COLAPSO
######################################################################

POC_E1 = norm.cdf(np.log(IM_bin_data), np.log(theta_colapse), beta_colapse)

#--------------------------------------------------------------------- 
# GRAFICA DE PROBABILIDAD DE COLAPSO
#---------------------------------------------------------------------
# fig8, ax8 = plt.subplots(figsize=(8,5))

# ax8.plot(IM_bin_data, POC_E1, 'o-', linewidth = 3)
# ax8.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
# ax8.set_ylabel("P(Collapse)", size = 10)
# ax8.grid(which="both")

######################################################################
# ESTIMACIÓN DE PROBABILIDAD DE DEMOLICIÓN
######################################################################

# Parámetros de curvas pdf RSDR para cada IM_bin
parameters_RSDR_E1 = binning_and_pdfs_RSDRmax(dict_EDPs_Cens_E1, T_E1, tipo_bin_E1, min_datos_bin_E1, num_bins_inicial_E1)

# Probabilidad de demolición
edp_max_RSDR = delta_max_edp['RSDR']['edp_max']
d_edp_RSDR = delta_max_edp['RSDR']['d_edp']
POD_E1 = function_POD(parameters_RSDR_E1, theta_rsdr_lim, beta_rsdr_lim, edp_max_RSDR, d_edp_RSDR)


######################################################################
# PERDIDAS ESPERADAS DE TODA LA EDIFICACIÓN
######################################################################

EL_NC_ND_E1 = dict_DV_IM_NC_E1['Building']['Loss_building_NC']*(1-POC_E1)*(1-POD_E1['Prob'])
EL_NC_D_E1 = E_D*(1-POC_E1)*POD_E1['Prob']
EL_C_E1 = E_C*POC_E1

#--------------------------------------------------------------------- 
# GRAFICA DE PÉRDIDAS ESPERADAS PARA NC+ND, NC+D, Y C DE LA EDIFICACIÓN
#---------------------------------------------------------------------
fig9, ax9 = plt.subplots(figsize=(8,5))

ax9.plot(IM_bin_data, EL_NC_ND_E1, 'o-', linewidth = 3, color = 'blue', label ='NC + ND')
ax9.plot(IM_bin_data, EL_NC_D_E1, 'o-', linewidth = 3, color = 'black', label ='NC + D')
ax9.plot(IM_bin_data, EL_C_E1, 'o-', linewidth = 3, color = 'red', label ='C')

ax9.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax9.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
ax9.legend(fontsize=10, loc = 'best')
ax9.grid(which="both")

#---------------------------------------------------------------------
# GRAFICA DE PÉRDIDAS ESPERADAS DE TODA LA EDIFICACIÓN
#---------------------------------------------------------------------

EL_total_E1 = EL_NC_ND_E1 + EL_NC_D_E1 + EL_C_E1

fig10, ax10 = plt.subplots(figsize=(8,5))

# ax10.plot(IM_bin_data, EL_NC_ND_E1, 'o-', linewidth = 3, color = 'blue', label ='NC + ND')
# ax10.plot(IM_bin_data, EL_NC_D_E1, 'o-', linewidth = 3, color = 'black', label ='NC + D')
# ax10.plot(IM_bin_data, EL_C_E1, 'o-', linewidth = 3, color = 'red', label ='C')

ax10.set_xlim(0, 2)
ax10.set_ylim(0, 1.1)
ax10.set_title('Loss for without fitting of ' + CSS)

ax10.plot(IM_bin_data, EL_total_E1, 'o-', linewidth = 3)
ax10.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax10.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
ax10.grid(which="both")


#--------------------------------------------------------------------- 
# GRAFICA DE PROBABILIDADES
#---------------------------------------------------------------------

fig11, ax11 = plt.subplots(figsize=(8,5))

ax11.plot(IM_bin_data, (1-POC_E1)*(1-POD_E1['Prob']), 'o-', linewidth = 3, color = 'blue', label ='NC + ND')
ax11.plot(IM_bin_data, (1-POC_E1)*POD_E1['Prob'], 'o-', linewidth = 3, color = 'black', label ='NC + D')
ax11.plot(IM_bin_data, POC_E1, 'o-', linewidth = 3, color = 'red', label ='C')

ax11.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax11.set_ylabel("Probability", size = 10)
ax11.legend(fontsize=10, loc = 'best')
ax11.grid(which="both")

#%% AJUSTES

# ----------------------------------------------------------
# Ajuste minimizando

def Papadopoulos(x, alpha, beta, gamma, delta, epsilon):
    
    maxCost = 1
    fun = maxCost*(epsilon*(x**alpha)/(beta**alpha + x**alpha) + (1-epsilon)*(x)**gamma/(delta**gamma + x**gamma))
    
    return fun

def min_error_papad(params, x, y):
    
    alpha, beta, gamma, delta, epsilon = params
    y_pred = Papadopoulos(x, alpha, beta, gamma, delta, epsilon)
    error = np.sum((y-y_pred)**2)
    
    return error


semilla = [1,1,1,1,1]
result = minimize(min_error_papad, semilla, args=(IM_bin_data, EL_total_E1))
alpha_opt, beta_opt, gamma_opt, delta_opt, epsilon_opt = result.x
print("Parámetros óptimos:", alpha_opt, beta_opt, gamma_opt, delta_opt, epsilon_opt)


max_IM = 2
delta_IM = 0.01

IM_plot = np.arange(0, max_IM + delta_IM, delta_IM)
EL_plot_p = Papadopoulos(IM_plot, alpha_opt, beta_opt, gamma_opt, delta_opt, epsilon_opt)

# ----------------------------------------------------------
# Grafica
# fig12, ax12 = plt.subplots(figsize=(8,5))


# ax12.plot(IM_bin_data, EL_total_E1, 'o', linewidth = 3, color = 'black')
# ax12.plot(IM_plot, EL_plot_p, linestyle = '-', linewidth = 3, color = 'black')

# ax12.set_xlim(0, 4)
# ax12.set_ylim(0, 1.2)
# ax12.set_title('Loss for with Papadopoulos fitting of' + CSS)
# ax12.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
# ax12.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
# ax12.grid(which="both")

# ----------------------------------------------------------
# Ajuste con otra libreria

# from lmfit import Model

# # Datos experimentales x e y
# x_data = IM_bin_data  # Coloca tus datos de x aquí
# y_data = EL_total_E1  # Coloca tus datos de y aquí

# # Modelo para ajuste
# model = Model(Papadopoulos)

# # Definir parámetros iniciales y límites
# params = model.make_params(alpha=1, beta=15, gamma=2, delta=10, epsilon=52)
# params['alpha'].min = 0
# params['beta'].min = 0
# params['gamma'].min = 0
# params['delta'].min = 0
# params['epsilon'].min = 0

# # Realizar el ajuste
# result = model.fit(y_data, params, x=x_data)

# # Imprimir resultados
# print(result.fit_report())

# # Parámetros óptimos y sus valores
# alpha_opt = result.params['alpha'].value
# beta_opt = result.params['beta'].value
# gamma_opt = result.params['gamma'].value
# delta_opt = result.params['delta'].value
# epsilon_opt = result.params['epsilon'].value

# print("Parámetros óptimos:", alpha_opt, beta_opt, gamma_opt, delta_opt, epsilon_opt)

# ----------------------------------------------------------
# Ajuste con Weibull

x_data = IM_bin_data
y_data = EL_total_E1

# Definir la función de distribución Weibull
def weibull(x, shape, loc, scale):
    return weibull_min.cdf(x, shape, loc=loc, scale=scale)

# Ajustar la función Weibull a los datos
params, covariance = curve_fit(weibull, x_data, y_data, p0=[1, 0, 1])

# Parámetros estimados
shape_est, loc_est, scale_est = params

print("Parámetros estimados:")
print("Forma:", shape_est)
print("Locación:", loc_est)
print("Escala:", scale_est)

max_IM = 2
delta_IM = 0.01

IM_plot = np.arange(0, max_IM + delta_IM, delta_IM)
EL_plot_w = weibull(IM_plot, shape_est, loc_est, scale_est)

# ----------------------------------------------------------
# Grafica
# fig13, ax13 = plt.subplots(figsize=(8,5))


# ax13.plot(IM_bin_data, EL_total_E1, 'o', linewidth = 3, color = 'black')
# ax13.plot(IM_plot, EL_plot_w, linestyle = '-', linewidth = 3, color = 'black')

# ax13.set_xlim(0, 4)
# ax13.set_ylim(0, 1.2)
# ax13.set_title('Loss for with Weibull fitting of ' + CSS)
# ax13.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
# ax13.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
# ax13.grid(which="both")

# ----------------------------------------------------------
# Grafica comparacion de ajustes

fig14, ax14 = plt.subplots(figsize=(8,5))

ax14.plot(IM_bin_data, EL_total_E1, 'o', linewidth = 2, color = 'black')
ax14.plot(IM_plot, EL_plot_w, linestyle = '-', linewidth = 3, color = 'blue', label = 'Weibul')
ax14.plot(IM_plot, EL_plot_p, linestyle = '-', linewidth = 3, color = 'red', label = 'Papadopaulos')

ax14.set_xlim(0, 2)
ax14.set_ylim(0, 1.1)
ax14.set_title('Loss for with fitting of ' + CSS)
ax14.set_xlabel(IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)', size = 10)   
ax14.set_ylabel("E'[L$_{Building}$ | " + IM_name_graph_E1 + '(T = ' + str(T_E1) + 's)]', size = 10)
ax14.legend(fontsize=10, loc = 'lower right')
ax14.grid(which="both")



