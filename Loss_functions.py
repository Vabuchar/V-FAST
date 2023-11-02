# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 19:16:35 2023

@author: vabuc
"""

#%% LIBRERIAS
import os 
import glob
import pandas as pd
import numpy as np
from scipy.stats import norm
from scipy import stats

from exponente import exponente


#%% 
################################################################################
# FUNCIONES PARA PÉRDIDAS DE COMPONENTES Y POR PISO DE LA FORMA DV VS EDP
################################################################################

#%% FUNCIÓN PARA ESTIMAR POE Y PROBABILIDADES DE ESTAR EN UN ESTADO DE DAÑO, Y VALOR ESPERADO DE COMPONENTES

def Expected_loss_one_component(data_ds_component, d_edp, edp_max, costType):
    plot_ds = pd.DataFrame()
    plot_ds['EDP'] = np.arange(d_edp, edp_max + d_edp, d_edp)
    
    # Estimación de probabilidad de excedencia de cada estado de daño
    for ds_k in range (len(data_ds_component)):
        plot_ds[data_ds_component.iloc[ds_k]['Damage State']] = norm.cdf(np.log(plot_ds['EDP']), np.log(data_ds_component['θ'][ds_k]), data_ds_component['β'][ds_k])
    
    # Estimación de probabilidad de cada estado daño
    for i in range(len(data_ds_component)+1):
        DS_num = i
        plot_ds['P(DS = ds' +  str(DS_num) +')'] = np.zeros(len(plot_ds))
    
    for i in range(len(plot_ds)):
        
        for k in range(len(data_ds_component)+1):
            DS_num = len(data_ds_component)-k
            
            if k == 0:
                plot_ds['P(DS = ds' +  str(DS_num) +')'][i] = plot_ds['DS' + str(DS_num)][i]
            elif DS_num > 0:
                plot_ds['P(DS = ds' +  str(DS_num) +')'][i] = plot_ds['DS' + str(DS_num)][i] - plot_ds['DS' + str(DS_num+1)][i]
            else:
                plot_ds['P(DS = ds' +  str(DS_num) +')'][i] = 1 - plot_ds['DS' + str(DS_num+1)][i]
    
    # Estimación de perdidas
    if costType == "E[L|Dsi]":
    
        plot_ds['E[L|EDP]'] = np.zeros(len(plot_ds))
        
        for i in range(len(plot_ds)):
            expected_value = 0
            
            for k in range(len(data_ds_component)):
                DS_num = k+1
                expected_value = expected_value + data_ds_component['E[Lj/Dsi]'][k]*plot_ds['P(DS = ds' +  str(DS_num) +')'][i]
            
            plot_ds['E[L|EDP]'][i] = expected_value
        
        plot_ds["E'[L|EDP]"] = plot_ds['E[L|EDP]']/max(data_ds_component['E[Lj/Dsi]'])
        
    elif costType == "E'[L|Dsi]":
        
        plot_ds["E'[L|EDP]"] = np.zeros(len(plot_ds))
        
        for i in range(len(plot_ds)):
            expected_value = 0
            
            for k in range(len(data_ds_component)):
                DS_num = k+1
                expected_value = expected_value + data_ds_component["E[Lj/Dsi]"][k]*plot_ds['P(DS = ds' +  str(DS_num) +')'][i]
            
            plot_ds["E'[L|EDP]"][i] = expected_value
    
    # Adicionando la primera fila cero
    dataframe_aux = pd.DataFrame()
    for i in range(len(plot_ds.columns)):
        dataframe_aux[plot_ds.columns[i]] = np.zeros(len(plot_ds)+1)

    dataframe_aux['P(DS = ds0)'][0] = 1
    dataframe_aux[1::] = plot_ds
    
    del plot_ds
    plot_ds = dataframe_aux
            
    return plot_ds

#%% FUNCIÓN PARA ESTIMAR PERDIDAS ESPERADAS DE TODOS LOS ELEMENTOS DE UN PISO

def loss_one_story_allElements (current_story, costType, data_story, delta_max_edp, fname_compGuide, guide):
    
    edp_max_SDR = delta_max_edp['SDR']['edp_max']
    edp_max_PFA = delta_max_edp['PFA']['edp_max']
    d_edp_SDR = delta_max_edp['SDR']['d_edp']
    d_edp_PFA = delta_max_edp['PFA']['d_edp']

    # Número de elementos que tiene la edificación
    num_elements = len(data_story)

    # Data frame con pérdidas
    Loss_by_story_SDR = pd.DataFrame()
    Loss_by_story_SDR['SDR'] = np.arange(0, edp_max_SDR + d_edp_SDR, d_edp_SDR)
    Loss_by_story_PFA = pd.DataFrame()
    Loss_by_story_PFA['PFA'] = np.arange(0, edp_max_PFA + d_edp_PFA, d_edp_PFA)

    for i in range(num_elements):
        
        # Componente i de la edificación
        comp = data_story['Fragility Group'][i]
        ID = data_story['ID'][i]
        
        # Estados de daño del componente i de la edificación
        data_ds_comp = pd.read_excel(fname_compGuide, sheet_name = comp)
        
        # Definición de EDP asociado al componente
        EDP_comp1 = guide.loc[guide['Fragility Group'] == comp]['EDP_Associated']
        EDP_comp1.reset_index(drop = True, inplace=True)
        EDP_comp1 = EDP_comp1[0]
        
        if EDP_comp1 == 'SDR':
            edp_max = edp_max_SDR
            d_edp = d_edp_SDR
            expon = abs(exponente(d_edp)) # para aproximar a ese número
        elif EDP_comp1 == 'PFA':
            edp_max = edp_max_PFA
            d_edp = d_edp_PFA
            expon = abs(exponente(d_edp)) # para aproximar a ese número
        
        # Función para estimar funciones de pérdidas de componentes
        plot_ds = Expected_loss_one_component(data_ds_comp, d_edp, edp_max, costType)
        if EDP_comp1 == 'SDR':
            Loss_by_story_SDR[str(int(ID))] = plot_ds["E'[L|EDP]"]*data_story['Relative Cost'][i]
        elif EDP_comp1 == 'PFA':
            Loss_by_story_PFA[str(int(ID))] = plot_ds["E'[L|EDP]"]*data_story['Relative Cost'][i]
    
    return Loss_by_story_SDR, Loss_by_story_PFA

#%% FUNCIÓN PARA ESTIMAR PERDIDAS ESPERADAS DE TODOS LOS ELEMENTOS DE TODOS LOS PISOS

def loss_all_stories_allElements (costType, fname_Edp, delta_max_edp, fname_compGuide, guide):
    
    edp_max_SDR = delta_max_edp['SDR']['edp_max']
    edp_max_PFA = delta_max_edp['PFA']['edp_max']
    d_edp_SDR = delta_max_edp['SDR']['d_edp']
    d_edp_PFA = delta_max_edp['PFA']['d_edp']
    
    ###################
    # CARGAR DATOS GENERALES DE LA EDIFICACIÓN

    # Ubicación de archivo de edificación
    os.chdir(fname_Edp)

    # Lectura del archivo de la edificación con los datos
    file_name = glob.glob('*Loss_distribution*')
    sheet_principal = 'Guide'

    data_StoryTypes = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = sheet_principal)

    ###################
    # VARIABLES

    # Nombres base de
    SDR_base_name = 'Loss_by_story_SDR_'
    PFA_base_name = 'Loss_by_story_PFA_'

    # Inicialización de diccionario de pérdidas
    dictionary_loss = {}

    ###################
    # ESTIMACIÓN DE DATOS POR PISO

    for k in range(len(data_StoryTypes['Story Type'].unique())):
        
        # -----
        # Definición de piso
        
        # Selección de piso
        current_story = data_StoryTypes['Story Type'].unique()[k]
        print('############## CALCULATE: ' + current_story + ' ##############')

        # Datos de elementos y sus costos relativos
        data_story = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = current_story)
        data_story['Component + Fragility Group'] = data_story['Component'] + ' (' + data_story['Fragility Group'] + ')'
        
        # Número de elementos que tiene la edificación para costos relativos
        num_elements = len(data_story)
        
        # Data frame con pérdidas añadiendo el EDP de interés en la primera columna
        Loss_by_story_SDR = pd.DataFrame()
        Loss_by_story_SDR['SDR'] = np.arange(0, edp_max_SDR + d_edp_SDR, d_edp_SDR)
        Loss_by_story_PFA = pd.DataFrame()
        Loss_by_story_PFA['PFA'] = np.arange(0, edp_max_PFA + d_edp_PFA, d_edp_PFA)
            
        # Bucle para estimación de pérdidas relativas de elemento por elemento de los pisos
        for i in range(num_elements):
            
            # Componente i de la edificación
            comp = data_story['Fragility Group'][i]
            ID = data_story['ID'][i]
            
            # Estados de daño del componente i de la edificación
            data_ds_comp = pd.read_excel(fname_compGuide, sheet_name = comp)
            
            # Definición de EDP asociado al elemento
            EDP_comp1 = guide.loc[guide['Fragility Group'] == comp]['EDP_Associated']
            EDP_comp1.reset_index(drop = True, inplace=True)
            EDP_comp1 = EDP_comp1[0]
            
            # Definición de valores dependiendo el edp asociado
            edp_max = delta_max_edp[EDP_comp1]['edp_max']
            d_edp = delta_max_edp[EDP_comp1]['d_edp']
            expon = abs(exponente(d_edp)) # para aproximar a ese número
            
            # Función para estimar funciones de pérdidas de componentes
            plot_ds = Expected_loss_one_component(data_ds_comp, d_edp, edp_max, costType)
            if EDP_comp1 == 'SDR':
                Loss_by_story_SDR[str(int(ID))] = plot_ds["E'[L|EDP]"]*data_story['Relative Cost'][i]
            elif EDP_comp1 == 'PFA':
                Loss_by_story_PFA[str(int(ID))] = plot_ds["E'[L|EDP]"]*data_story['Relative Cost'][i]
            
            print('Component #' + str(ID) + ' finished')
            
        dictionary_loss[SDR_base_name + current_story] = Loss_by_story_SDR
        dictionary_loss[PFA_base_name + current_story] = Loss_by_story_PFA
        
    return dictionary_loss


#%% FUNCIÓN PARA DEFINIR SUBGRUPO DE DATOS DE PÉRDIDAS QUE SERÁN GRAFICADOS

def plot_loss_groups(current_inputdata, current_element, dictionary_loss, fname_Edp, guide):
    
    # Generalidades de la edificación
    os.chdir(fname_Edp)
    file_name = glob.glob('*Loss_distribution*')
    sheet_principal = 'Guide'
    
    # Nombres de los pisos
    data_StoryTypes = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = sheet_principal)
    
    # Diccionario que contendrá los datos a utilizar para los plots
    dictionary_plot = {}

    for i in range(len(data_StoryTypes['Story Type'].unique())):
        
        # Selección de piso
        current_story = data_StoryTypes['Story Type'].unique()[i]
        
        # Cargar datos del piso
        data_story = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = current_story)
        data_story['Component + Fragility Group'] = data_story['Component'] + ' (' + data_story['Fragility Group'] + ')'

        # Obtención de matriz del diccionario
        Loss_by_story_SDR = dictionary_loss['Loss_by_story_SDR_'  +  current_story].copy()
        Loss_by_story_PFA = dictionary_loss['Loss_by_story_PFA_'  +  current_story].copy()
        
        # Matriz con todas las opciones que contengan el elemento actual
        ind =  data_story.loc[data_story[current_inputdata] == current_element]
        ind.reset_index(drop = True, inplace=True)
        
        # Busqueda de EDP asociado al elemento descrito
        EDP_assoc = guide.loc[guide['Fragility Group'] == ind['Fragility Group'][0]]['EDP_Associated']
        EDP_assoc.reset_index(drop = True, inplace=True)
        EDP_assoc = EDP_assoc[0]
        
        # Matriz con data necesaria para graficar perdidas por piso
        loss_data_plot = pd.DataFrame()
        if EDP_assoc == 'SDR':
            loss_data_plot['SDR'] = Loss_by_story_SDR['SDR']
            loss_data_plot['Loss'] = np.zeros(len(loss_data_plot))
            for k in range (len(ind)):
                loss_data_plot['Loss'] = Loss_by_story_SDR[str(ind['ID'][k])] + loss_data_plot['Loss']
                loss_data_plot[str(ind['ID'][k])] = Loss_by_story_SDR[str(ind['ID'][k])]
            
        elif EDP_assoc == 'PFA':
            loss_data_plot['PFA'] = Loss_by_story_PFA['PFA']
            loss_data_plot['Loss'] = np.zeros(len(loss_data_plot))
            for k in range (len(ind)):
                loss_data_plot['Loss'] = Loss_by_story_PFA[str(ind['ID'][k])] + loss_data_plot['Loss']
                loss_data_plot[str(ind['ID'][k])] = Loss_by_story_PFA[str(ind['ID'][k])]
        
        dictionary_plot['Loss_data_plot_' + current_story] = loss_data_plot
    
    return dictionary_plot, EDP_assoc

#%% FUNCIÓN PARA DEFINIR PÉRDIDAS DE LOS PRIMARY GROUPS (PG) POR PISO

def data_plot_primaryGroups (fname_Edp, guide, dictionary_loss):
    
    # Definición de parámetros para realizar agrupación por primary groups
    current_story = 'All'
    current_inputdata = 'Primary Group'
    
    # Generalidades de la edificación
    os.chdir(fname_Edp)
    file_name = glob.glob('*Loss_distribution*')
    sheet_principal = 'Guide'
    
    # Nombres de los pisos
    data_StoryTypes = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = sheet_principal)
    
    # Diccionario que contendrá los datos a utilizar para los plots
    dict_PG_loss = {}
    
    for i in range(len(data_StoryTypes['Story Type'].unique())):
        
        # Selección de piso
        current_story = data_StoryTypes['Story Type'].unique()[i]
        
        # Cargar datos del piso
        data_story = pd.read_excel(fname_Edp + '\\' + file_name[0], sheet_name = current_story)
        
        # Cargar primary groups del tipo de piso i
        primaryGroups_list = data_story ['Primary Group'].unique()
        
        # Obtención de matriz del diccionario
        Loss_by_story_SDR = dictionary_loss['Loss_by_story_SDR_'  +  current_story]
        Loss_by_story_PFA = dictionary_loss['Loss_by_story_PFA_'  +  current_story]
        
        # Definción de diccionario que contiene los primary groups del piso i
        dict_PG_story_i =  {}
        
        # Loop para cada primary group
        for k in range(len(primaryGroups_list)):
            
            # Primary group actual de la iteración k
            current_element = primaryGroups_list[k]
            
            # Matriz con todas las opciones que contengan el elemento actual
            ind =  data_story.loc[data_story[current_inputdata] == current_element]
            ind.reset_index(drop = True, inplace=True)
            
            # Busqueda de EDP asociado al elemento descrito
            EDP_assoc = guide.loc[guide['Fragility Group'] == ind['Fragility Group'][0]]['EDP_Associated']
            EDP_assoc.reset_index(drop = True, inplace=True)
            EDP_assoc = EDP_assoc[0]
            
            # Matriz con data necesaria para graficar perdidas por piso
            loss_data_plot = pd.DataFrame()
            if EDP_assoc == 'SDR':
                loss_data_plot['SDR'] = Loss_by_story_SDR['SDR']
                loss_data_plot['Loss'] = np.zeros(len(loss_data_plot))
                for l in range (len(ind)):
                    loss_data_plot['Loss'] = Loss_by_story_SDR[str(ind['ID'][l])] + loss_data_plot['Loss']
                
            elif EDP_assoc == 'PFA':
                loss_data_plot['PFA'] = Loss_by_story_PFA['PFA']
                loss_data_plot['Loss'] = np.zeros(len(loss_data_plot))
                for l in range (len(ind)):
                    loss_data_plot['Loss'] = Loss_by_story_PFA[str(ind['ID'][l])] + loss_data_plot['Loss']
                    
            # Guardado de data de cada PG en diccionario de piso actual
            dict_PG_story_i[current_element] = loss_data_plot
        
        # Guardado de data de cada piso actual en diccionario general
        dict_PG_loss[current_story] = dict_PG_story_i
        
    return dict_PG_loss
        
#%% FUNCIÓN PARA DEFINIR PÉRDIDAS DE LA FORMA DV VS IM PARA LOS CASOS DE NO COLAPSO

# Importante: esta función es válida si los IMs bineados son iguales para todos los EDPs y todos los pisos

def DV_IM_curves_NC(dict_params_log, dict_PG_NC_loss, data_StoryTypes):
    
    # Listas de parámetros iniciales de interés interés
    edps = list(dict_params_log.keys())
    stories = list(dict_params_log[edps[0]])
    bins = dict_params_log[edps[0]][stories[0]]['IM_bin']
    story_types = list(dict_PG_NC_loss.keys())
    primary_groups = list(dict_PG_NC_loss[story_types[0]].keys())
    
    # Diccinario general de la forma: story -->  IM_bin - STR - NSTR_D - NSTR_A - All
    dict_DV_IM_NC = {}
    
    # Loop para recorrer todos los pisos     
    for k in range(len(stories)):
        # Creación de dataframe de datos de un solo piso
        DV_IM_onestory = pd.DataFrame()
        DV_IM_onestory['IM_bin'] = bins
        
        # Piso actual y tipo de piso
        current_story = stories[k]
        current_storyType  = data_StoryTypes.loc[data_StoryTypes['Story num'] == current_story]['Story Type'].values[0]
        
        # Primary groups del tipo de piso
        primary_groups = list(dict_PG_NC_loss[current_storyType].keys())
        
        # Loop para recorrer todos los primary groups
        for m in range(len(primary_groups)):
            # Primary group actual y edp asociado
            current_primary_group = primary_groups[m]
            current_edp_assoc = dict_PG_NC_loss[current_storyType][current_primary_group].columns[0]
            
            # Datos de las cuvas de pérdidas DV vs EDP
            edp_values = dict_PG_NC_loss[current_storyType][current_primary_group][current_edp_assoc]
            dv_values = dict_PG_NC_loss[current_storyType][current_primary_group]['Loss']
            delta_edp = edp_values[1]
            
            # Creación de columna donde estarán los datos del primary group en el dataframe
            DV_IM_onestory[current_primary_group] = np.zeros(len(DV_IM_onestory))
            
            # Loop para recorrer todos los bins
            for i in range(len(bins)):                
                # Parámetros de curvas del bin actual
                mu = dict_params_log[current_edp_assoc][current_story]['mu'][i]
                sigma = dict_params_log[current_edp_assoc][current_story]['sigma'][i]
                
                # Valores pdf(edp_values)
                pdf_edp_values = stats.lognorm.pdf(x = edp_values, scale = np.exp(mu), s = sigma)
                
                # valor de DV para el valor dado
                dv_imbin_value = sum(dv_values*pdf_edp_values)*delta_edp
                
                # Guardado del dv para el im_bineado
                DV_IM_onestory[current_primary_group][i] =  dv_imbin_value
                
        
        # Nueva columna con la suma de las columnas, de tal forma que se tenga la suma de las perdidas de todos los primary groups
        DV_IM_onestory['All_PG'] = DV_IM_onestory.sum(axis = 1) - DV_IM_onestory['IM_bin']
        
        
        # Guardado de dataframe del piso en diccionario
        dict_DV_IM_NC[current_story] = DV_IM_onestory
        
    # Adicion de perdidas de todo el edificia por no colapso
    loss_all_building = pd.DataFrame()
    loss_all_building['IM_bin'] = DV_IM_onestory['IM_bin']
    loss_all_building['Loss_building_NC'] = np.zeros(len(loss_all_building))
    
    for i in range(len(stories)):
        current_RC = data_StoryTypes.loc[data_StoryTypes['Story num'] == stories[i]]['R_Cost_Building'].values[0]
        loss_all_building['Loss_building_NC'] = loss_all_building['Loss_building_NC'] + dict_DV_IM_NC[stories[i]]['All_PG']*current_RC
        
    dict_DV_IM_NC['Building'] = loss_all_building
    
        
    return dict_DV_IM_NC
            
#%% FUNCIÓN PARA DEFINIR PROBABILIDAD DE DEMOLICIÓN

def function_POD(parameters_RSDR, theta_rsdr_lim, beta_rsdr_lim, edp_max_RSDR, d_edp_RSDR):
    
    # Bines
    bins = parameters_RSDR['IM_bin']
    
    # ------------------------------------------------------
    # Curva de fragilidad de RSDR: Probabilidad de superar el estado de daño dado EDP
    
    # Vector RSDR
    rsdr_values = np.arange(d_edp_RSDR, edp_max_RSDR + d_edp_RSDR, d_edp_RSDR)
    
    # Valores cdf(rsdr_values)
    cdf_rsdr_values = norm.cdf(np.log(rsdr_values), np.log(theta_rsdr_lim), beta_rsdr_lim)
    
    # ------------------------------------------------------
    # Convolución para obtener probabilidad de demolición
    
    # Dataframe donde se guarda IM y POD
    POD = pd.DataFrame()
    POD['IM_bin'] = bins
    POD['Prob'] = np.zeros(len(bins))
    
    # Loop para recorrer todos los bins
    for i in range(len(bins)):
        
        # Parámetros de curvas del bin actual
        mu = parameters_RSDR['mu'][i]
        sigma = parameters_RSDR['sigma'][i]

        # ------------------------------------------------------
        # Curva pdf de los EDPs del bin actual    
        
        # Valores pdf(edp_values)
        edp_values = rsdr_values
        pdf_edp_value_i = stats.lognorm.pdf(x = edp_values, scale = np.exp(mu), s = sigma)
        
        # Convolución para obtener probabilidad de demolición
        POD_imbin_value = sum(cdf_rsdr_values * pdf_edp_value_i)*d_edp_RSDR
        
        # Guardado de la POD
        POD['Prob'][i] =  POD_imbin_value
        
    return POD
            
                
    
    



