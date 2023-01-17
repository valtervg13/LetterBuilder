# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:46:41 2022

@author: valter.gonzaga
"""
import Utilities.util as util
from Utilities.News_Builder import Newsletter
from SUPPORT_PAGES.Profilers.profiler_src import profiler

"""
=====================================================================
VARIÁVEIS GLOBAIS
=====================================================================
"""

#====================================================================
#GATILHOS
#====================================================================
   
fomat_wd_inst = None

html_errmessages = False

#====================================================================
#DADOS PADRÃO
#====================================================================


#Browse path

browse_path = util.fetch_data('./Data/config.cfg')['browse_path']

#Format data

format_data_path = './Data/format_profiles'

format_dict = util.fetch_data('./Data/format_data.cfg')

#Import data

import_data_path = './Data/import_profiles'

import_dict = util.fetch_data('./Data/import_config.cfg')

#Newsapi data

newsapi_dict = util.fetch_data('./Data/newsapi.cfg')

info_dict_list = []

#Datetime data

monthdays = ['   ' if day == 0
             else day 
             for day in range(0,32)]

months_dict = {'   ':0,
               'Jan':1,
               'Fev':2,
               'Mar':3,
               'Abr':4,
               'Mai':5,
               'Jun':6,
               'Jul':7,
               'Ago':8,
               'Set':9,
               'Out':10,
               'Nov':11,
               'Dez':12
               }

#====================================================================
#OBJETOS GLOBAIS
#====================================================================

news = Newsletter()

format_profiler = profiler(path=format_data_path)
import_profiler = profiler(path=import_data_path)