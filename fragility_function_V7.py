# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 10:35:02 2022

@author: Verónica Abuchar

Versión 7 - 2022-12-14
"""

# IMPORTAR LIBRERIAS
import os 
import glob
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from scipy import stats
import statsmodels.api as sm
from scipy.stats import norm
from scipy.optimize import curve_fit
import statistics
from PyQt5.QtWidgets import QApplication



# IMPORTAR FUNCIONES
from exponente import exponente
from Lectura_Archivos_V2 import *
from Definicion_IM_EDP import *

# IMPORTAR GUI
from GUIFragilityCurvesTool import Ui_FragilityCurvesTool


#%% FUNCIÓN PARA ESTIMAR CURVAS DE FRAGILIDAD DETERMINISTICAS

def fragility_function_det(dataF_IM_EDP_Hz, j, tipo_bin, min_datos_bin, num_bins_inicial, IM_max_graph, IM_delta_graph):
    
    ################################################################
    # 1. BINEADO
    ################################################################
    
    # Especificacion de que no se tiene en cuenta censura para bineo
    include_cens = 0
    EDP_cens = 0.1 # puede ser cualquier numero porque en excedencia no se censura
    
    # Se llama la función que realiza el bineado
    [matriz_IM_EDP, IM_bin_ref, conteo_IM_bin2] = binning_with_cens(dataF_IM_EDP_Hz, tipo_bin, min_datos_bin, num_bins_inicial, include_cens, EDP_cens)
    
    ################################################################
    # 2. CREACIÓN DE MATRIZ DE VALORES J:
    ################################################################

    # j = 1: si la observación SÍ supera el límite del EDP
    # j = 0: si la observación NO supera el límie del EDP
    # La matriz tendrá tantas columnas como valores j+1 haya en el vector j
    # La primera columna corresponde al IM bineado

    matriz_j = pd.DataFrame()
    matriz_j['IM_bin'] = matriz_IM_EDP['IM_bin']

    # Se resetea la numeracion del indice para que se peguen bien los datos j
    matriz_j.reset_index(level=None, drop=True, inplace=True)

    for k in range(len(j)):
        j_aux = pd.DataFrame()
        j_aux['Superó lim?'] = np.zeros(len(matriz_j))
        
        for i in range(0, len(matriz_IM_EDP['IM_bin'])):
            if matriz_IM_EDP.at[i,'EDP'] >= j[k]:
               j_aux.iloc[i] = 1
        
        matriz_j['j = ' + str(j[k])] = j_aux
    
    ################################################################
    # 3. CREACIÓN DE MATRIZ FRAGILITY DE LA FORMA IM_BIN - N - Zi
    ################################################################

    # IM_BIN es la columna que contiene todas las categorías de los bines
    # N es el número de observaciones que tiene un IM_BIN específico
    # Zi es el número de observaciones que superan un j especifico
    # Zi NO es una única columna ¿ habrán tantos Zi comom j hayan

    fragility = pd.DataFrame()
    fragility['IM_bin'] =  IM_bin_ref
    fragility['N'] = conteo_IM_bin2['Cantidad']

    # Estimación de Zi
    for k in range(len(j)):
        fragility['Zi - j = ' + str(j[k])] = matriz_j.groupby(['IM_bin']).aggregate({'j = ' + str(j[k]): 'sum'}).values 


    ################################################################
    # 4. CÁLCULO DE PARÁMETROS DE CURVAS DE FRAGILIDAD
    ################################################################

    # Se crea una matriz con tres columnas:
    # (1) Niveles j
    # (2) Mediana de cada curva j
    # (3) Desviación de cada curva j

    parameters = pd.DataFrame()
    parameters['j'] = j
    parameters['theta'] = np.zeros(len(j))
    parameters['sigma'] = np.zeros(len(j))

    delta_im = IM_delta_graph # Delta para graficar
    IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)

    # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva para cada j
    matriz_plot = pd.DataFrame()
    matriz_plot['IM'] =  IM_plot


    for i in range(len(j)):
        Y = pd.DataFrame()
        
        Y['Zi'] = fragility['Zi - j = ' + str(j[i])]
        
        Y['N-Zi'] = fragility['N'] - fragility['Zi - j = ' + str(j[i])]
        
        
        # Intenta hacer el ajuste, si no lo logra, entonces manda a la consola un error
        try:
            sm_probit_Link = sm.genmod.families.links.probit
            x = np.log(fragility['IM_bin'])
            glm_binom = sm.GLM(Y, sm.add_constant(x), family=sm.families.Binomial(link=sm_probit_Link()))
            
            glm_result = glm_binom.fit()
            weights_py = glm_result.params
            
            # Conversion de coeficientes probit a parámetros de la distribucion lognormal
            sigma_ln = 1/weights_py[1]
            mu_ln = -weights_py[0]/weights_py[1]
        except:
            raise Exception('Error: For j = {} Fragility curves cannot be generated. Try with other parameters.'.format(j[i]))
          
        parameters.at[i,'theta'] = np.exp(mu_ln)
        parameters.at[i,'sigma'] = sigma_ln
        
        matriz_plot['j = ' + str(j[i])] = norm.cdf(np.log(IM_plot), mu_ln, sigma_ln)
    
    return parameters, matriz_plot, fragility, matriz_IM_EDP

#%% FUNCIÓN PARA ESTIMAR CURVAS DE FRAGILIDAD PROBABILISTICAS
# Esta funcion censura y solo ajusta con los datos censurados

def fragility_function_prob(IM, EDP, thetas_DS, betas_DS, tipo_bin, min_datos_bin, num_bins_inicial, IM_max_graph, d_edp, edp_max):
    
    ################################################################
    # 1. BINEADO
    ################################################################
    
    # Se llama la función que realiza el bineado
    [matriz_IM_EDP, IM_bin_ref, conteo_IM_bin2] = binning(IM, EDP, tipo_bin, min_datos_bin, num_bins_inicial)
    
    ################################################################
    # 2. ESTIMACIÓN DE PDFS DE EDPS DE CADA IM BINEADO
    ################################################################
    
    # Definción de dataframe con parametros de las EDPs por bin
    parameters = pd.DataFrame()
    parameters['IM_bin'] = IM_bin_ref
    parameters['#Datos'] = np.zeros(len(IM_bin_ref))
    parameters['mu'] = np.zeros(len(IM_bin_ref))
    parameters['theta'] = np.zeros(len(IM_bin_ref))
    parameters['sigma'] = np.zeros(len(IM_bin_ref))
    
    for i in range(len(conteo_IM_bin2)):
        
        # Selección de IM bineado de interés
        current_IM_bin = IM_bin_ref[i]
        
        # Seleccion de datos que cuentan con el IM de interés
        ind = matriz_IM_EDP.loc[matriz_IM_EDP['IM_bin'] == current_IM_bin]
        
        # Remoción de data que contenga NAN (ocurre con RSDR)
        ind = ind.dropna()
        ind.reset_index(drop = True, inplace=True)
        
        # Remplazo de deriva residual (cuando sea el caso) de 0 a un numero muy pequeño
        ind[ind['EDP'] == 0] = 1e-8
        
        ind['EDP'] = ind['EDP'].astype('float')
        
        # Ajuste a función lognormal
        shape, loc, scale = stats.lognorm.fit(ind['EDP'], floc=0)
        mu = np.log(scale)
        sigma = shape
        
        parameters['#Datos'][i] = len(ind)
        parameters['mu'][i] = mu
        parameters['theta'][i] = np.exp(mu)
        parameters['sigma'][i] = sigma
        
    ################################################################
    # 3. ESTIMACIÓN DE P(DS>ds|EDP)*p(EDP|IM)
    ################################################################
    
    # Dataframe donde se guarda IM y P(DS>ds|EDP)*p(EDP|IM) de cada estado de daño
    DS_IM_data = pd.DataFrame()
    DS_IM_data['IM_bin'] = IM_bin_ref
    
    # Creación de columnas en el DataFrame por DS
    for i in range (len(thetas_DS)):
        var_col = 'DS' + str(i+1)
        DS_IM_data[var_col] = np.zeros(len(IM_bin_ref))
        
    # Dataframe con valores edps a evaluar en la pdf y valores en las curvas de fragilidad DSvsEDP
    CDFs_DS = pd.DataFrame()
    edp_values = np.arange(d_edp, edp_max + d_edp, d_edp)
    CDFs_DS['edp'] = edp_values
    for i in range (len(thetas_DS)):
        var_col = 'CDF_DS' + str(i+1)
        CDFs_DS[var_col] = norm.cdf(np.log(edp_values), np.log(thetas_DS[i]), betas_DS[i])
        
    # Llenado de P(DS>ds|EDP)*p(EDP|IM) en cada IM_bin
    for i in range(len(IM_bin_ref)):
        
        # Parámetros de curvas del bin actual
        mu = parameters['mu'][i]
        sigma = parameters['sigma'][i]
        
        # ------------------------------------------------------
        # Curva pdf de los EDPs del bin actual    
        
        # Valores pdf(edp_values)
        pdf_edp_value_i = stats.lognorm.pdf(x = edp_values, scale = np.exp(mu), s = sigma)
        
        # Convolución para obtener probabilidad en cada estado de daño
        for k in range(len(thetas_DS)):
            var_col_DS = 'DS' + str(k+1)
            var_col_cdf = 'CDF_DS' + str(k+1)
            
            cdf_DSk = CDFs_DS[var_col_cdf]
            
            DS_IM_data[var_col_DS][i] = sum(cdf_DSk * pdf_edp_value_i)*d_edp
    
    
    ################################################################
    # 4. CREACIÓN DE MATRIZ FRAGILITY DE LA FORMA IM_BIN - N - Zi
    ################################################################

    # IM_BIN es la columna que contiene todas las categorías de los bines
    # N es el número de observaciones que tiene un IM_BIN específico
    # Zi es el número de observaciones que superan un j especifico
    # Zi NO es una única columna, habrán tantos Zi comom j hayan

    fragility = pd.DataFrame()
    fragility['IM_bin'] =  IM_bin_ref
    fragility['N'] = 100

    # Estimación de Zi
    for k in range(len(thetas_DS)):
        fragility['Zi - DS' + str(k+1)] =  round(DS_IM_data['DS' + str(k+1)]*100)
    
    ################################################################
    # 5. CÁLCULO DE PARÁMETROS DE CURVAS DE FRAGILIDAD
    ################################################################
    
    # Se crea una matriz con tres columnas:
    # (1) Estados de daño
    # (2) Mediana de cada curva j
    # (3) Desviación de cada curva j

    parameters_DSIM = pd.DataFrame()
    parameters_DSIM['DS'] = np.arange(1, len(thetas_DS)+1)
    parameters_DSIM['theta'] = np.zeros(len(thetas_DS))
    parameters_DSIM['sigma'] = np.zeros(len(thetas_DS))
    
    delta_im = 0.001 # Delta para graficar
    IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)

    # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva para cada j
    matriz_plot = pd.DataFrame()
    matriz_plot['IM'] =  IM_plot
    
    for i in range(len(thetas_DS)):
        
        # Data a ajustar
        Y = pd.DataFrame()
        Y['Zi'] = fragility['Zi - DS' + str(i+1)]
        Y['N-Zi'] = fragility['N'] - fragility['Zi - DS' + str(i+1)]
        
        # Ajuste de curvas
        sm_probit_Link = sm.genmod.families.links.probit
        x = np.log(fragility['IM_bin'])
        glm_binom = sm.GLM(Y, sm.add_constant(x), family=sm.families.Binomial(link=sm_probit_Link()))
        
        glm_result = glm_binom.fit()
        weights_py = glm_result.params
        
        # Conversion de coeficientes probit a parámetros de la distribucion lognormal
        sigma_ln = 1/weights_py[1]
        mu_ln = -weights_py[0]/weights_py[1]
        
        # Guardado de los parámetros
        parameters_DSIM.at[i,'theta'] = np.exp(mu_ln)
        parameters_DSIM.at[i,'sigma'] = sigma_ln
        
        matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), mu_ln, sigma_ln)
    
    return parameters_DSIM, matriz_plot, fragility, matriz_IM_EDP
    
    
    # fig1, ax1 = plt.subplots(figsize=(8,5))
    # for i in range(len(thetas_DS)):
    #     ax1.plot(DS_IM_data['IM_bin'], DS_IM_data['DS'+str(i+1)])
    color = ['green', 'orange', 'red']
    fig1, ax1 = plt.subplots(figsize=(8,5))
    for i in range(len(thetas_DS)):
        ax1.plot(matriz_plot['IM'], matriz_plot['DS' + str(i+1)], color = color[i])
        ax1.plot(DS_IM_data['IM_bin'], DS_IM_data['DS' + str(i+1)], 'o', color = color[i])

#%% FUNCIÓN PARA ESTIMAR FRAGILDIAD CON OPCIONES DE COLAPSO

# include_cens = 1  # 1 = Yes, 0 = No
# porc_fit_curves = [1,1,0.5,0.5] # Puntos que se tendrán en cuenta para el ajuste
# collapse_method = 'count' # 'count': conteo, 'fit': ajuste de censurando

def fragility_function_prob_collapseOptions(dataF_IM_EDP_Hz, EDP_cens, thetas_DS, betas_DS, tipo_bin, min_datos_bin, 
                                            num_bins_inicial, IM_max_graph, d_edp, edp_max, include_cens, porc_curves,
                                            collapse_method, EDP_collapse, IM_delta_graph, count_colap_columns):
    
    ################################################################
    # 1. BINEADO
    ################################################################
    
    # Se llama la función que realiza el bineado
    [matriz_IM_EDP, IM_bin_ref, conteo_IM_bin2] = binning_with_cens(dataF_IM_EDP_Hz, tipo_bin, min_datos_bin, 
                                                                    num_bins_inicial, include_cens, EDP_cens)
      
    ################################################################
    # 2. ESTIMACIÓN DE PDFS DE EDPS DE CADA IM BINEADO
    ################################################################
    
    # Definción de dataframe con parametros de las EDPs por bin
    parameters = pd.DataFrame()
    parameters['IM_bin'] = IM_bin_ref
    parameters['#DatosCensurados'] = np.zeros(len(IM_bin_ref))
    parameters['mu'] = np.zeros(len(IM_bin_ref))
    parameters['theta'] = np.zeros(len(IM_bin_ref))
    parameters['sigma'] = np.zeros(len(IM_bin_ref))
    
    # Definición de dataframe para conteo de datos que sobrepasan el límite de colapso
    collapse_count = pd.DataFrame()
    collapse_count['IM_bin'] = IM_bin_ref
    collapse_count['#DatosTodos'] = np.zeros(len(IM_bin_ref))
    collapse_count['#ColapsosCens'] = np.zeros(len(IM_bin_ref))
    collapse_count['P(ColapsoNoCens)'] = np.zeros(len(IM_bin_ref))
    
    for i in range(len(conteo_IM_bin2)):
        
        # Selección de IM bineado de interés
        current_IM_bin = IM_bin_ref[i]
        
        # Seleccion de datos que cuentan con el IM de interés
        ind = matriz_IM_EDP.loc[matriz_IM_EDP['IM_bin'] == current_IM_bin]
        
        # Remoción de data que contenga NAN (ocurre con RSDR)
        ind = ind.dropna()
        ind.reset_index(drop = True, inplace=True)
        
        # LLenado de número de datos antes de censurar
        collapse_count['#DatosTodos'][i] = len(ind)
        
        # Selección de datos que cuentan con EDP menor a EDP_cens
        ind = ind.loc[ind['EDP'] <= EDP_cens]
        
        # LLenado de número de datos que sobrepasan EDP_cens
        collapse_count['#ColapsosCens'][i] = collapse_count['#DatosTodos'][i] - len(ind)
        
        # Estimación de probabilidad de colapso a partir del conteo de soprepaso o no del límite de Censura
        collapse_count['P(ColapsoNoCens)'][i] = collapse_count['#ColapsosCens'][i]/collapse_count['#DatosTodos'][i]
        
        # Remplazo de deriva residual (cuando sea el caso) de 0 a un numero muy pequeño
        ind[ind['EDP'] == 0] = 1e-8
        
        try:
            # Ajuste a función lognormal de los datos que se encuentran por debajo de la censura
            shape, loc, scale = stats.lognorm.fit(ind['EDP'].astype(float), floc=0)
            mu = np.log(scale)
            sigma = shape
        except:
            raise Exception('Error in Step 2 of the function of Fragility: It is not possible to fit a lognormal for IM_bin = {}'.format(current_IM_bin))
        
        # Guardado de parámetros fitted
        parameters['#DatosCensurados'][i] = len(ind)
        parameters['mu'][i] = mu
        parameters['theta'][i] = np.exp(mu)
        parameters['sigma'][i] = sigma
    
    ################################################################
    # 3. ESTIMACIÓN DE P(DS>ds|EDP)*p(EDP|IM) -- Convolución
    ################################################################
    
    # Cantidad de estados de daño considerados
    if collapse_method == 'fit':
        num_DS = len(thetas_DS)
    elif collapse_method == 'count' or 'count columns':
        num_DS = len(thetas_DS)+1
    
    # Dataframe donde se guarda IM y P(DS>ds|EDP)*p(EDP|IM) de cada estado de daño
    DS_IM_data = pd.DataFrame()
    DS_IM_data['IM_bin'] = IM_bin_ref
    
    # Creación de columnas en el DataFrame por DS
    for i in range (num_DS):
        var_col = 'DS' + str(i+1)
        DS_IM_data[var_col] = np.zeros(len(IM_bin_ref))
        
    # Dataframe con valores edps a evaluar en la pdf y valores en las curvas de fragilidad DSvsEDP
    CDFs_DS = pd.DataFrame()
    edp_values = np.arange(d_edp, edp_max + d_edp, d_edp)
    CDFs_DS['edp'] = edp_values
    for i in range (len(thetas_DS)):
        var_col = 'CDF_DS' + str(i+1)
        CDFs_DS[var_col] = norm.cdf(np.log(edp_values), np.log(thetas_DS[i]), betas_DS[i])
        
    # Llenado de P(DS>ds|EDP)*p(EDP|IM) en cada IM_bin
    for i in range(len(IM_bin_ref)):
        
        # Parámetros de curvas del bin actual
        mu = parameters['mu'][i]
        sigma = parameters['sigma'][i]
        
        # Valores pdf(edp_values)
        pdf_edp_value_i = stats.lognorm.pdf(x = edp_values, scale = np.exp(mu), s = sigma)
        
        # Convolución para obtener probabilidad en cada estado de daño: puntos para generacion de curvas
        for k in range(len(thetas_DS)):
            var_col_DS = 'DS' + str(k+1)
            var_col_cdf = 'CDF_DS' + str(k+1)
            
            cdf_DSk = CDFs_DS[var_col_cdf]
            
            DS_IM_data[var_col_DS][i] = sum(cdf_DSk * pdf_edp_value_i)*d_edp
            
    
    ################################################################
    # 4. AJUSTE DE PROBABILIDAD PARA COLAPSO
    ################################################################
    
    Prob_diferent_for_colapse = 1 #0: No se ajusta el colapso de forma distinta a los demas DS, 1: Si se ajusta diferente y entra al primer if
    
    if collapse_method == 'fit' and Prob_diferent_for_colapse == 1:
        # Para colapso (DS4) la formulación de la probabilidad se hace un ponderado de la siguiente forma:
        # P(conv)*(1-P(ColapsoNoCens)) + P(ColapsoNoCens)
    
        for i in range(len(IM_bin_ref)):
            P_colapseNoCens = collapse_count['P(ColapsoNoCens)'][i]
            DS_IM_data[DS_IM_data.columns[-1]][i] = DS_IM_data[DS_IM_data.columns[-1]][i] * (1 - P_colapseNoCens) + P_colapseNoCens
    
    elif collapse_method == 'count':
        # se establece un limite de colapso y se determina cuantos datos lo superan o no
        
        collapse_limit = EDP_collapse
        
        for i in range(len(IM_bin_ref)):
            
            # Selección de IM bineado de interés
            current_IM_bin = IM_bin_ref[i]
            
            # Seleccion de datos que cuentan con el IM de interés
            ind = matriz_IM_EDP.loc[matriz_IM_EDP['IM_bin'] == current_IM_bin]
            
            # Remoción de data que contenga NAN (ocurre con RSDR)
            ind = ind.dropna()
            ind.reset_index(drop = True, inplace=True)
            
            # Conteo de datos que estan en el current_IM_bin
            current_total_data = len(ind)
            
            # Selección de datos que cuentan con EDP menor a EDP_cens
            ind = ind.loc[ind['EDP'] <= collapse_limit]
            
            # Conteo de colapsos
            current_colapse_data = current_total_data - len(ind)
            
            # Asignación de probabilidad de colapso
            DS_IM_data[DS_IM_data.columns[-1]][i] = current_colapse_data/current_total_data
            
    elif collapse_method == 'count columns':
        
        # Se llama la función que realiza el bineado
        [matriz_IM_EDP_count, IM_bin_ref_count, conteo_IM_bin2_count] = binning_with_cens(count_colap_columns, tipo_bin, min_datos_bin, 
                                                                                                   num_bins_inicial, include_cens, EDP_cens) 
        for i in range(len(IM_bin_ref_count)):
            
            # Selección de IM bineado de interés
            current_IM_bin = IM_bin_ref_count[i]
            
            # Seleccion de datos que cuentan con el IM de interés
            ind = matriz_IM_EDP_count.loc[matriz_IM_EDP_count['IM_bin'] == current_IM_bin]
            
            # Conteo de datos que estan en el current_IM_bin
            current_total_data = len(ind)
            
            # Conteo de colapsos
            current_colapse_data = ind['count_colap'].sum()
            
            # Asignación de probabilidad de colapso
            DS_IM_data[DS_IM_data.columns[-1]][i] = current_colapse_data/current_total_data
    
    
    ################################################################
    # 5. CREACIÓN DE MATRIZ FRAGILITY DE LA FORMA IM_BIN - N - Zi
    ################################################################

    # IM_BIN es la columna que contiene todas las categorías de los bines
    # N es el número de observaciones que tiene un IM_BIN específico
    # Zi es el número de observaciones que superan un j especifico
    # Zi NO es una única columna, habrán tantos Zi comom j hayan

    fragility = pd.DataFrame()
    fragility['IM_bin'] =  IM_bin_ref
    fragility['N'] = 100

    # Estimación de Zi
    for k in range(num_DS):
        fragility['Zi - DS' + str(k+1)] =  round(DS_IM_data['DS' + str(k+1)]*100)
    
    ################################################################
    # 6. CÁLCULO DE PARÁMETROS DE CURVAS DE FRAGILIDAD
    ################################################################
    
    # Se crea una matriz con tres columnas:
    # (1) Estados de daño
    # (2) Mediana de cada curva j
    # (3) Desviación de cada curva j

    parameters_DSIM = pd.DataFrame()
    parameters_DSIM['DS'] = np.arange(1, num_DS+1)
    parameters_DSIM['theta'] = np.zeros(num_DS)
    parameters_DSIM['sigma'] = np.zeros(num_DS)
    
    delta_im = IM_delta_graph # Delta para graficar
    IM_plot = np.arange(delta_im, IM_max_graph + delta_im, delta_im)

    # Matriz con primera columna IM_plot y las demás columnas son los puntos que arman la curva para cada j
    matriz_plot = pd.DataFrame()
    matriz_plot['IM'] =  IM_plot
    
    for i in range(num_DS):
        
        # Data a ajustar
        Y = pd.DataFrame()
        Y['Zi'] = fragility['Zi - DS' + str(i+1)]
        Y['N-Zi'] = fragility['N'] - fragility['Zi - DS' + str(i+1)]
        
        # --------------------------------------------------------------------
        # Determinación de los valores de los puntos que se tendrán en cuenta para estimar los parámetros
        Y2 = Y.copy()
        fragility2 = fragility.copy()
        
        current_porc = porc_curves[i]
        
        # Se borra la data que no supere el valor máximo alcanzado        
        ind = Y.loc[Y['Zi'] <= current_porc*100]
        lista_index = list(ind.index)
        # last_index = lista_index[-1]
        
        for k in range(len(Y)):
            if k in lista_index:
                pass
            else:
                Y2.drop(k, axis=0, inplace=True)
                fragility2.drop(k, axis=0, inplace=True)
        
        # --------------------------------------------------------------------
        # Ajuste de curvas
        
        # Intenta hacer el ajuste, si no lo logra, entonces manda a la consola un error
        try:
            sm_probit_Link = sm.genmod.families.links.probit
            x = np.log(fragility2['IM_bin'])
            glm_binom = sm.GLM(Y2, sm.add_constant(x), family=sm.families.Binomial(link=sm_probit_Link()))
            
            glm_result = glm_binom.fit()
            weights_py = glm_result.params
            
            # Conversion de coeficientes probit a parámetros de la distribucion lognormal
            sigma_ln = 1/weights_py[1]
            mu_ln = -weights_py[0]/weights_py[1]
        except:
            raise Exception('Error: For DS{}, Fragility curves cannot be generated. Try with other parameters.'.format(i+1))
            
        # Guardado de los parámetros
        parameters_DSIM.at[i,'theta'] = np.exp(mu_ln)
        parameters_DSIM.at[i,'sigma'] = sigma_ln
        
        matriz_plot['DS' + str(i+1)] = norm.cdf(np.log(IM_plot), mu_ln, sigma_ln)
    
    return parameters_DSIM, matriz_plot, fragility, matriz_IM_EDP

#%% FUNCIÓN PARA BINEAR DATA

def binning(IM, EDP, tipo_bin, min_datos_bin, num_bins_inicial):
    
    #################################################
    # 1. ORDENAR DATOS DE MENOR A MAYOR IM:
    #################################################

    IM_EDP = pd.DataFrame()
    IM_EDP['IM'] = IM
    IM_EDP['EDP'] = EDP

    IM_EDP = IM_EDP.sort_values('IM')
    IM_EDP = IM_EDP.reset_index(drop=True)
    
    #################################################
    # 2. BINEADO:
    #################################################

    # Se presentan dos tipos de bineado:
    # 1 = bineado con bines igualmente espaceados
    # 2 = bineado con bines espaciados en el espacio log 

    IM_min = IM_EDP['IM'].min()
    IM_max = IM_EDP['IM'].max() 
        
    if tipo_bin == 1:
        d_im = (IM_max - IM_min)/(num_bins_inicial-1)
        IM_bin_ref = np.arange(IM_min-2*d_im,IM_max+2*d_im, step = d_im)
        
    elif tipo_bin == 2:
        # Exponente mínimo y máximo
        exp_min = exponente(IM_min)
        exp_max = exponente(IM_max)
        IM_bin_ref = np.logspace(exp_min, exp_max+1, num = num_bins_inicial)
        
    #-----------------------------------------------------------------------------
    # DESCRIPCIÓN
    # Para la realización del bineo hay dos fases: 
    # FASE 1: Se realiza el bineo con los binesespecificados inicialmente, estos es, habrá cuantas clases se obtengan 
    # a partir del d_im definido (tipo 1) o cuantas clases se obtengan de la variable num_bins_inicial (tipos 2)
    # FASE 2: Se agrupan los bines de la fase 1 hasta que haya un mpinimo de datos por bin que corresponde a la variable
    # de entrada min_datos_bin

    #-----------------------------------------------------------------------------
    # FASE 1:
    IM_bin = np.zeros(len(IM_EDP['IM']))

    # Dataframe con tres columnas: IM, nuevo IM bineado y EDP
    matriz_IM_EDP = pd.DataFrame()
    matriz_IM_EDP['IM'] = IM_EDP['IM']
    matriz_IM_EDP['IM_bin'] = IM_bin
    matriz_IM_EDP['EDP'] = IM_EDP['EDP']

    # Dataframe que contará cuantos IMs incluyen cada clase IM bineado
    conteo_IM_bin = pd.DataFrame()
    conteo_IM_bin['IM_bin_ref'] = IM_bin_ref
    conteo_IM_bin['Cantidad'] = np.zeros(len(IM_bin_ref)) 

    # Llenado de DataFrames
    indice = 0      # Revisa los indices de la matriz IM_bin_ref
    ind_ref = 0     # Indice de la matriz conteo_IM_bin
    cont1 = 0       # Contador de datos en los bines
    cont2 = 0       # Contador para el último bin
    flag = 0        # Indica que la data ya entró al elif, es decir, a la ultima clase de IM_bin_ref si no lo detecta el primer if

    for i in range (0, len(IM_EDP['IM'])):
        ok = 0
        
        while ok == 0:
            if matriz_IM_EDP.iloc[i,0] <= (IM_bin_ref[indice] + IM_bin_ref[indice+1])/2:
                ok = 1
                matriz_IM_EDP.iloc[i,1] = IM_bin_ref[indice]
                cont1 = cont1 + 1
                
            elif matriz_IM_EDP.iloc[i,0] > (IM_bin_ref[-1] + IM_bin_ref[-2])/2:
                flag = 1
                ok = 1
                matriz_IM_EDP.iloc[i,1] = IM_bin_ref[-1]
                cont2 = cont2 + 1
                
            else:
                # Este else indica que ya salió de un bin_ref y pasa al siguiente
                conteo_IM_bin.iloc[ind_ref,1] = cont1
                indice = indice + 1
                cont1 = 0 # se reinicia el contador de bines
                ind_ref = ind_ref + 1

    # Asignación de cantidad de data por si el i = len(IM_EDP['IM']) y no alcanza a entrar al else
    conteo_IM_bin.iloc[ind_ref,1] = cont1

    # Si el algoritmo entra al elif entonces se asigna el conteo de esa última categoria
    if flag == 1:
        conteo_IM_bin.iloc[ind_ref+1,1] = cont2

    # Dataframe que no incluye bines con cero
    conteo_IM_bin = conteo_IM_bin[conteo_IM_bin['Cantidad']>0]
    conteo_IM_bin =conteo_IM_bin.reset_index(drop=True)

    #-----------------------------------------------------------------------------
    # FASE 2:

    # Se agrupan bines hasta contar con el mínimo de datos
    # Dataframe conteo_IM_bin2 tendrá 3 columnas:
    # (1) El im de referencia desde el que se toman los datos para ese bin
    # (2) El im de referencia hasta el que se completan los datos para ese bin
    # (3) El total de datos en esa agrupación de bines

    conteo_IM_bin2 = pd.DataFrame()
    conteo_IM_bin2['IM inferior'] = np.zeros(len(conteo_IM_bin)) 
    conteo_IM_bin2['IM superior'] = np.zeros(len(conteo_IM_bin))
    conteo_IM_bin2['Cantidad'] = np.zeros(len(conteo_IM_bin))  

    i = 0       # Contador de fila de conteo_IM_bin
    k = 0       # Contador de fila de conteo_IM_bin2

    while i <= len(conteo_IM_bin)-1:
        if conteo_IM_bin.iloc[i,1] >= min_datos_bin:
            conteo_IM_bin2.iloc[k,0] = conteo_IM_bin.iloc[i,0]
            conteo_IM_bin2.iloc[k,1] = conteo_IM_bin.iloc[i,0]
            conteo_IM_bin2.iloc[k,2] = conteo_IM_bin.iloc[i,1]
            i = i+1
            k = k+1
            
        else:
            flag = True
            pos_0 = i
            suma = conteo_IM_bin.iloc[pos_0,1]
            
            if i == len(conteo_IM_bin)-1:
                pos_f = i
                flag = False
            else:
                while flag == True:
                    i = i+1
                    suma = suma + conteo_IM_bin.iloc[i,1]
                    if (suma >= min_datos_bin) or (i==len(conteo_IM_bin)-1):
                        pos_f = i
                        flag = False
            
            conteo_IM_bin2.iloc[k,0] = conteo_IM_bin.iloc[pos_0,0]
            conteo_IM_bin2.iloc[k,1] = conteo_IM_bin.iloc[pos_f,0]
            conteo_IM_bin2.iloc[k,2] = suma
            i = i+1
            k = k+1

    conteo_IM_bin2 = conteo_IM_bin2[conteo_IM_bin2['Cantidad']>0] 
    conteo_IM_bin2 = conteo_IM_bin2.reset_index(drop=True)          

    # Revisión del último bin ya que puede contener menos datos que el min_datos_bin
    if conteo_IM_bin2.iloc[-1,2] < min_datos_bin:
        conteo_IM_bin2.iloc[-2,1] = conteo_IM_bin2.iloc[-1,1]
        conteo_IM_bin2.iloc[-2,2] = conteo_IM_bin2.iloc[-2,2] + conteo_IM_bin2.iloc[-1,2]
        conteo_IM_bin2.drop(conteo_IM_bin2.tail(1).index, inplace = True)  # Elimina la ultima fila
        
    #-----------------------------------------------------------------------------
    # CORRECCIÓN DE matriz_IM_EDP CON NUEVO BINEADO

    # Suposición: el IM_bin corresponderá a la suma producto de cada bin original con la cantidad de datos
    # de esa clase entre el total de datos para esa nueva agrupación

    cont1 = 0       # Posición de im bineado original (conteo_IM_bin)
    cont2 = 0       # Posición de matriz_IM_EDP
    i = 0           # Posición de conteo_IM_bin2

    while i <= len(conteo_IM_bin2)-1:
        flag = True
        pos_0 = conteo_IM_bin2.iloc[i,0]
        pos_f = conteo_IM_bin2.iloc[i,1]
        sumaproducto = 0
        
        while flag == True:
            if (conteo_IM_bin.iloc[cont1,0] >= pos_0) and (conteo_IM_bin.iloc[cont1,0] <= pos_f):
                sumaproducto = sumaproducto + conteo_IM_bin.iloc[cont1,0]*conteo_IM_bin.iloc[cont1,1]
                cont1 = cont1 + 1
                
                # Se saca de la iteración cuando el contador supere el indice máximo
                if cont1 == len(conteo_IM_bin):
                    flag = False
            else:
                flag = False
        
        nuevo_bin =  sumaproducto/conteo_IM_bin2.iloc[i,2]
        
        # Cambio de bines por el nuevo bin
        for k in range(int(cont2), int(cont2+conteo_IM_bin2.iloc[i,2])):
            matriz_IM_EDP.iloc[k,1] = nuevo_bin
        
        cont2 = cont2 + conteo_IM_bin2.iloc[i,2]
        
        i = i+1

    # Creación de nueva matriz de IMs bineados de reference
    del IM_bin_ref
    IM_bin_ref = matriz_IM_EDP['IM_bin'].unique()
    
    return matriz_IM_EDP, IM_bin_ref, conteo_IM_bin2

#%% FUNCIÓN PARA BINEAR DATA TENIENDO EN CUENTA EDP DE CENSURA

def binning_with_cens(dataF_IM_EDP_Hz, tipo_bin, min_datos_bin, num_bins_inicial, include_cens, EDP_cens):
    
    #################################################
    # 1. ORDENAR DATOS DE MENOR A MAYOR IM:
    #################################################

    dataF_IM_EDP_Hz = dataF_IM_EDP_Hz.sort_values('IM')
    dataF_IM_EDP_Hz = dataF_IM_EDP_Hz.reset_index(drop = True)
    
    #################################################
    # 2. BINEADO:
    #################################################

    # Se presentan dos tipos de bineado:
    # 1 = bineado con bines igualmente espaceados
    # 2 = bineado con bines espaciados en el espacio log 

    IM_min = dataF_IM_EDP_Hz['IM'].min()
    IM_max = dataF_IM_EDP_Hz['IM'].max()
        
    if tipo_bin == 1:
        d_im = (IM_max - IM_min)/(num_bins_inicial-1)
        IM_bin_ref = np.arange(IM_min-2*d_im,IM_max+2*d_im, step = d_im)
        
    elif tipo_bin == 2:
        # Exponente mínimo y máximo
        exp_min = exponente(IM_min)
        exp_max = exponente(IM_max)
        IM_bin_ref = np.logspace(exp_min, exp_max+1, num = num_bins_inicial)
        
    #-----------------------------------------------------------------------------
    # DESCRIPCIÓN
    # Para la realización del bineo hay dos fases: 
        
    # FASE 1: Se realiza el bineo con los bines especificados inicialmente, estos es, habrá cuantas clases se obtengan 
    # a partir del d_im definido (tipo 1) o cuantas clases se obtengan de la variable num_bins_inicial (tipos 2)
    
    # FASE 2: Se agrupan los bines de la fase 1 hasta que haya un minimo de datos por bin que corresponde a la variable
    # de entrada min_datos_bin excluyendo aquellos que sean censurados

    #-----------------------------------------------------------------------------
    # FASE 1:

    # Dataframe con cuatro columnas: IM, nuevo IM bineado, EDP y Hz Lvl
    matriz_IM_EDP_Hz = dataF_IM_EDP_Hz.copy()
    matriz_IM_EDP_Hz['IM_bin'] = np.zeros(len(dataF_IM_EDP_Hz['IM']))

    # Dataframe que contará cuantos IMs incluyen cada clase IM bineado
    conteo_IM_bin = pd.DataFrame()
    conteo_IM_bin['IM_bin_ref'] = IM_bin_ref
    conteo_IM_bin['Cantidad'] = np.zeros(len(IM_bin_ref)) 

    # Llenado de DataFrames
    indice = 0      # Revisa los indices de la matriz IM_bin_ref
    ind_ref = 0     # Indice de la matriz conteo_IM_bin
    cont1 = 0       # Contador de datos en los bines
    cont2 = 0       # Contador para el último bin
    flag = 0        # Indica que la data ya entró al elif, es decir, a la ultima clase de IM_bin_ref si no lo detecta el primer if

    for i in range (len(dataF_IM_EDP_Hz['IM'])):
        ok = 0
        
        while ok == 0:
            if matriz_IM_EDP_Hz.at[i,'IM'] <= (IM_bin_ref[indice] + IM_bin_ref[indice+1])/2:
                ok = 1
                matriz_IM_EDP_Hz.at[i,'IM_bin'] = IM_bin_ref[indice]
                cont1 = cont1 + 1
                
            elif matriz_IM_EDP_Hz.at[i,'IM'] > (IM_bin_ref[-1] + IM_bin_ref[-2])/2:
                flag = 1
                ok = 1
                matriz_IM_EDP_Hz.at[i,'IM_bin'] = IM_bin_ref[-1]
                cont2 = cont2 + 1
                
            else:
                # Este else indica que ya salió de un bin_ref y pasa al siguiente
                conteo_IM_bin.at[ind_ref,'Cantidad'] = cont1
                indice = indice + 1
                cont1 = 0 # se reinicia el contador de bines
                ind_ref = ind_ref + 1

    # Asignación de cantidad de data por si el i = len(dataF_IM_EDP_Hz['IM']) y no alcanza a entrar al else
    conteo_IM_bin.at[ind_ref,'Cantidad'] = cont1

    # Si el algoritmo entra al elif entonces se asigna el conteo de esa última categoria
    if flag == 1:
        conteo_IM_bin.at[ind_ref+1,'Cantidad'] = cont2

    # Dataframe que no incluye bines con cero
    conteo_IM_bin = conteo_IM_bin[conteo_IM_bin['Cantidad']>0]
    conteo_IM_bin = conteo_IM_bin.reset_index(drop = True)

    #-----------------------------------------------------------------------------
    # FASE 2:

    # Se agrupan bines hasta contar con el mínimo de datos sin incluir la data que será censurada
    # en caso de que la opcion de censura vaya incluida
    # Dataframe conteo_IM_bin2 tendrá 3 columnas:
    # (1) El im de referencia desde el que se toman los datos para ese bin
    # (2) El im de referencia hasta el que se completan los datos para ese bin
    # (3) El total de datos en esa agrupación de bines

    conteo_IM_bin2 = pd.DataFrame()
    conteo_IM_bin2['IM inferior'] = np.zeros(len(conteo_IM_bin)) 
    conteo_IM_bin2['IM superior'] = np.zeros(len(conteo_IM_bin))
    conteo_IM_bin2['Cantidad'] = np.zeros(len(conteo_IM_bin))  

    i = 0       # Contador de fila de conteo_IM_bin
    k = 0       # Contador de fila de conteo_IM_bin2
    
    # Si NO se tiene cuenta la censura
    if include_cens == 0:
        
        while i <= len(conteo_IM_bin)-1:
            
            # Verificacion de si el bin cumple la cantidad mínima de datos
            if conteo_IM_bin.at[i,'Cantidad'] >= min_datos_bin:
                
                conteo_IM_bin2.at[k,'IM inferior'] = conteo_IM_bin.at[i,'IM_bin_ref']
                conteo_IM_bin2.at[k,'IM superior'] = conteo_IM_bin.at[i,'IM_bin_ref']
                conteo_IM_bin2.at[k,'Cantidad'] = conteo_IM_bin.at[i,'Cantidad']
                i = i+1
                k = k+1
            
            else:
                flag = True
                pos_0 = i   # Posicion inicial
                suma = conteo_IM_bin.at[pos_0,'Cantidad']
                
                # Si se está en el último bin
                if i == len(conteo_IM_bin)-1:
                    pos_f = i
                    flag = False
                    
                # Si no se está en el ultimo bin
                else:
                    while flag == True:
                        i = i+1
                        suma = suma + conteo_IM_bin.at[i,'Cantidad']
                        
                        # Verificacion de si el bin cumple la cantidad mínima o si se tiene que salir por estar en el ultimo bin
                        if (suma >= min_datos_bin) or (i==len(conteo_IM_bin)-1):
                            pos_f = i
                            flag = False
                    
                conteo_IM_bin2.at[k,'IM inferior'] = conteo_IM_bin.at[pos_0,'IM_bin_ref']
                conteo_IM_bin2.at[k,'IM superior'] = conteo_IM_bin.at[pos_f,'IM_bin_ref']
                conteo_IM_bin2.at[k,'Cantidad'] = suma
                i = i+1
                k = k+1
                
    # Si se tiene cuenta la censura            
    else:
        # Se adiciona una columna que cuenta la cantidad de datos luego de la censura
        conteo_IM_bin2['Cantidad_cens'] = np.zeros(len(conteo_IM_bin))
        
        while i <= len(conteo_IM_bin)-1:
            
            # Matriz que incluye los EDP que no superan el SDR_lim
            ind = matriz_IM_EDP_Hz.loc[matriz_IM_EDP_Hz['IM_bin'] == conteo_IM_bin.at[i,'IM_bin_ref']]
            ind = ind.loc[ind['EDP'] <= EDP_cens]
            
            # Verificación si cumple la cantidad de datos
            if len(ind) >= min_datos_bin:
                conteo_IM_bin2.at[k,'IM inferior'] = conteo_IM_bin.at[i,'IM_bin_ref']
                conteo_IM_bin2.at[k,'IM superior'] = conteo_IM_bin.at[i,'IM_bin_ref']
                conteo_IM_bin2.at[k,'Cantidad'] = conteo_IM_bin.at[i,'Cantidad']
                conteo_IM_bin2.at[k,'Cantidad_cens'] = len(ind)
                i = i+1
                k = k+1
            
            # Si el bin no cumple la cantidad mínima de datos
            else:
                flag = True
                pos_0 = i   # Posicion inicial
                suma = conteo_IM_bin.at[pos_0,'Cantidad']
                
                # Si se está en el último bin
                if i == len(conteo_IM_bin)-1:
                    pos_f = i
                    flag = False
                    
                # Si no se está en el ultimo bin
                else:
                    while flag == True:
                        i = i+1
                        suma = suma + conteo_IM_bin.at[i,'Cantidad']
                        
                        # Ampliacion de la matriz ind que verifica la longitud con cens
                        ind = pd.concat([ind, matriz_IM_EDP_Hz.loc[matriz_IM_EDP_Hz['IM_bin'] == conteo_IM_bin.at[i,'IM_bin_ref']]],
                                        axis = 0, ignore_index = True)
                        ind = ind.loc[ind['EDP'] <= EDP_cens]
                        
                        # Verificacion de si el bin cumple la cantidad mínima o si se tiene que salir por estar en el ultimo bin
                        if len(ind) >= min_datos_bin or (i==len(conteo_IM_bin)-1):
                            pos_f = i
                            flag = False
                                          
                conteo_IM_bin2.at[k,'IM inferior'] = conteo_IM_bin.at[pos_0,'IM_bin_ref']
                conteo_IM_bin2.at[k,'IM superior'] = conteo_IM_bin.at[pos_f,'IM_bin_ref']
                conteo_IM_bin2.at[k,'Cantidad'] = suma
                conteo_IM_bin2.at[k,'Cantidad_cens'] = len(ind)
                i = i+1
                k = k+1
            
    conteo_IM_bin2 = conteo_IM_bin2[conteo_IM_bin2['Cantidad']>0]
    conteo_IM_bin2 = conteo_IM_bin2.reset_index(drop=True)
           

    # Revisión del último bin ya que puede contener menos datos que el min_datos_bin
    if include_cens == 0:
        if conteo_IM_bin2.iloc[-1]['Cantidad'] < min_datos_bin:
            conteo_IM_bin2.iloc[-2]['IM superior'] = conteo_IM_bin2.iloc[-1]['IM superior']
            conteo_IM_bin2.iloc[-2]['Cantidad'] = conteo_IM_bin2.iloc[-2]['Cantidad'] + conteo_IM_bin2.iloc[-1]['Cantidad']
            conteo_IM_bin2.drop(conteo_IM_bin2.tail(1).index, inplace = True)  # Elimina la ultima fila
    else:
        if conteo_IM_bin2.iloc[-1]['Cantidad_cens'] < min_datos_bin:
            conteo_IM_bin2.iloc[-2]['IM superior'] = conteo_IM_bin2.iloc[-1]['IM superior']
            conteo_IM_bin2.iloc[-2]['Cantidad'] = conteo_IM_bin2.iloc[-2]['Cantidad'] + conteo_IM_bin2.iloc[-1]['Cantidad']
            conteo_IM_bin2.iloc[-2]['Cantidad_cens'] = conteo_IM_bin2.iloc[-2]['Cantidad_cens'] + conteo_IM_bin2.iloc[-1]['Cantidad_cens']
            conteo_IM_bin2.drop(conteo_IM_bin2.tail(1).index, inplace = True)  # Elimina la ultima fila
        
    
       
    #-----------------------------------------------------------------------------
    # CORRECCIÓN DE matriz_IM_EDP_Hz CON NUEVO BINEADO

    # Suposición: el IM_bin corresponderá a la suma producto de cada bin original con la cantidad de datos
    # de esa clase entre el total de datos para esa nueva agrupación

    cont1 = 0       # Posición de im bineado original (conteo_IM_bin)
    cont2 = 0       # Posición de matriz_IM_EDP_Hz
    i = 0           # Posición de conteo_IM_bin2

    while i <= len(conteo_IM_bin2)-1:
        flag = True
        pos_0 = conteo_IM_bin2.at[i,'IM inferior']
        pos_f = conteo_IM_bin2.at[i,'IM superior']
        sumaproducto = 0
        
        while flag == True:
            if (conteo_IM_bin.at[cont1,'IM_bin_ref'] >= pos_0) and (conteo_IM_bin.at[cont1,'IM_bin_ref'] <= pos_f):
                sumaproducto = sumaproducto + conteo_IM_bin.at[cont1,'IM_bin_ref'] * conteo_IM_bin.at[cont1,'Cantidad']
                cont1 = cont1 + 1
                
                # Se saca de la iteración cuando el contador supere el indice máximo
                if cont1 == len(conteo_IM_bin):
                    flag = False
            else:
                flag = False
        
        nuevo_bin =  sumaproducto/conteo_IM_bin2.at[i,'Cantidad']
        
        # Cambio de bines por el nuevo bin
        for k in range(int(cont2), int(cont2+conteo_IM_bin2.at[i,'Cantidad'])):
            matriz_IM_EDP_Hz.at[k,'IM_bin'] = nuevo_bin
        
        cont2 = cont2 + conteo_IM_bin2.at[i,'Cantidad']
        
        i = i+1

    # Creación de nueva matriz de IMs bineados de reference
    del IM_bin_ref
    IM_bin_ref = matriz_IM_EDP_Hz['IM_bin'].unique()
    
    return matriz_IM_EDP_Hz, IM_bin_ref, conteo_IM_bin2



#%% FUNCIÓN PARA BINEADO Y ESTIMACIÓN DE PARÁMETROS DE PDFs DE ESOS BINES PARA TODOS LOS PISOS Y EDPs CONSIDERADAS

def binning_and_pdfs_bystory(dict_EDPs_cens, EDPs_list, T, tipo_bin, min_datos_bin, num_bins_inicial):
    
    
    dict_EDPs_bin = {}           # diccionario EDP -> Story -> IM - IM_bin - EDP
    dict_params_log = {}         # diccionario EDP -> Story -> IM_bin - mu - sigma
    
    # ---------------------------------------------------
    # Diccionario para bineado de los edps por piso
    # ---------------------------------------------------
    
    for EDP in EDPs_list:
        # Generación de diccionario de resultados por piso
        dict_stories_bin = {}       # diccionario para el piso actual para el diccionario de bineado
        dict_stories_params = {}    # diccionario para el piso actual para el diccionario de parámetros
        
        for story in dict_EDPs_cens['SDR'].columns[0:-2]:    
            # Data
            IM_data = dict_EDPs_cens['IM'][T]
            EDP_data = dict_EDPs_cens[EDP][story]
            
            # ------------------------------------------------------------
            # Generación de diccionario de la forma EDP -> Story -> IM - IM_bin - EDP

            # Llamado a la función de bineado
            [matriz_IM_EDP, IM_bin_ref, conteo_IM_bin] = binning(IM_data, EDP_data, tipo_bin, min_datos_bin, num_bins_inicial)
            
            # Inclusión del resultado de la matriz en el diccionario de bineado general
            dict_stories_bin[story] = matriz_IM_EDP
            
            # ------------------------------------------------------------
            # Generación de diccionario de la forma EDP -> Story -> IM_bin - #Datos - mu - sigma
            parameters = pd.DataFrame()
            parameters['IM_bin'] = IM_bin_ref
            parameters['#Datos'] = np.zeros(len(IM_bin_ref))
            parameters['mu'] = np.zeros(len(IM_bin_ref))
            parameters['sigma'] = np.zeros(len(IM_bin_ref))
            
            for i in range(len(conteo_IM_bin)):
                
                # Selección de IM bineado de interés
                current_IM_bin = IM_bin_ref[i]
                
                # Seleccion de datos que cuentan con el IM de interés
                ind = matriz_IM_EDP.loc[matriz_IM_EDP['IM_bin'] == current_IM_bin]
                
                # Remoción de data que contenga NAN (ocurre con RSDR)
                ind = ind.dropna()
                ind.reset_index(drop = True, inplace=True)
                
                # Remplazo de deriva residual de 0 a un numero muy pequeño
                # vetor_remp = ind.index[ind['EDP'] == 0].tolist()
                ind[ind['EDP'] == 0] = 1e-8
                
                # Ajuste a función lognormal
                shape, loc, scale = stats.lognorm.fit(ind['EDP'], floc=0)
                mu = np.log(scale)
                sigma = shape
                
                parameters['#Datos'][i] = len(ind)
                parameters['mu'][i] = mu
                parameters['sigma'][i] = sigma
            
            # Inclusión del resultado de la matriz en el diccionario de parámetros de cada bin
            dict_stories_params[story] = parameters
            
        # Inclusión de diccionarios de pisos en los diccionarios generales
        dict_EDPs_bin[EDP] = dict_stories_bin
        dict_params_log[EDP] = dict_stories_params
        
    return dict_EDPs_bin, dict_params_log
    
    
#%% FUNCIÓN PARA BINEADO DE MÁXIMOS VALORES DE RSDR

# A diferencia de la función 'binning_and_pdfs_bystory', esta función toma la deriva residual máxima de todos los pisos,
# es decir, que no hace un ajuste por piso sino por el máximo de ellos.

def binning_and_pdfs_RSDRmax(dict_EDPs_cens, T, tipo_bin, min_datos_bin, num_bins_inicial):   
    
    # Data
    IM_data = dict_EDPs_cens['IM'][T]
    EDP_data = dict_EDPs_cens['RSDR']['max'].copy()
    
    # Llamado a la función de bineado
    [matriz_IM_EDP, IM_bin_ref, conteo_IM_bin] = binning(IM_data, EDP_data, tipo_bin, min_datos_bin, num_bins_inicial)
    
    # Creación de dataframe con parámetros
    parameters = pd.DataFrame()
    parameters['IM_bin'] = IM_bin_ref
    parameters['#Datos'] = np.zeros(len(IM_bin_ref))
    parameters['mu'] = np.zeros(len(IM_bin_ref))
    parameters['sigma'] = np.zeros(len(IM_bin_ref))
    
    for i in range(len(conteo_IM_bin)):
        
        # Selección de IM bineado de interés
        current_IM_bin = IM_bin_ref[i]
        
        # Seleccion de datos que cuentan con el IM de interés
        ind = matriz_IM_EDP.loc[matriz_IM_EDP['IM_bin'] == current_IM_bin]
        
        # Remoción de data que contenga NAN
        ind = ind.dropna()
        ind.reset_index(drop = True, inplace=True)
        
        # Remplazo de deriva residual de 0 a un numero muy pequeño
        # vetor_remp = ind.index[ind['EDP'] == 0].tolist()
        ind[ind['EDP'] == 0] = 1e-8
        
        # Ajuste a función lognormal
        shape, loc, scale = stats.lognorm.fit(ind['EDP'], floc=0)
        mu = np.log(scale)
        sigma = shape
        
        parameters['#Datos'][i] = len(ind)
        parameters['mu'][i] = mu
        parameters['sigma'][i] = sigma
    
    return parameters
    
    
#%% FUNCIÓN QUE GENERA DICCIONARIOS DE CORRIDAS DE TAXONOMIA Y EDIFICACIONES INDIVIDUALES

"""
Se crean cuatro diccionarios de interés:
    
    1) dict_param_buildings
    Este diccionario contiene diccionarios de cada IM utilizada
    Cada diccionario de IM contiene un data frame con las siguientes columnas:
        Edificación - Descripcion - Taxonomia - IM - T - Theta1 - Beta1 - ... - Theta4 - Beta4
    
    2) dict_parm_taxonomy
    Este diccionario contiene diccionarios de cada IM utilizada
    Cada diccionario de IM contiene un data frame con las siguientes columnas:
        Taxonomia - # Edificaciones - IM - T - Theta1 - Beta1 - ... - Theta4 - Beta4
        
    3) dict_points_fragility
    Este diccionario contiene diccionarios de cada IM utilizada
    Cada diccionario de IM contiene diccionarios de cada Edificacion (e.g., CSS_1) y cada Taxonomia
    Cada diccionario de cada Edificación o Taxonomia contiene un data frame con las siguientes columnas
    que contienen la proporcion Z/N con la que se realiza el ajuste
        IM_bin - DS1 - DS2 - DS2 - DS4
    
    4) dict_data_IM_EDP_HzLv
    Este diccionario contiene diccionarios de cada IM utilizada
    Cada diccionario de IM contiene diccionarios de cada Edificacion (e.g., CSS_1) y cada Taxonomia
    Cada diccionario de cada Edificación o Taxonomia contiene un dataframe de la forma:
        IM - EDP - HzLv
"""

def taxonomy_calculation(fname_resultsBuildings, T, taxonomy_list, matriz_filter_tax, results_path, IM_name_graph, EDP_name_graph, story, include_cens,
                         porc_curves, collapse_method, tipo_bin, min_datos_bin, num_bins_inicial, IM_max_graph, ventana_GUI, col_name_tax, delta_max_edp):
    
    
    # # Definición de deltas y valores maximios de  EDPs
    # edp_max_SDR,  edp_max_PFA, edp_max_RSDR = 0.2, 80, 0.2
    # d_edp_SDR, d_edp_PFA, d_edp_RSDR = 0.001, 0.1, 0.0001
    
    IM_delta_graph = 0.001
    
    # Nombre de columnas del matriz_filter_tax sin tax
    columnas_matriz_guia = matriz_filter_tax.columns.tolist()
    columnas_matriz_guia = pd.Series(columnas_matriz_guia)
    columnas_matriz_guia = columnas_matriz_guia.dropna().tolist()
    
    # Cantidad de estados límite: Leer del excel cuantas columnas comienzan con la palabra 'Theta'
    palabra_ds = 'Theta'
    cantidad_DS = sum(1 for valor in columnas_matriz_guia if valor.startswith(palabra_ds))
    
    # Carpetas donde se entrará a buscar resultados
    folders_results_list = os.listdir(fname_resultsBuildings)
    
    # Lista de T de un IM especifico
    IM_T_list = T
    
    # Creación de diccionarios de interés
    dict_param_buildings = {}
    dict_param_taxonomy = {}
    dict_points_fragility = {}
    dict_data_IM_EDP_HzLv = {}
    
    # Contador de IMs
    cont_IM = 0
    
    # Loop que recorre los IM de interés
    for current_IM_T in IM_T_list:
        
        # Periodo de interés
        T = current_IM_T
        
        # Creación de DataFrame de interés para el current_IM_T
        dataF_param_buildings = pd.DataFrame(columns=['Building', 'Code', 'Description', 'Taxonomy',
                                                      'IM', 'T', 'Theta1', 'Beta1', 'Theta2', 'Beta2',
                                                      'Theta3', 'Beta3', 'Theta4', 'Beta4'])
        
        dataF_param_taxonomy = pd.DataFrame(columns = ['Taxonomy', '#Buildings', 'IM', 'T', 
                                                       'Theta1', 'Beta1', 'Theta2', 'Beta2',
                                                       'Theta3', 'Beta3', 'Theta4', 'Beta4'])
        
        
        # Creación de diccionario de cada edificación que contendrá Z/N de cada estado de daño para
        # graficar los puntos que generan las curvas de fragilidad
        dict_buildings_points = {}
        
        # Creación de dataFrame de cada edificacion que contendrá la data IM - EDP - HzLv de datos totales
        dict_building_alldata = {}
        
        # Contador de taxonomia
        cont_tax = 0
        
        # Loop que recorre las taxonomías de interés
        for current_taxonomy in taxonomy_list:
            
            # Matriz con edificaciones que hacen parte de la taxonomia de interés
            buildings = matriz_filter_tax.loc[matriz_filter_tax[col_name_tax] == current_taxonomy]
            
            # Lista de edificaciones que hacen parte de la taxonomia
            buildings_list = buildings['Building Folder Name'].tolist()
            
            # DataFrames para las IM y EDPS totales para combinar toda la data para una misma taxonomia
            dataF_IM_EDP = pd.DataFrame(columns=['IM', 'EDP', 'Hz Lv'])
            
            # DataFrames para conteos de colapso por columnas (count columns)
            dataF_count_colap_columns = pd.DataFrame(columns=['IM', 'EDP', 'count_colap', 'Hz Lv'])
            
            # Contador de edificacion
            cont_build = 0
            
            # Loop que recorre las edificaciones que hacen parte de la taxonomía de interés
            for current_building in buildings_list:
                
                print('Start the calculation of: ', str(current_building))
                
                # # Imprime los valores en la variable satatus_taxonomy de la GUI
                # ventana_GUI.status_taxonomy.setText('Start the calculation of: ' + str(current_building))
                # QApplication.processEvents() # Forzar la actualización de la interfaz gráfica en cada iteración
                
                ######################################################################  
                # Busqueda de carpeta de resultados de interés
                ######################################################################  
                
                # Nombre de carpeta que se desea encontrar
                building_folder_name = str(current_building)
                
                # Ruta de la edificacion
                for posible_folder in folders_results_list:
                    
                    # Creacion de posible ruta
                    building_folder_path = os.path.join(results_path, posible_folder, building_folder_name)
                    
                    # Verificación de si la ruta existe
                    if os.path.isdir(building_folder_path):
                        break
                
                # Se salta el current building si no fue encontrado y va al siguiente
                if os.path.isdir(building_folder_path) == False:
                    print(str(current_building) + ' was not found')
                    continue
                
                ######################################################################  
                # Busqueda de carpeta CSS con la que se corrió la edificación
                ######################################################################  
                
                # Nombre de la carpeta que contiene los acelerogramas con los que se corrió la edificacion
                accel_folder_name = buildings.loc[buildings['Building Folder Name']==current_building]['CSS'].tolist()[0]
                
                # Ruta en la que se encuentra el folder de acelerogramas
                accel_folder_path = os.path.join(results_path, accel_folder_name)
                
                ######################################################################  
                # Hazard Levels de interes y test de tiempos
                ######################################################################
                
                Hzlv_curves = buildings.loc[buildings['Building Folder Name']==current_building]['Hz_levels'].tolist()[0]
                Hzlv_curves = np.asarray(Hzlv_curves.split(",")).astype(int)
                
                timeOK = float(buildings.loc[buildings['Building Folder Name']==current_building]['Time clean'].tolist()[0])
                EDP_limit = float(buildings.loc[buildings['Building Folder Name']==current_building]['SDR clean'].tolist()[0])
                
                ######################################################################
                # Lectura de Datos
                ######################################################################
                
                [Sa_All_HzLVLs, SaAVG_All_HzLVLs, Hazard_All] = RSP_total(accel_folder_path)
                dict_all_EDPs = lectura_EDPs(building_folder_path, Hazard_All)
                test = testRun(building_folder_path, timeOK, EDP_limit, EDP_name_graph, dict_all_EDPs)
                [Sa_All_HzLVLs, SaAVG_All_HzLVLs, dict_all_EDPs] = correccion_test (Sa_All_HzLVLs, SaAVG_All_HzLVLs, dict_all_EDPs, test)
                                
                # Si la longitud de los datos de IM y de EDP no es la misma, entonces este edificio no es tenido en cuenta
                if len(Sa_All_HzLVLs) != len(dict_all_EDPs['SDR']):
                    print('IM and EDP data of the building ', building_folder_name, 'have no the same length')
                    continue
                
                ######################################################################    
                # Organización de datos para estimar fragilidad
                ######################################################################
                
                # Se define si el IM es Sa o SaAVG
                if IM_name_graph == "Sa":
                    IM_data = Sa_All_HzLVLs
                elif IM_name_graph == "SaAVG":
                    IM_data = SaAVG_All_HzLVLs
                   
                # Se define el edp de interés
                EDP_data = dict_all_EDPs[EDP_name_graph]
                    
                # ------------------------------------------
                # Data para estimar fragilidad
                
                # Seleccion de IM y EDP de interés selccionando T y story    
                IM_curva = lista_IM(T, Hzlv_curves, IM_data)
                EDP_curva = lista_EDP(story, Hzlv_curves, EDP_data)
                
                # Datos que contienen unicamente una columna: IM y EDP en cada caso
                IM = IM_curva[T]
                EDP = EDP_curva[story]
                HzLv = EDP_curva['Hz Lv']
                
                # Definición de DataFrame que IM - EDP - HzL
                dataF_IM_EDP_building = pd.DataFrame()
                dataF_IM_EDP_building['IM'] = IM_curva[T]
                dataF_IM_EDP_building['EDP'] = EDP_curva[story]
                dataF_IM_EDP_building['Hz Lv'] = IM_curva['Hz Lv']
                
                # Definición de delta y edp_max
                d_edp = delta_max_edp[EDP_name_graph]['d_edp']
                edp_max = delta_max_edp[EDP_name_graph]['edp_max']
                    
                # Este try es para que si no es posible estimar fragilidad, no se tenga en cuenta
                try:
                
                    ######################################################################    
                    # Generacion de curvas de fragilidad para la edificación actual
                    ######################################################################
                    
                    theta_ds = []
                    beta_ds = []
                    
                    # OJO CON ESTO: Asume que siempre se coloca en el excel guia el ultimo DS aun cuando el método no sea fit
                    if collapse_method == 'count' or collapse_method == 'count columns':
                        cantidad_DS_cens = cantidad_DS - 1
                    else:
                        cantidad_DS_cens = cantidad_DS
                    
                    for i in range (cantidad_DS_cens):
                        theta_ds.append(buildings.loc[buildings['Building Folder Name']==current_building]['Theta'+str(i+1)+' DS-EDP'].tolist()[0])
                        beta_ds.append(buildings.loc[buildings['Building Folder Name']==current_building]['Beta'+str(i+1)+' DS-EDP'].tolist()[0])
                        
                    EDP_collapse = float(buildings.loc[buildings['Building Folder Name']==current_building]['Limit Collapse (count)'].tolist()[0])
                    EDP_cens = float(buildings.loc[buildings['Building Folder Name']==current_building]['EDP cens'].tolist()[0])

                    # Intenta crear una dataframe para el conteo de columnas cuando sea el caso, si no lo encuentra lo crea vacío
                    if collapse_method =='count columns':
                        count_colap_columns = input_colum_count(accel_folder_path, building_folder_path, T, IM_name_graph, EDP_name_graph, story, EDP_collapse, timeOK, EDP_limit)
                        count_colap_columns = count_colap_columns.loc[count_colap_columns['Hz Lv'].isin(Hzlv_curves)]
                    else:
                        count_colap_columns = {}
                        
                    [parameters, matriz_plot, fragility, matriz_IM_EDP] = fragility_function_prob_collapseOptions(dataF_IM_EDP_building, EDP_cens, theta_ds, beta_ds, tipo_bin, min_datos_bin, 
                                                                                                                  num_bins_inicial, IM_max_graph, d_edp, edp_max, include_cens, porc_curves,
                                                                                                                  collapse_method, EDP_collapse, IM_delta_graph, count_colap_columns)
                
                except:
                    print('There are problems generating fragility of the building', building_folder_name)
                
                # Si es posible el try, entonces que continue ejecutando lo siguiente    
                else: 
                    
                    # ------------------------------------------
                    # Guardado de puntos que generan las curvas de fragilidad
                    
                    DS_points_fragility = pd.DataFrame()
                    DS_points_fragility['IM_bin'] = fragility['IM_bin']
                    for i in range(cantidad_DS):
                        DS_points_fragility['DS'+str(i+1)] = fragility['Zi - DS'+str(i+1)]/fragility['N']
                    
                    # Guardado de puntos en diccionario de edificios que tambien contendrá de taxonomias completas
                    dict_buildings_points[building_folder_name] = DS_points_fragility
                    
                    
                    ######################################################################    
                    # Llenado de DataFrames
                    ######################################################################
                    
                    decimales = 6
                    
                    pd_edificacion = current_building
                    pd_numeration = buildings.loc[buildings['Building Folder Name']==current_building]['Internal Code'].tolist()[0]
                    pd_descripcion = buildings.loc[buildings['Building Folder Name']==current_building]['Description Name'].tolist()[0]
                    pd_taxonomia = current_taxonomy 
                    pd_IM = IM_name_graph
                    pd_T = T
                    pd_theta1 = round(parameters['theta'][0],decimales)
                    pd_beta1 = round(parameters['sigma'][0],decimales)
                    pd_theta2 = round(parameters['theta'][1],decimales)
                    pd_beta2 = round(parameters['sigma'][1],decimales)
                    pd_theta3 = round(parameters['theta'][2],decimales)
                    pd_beta3 = round(parameters['sigma'][2],decimales)
                    pd_theta4 = round(parameters['theta'][3],decimales)
                    pd_beta4 = round(parameters['sigma'][3],decimales)
                    
                    
                    # DataFrame con los datos del edificio actual 
                    data_list = pd.DataFrame()
                    data_list[dataF_param_buildings.columns] = [[pd_edificacion, pd_numeration, pd_descripcion, pd_taxonomia, 
                                                                 pd_IM, pd_T, pd_theta1, pd_beta1, pd_theta2, pd_beta2, pd_theta3,
                                                                 pd_beta3, pd_theta4, pd_beta4]]
                    
                    # Guardado de edificio actual en dataframe general
                    dataF_param_buildings = pd.concat([dataF_param_buildings, data_list], axis = 0, ignore_index = True)
                
                # Aunque no se genere fragilidad de una edificación en particular, la data sí se utiliza en la nube de puntos para la taxonomia
                finally:
                    # Guardado de valores IM y EDP en dataframe para generar fragilidad de toda la taxonomia
                    current_IM_T_EDP = pd.DataFrame()
                    current_IM_T_EDP['IM'] = IM
                    current_IM_T_EDP['EDP'] = EDP
                    current_IM_T_EDP['Hz Lv'] = HzLv.astype(int)
                    dataF_IM_EDP = pd.concat([dataF_IM_EDP, current_IM_T_EDP], axis = 0, ignore_index = True)
                    
                    # Guardado de data IM EDP HzLv de la edificacion en diccionario
                    dict_building_alldata[building_folder_name] = current_IM_T_EDP
                    
                    # Guardado de revision de colapsos por conteo
                    try:
                        dataF_count_colap_columns = pd.concat([dataF_count_colap_columns, count_colap_columns], axis = 0, ignore_index = True)
                    except:
                        pass
                    
                    # Incremento de contador
                    cont_build = cont_build + 1
                    print('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+'; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)))
                    
                    # Imprime los valores en la variable satatus_taxonomy de la GUI
                    ventana_GUI.status_taxonomy.setText('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+
                                                        '; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)) + '-- COMPLETED BUILD: '+str(current_building))
                    QApplication.processEvents() # Forzar la actualización de la interfaz gráfica en cada iteración
            
            # El código se sale del loop de todas las edificaciones de una misma taxonomía para estimar fragilidad completa de esta
            
            ######################################################################    
            # Generacion de curvas de fragilidad para la taxonomia actual
            ######################################################################
            
            # IMPORTANTE:
            # Se asume que el theta y beta para una misma taxonomia es el promedio de los thetas y betas de las edificaciones
            
            print('Start the calculation of: ', str(current_taxonomy))
            
            
            # ------------------------------------------
            # Data para estimar fragilidad
            
            
            # Este try es para que si no es posible estimar fragilidad, no se tenga en cuenta
            try:
            
                theta_ds = []
                beta_ds = []
                
                if collapse_method == 'count' or collapse_method == 'count columns':
                    cantidad_DS_cens = cantidad_DS - 1
                else:
                    cantidad_DS_cens = cantidad_DS
                
                for i in range (cantidad_DS_cens):
                    theta_ds.append(round(buildings['Theta'+str(i+1)+' DS-EDP'].mean(),4))
                    beta_ds.append(round(buildings['Beta'+str(i+1)+' DS-EDP'].mean(),4))
                
                EDP_collapse = round(buildings['Limit Collapse (count)'].mean(),4)
                EDP_cens = round(buildings['EDP cens'].mean(),4)
                    
                [parameters, matriz_plot, fragility, matriz_IM_EDP] = fragility_function_prob_collapseOptions(dataF_IM_EDP, EDP_cens, theta_ds, beta_ds, tipo_bin, min_datos_bin, 
                                                                                                              num_bins_inicial, IM_max_graph, d_edp, edp_max, include_cens, porc_curves,
                                                                                                              collapse_method, EDP_collapse, IM_delta_graph, dataF_count_colap_columns)
            except:
                
                print('It was not possible to generate the taxonomy: ', str(current_taxonomy))
            
            # Si es posible el try, entonces que continue ejecutando lo siguiente  
            else:
           
                # ------------------------------------------
                # Guardado de puntos que generan las curvas de fragilidad
                
                DS_points_fragility = pd.DataFrame()
                DS_points_fragility['IM_bin'] = fragility['IM_bin']
                for i in range(cantidad_DS):
                    DS_points_fragility['DS'+str(i+1)] = fragility['Zi - DS'+str(i+1)]/fragility['N']
                
                # Guardado de puntos en diccionario de edificios que tambien contendrá de taxonomias completas
                dict_buildings_points[current_taxonomy] = DS_points_fragility
                
                ######################################################################    
                # Llenado de DataFrames
                ######################################################################
                
                pd_taxonomia = current_taxonomy
                pd_num_buildings = cont_build
                pd_IM = IM_name_graph
                pd_T = T
                pd_theta1 = round(parameters['theta'][0],decimales)
                pd_beta1 = round(parameters['sigma'][0],decimales)
                pd_theta2 = round(parameters['theta'][1],decimales)
                pd_beta2 = round(parameters['sigma'][1],decimales)
                pd_theta3 = round(parameters['theta'][2],decimales)
                pd_beta3 = round(parameters['sigma'][2],decimales)
                pd_theta4 = round(parameters['theta'][3],decimales)
                pd_beta4 = round(parameters['sigma'][3],decimales)
                
                # DataFrame con los datos de la taxonomia actual 
                data_list = pd.DataFrame()
                data_list[dataF_param_taxonomy.columns] = [[pd_taxonomia, pd_num_buildings, pd_IM, pd_T,
                                                             pd_theta1, pd_beta1, pd_theta2, pd_beta2, pd_theta3,
                                                             pd_beta3, pd_theta4, pd_beta4]]
                
                # Guardado de edificio actual en dataframe general
                dataF_param_taxonomy = pd.concat([dataF_param_taxonomy, data_list], axis = 0, ignore_index = True)
                
                # Guardado de data IM EDP HzLv de la edificacion en diccionario
                dict_building_alldata[current_taxonomy] = dataF_IM_EDP
            
            # Incremento de contador
            cont_tax = cont_tax + 1
            print('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+'; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)))
            
            # Imprime los valores en la variable satatus_taxonomy de la GUI
            ventana_GUI.status_taxonomy.setText('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+
                                                '; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)) + '-- COMPLETED TAX: '+str(current_taxonomy))
            QApplication.processEvents() # Forzar la actualización de la interfaz gráfica en cada iteración
        
        
        # El código se sale del loop de la taxonomia de un mismo valor de IM para guardar la info y pasar al siguiente IM
        
        # Guardado de DataFrames y diccionarios en diccionarios generales que tiene en cuenta la IM
        dict_param_buildings[str(current_IM_T)] = dataF_param_buildings
        dict_param_taxonomy[str(current_IM_T)] = dataF_param_taxonomy
        dict_points_fragility[str(current_IM_T)] = dict_buildings_points
        dict_data_IM_EDP_HzLv[str(current_IM_T)] = dict_building_alldata
        
        # Incremento de contador
        cont_IM = cont_IM + 1
        print('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+'; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)))
        
        # Imprime los valores en la variable satatus_taxonomy de la GUI
        ventana_GUI.status_taxonomy.setText('T:'+str(cont_IM)+'/'+str(len(IM_T_list))+'; TAX:'+str(cont_tax)+'/'+str(len(taxonomy_list))+
                                            '; BUILD:'+str(cont_build)+'/'+str(len(buildings_list)) + '-- COMPLETED T: '+str(current_IM_T))
        QApplication.processEvents() # Forzar la actualización de la interfaz gráfica en cada iteración
    
    return dict_param_buildings, dict_param_taxonomy, dict_points_fragility, dict_data_IM_EDP_HzLv
    
    
    
    
    