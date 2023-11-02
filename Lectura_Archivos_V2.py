# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 12:48:23 2022

@author: Verónica Abuchar
"""
#%% LIBRERIAS
import os 
import glob
import pandas as pd
import numpy as np
os.getcwd()


#%% LECTURA DE RESPONSE SPECTRA DE SA Y SAAVG  -- OK

# Carpeta_con_HzLvls = 'C:\\Users\\vabuc\\OneDrive - Universidad del Norte\\+Informes Uninorte MNRS\\++CORRIDAS\\CSS\\CSS_BOG_Soil_T1s\\'

def RSP_total(Carpeta_con_HzLvls):
    """
    Input
    --------------
    Carpeta_con_HzLvls:     Direccion de la carpeta que contiene los hazards
    
    Output
    --------------
    Sa_All_HzLVLs:          DataFrame con todos los Sa por periodo estructural y hazard level en la última columna
    SaAVG_All_HzLVLs:       DataFrame con todos los SaAVG por periodo estructural y hazard level en la última columna
    Hazard_All:             DataFrame con los hazards levels de los IMs anteriores
    """
  
    # Lectura de carpetas dentro del directorio
    contenido = os.listdir(Carpeta_con_HzLvls)
    Lista_HzLvLs = []
    for fichero in contenido:
        if os.path.isdir(os.path.join(Carpeta_con_HzLvls, fichero)):
            Lista_HzLvLs.append(fichero)
          
    # Lista con los Hazards ordenados. El anteior no los presenta ordenados necesariamente
    Lista_De_Carpetas_HzLvLs = []
    for i in range(len(Lista_HzLvLs)):
        Lista_De_Carpetas_HzLvLs.append('Hazard_Level_' + str(i+1))
    
    # Entra a cada carpeta de Hz Lv
    for i_folder in range(len(Lista_De_Carpetas_HzLvLs)):
        Carpet_HzLvl = Lista_De_Carpetas_HzLvLs[i_folder]
        Hazard_level_path = os.path.join(Carpeta_con_HzLvls, Carpet_HzLvl)
        gmotions_path = os.path.join(Hazard_level_path, 'gmotions')
        os.chdir(gmotions_path)
        Sa_HzLvl = glob.glob('*ResponseSpectra*')
        SaAVG_HzLvl = glob.glob('*SA_average*')
        
        # Lee los exceles de Sa y SaAVG
        try:
            Excel_Sa = pd.read_csv(Sa_HzLvl[0])
        except:
            print('WARNING: ResponseSpectra file is not in the directory or the name is incorrect')
        try:
            Excel_SaAVG = pd.read_csv(SaAVG_HzLvl[0])
        except:
            print('WARNING: SA_average file is not in the directory or the name is incorrect')
        
        # Para evitar errores en numeración de periodos
        names_Sa = []
        names_SaAVG = []
        for k in range(len(Excel_Sa.columns)):
            names_Sa.append(round(float(Excel_Sa.columns[k]),2))
            
        for k in range(len(Excel_SaAVG.columns)):
            names_SaAVG.append(round(float(Excel_SaAVG.columns[k]),2))
            
        Excel_Sa.columns = names_Sa
        Excel_SaAVG.columns = names_SaAVG
        
        # Adicion de una columna que incluye Hazard level del registro
        Excel_Sa['Hz Lv'] = i_folder+1
        Excel_SaAVG['Hz Lv'] = i_folder+1
        Hazard = pd.DataFrame()
        Hazard['Hz Lv'] = Excel_Sa['Hz Lv']
        
        # CReación de DataFrame que une la información para todas las carpetas de los Hz Lv
        if i_folder == 0:
            Sa_All_HzLVLs = Excel_Sa.copy()
            SaAVG_All_HzLVLs = Excel_SaAVG.copy()
            Hazard_All = Hazard.copy()
        else:
            Sa_All_HzLVLs = pd.concat([Sa_All_HzLVLs, Excel_Sa], axis = 0, ignore_index = True)
            SaAVG_All_HzLVLs = pd.concat([SaAVG_All_HzLVLs, Excel_SaAVG], axis = 0, ignore_index = True)
            Hazard_All = pd.concat([Hazard_All, Hazard], axis = 0, ignore_index = True)
        
        os.chdir(Carpeta_con_HzLvls)
        
        del Excel_Sa
        del Excel_SaAVG
        del Hazard
    
    return Sa_All_HzLVLs, SaAVG_All_HzLVLs, Hazard_All

#%% LECTURA DE EDPS PARA PÉRDIDAS, INCLUYE RSDR -- OK

def lectura_EDPs(Carpeta_con_EDPs, Hazard_All):
    """
    Input
    ----------
    Carpeta_con_EDPs:       Direccion de la carpeta que contiene los outputs del análisis: EDPs, TestRun, etc
    Hazard_All:             Vector de hazards de cada registro. Se obtiene de la funcion 'RSP_total'
    
    Output
    --------------
    dict_all_EDPs_E1:       Diccionario que contiene:
                            PFA:    DataFrame con los PFA de cada piso y el máximo de cada registro. La ultima columna incluye el Hz lev
                            SDR:    DataFrame con los SDR de cada piso y el máximo de cada registro. La ultima columna incluye el Hz lev
                            RSDR:   DataFrame con los RSDR de cada piso y el máximo de cada registro. La ultima columna incluye el Hz lev
                            RDR:    Dataframe con los RDR max. La ultima columna incluye el Hz lev
    """
    # Ubicación en el directorio
    os.chdir(Carpeta_con_EDPs)
    
    # Busca el nombre del archivo    
    PFA_fileName = glob.glob('*_PFA*')
    SDR_fileName = glob.glob('*_SDR*')
    RSDR_fileName = glob.glob('*_RSDR*')
    RDR_fileName = glob.glob('*_RDR*')
    
    # Lectura del archivos de EDPs
    try:
        PFA_All = pd.read_csv(PFA_fileName[0], header = None, sep = ' ')
    except IndexError:
        print('WARNING: The building has not PFA file')
    try:
        SDR_All = pd.read_csv(SDR_fileName[0], header = None, sep = ' ')
    except IndexError:
        print('WARNING: The building has not SDR file')
    try:
        RSDR_All = pd.read_csv(RSDR_fileName[0], header = None, sep = ' ')
    except IndexError:
        print('WARNING: The building has not RSDR file')
    try:
        RDR_All = pd.read_csv(RDR_fileName[0], header = None, sep = ' ')
    except IndexError:
        pass
    

    # Nombres de columnas
    Nstory = len(SDR_All.columns)
    story_name = []
    for i in range(Nstory):
        story_name.append('S' + str(i+1))
    
    PFA_All.columns = story_name
    SDR_All.columns = story_name
    try:
        RSDR_All.columns = story_name
    except:
        pass
    try:
        RDR_All = RDR_All.rename(columns={0: 'max'})
    except:
        pass
    
    # Se crea una nueva columna con los máximos de cada EDP
    PFA_All['max']=PFA_All.max(axis=1)
    SDR_All['max']=SDR_All.max(axis=1)
    try:
        RSDR_All['max']=RSDR_All.max(axis=1)
    except:
        pass
    
    # Se adiciona una columna para incluir el Hazard del EDP
    PFA_All['Hz Lv'] = Hazard_All
    SDR_All['Hz Lv'] = Hazard_All
    try:
        RSDR_All['Hz Lv'] = Hazard_All
    except:
        pass
    try:
        RDR_All['Hz Lv'] = Hazard_All
    except:
        pass
    
    # Se crea un diccionario con todas las EDP
    dict_all_EDPs = {}
    dict_all_EDPs['PFA'] = PFA_All
    dict_all_EDPs['SDR'] = SDR_All
    try:
        dict_all_EDPs['RSDR'] = RSDR_All
    except NameError:
        pass
    try:
        dict_all_EDPs['RDR'] = RDR_All
    except NameError:
        pass
    
    return dict_all_EDPs


#%% LECTURA DE TEST RUN Y DEFINICIÓN DE TEST EXITOSOS -- OK

def testRun(Carpeta_con_EDPs, timeOK, EDP_limit, EDP_name_graph, dict_all_EDPs):
    """
    Input
    ----------
    Carpeta_con_EDPs:       Direccion de la carpeta que contiene los outputs del análisis: EDPs, TestRun, etc
    timeOK:                 Fracción de tiempo de corrida con respecto al tiempo del GM a partir del cual se considera que el análisis fue exitos
    EDP_limit:              Valor de EDP a partir del cual se acepta el análisis si no cumple con el tiempo mínimo timeOK
    EDP_name_graph:         Tipo de EDP para definir cual emplear en EDP_limit (SDR,PFA,RDR,RSDR)
    dict_all_EDPs:          Diccionario con todos los EDPs. Se obtiene a partit de la función lectura_EDPs()
    
    Output
    ----------
    test:                   DataFrame test de la corrida cuya última fila indica si el registro fue exitoso (1) o no (0)
    """
    # Ubicación en el directorio
    os.chdir(Carpeta_con_EDPs)
    
    # Cargar archivo test run
    test_fileName = glob.glob('*Test_Run_Earthquake*')
    test = pd.read_csv(test_fileName[0], header = None, sep = ',')
    
    # DataF con la EDP de interes a revisar
    dataF_EDP = dict_all_EDPs[EDP_name_graph]['max'].copy()
    
    # Revision de corridas exitosas
    ok_run = pd.DataFrame()
    ok_run['OK'] = np.zeros(len(test))
    for i in range (len(test)):
        if test.iloc[i,2] >= test.iloc[i,3]*timeOK:
            ok_run.loc[i] =  1 
        elif dataF_EDP[i] >= EDP_limit:
            ok_run.loc[i] =  1
    
    test['OK'] = ok_run
    
    return test

#%% ELIMINACION DE REGISTROS EN HAZARDS Y EDPS QUE NO SON EXITOSOS -- OK

def correccion_test (Sa_All_HzLVLs, SaAVG_All_HzLVLs, dict_all_EDPs, test):
    """
    Input
    ----------
    Sa_All_HzLVLs:      DataFrame con todos los Sa por periodo estructural y hazard level en la última columna. Se obtiene de la funcion 'RSP_total()'  
    SaAVG_All_HzLVLs:   DataFrame con todos los SaAVG por periodo estructural y hazard level en la última columna. Se obtiene de la funcion 'RSP_total()'
    dict_all_EDPs::     Diccionario con los EDPs de cada piso y el máximo de cada registro. La ultima columna incluye el Hz lev. Se obtiene de la función 'lectura_EDPs()'
    test:               DataFrame test de la corrida cuya última fila indica si el registro fue exitoso (1) o no (0). Se obtiene de la función'testRun()'
    
    Output
    ----------
    Sa_All_HzLVLs:      DataFrame del input pero sin los registros que no fueron exitosos
    SaAVG_All_HzLVLs:   DataFrame del input pero sin los registros que no fueron exitosos
    dict_all_EDPs:      Diccionario del input pero sin los registros que no fueron exitosos
    """
    
    # Creacion de columna ok en cada variable de interés
    Sa_All_HzLVLs['OK'] = test['OK']
    SaAVG_All_HzLVLs['OK'] = test['OK']
    
    edp_list = list(dict_all_EDPs.keys())
    for current_edp in edp_list:
        dict_all_EDPs[current_edp]['OK'] = test['OK']
    
    # Eliminación de filas con OK = 0
    Sa_All_HzLVLs = Sa_All_HzLVLs.loc[Sa_All_HzLVLs['OK']==1]
    SaAVG_All_HzLVLs = SaAVG_All_HzLVLs.loc[SaAVG_All_HzLVLs['OK']==1]
    
    for current_edp in edp_list:
        dict_all_EDPs[current_edp] = dict_all_EDPs[current_edp].loc[dict_all_EDPs[current_edp]['OK']==1]
    
    # Se elimmina la columa de OK agregada
    Sa_All_HzLVLs = Sa_All_HzLVLs.drop(['OK'], axis=1)
    SaAVG_All_HzLVLs = SaAVG_All_HzLVLs.drop(['OK'], axis=1)
    
    for current_edp in edp_list:
        dict_all_EDPs[current_edp] = dict_all_EDPs[current_edp].drop(['OK'], axis=1)
    
    return Sa_All_HzLVLs, SaAVG_All_HzLVLs, dict_all_EDPs

#%% ELIMINACION DE REGISTROS EN HAZARDS Y EDPS QUE NO HAYAN SIDO EXITOSOS SOLO PARA UNA OPCION DE IM Y EDP

# def correccion_test_V2 (IM_All_HzLVLs, EDP_All, test):
#     """
#     Input
#     ----------
#     IM_All_HzLVLs:      DataFrame con todos los Sa o SaAVG por periodo estructural y hazard level en la última columna. Se obtiene de la funcion 'RSP_total'  
#     EDP_All:            DataFrame con los SDR o PFA de cada piso y el máximo de cada registro. La ultima columna incluye el Hz lev. Se obtiene de la función 'lectura_EDPs'
#     test:               DataFrame test de la corrida cuya última fila indica si el registro fue exitoso (1) o no (0). Se obtiene de la función'testRun'
    
#     Output
#     ----------
#     IM_All_HzLVLs:      DataFrame del input pero sin los registros que no fueron exitosos
#     EDP_All:            DataFrame del input pero sin los registros que no fueron exitosos
#     """
#     # Creacion de columna ok en cada vector de interés
#     IM_All_HzLVLs['OK'] = test['OK']
#     EDP_All['OK'] = test['OK']
    
#     # Eliminación de filas con OK = 0
#     IM_All_HzLVLs = IM_All_HzLVLs[IM_All_HzLVLs['OK']==1]
#     EDP_All = EDP_All[EDP_All['OK']==1]
    
#     # Se elimmina la columa de OK agregada
#     IM_All_HzLVLs = IM_All_HzLVLs.drop(['OK'], axis=1)
#     EDP_All = EDP_All.drop(['OK'], axis=1)
    
#     return IM_All_HzLVLs, EDP_All
    
#%% FUNCIÓN PARA CENSURAR DATOS

def EDP_censor_data (SDR_cens, type_cens, dict_EDPs_Original):
    """
    Input
    ----------
    SDR_cens:           SDR a partir del cual se va a censurar la data 
    type_cens:          'lower': Si se van a tomar los datos inferiores o iguales a SDR_cens; 'upper': Si se van a tomar los datos mayores a SDR_cens
    dict_EDPs_Original: Diccionario con valores de IM, y delos EDPs SDR, RSDR y PFA para cada piso

    Output
    ----------
    dict_EDPs_cens: Diccionario con los EDPs censurados
    """
    
    # Definición de EDPs en DataFrames independientes
    IM = dict_EDPs_Original['IM'].copy()
    PFA_All = dict_EDPs_Original['PFA'].copy()
    SDR_All = dict_EDPs_Original['SDR'].copy()
    RSDR_All = dict_EDPs_Original['RSDR'].copy()
    
    # Revisión de los SDR que no superan el límite de interés
    ok_run = pd.DataFrame()
    ok_run['OK'] = np.zeros(len(SDR_All))
    
    for i in range (len(SDR_All)):
        NoSurpass = 1 # Si sobrepasa el límite se vuelve 0
        
        for k in range(len(SDR_All.columns)-2):
            if SDR_All.iloc[i,k] > SDR_cens:
                NoSurpass = 0
                break
        ok_run['OK'][i] = NoSurpass
    
    # Ajuste de los indices de ok_run para que coincidan con los de EDP
    ok_run.index = SDR_All.index
    
    # Creacion de columna ok en cada vector de interés
    IM['OK'] = ok_run['OK']
    PFA_All['OK'] = ok_run['OK']
    SDR_All['OK'] = ok_run['OK']
    RSDR_All['OK'] = ok_run['OK']
    
    if type_cens == 'lower':
        # Eliminación de filas con OK = 0
        IM = IM[IM['OK']==1]
        PFA_All = PFA_All[PFA_All['OK']==1]
        SDR_All = SDR_All[SDR_All['OK']==1]
        RSDR_All = RSDR_All[RSDR_All['OK']==1]
        
    elif type_cens == 'upper':
        # Eliminación de filas con OK = 1
        IM = IM[IM['OK']==0]
        PFA_All = PFA_All[PFA_All['OK']==0]
        SDR_All = SDR_All[SDR_All['OK']==0]
        RSDR_All = RSDR_All[RSDR_All['OK']==0]
        
    # Se elimmina la columa de OK agregada
    IM = IM.drop(['OK'], axis=1)
    PFA_All = PFA_All.drop(['OK'], axis=1)
    SDR_All = SDR_All.drop(['OK'], axis=1)
    RSDR_All = RSDR_All.drop(['OK'], axis=1)
    
    # Se genera diccionario con los datos censurados
    dict_EDPs_cens = {}
    dict_EDPs_cens['IM'] = IM
    dict_EDPs_cens['SDR'] = SDR_All
    dict_EDPs_cens['RSDR'] = RSDR_All
    dict_EDPs_cens['PFA'] = PFA_All
    
    return dict_EDPs_cens

#%% FUNCIÓN PARA LECTURA Y GENERACIÓN DE ARCHIVOS PARA COLAPSO DEL TIPO CONTEO DE FALLAS DE COLUMNAS

def input_colum_count(fname_HzB1, fname_EdpB1, T, IM_name_graph, EDP_name_graph, story, EDP_collapse, timeOK, EDP_limit):
    
    # Lectura de IMs
    [Sa_All_HzLVLs, SaAVG_All_HzLVLs, Hazard_All] = RSP_total(fname_HzB1)

    # Definición de IM_data
    if IM_name_graph == "Sa":
        IM_data = Sa_All_HzLVLs.copy()
    elif IM_name_graph == "SaAVG":
        IM_data = SaAVG_All_HzLVLs.copy()

    # Unicacion de archivo
    os.chdir(fname_EdpB1)

    # Busca el de los archivos de EDPs
    name = '_'+EDP_name_graph
    pattern_EDP = f"*{name}*"
    EDP_fileName = glob.glob(pattern_EDP)
    Col_colap_ALL = glob.glob('*_Count_Colap_V*')

    # Lectura de los archivos de EDPs
    EDP_All = pd.read_csv(EDP_fileName[0], header = None, sep = ' ')
    EDP_All['max'] = EDP_All.max(axis=1)
    Col_colap_ALL = pd.read_csv(Col_colap_ALL[0], header = None, sep = ' ')

    # -------------------------------------------
    # Creacion de DataFrame con informacion de IM, EDP, colapsos y Hazard lev

    # Se crea una nueva columna con los máximos de cada EDP
    dataF_count_colap = pd.DataFrame()
    dataF_count_colap['IM'] = IM_data[T]
    dataF_count_colap[story] = EDP_All.max(axis=1)
    dataF_count_colap['count_colap'] = np.zeros(len(EDP_All))
    dataF_count_colap['Hz Lv'] = Hazard_All

    for i in range (len(EDP_All)):
        
        # La data de todos los pisos para un mismo GM
        current_row = Col_colap_ALL.iloc[i,:]
        
        # Se crea una nueva variable que es 0 si la data anterior es menor a 0.5, y 1 en caso contrario
        # Esto quiere decir que si fallan mas del 50% de las columnas del piso, entonces el piso colapsa
        new_row = [0 if x < 0.5 else 1 for x in current_row]
        
        # Definición de si colapsa a partir de conteo de columnas: si colapsa un piso, entonces la estructura colapsa
        cont_col =  1 if sum(new_row) > 0 else 0
        
        # Definicion de si colapsa a partir de EDP_max
        cont_edp = 1 if dataF_count_colap.at[i,story] >= EDP_collapse else 0
        
        # Definición de conteo de colapso
        dataF_count_colap.at[i,'count_colap'] = 1 if (cont_col + cont_edp) > 0 else 0
        
    # -------------------------------------------
    # Verificacion de simulaciones que sí corrieron - testrun

    # Cargar archivo test run
    test_fileName = glob.glob('*Test_Run_Earthquake*')
    test = pd.read_csv(test_fileName[0], header = None, sep = ',')

    # dataF de interes para revisar
    dataF_EDP = EDP_All['max'].copy()

    ok_run = pd.DataFrame()
    ok_run['OK'] = np.zeros(len(test))

    for i in range (len(test)):
        if test.iloc[i,2] >= test.iloc[i,3]*timeOK:
            ok_run.loc[i] =  1
            
        elif dataF_EDP[i] >= EDP_limit:
            ok_run.loc[i] =  1

    # Guardado de ok_run en dataframe general
    dataF_count_colap['OK'] = ok_run

    # Eliminacion de filas que con OK = 0
    dataF_count_colap = dataF_count_colap.loc[dataF_count_colap['OK']==1]

    # Se elimmina la columa de OK agregada
    dataF_count_colap = dataF_count_colap.drop(['OK'], axis = 1)
    
    # Renombrar columna de EDP de piso, por 'EDP'
    dataF_count_colap = dataF_count_colap.rename(columns={story:'EDP'})
    
    return dataF_count_colap

#%%
def SDR_censor_data (SDR_cens, type_cens, dict_EDPs_Original):
    """
    Input
    ----------
    SDR_cens:           SDR a partir del cual se va a censurar la data 
    type_cens:          'lower': Si se van a tomar los datos inferiores o iguales a SDR_cens; 'upper': Si se van a tomar los datos mayores a SDR_cens
    dict_EDPs_Original: Diccionario con valores de IM, y delos EDPs SDR, RSDR y PFA para cada piso

    Output
    ----------
    dict_EDPs_cens: Diccionario con los EDPs censurados
    """
    
    # Definición de EDPs en DataFrames independientes
    IM = dict_EDPs_Original['IM'].copy()
    # PFA_All = dict_EDPs_Original['PFA'].copy()
    SDR_All = dict_EDPs_Original['SDR'].copy()
    # RSDR_All = dict_EDPs_Original['RSDR'].copy()
    
    # Revisión de los SDR que no superan el límite de interés
    ok_run = pd.DataFrame()
    ok_run['OK'] = np.zeros(len(SDR_All))
    
    for i in range (len(SDR_All)):
        NoSurpass = 1 # Si sobrepasa el límite se vuelve 0
        
        for k in range(len(SDR_All.columns)-2):
            if SDR_All.iloc[i,k] > SDR_cens:
                NoSurpass = 0
                break
        ok_run['OK'][i] = NoSurpass
    
    # Ajuste de los indices de ok_run para que coincidan con los de EDP
    ok_run.index = SDR_All.index
    
    # Creacion de columna ok en cada vector de interés
    IM['OK'] = ok_run['OK']
    # PFA_All['OK'] = ok_run['OK']
    SDR_All['OK'] = ok_run['OK']
    # RSDR_All['OK'] = ok_run['OK']
    
    if type_cens == 'lower':
        # Eliminación de filas con OK = 0
        IM = IM[IM['OK']==1]
        # PFA_All = PFA_All[PFA_All['OK']==1]
        SDR_All = SDR_All[SDR_All['OK']==1]
        # RSDR_All = RSDR_All[RSDR_All['OK']==1]
        
    elif type_cens == 'upper':
        # Eliminación de filas con OK = 1
        IM = IM[IM['OK']==0]
        # PFA_All = PFA_All[PFA_All['OK']==0]
        SDR_All = SDR_All[SDR_All['OK']==0]
        # RSDR_All = RSDR_All[RSDR_All['OK']==0]
        
    # Se elimmina la columa de OK agregada
    IM = IM.drop(['OK'], axis=1)
    # PFA_All = PFA_All.drop(['OK'], axis=1)
    SDR_All = SDR_All.drop(['OK'], axis=1)
    # RSDR_All = RSDR_All.drop(['OK'], axis=1)
    
    # Se genera diccionario con los datos censurados
    dict_EDPs_cens = {}
    dict_EDPs_cens['IM'] = IM
    dict_EDPs_cens['SDR'] = SDR_All
    # dict_EDPs_cens['RSDR'] = RSDR_All
    # dict_EDPs_cens['PFA'] = PFA_All
    
    return dict_EDPs_cens
    