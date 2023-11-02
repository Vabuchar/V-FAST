# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 19:53:19 2022

@author: Verónica Abuchar
"""
import pandas as pd

#%% DEFINICIÓN DE VALORES IM A UTILIZAR -- OK

def lista_IM(T,Hzlv_curves, IM_data):
    """
    Input
    ----------
    T:              Periodo estructural redondeado a dos decimales
    Hzlv_curves:    Vector de Hazards Levels con los que se generaran las curvas de fragilidad
    IM_data:        DataFrame que contiene los IMs para cada periodo estructural. Se obtiene de la funcion 'correccion_test()'
    
    Output
    ----------
    IM_curva:      Dataframe con la lista de IMs que serán utilizados para generar las curvas de fragilidad y los hazards corrrespondientes
    """
    IM_curva = pd.DataFrame()
    IM_data_red = IM_data[IM_data['Hz Lv'].isin(Hzlv_curves)]
    IM_curva[T] = IM_data_red[T]
    IM_curva['Hz Lv'] = IM_data_red['Hz Lv']
    
    return IM_curva


#%% DEFINICIÓN DE VALORES EDP A UTILIZAR - OK

def lista_EDP(story, Hzlv_curves, EDP_data):
    """
    Input
    ----------
    story:          Piso escogido para graficar fragilidad
    Hzlv_curves:    Vector de Hazards Levels con los que se generaran las curvas de fragilidad
    EDP_data:       DataFrame que contiene los EDPs para cada piso. Se obtiene de la funcion 'correccion_test'
    
    Output
    ----------
    EDP_curva:      Dataframe con la lista de EDPs que serán utilizados para generar las curvas de fragilidad y los hazards corrrespondientes
    """
    EDP_curva = pd.DataFrame()
    EDP_data_red = EDP_data[EDP_data['Hz Lv'].isin(Hzlv_curves)]
    EDP_curva[story] = EDP_data_red[story]
    EDP_curva['Hz Lv'] = EDP_data_red['Hz Lv']
    
    return EDP_curva
    
    