# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:46:41 2022

@author: valter.gonzaga
"""
import util as util
from News_Builder import Newsletter

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

browse_path = util.fetch_data('Data/config.cfg')['browse_path']

format_data_path = 'Data/format_profiles'

import_data_path = 'Data/import_profiles'


format_dict = util.fetch_data('Data/format_data.cfg')

import_dict = util.fetch_data('Data/import_config.cfg')

info_dict_list = []


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
#NEWSLETTER
#====================================================================

news = Newsletter()