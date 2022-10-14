# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:59:43 2022

@author: valter.gonzaga
"""

import tkinter as tk
from tkinter import ttk
from tktip import CreateToolTip
from tkcalendar import DateEntry

import datetime as dt
import pandas as pd

from cfg import (news,
                 monthdays,
                 import_dict,
                 format_dict
                 )

import util
from util import browseFiles
from time_check import time_check as tc
from Preview_Window import pvWidget


class card_importer(ttk.Frame):
    def __init__(self, parent, controller):
        
        from format_wd import format_wd
        from adding_page import adding_page
        from profilers import (profile_load_wd,
                               profile_save_wd,
                               import_profiler)
        from html_viewport import HTML_viewport


        ttk.Frame.__init__(self, parent,
                          height=parent.winfo_height(),
                          width=parent.winfo_width())
        self.controller = controller
        
        

        def load_profile():
            
            parent.show_window(profile_load_wd,
                               parent=self,
                               parent_class=('frame',card_importer),
                               profiler_obj = import_profiler,
                               data_dict = import_dict,
                               title='Importar Perfil')
            
        def save_profile():

            getConfigs()
            
            parent.show_window(profile_save_wd,
                               profiler_obj = import_profiler,
                               data_dict = import_dict,
                               title='Salvar Perfil',
                               enable_add=True)
        
        #---------------------------------------------------------------
        #FUNÇÃO: CRIA O DICIONÁRIO DE INFORMAÇÕES DE IMPORTAÇÃO
        #---------------------------------------------------------------   
        def getConfigs():
            
            global import_dict
            
            import_dict['xlsx_path'] = path_sht.get()
            import_dict['heading_lines'] = number_head.get()
            import_dict['xlsx_sheet'] = name_sht.get()
            
            import_dict['header_var'] = (('col',id_hd.get()) if id_hd.get() != ''
                                       else ('default',id_hd_default.get())
                                       )
            
            
            import_dict['body_var'] = ('col',id_bd.get())
            
            import_dict['title_var'] = (('col',id_ttl.get()) if id_ttl.get() != ''
                                       else ('default',id_ttl_default.get())
                                       )
            
            import_dict['banner_var'] = (('col',id_bn.get()) if id_bn.get() != ''
                                       else ('default',id_bn_default.get())
                                       )
            import_dict['banner_mode'] = figureopt_bn.get()
            import_dict['banner_link'] = (('col',link_bn.get()) if link_bn.get() != ''
                                         else ('default',link_bn_default.get())
                                         )
            import_dict['banner_caption'] = (('col',cpt_bn.get()) if cpt_bn.get() != ''
                                         else ('default',cpt_bn_default.get())
                                         )
            import_dict['banner_empty_alt'] = cpt_bn_empty.get()
            
            import_dict['footer_var'] = (('col',id_ft.get()) if id_ft.get() != ''
                                         else ('default',id_ft_default.get())
                                         )
            import_dict['footer_mode'] = figureopt_ft.get()
            import_dict['footer_link'] = (('col',link_ft.get()) if link_ft.get() != ''
                                          else ('default',link_ft_default.get())
                                          )
            import_dict['footer_caption'] = (('col',cpt_ft.get()) if cpt_ft.get() != ''
                                         else ('default',cpt_ft_default.get())
                                         )
            import_dict['footer_empty_alt'] = cpt_ft_empty.get()
            
            import_dict['tag_var'] = ('col',id_tag.get())
            import_dict['tag_key'] = key_tag.get()            

            import_dict['date_var'] = ('col',id_date.get())
            
            
            
            weekopt = self.weekopt_date.get()
            monthopt = self.monthopt_date.get()
            compopt = self.compopt_date.get()
            
            is_week = ((monthopt == '   ' and compopt == '') 
                       and weekopt != ''
                       )
            
            is_month = (( weekopt == '' and compopt == '') 
                       and monthopt != '   '
                       )
            
            is_compare = (( weekopt == '' and monthopt == '   ') 
                          and compopt != ''
                          )
            
            import_dict['date_freq'] = (('weekly', weekopt) 
                                        if is_week
                                        else ('monthly', monthopt)
                                        if is_month
                                        else ('comparison', compopt)
                                        if is_compare
                                        else ('all time','0')
                                        )

            import_dict['ref_date'] = act_ref_cal.get()
            util.store_data('Data/import_config.cfg', import_dict)
            
            
            return import_dict
        
        
        def infoDicts():
            
            #------------------------------------------
            #Obtém dicionário de importações atualizado
            #------------------------------------------
            
            import_data = getConfigs()
            
            #Aquisição dos valores
            #-Dados da planilha
            excel_path = import_data['xlsx_path']
            heading_lines = int(import_data['heading_lines'])
            excel_sheet = import_data['xlsx_sheet']
            if excel_sheet.isnumeric():
                excel_sheet = int(excel_sheet)
            
            #-Dados das colunas
            header_col_type =  import_data['header_var'][0]
            header_col_id = import_data['header_var'][1]
            
            title_col_type =  import_data['title_var'][0]
            title_col_id = import_data['title_var'][1]
            
            body_col_type =  import_data['body_var'][0]
            body_col_id = import_data['body_var'][1]
            
            banner_col_type =  import_data['banner_var'][0]
            banner_col_id = import_data['banner_var'][1]
            banner_mode = import_data['banner_mode']
            banner_link_type = import_data['banner_link'][0]
            banner_link_id = import_data['banner_link'][1]
            banner_caption_type = import_data['banner_caption'][0]
            banner_caption_id = import_data['banner_caption'][1]
            banner_caption_empty = import_data['banner_empty_alt']
            
            footer_col_type =  import_data['footer_var'][0]
            footer_col_id = import_data['footer_var'][1]
            footer_mode = import_data['footer_mode']
            footer_link_type = import_data['footer_link'][0]
            footer_link_id = import_data['footer_link'][1]
            footer_caption_type = import_data['footer_caption'][0]
            footer_caption_id = import_data['footer_caption'][1]
            footer_caption_empty = import_data['footer_empty_alt']
            
            #dados de filtragem
            date_col_type =  import_data['date_var'][0]
            date_col_id = import_data['date_var'][1]
            date_frequency = import_data['date_freq'][0]
            date_value = (import_data['date_freq'][1])
            date_ref = import_data['ref_date']
            
            ref_day,ref_month,ref_year = map(int,date_ref.split('/'))
            ref_dt = dt.date(ref_year, ref_month, ref_day)
            
            tag_col_type =  import_data['tag_var'][0]
            tag_col_id = import_data['tag_var'][1]
            tag_key = import_data['tag_key'].lower()
        
            #---------------------------------------
            #Cria um Data Frame a partir da planilha
            #---------------------------------------
            

            data_frame = pd.read_excel(excel_path, #caminho da pasta
                                       sheet_name=excel_sheet, #primeira worksheet
                                       header=None, #indice das colunas: números de coluna
                                       skiprows=heading_lines, #pula as linhas de cabeçalho
                                       parse_dates=True,
                                       )
            
            
            data_frame.fillna('',inplace=True)
            
            
            #-----------------------------------------
            #Aquisição das colunas de dados relevantes
            #-----------------------------------------
            
            cols_dict = {}
            
            #-Cabeçalho
            header_val = (list(data_frame[util.col2num(header_col_id)])   
                         if header_col_type == 'col'
                         else header_col_id)
            cols_dict['header'] = {'type':header_col_type,
                                  'value':header_val
                                  }
            
            #-Título
            title_val = (list(data_frame[util.col2num(title_col_id)])   
                         if title_col_type == 'col'
                         else title_col_id)
            cols_dict['title'] = {'type':title_col_type,
                                  'value':title_val
                                  }
            
            #Corpo
            body_val = (list(data_frame[util.col2num(body_col_id)]) 
                         if body_col_type == 'col'
                         else body_col_id)
            cols_dict['body'] = {'type':body_col_type,
                                 'value':body_val}
            
            #Banner
            banner_val = (list(data_frame[util.col2num(banner_col_id)])
                         if banner_col_type == 'col'
                         else banner_col_id)
            cols_dict['banner'] = {'type':banner_col_type,
                                   'value':banner_val}
            banner_link_val = (list(data_frame[util.col2num(banner_link_id)])
                               if banner_link_type == 'col'
                               else banner_link_id)
            cols_dict['banner_link'] = {'type':banner_link_type,
                                        'value':banner_link_val}
            banner_cpt_val = ([value 
                               if value != '' 
                               else banner_caption_empty
                               for value in list(data_frame[util.col2num(banner_caption_id)])
                               ]
                              if banner_caption_type == 'col'
                              else banner_caption_id
                              )
            cols_dict['banner_caption'] = {'type':banner_caption_type,
                                           'value':banner_cpt_val}
            
            
            #Rodapé
            footer_val = (list(data_frame[util.col2num(footer_col_id)])
                         if footer_col_type == 'col'
                         else footer_col_id)
            cols_dict['footer'] = {'type':footer_col_type,
                                  'value':footer_val}
            footer_link_val = (list(data_frame[util.col2num(footer_link_id)])
                               if footer_link_type == 'col'
                               else footer_link_id)
            cols_dict['footer_link'] = {'type':footer_link_type,
                                        'value':footer_link_val}  
            footer_cpt_val = ([value 
                               if value != '' 
                               else footer_caption_empty
                               for value in list(data_frame[util.col2num(footer_caption_id)])
                               ]
                              if footer_caption_type == 'col'
                              else footer_caption_id)
            cols_dict['footer_caption'] = {'type':footer_caption_type,
                                           'value':footer_cpt_val}
            
            #Datas
            date_val = ([dt.date(timestamp.year,timestamp.month,timestamp.day)
                         for timestamp in list(data_frame[util.col2num(date_col_id)])
                         ] 
                        if date_col_type == 'col' and date_col_id != ''
                        else ''
                        )
            cols_dict['date'] = {'type': ('col'
                                          if date_col_id != ''
                                          else 'default'),
                                 'value':date_val}
            
            #Etiqueta de Inclusão
            tag_val = ([tag.lower()
                        if type(tag) == str
                        else '' 
                        for tag in list(data_frame[util.col2num(tag_col_id)])
                        ]
                       if tag_col_type == 'col' and tag_col_id != ''
                       else tag_col_id
                       )
            cols_dict['tag'] = {'type':('col'
                                          if tag_col_id != ''
                                          else 'default'),
                                'value':tag_val}


            #-------------------
            #Filtragem dos dados
            #-------------------
            
            #---------------------------------------------------------------
            
            #FILTRAGEM POR DATA
            
            if date_col_id != '':
                mindate = dt.date.min + dt.timedelta(1)
                maxdate = dt.date.max - dt.timedelta(1)
                


                #-Frequencia semanal
                if date_frequency == 'weekly':
                    date_value = int(date_value)
                    lower_date,upper_date = tc.week_bounds(ref_dt, 
                                                           date_value
                                                           )
    
                    
                
                #-Frequencia mensal
                elif date_frequency == 'monthly':
                    date_value = int(date_value)
                    upper_date,lower_date = tc.month_bounds(ref_dt, 
                                                            date_value
                                                            )
                
                #-A partir da data referência
                elif date_frequency == 'comparison':
                    if date_value == 'Igual referência' or '':
                        lower_date = ref_dt
                        upper_date = ref_dt+dt.timedelta(1)
                    elif date_value == 'Antes da referência':
                        lower_date = mindate
                        upper_date = ref_dt
                    else:
                        lower_date = ref_dt
                        upper_date = maxdate
                        
                else:
                    lower_date = mindate
                    upper_date = maxdate
                
    
                #-Obtenção dos indices correspondentes a datas validas
                date_filtered_ids = []
                for i in range(len(date_val)):
                    date = date_val[i]
                    if tc.is_between(date,
                                     lower_date,
                                     upper_date
                                     ):

                        date_filtered_ids.append(i)
                
                #Filtragem dos items
                for key,val in cols_dict.items():
                    if val['type'] == 'col':
                        cols_dict[key]['value'] = [val['value'][i]
                                                   for i in date_filtered_ids]
            
            

            #------------------------------------------------------------------

            #FILTRAGEM POR ETIQUETAGEM
            
            tag_col = cols_dict['tag']['value']
            
            if tag_col_id != '':
                #-Obtenção dos indices correspondentes a etiquetas validas
    
                tag_filtered_ids = []
                for i in range(len(tag_col)):
                    if tag_col[i] == tag_key:
                        tag_filtered_ids.append(i)
                
                
                #Filtragem dos items
                for key,val in cols_dict.items():
                    if val['type'] == 'col':
                        cols_dict[key]['value'] = [val['value'][i]
                                                   for i in tag_filtered_ids]
            
            #------------------------------------------------------------------
            
            #--------------------------------------------------------------
            #Formatação dos valores padrão como listas de valores repetidos
            #--------------------------------------------------------------
            
            col_len = len(cols_dict['body']['value'])

            
            
            for key,val in cols_dict.items():
                if val['type'] == 'default':
                    cols_dict[key]['value'] = [val['value']
                                               for i in range(col_len)
                                               ]
                    
            #-----------------------------------------
            #Construção dos dicionários de informações
            #-----------------------------------------
            
            global info_dict_list
            
            info_dict_list = []
            
            for i in range(col_len):
            
                info_dict = {}
                
                info_dict['header'] = cols_dict['header']['value'][i]
                
                info_dict['title'] = cols_dict['title']['value'][i]
                
                info_dict['banner'] = cols_dict['banner']['value'][i]
                info_dict['banner_link'] = cols_dict['banner_link']['value'][i]
                info_dict['banner_mode'] = banner_mode
                info_dict['banner_caption'] = cols_dict['banner_caption']['value'][i]
                
                info_dict['body'] = cols_dict['body']['value'][i].split('\n')
                
                info_dict['footer'] = cols_dict['footer']['value'][i]
                info_dict['footer_link'] = cols_dict['footer_link']['value'][i]
                info_dict['footer_mode'] = footer_mode
                info_dict['footer_caption'] = cols_dict['footer_caption']['value'][i]
                
                info_dict_list.append(info_dict)
            return info_dict_list
        
    
        
        """
        #======================================================================
        #FUNÇÃO: IMPORTA DADOS DA PLANILHA E CRIA NEWSLETTER
        #======================================================================
        """
        
        def createNewsletter(newsletter,reset=True,pos='end'):
            
            if reset:
                newsletter.reset()
            
            #-------------------
            #Dados de Importação
            #-------------------
            global format_dict
            
            info_dict_list = infoDicts()
            
            
            for info_dict in info_dict_list:
            
                controller.createCard(newsletter,
                                      info=info_dict,
                                      format_dict=format_dict,
                                      pos=pos)
                
                
            display = open('display_text.html',encoding='utf8')
            pv_text.load_html(display.read())
            pv_text.update()
            display.close()
            

        
        """
        #======================================================================
        #JANELA DE VIZUALISAÇÃO
        #======================================================================
        """

        pv_widget = pvWidget(window_obj=self, 
                             parent=parent, 
                             controller=self.controller,
                             width=0.4,
                             height=0.9)
        
        pv_frame = pv_widget.pv_frame
        pv_text = pv_widget.pv_text
        """
        #======================================================================
        #FRAME DAS AÇÕES
        #======================================================================
        """
        
        act_frame = ttk.Frame(self,width=0.6*parent.winfo_width())
        act_frame.grid(row=0,column=2,
                       columnspan=4,
                       rowspan=3,
                       sticky='nsew',pady=2,padx=20)
        act_frame.update()
        

        act_container = ttk.Notebook(act_frame,
                                     width=act_frame.winfo_width(),
                                     height=act_frame.winfo_height()
                                     )
        act_container.grid(row=0,column=0,sticky='nsew',pady=10)
        act_container.update()
        
        """
        #=================
        #Dados da Planilha
        #=================
        """
        
        sheet_frame = ttk.Frame(act_container)
        sheet_frame.grid(row=0,column=0,sticky='nsew',pady=10)
        sheet_frame.update()
        
        
        #--Caminho da Planilha
        #---Label
        act_xlpath_lbl = ttk.Label(sheet_frame,text='Caminho da Planilha:',anchor='w',)
        act_xlpath_lbl.grid(row=0,column=0,padx=(10,5),pady=(10,5),sticky='w')
        
        #---Mensagem de ajuda
        xlpath_lbl_tip='Caminho para a planilha contendo os dados do informe'
        CreateToolTip(act_xlpath_lbl,xlpath_lbl_tip)
        
        #---Entrada
        path_sht = tk.StringVar('')
        path_sht.set(import_dict['xlsx_path'])
        act_xlpath_ent = ttk.Entry(sheet_frame,textvariable=path_sht,width=30)
        act_xlpath_ent.grid(row=0,column=1,columnspan=2,padx=(5,5),pady=(10,5),sticky='we')
        
        #---Explorador de Arquivos
        act_xlpath_btt =ttk.Button(sheet_frame,text='Buscar',
                                  command=lambda: browseFiles(path_sht)
                                  )
        act_xlpath_btt.grid(row=0,column=3,padx=(5,10),pady=(10,5),sticky='w')
        
        #--Nome da Aba
        #---Label
        act_xlpath_sht = ttk.Label(sheet_frame,text='Nome ou Número da Aba:',anchor='w',)
        act_xlpath_sht.grid(row=1,column=0,padx=(10,5),pady=(10,5),sticky='w')
        
        #---Mensagem de ajuda
        xlpath_sht_tip='Título da aba contendo a planílha'
        CreateToolTip(act_xlpath_sht,xlpath_sht_tip)
        
        #---Entrada
        name_sht = tk.StringVar('')
        name_sht.set(import_dict['xlsx_sheet'])
        act_xlpath_ent = ttk.Entry(sheet_frame,textvariable=name_sht,width=30)
        act_xlpath_ent.grid(row=1,column=1,columnspan=2,padx=(5,5),pady=(10,5),sticky='we')
        
        #--Cabeçalhos
        #---Label
        act_heading_lbl = ttk.Label(sheet_frame,text='Linhas de Cabeçalho:',anchor='w')
        act_heading_lbl.grid(row=2,column=0,padx=(10,5),pady=(5,5),sticky='w')
        
        #---Mensagem de ajuda
        heading_lbl_tip='Número de linhas do cabeçalho na planilha'
        CreateToolTip(act_heading_lbl,heading_lbl_tip)
        
        #---Entrada
        number_head = tk.StringVar('')
        number_head.set(import_dict['heading_lines'])
        act_heading_ent = ttk.Entry(sheet_frame,textvariable=number_head,width=3)
        act_heading_ent.grid(row=2,column=1,padx=(5,10),pady=(5,5),sticky='e')
        
        
        #---===================================================================
        
        """
        #=========================
        #Identificação das Colunas
        #=========================
        """
        col_frame = ttk.Frame(act_container)
        col_frame.grid(row=2,column=0,sticky='nsew',pady=10)
        col_frame.update()
        
        #---Label
        act_heading_lbl = ttk.Label(col_frame,text='Seleção das Colunas Significativas',anchor='center')
        act_heading_lbl.grid(row=3,column=0,columnspan=4,pady=(2,5),sticky='new')
        
        
        #---Cabeçalho
        #----Label
        act_header_lbl = ttk.Label(col_frame,text='Coluna do Cabeçalho:',anchor='w')
        act_header_lbl.grid(row=4,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        header_lbl_tip=('Letras correspondentes à coluna dos Cabeçalhos na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_header_lbl,header_lbl_tip)
        
        #----Entrada
        id_hd = tk.StringVar('')
        id_hd.set(import_dict['header_var'][1] if import_dict['header_var'][0] == 'col'
                   else ''
                   )
        act_header_ent = ttk.Entry(col_frame,textvariable=id_hd,width=3)
        act_header_ent.grid(row=4,column=1,padx=(5,10),pady=(5,5),sticky='ne')
        
        #----Label-default
        act_header_lbl2 = ttk.Label(col_frame,text='[OU] Padrão:',anchor='w')
        act_header_lbl2.grid(row=4,column=2,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda-default
        header_lbl_tip2=('Valor padrão aplicado a todos os cards')
        CreateToolTip(act_header_lbl2,header_lbl_tip2)
        
        #----Entrada-default
        id_hd_default = tk.StringVar('')
        id_hd_default.set(import_dict['header_var'][1] if import_dict['header_var'][0] == 'default'
                           else ''
                           )
        act_header_ent2 = ttk.Entry(col_frame,textvariable=id_hd_default,width=20)
        act_header_ent2.grid(row=4,column=3,padx=(5,10),pady=(5,5),sticky='nw')
        
        #----------------------------------------------------------------------
        
        #---Título
        #----Label
        act_title_lbl = ttk.Label(col_frame,text='Coluna do Título:',anchor='w')
        act_title_lbl.grid(row=5,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        title_lbl_tip=('Letras correspondentes à coluna dos títulos na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_title_lbl,title_lbl_tip)
        
        #----Entrada
        id_ttl = tk.StringVar('')
        id_ttl.set(import_dict['title_var'][1] if import_dict['title_var'][0] == 'col'
                   else ''
                   )
        act_title_ent = ttk.Entry(col_frame,textvariable=id_ttl,width=3)
        act_title_ent.grid(row=5,column=1,padx=(5,10),pady=(5,5),sticky='ne')
        
        #----Label-default
        act_title_lbl2 = ttk.Label(col_frame,text='[OU] Padrão:',anchor='w')
        act_title_lbl2.grid(row=5,column=2,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda-default
        title_lbl_tip2=('Valor padrão aplicado a todos os cards')
        CreateToolTip(act_title_lbl2,title_lbl_tip2)
        
        #----Entrada-default
        id_ttl_default = tk.StringVar('')
        id_ttl_default.set(import_dict['title_var'][1] if import_dict['title_var'][0] == 'default'
                           else ''
                           )
        act_title_ent2 = ttk.Entry(col_frame,textvariable=id_ttl_default,width=20)
        act_title_ent2.grid(row=5,column=3,padx=(5,10),pady=(5,5),sticky='nw')
        
        #---===================================================================
        
        #---Corpo
        #----Label
        act_body_lbl = ttk.Label(col_frame,text='Coluna do Corpo:',anchor='w')
        act_body_lbl.grid(row=6,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        body_lbl_tip=('Letras correspondentes à coluna dos corpos de notícia na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_body_lbl,body_lbl_tip)
        
        #----Entrada
        id_bd = tk.StringVar('') 
        id_bd.set(import_dict['body_var'][1] if import_dict['body_var'][0] == 'col'
                  else ''
                  )
        act_body_ent = ttk.Entry(col_frame,textvariable=id_bd,width=3)
        act_body_ent.grid(row=6,column=1,padx=(5,10),pady=(5,5),sticky='ne')
        
        
        #---===================================================================
        
        #---Banner
        #----Label
        act_banner_lbl = ttk.Label(col_frame,text='Coluna do Banner:',anchor='w')
        act_banner_lbl.grid(row=7,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        banner_lbl_tip=('Letras correspondentes à coluna dos banners na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_banner_lbl,banner_lbl_tip)
        
        #----Entrada
        id_bn = tk.StringVar('')
        id_bn.set(import_dict['banner_var'][1] if import_dict['banner_var'][0] == 'col'
                  else ''
                  )
        act_banner_ent = ttk.Entry(col_frame,textvariable=id_bn,width=3)
        act_banner_ent.grid(row=7,column=1,padx=(5,10),pady=(5,5),sticky='ne')
        
        #----Label-default
        act_banner_lbl2 = ttk.Label(col_frame,text='[OU] Padrão:',anchor='w')
        act_banner_lbl2.grid(row=7,column=2,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda-default
        banner_lbl_tip2=('Valor padrão aplicado a todos os cards')
        CreateToolTip(act_banner_lbl2,banner_lbl_tip2)
        
        #----Entrada-default
        id_bn_default = tk.StringVar('') 
        id_bn_default.set(import_dict['banner_var'][1] if import_dict['banner_var'][0] == 'default'
                  else ''
                  )
        
        act_banner_ent2 = ttk.Entry(col_frame,textvariable=id_bn_default,width=20)
        
        act_banner_btt = ttk.Button(col_frame,
                                    text='Buscar',
                                    command = lambda: browseFiles(id_bn_default))
        
        act_banner_ent2.grid(row=7,column=3,padx=(5,10),pady=(5,5),sticky='nw')
        act_banner_btt.grid(row=7,column=4,padx=(5,10),pady=(5,5),sticky='nw')
        #---===================================================================
        
        #---Footer
        #----Label
        act_footer_lbl = ttk.Label(col_frame,text='Coluna do Rodapé:',anchor='w')
        act_footer_lbl.grid(row=8,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        footer_lbl_tip=('Letras correspondentes à coluna dos rodapés na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_footer_lbl,footer_lbl_tip)
        
        #----Entrada
        id_ft = tk.StringVar('')
        id_ft.set(import_dict['footer_var'][1] if import_dict['footer_var'][0] == 'col'
                  else ''
                  )
        act_footer_ent = ttk.Entry(col_frame,textvariable=id_ft,width=3)
        act_footer_ent.grid(row=8,column=1,padx=(5,10),pady=(5,5),sticky='ne')
        
        #----Label-default
        act_footer_lbl2 = ttk.Label(col_frame,text='[OU] Padrão:',anchor='w')
        act_footer_lbl2.grid(row=8,column=2,padx=(10,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda-default
        footer_lbl_tip2=('Valor padrão aplicado a todos os cards')
        CreateToolTip(act_footer_lbl2,footer_lbl_tip2)
        
        #----Entrada-default
        id_ft_default = tk.StringVar('')
        id_ft_default.set(import_dict['footer_var'][1] if import_dict['footer_var'][0] == 'default'
                          else ''
                          )
        act_footer_ent2 = ttk.Entry(col_frame,textvariable=id_ft_default,width=20)
        act_footer_btt = ttk.Button(col_frame,
                                    text='Buscar',
                                    command = lambda: browseFiles(id_ft_default))
        
        act_footer_ent2.grid(row=8,column=3,padx=(5,10),pady=(5,5),sticky='nw')
        act_footer_btt.grid(row=8,column=4,padx=(5,10),pady=(5,5),sticky='nw')
        #======================================================================
        """
        #======================
        #Parâmetros das Figuras
        #======================
        """
        act_params_frame = ttk.Frame(act_container)
        act_params_frame.grid(row=0,column=0,columnspan=2,sticky='ew')
        
        
        #-Label
        act_params_lbl = ttk.Label(act_params_frame,text='Parâmetros das Imagens',font='Times',anchor='center')
        act_params_lbl.grid(row=0,column=0,columnspan=2,padx=10,pady=(2,5))
        
        #======================================================================
        
        #-Banner
        
        #--frame
        act_bnparams_frame = ttk.LabelFrame(act_params_frame,text='Banner')
        act_bnparams_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nsew')
        
        #--Radial Buttons
        
        figureopt_bn = tk.StringVar()   #Variável da Decisão
        figureopt_bn.set(import_dict['banner_mode'])
        
        #---URL
        #----Label
        act_bnparams_URL_lbl = ttk.Label(act_bnparams_frame,
                                         text='URL',
                                         font='Times',
                                         anchor='center'
                                         )
        act_bnparams_URL_lbl.grid(row=0,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
  
        #----Button
        act_bnparams_URL_btt = ttk.Radiobutton(act_bnparams_frame,
                                              var=figureopt_bn,value='url'
                                              )
        act_bnparams_URL_btt.grid(row=1,column=0,padx=(5,5),pady=(5,5))
        
        #---LOCAL PATH
        #----Label
        act_bnparams_path_lbl = ttk.Label(act_bnparams_frame,
                                          text='Caminho\nLocal',
                                          font='Times',
                                          anchor='center'
                                          )
        act_bnparams_path_lbl.grid(row=0,column=1,padx=(5,5),pady=(5,5),sticky='ew')
        
  
        #----Button
        act_bnparams_path_btt = ttk.Radiobutton(act_bnparams_frame,
                                              var=figureopt_bn,value='path'
                                              )
        act_bnparams_path_btt.grid(row=1,column=1,padx=(5,5),pady=(5,5))
        
        #---LINK
        
        link_bn = tk.StringVar('')
        link_bn_default = tk.StringVar('')
        
        link_bn.set(import_dict['banner_link'][1] if import_dict['banner_var'][0] == 'col'
                            else ''
                            )
        link_bn_default.set(import_dict['banner_link'][1] if import_dict['banner_var'][0] == 'default'
                            else ''
                            )
        
        #----Label
        act_bnparams_link_lbl = ttk.Label(act_bnparams_frame,text='Coluna\n do Link',font='Times',anchor='center')
        act_bnparams_link_lbl.grid(row=2,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
        
        #----Entry
        act_bnparams_link_ent = ttk.Entry(act_bnparams_frame,
                                         textvariable=link_bn,
                                         width = 3
                                         )
        act_bnparams_link_ent.grid(row=2,column=1,padx=(2,5),pady=(5,5),sticky='W')
        
        #----Label2
        act_bnparams_link_lbl = ttk.Label(act_bnparams_frame,text='[OU] Link\n Padrão',
                                          font='Times',
                                          anchor='center'
                                          )
        act_bnparams_link_lbl.grid(row=2,column=2,padx=(5,5),pady=(5,5),sticky='Ew')
        
        
        #----Entry2
        act_bnparams_link_ent = ttk.Entry(act_bnparams_frame,
                                         textvariable=link_bn_default,
                                         width = 20
                                         )
        act_bnparams_link_ent.grid(row=2,column=3,padx=(2,5),pady=(5,5),sticky='w')
        
        #---LEGENDA
        
        cpt_bn = tk.StringVar('')
        cpt_bn_default = tk.StringVar('')
        cpt_bn_empty = tk.StringVar('')
        
        cpt_bn.set(import_dict['banner_caption'][1] if import_dict['banner_caption'][0] == 'col'
                            else ''
                            )
        cpt_bn_default.set(import_dict['banner_caption'][1] if import_dict['banner_caption'][0] == 'default'
                            else ''
                            )
        cpt_bn_empty.set(import_dict['banner_empty_alt'])
        
        #----Label
        
        act_bnparams_cpt_lbl = ttk.Label(act_bnparams_frame,text='Legenda:',font='Times',anchor='w')
        act_bnparams_cpt_lbl.grid(row=3,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
        #----Entry
        act_bnparams_cpt_ent = ttk.Entry(act_bnparams_frame,
                                         textvariable=cpt_bn,
                                         width = 20
                                         )
        act_bnparams_cpt_ent.grid(row=3,column=1,padx=(2,5),pady=(5,5),sticky='W')
        
        #----Label2
        act_bnparams_cpt_lbl = ttk.Label(act_bnparams_frame,
                                         text='[OU]\nLegenda\nPadrão',
                                         font='Times',
                                         anchor='center'
                                         )
        act_bnparams_cpt_lbl.grid(row=3,column=2,padx=(5,5),pady=(5,5),sticky='Ew')
        
        
        #----Entry2
        act_bnparams_cpt_ent = ttk.Entry(act_bnparams_frame,
                                         textvariable=cpt_bn_default,
                                         width = 20
                                         )
        act_bnparams_cpt_ent.grid(row=3,column=3,padx=(2,5),pady=(5,5),sticky='w')

        #----Label3
        act_bnparams_cpt_lbl = ttk.Label(act_bnparams_frame,text='Texto se\nvazio',font='Times',anchor='center')
        act_bnparams_cpt_lbl.grid(row=3,column=4,padx=(5,5),pady=(5,5),sticky='Ew')
        
        
        #----Entry3
        act_bnparams_cpt_ent = ttk.Entry(act_bnparams_frame,
                                         textvariable=cpt_bn_empty,
                                         width = 20
                                         )
        act_bnparams_cpt_ent.grid(row=3,column=5,padx=(2,5),pady=(5,5),sticky='w')        
        
        
        
        #======================================================================
        
        #-Footer
         
        #--RadialButton frame
        act_ftparams_frame = ttk.LabelFrame(act_params_frame,text='Rodapé')
        act_ftparams_frame.grid(row=2,column=0,padx=10,pady=10,sticky='nsew')
        
        #--Radial Buttons
        
        figureopt_ft = tk.StringVar()   #Variável da Decisão
        figureopt_ft.set(import_dict['footer_mode'])
        
        #---URL
        #----Label
        act_ftparams_URL_lbl = ttk.Label(act_ftparams_frame,text='URL',
                                         font='Times',
                                         anchor='center'
                                         )
        act_ftparams_URL_lbl.grid(row=0,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
  
        #----Button
        act_ftparams_URL_btt = ttk.Radiobutton(act_ftparams_frame,
                                              var=figureopt_ft,value='url'
                                              )
        act_ftparams_URL_btt.grid(row=1,column=0,padx=(5,5),pady=(5,5))
        
        #---LOCAL PATH
        #----Label
        act_ftparams_path_lbl = ttk.Label(act_ftparams_frame,text='Caminho\nLocal',
                                          font='Times',
                                          anchor='center'
                                          )
        act_ftparams_path_lbl.grid(row=0,column=1,padx=(5,5),pady=(5,5),sticky='ew')
        
  
        #----Button
        act_ftparams_path_btt = ttk.Radiobutton(act_ftparams_frame,
                                              var=figureopt_ft,value='path'
                                              )
        act_ftparams_path_btt.grid(row=1,column=1,padx=(5,5),pady=(5,5))
        
        #---TEXT
        #----Label
        act_ftparams_txt_lbl = ttk.Label(act_ftparams_frame,text='Texto',
                                         font='Times',
                                         anchor='center'
                                         )
        act_ftparams_txt_lbl.grid(row=0,column=2,padx=(5,5),pady=(5,5),sticky='ew')
        
  
        #----Button
        act_ftparams_txt_btt = ttk.Radiobutton(act_ftparams_frame,
                                              var=figureopt_ft,value='text'
                                              )
        act_ftparams_txt_btt.grid(row=1,column=2,padx=(5,5),pady=(5,5))
        
        #---LINK
        
        link_ft = tk.StringVar('')
        link_ft_default = tk.StringVar('')
        
        link_ft.set(import_dict['footer_link'][1] if import_dict['footer_link'][0] == 'col'
                            else ''
                            )
        link_ft_default.set(import_dict['footer_link'][1] if import_dict['footer_link'][0] == 'default'
                            else ''
                            )
        
        
        #----Label
        act_ftparams_link_lbl = ttk.Label(act_ftparams_frame,text='Coluna\n do Link',font='Times',anchor='center')
        act_ftparams_link_lbl.grid(row=2,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
        
        #----Entry
        act_ftparams_link_ent = ttk.Entry(act_ftparams_frame,
                                         textvariable=link_ft,
                                         width = 3
                                         )
        act_ftparams_link_ent.grid(row=2,column=1,padx=(2,5),pady=(5,5),sticky='w')
        
        #----Label2
        act_ftparams_link_lbl = ttk.Label(act_ftparams_frame,text='[OU] Link\n Padrão',font='Times',anchor='center')
        act_ftparams_link_lbl.grid(row=2,column=2,padx=(5,5),pady=(5,5),sticky='ew')
        
        
        #----Entry2
        act_ftparams_link_ent = ttk.Entry(act_ftparams_frame,
                                         textvariable=link_ft_default,
                                         width = 20
                                         )
        act_ftparams_link_ent.grid(row=2,column=3,padx=(2,5),pady=(5,5),sticky='w')
        
        #---LEGENDA
        
        cpt_ft = tk.StringVar('')
        cpt_ft_default = tk.StringVar('')
        cpt_ft_empty = tk.StringVar('')
        
        cpt_ft.set(import_dict['footer_caption'][1] if import_dict['footer_caption'][0] == 'col'
                            else ''
                            )
        cpt_ft_default.set(import_dict['footer_caption'][1] if import_dict['footer_caption'][0] == 'default'
                            else ''
                            )
        cpt_ft_empty.set(import_dict['footer_empty_alt'])
        
        #----Label
        
        act_ftparams_cpt_lbl = ttk.Label(act_ftparams_frame,text='Legenda:',font='Times',anchor='w')
        act_ftparams_cpt_lbl.grid(row=3,column=0,padx=(5,5),pady=(5,5),sticky='ew')
        
        #----Entry
        act_ftparams_cpt_ent = ttk.Entry(act_ftparams_frame,
                                         textvariable=cpt_ft,
                                         width = 20
                                         )
        act_ftparams_cpt_ent.grid(row=3,column=1,padx=(2,5),pady=(5,5),sticky='W')
        
        #----Label2
        act_ftparams_cpt_lbl = ttk.Label(act_ftparams_frame,
                                         text='[OU]\nLegenda\nPadrão',
                                         font='Times',
                                         anchor='center'
                                         )
        act_ftparams_cpt_lbl.grid(row=3,column=2,padx=(5,5),pady=(5,5),sticky='Ew')
        
        
        #----Entry2
        act_ftparams_cpt_ent = ttk.Entry(act_ftparams_frame,
                                         textvariable=cpt_ft_default,
                                         width = 20
                                         )
        act_ftparams_cpt_ent.grid(row=3,column=3,padx=(2,5),pady=(5,5),sticky='w')

        #----Label3
        act_ftparams_cpt_lbl = ttk.Label(act_ftparams_frame,text='Texto se\nvazio',font='Times',anchor='center')
        act_ftparams_cpt_lbl.grid(row=3,column=4,padx=(5,5),pady=(5,5),sticky='Ew')
        
        
        #----Entry3
        act_ftparams_cpt_ent = ttk.Entry(act_ftparams_frame,
                                         textvariable=cpt_ft_empty,
                                         width = 20
                                         )
        act_ftparams_cpt_ent.grid(row=3,column=5,padx=(2,5),pady=(5,5),sticky='w')
        
        """
        #======================
        #-Parametros de Seleção
        #======================
        """
        
        #-Frame
        act_filter_frame = ttk.Frame(act_container)
        act_filter_frame.grid(row=0,column=0,sticky='nsew')
        
        #-Label
        act_filter_lbl = ttk.Label(act_filter_frame,text='Filtragem de Dados',anchor='center',font='Times')
        act_filter_lbl.grid(row=0,column=0,columnspan=2,sticky='ew')
        
        #-Id da Coluna
        #--Label
        act_id_lbl = ttk.Label(act_filter_frame,text='Coluna\n das Datas:',anchor='w',font="Times")
        act_id_lbl.grid(row=1,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #--Mensagem de ajuda
        id_lbl_tip=('Letras correspondentes à coluna dos rodapés na planilha\n'+
                       'Ex. A, B, C...AA, AB')
        CreateToolTip(act_id_lbl,id_lbl_tip)
        
        #--Entrada
        id_date = tk.StringVar('') 
        id_date.set(import_dict['date_var'][1])
        act_id_ent = ttk.Entry(act_filter_frame,textvariable=id_date,width=3)
        act_id_ent.grid(row=1,column=1,padx=(5,10),pady=(5,5),sticky='w')
        
        #-Frequência
        #--Label
        act_freq_lbl = ttk.Label(act_filter_frame,text='Frequência:',anchor='w',font="Times")
        act_freq_lbl.grid(row=2,column=0,padx=(10,5),pady=(5,5),sticky='nsw')
        
        freq_lbl_tip=("""Define o intervalo de tempo:
                      
-Quando se seleciona um dia da semana:
    ->Todas as notícias entre o dia da semana anterior e 
      seguinte à data referência.
-Quando se seleciona um dia do mês:
    ->Todas as notícias entre o dia selecionado do mês 
      anterior à data referência e o dia selecionado 
      do mês seguinte à data de referência.
-Quando não há seleção:
    ->Todas as notícias desde a data de referência 
      até hoje"""
                    )
        CreateToolTip(act_freq_lbl,freq_lbl_tip)
        
        #--RadialButton frame
        act_freqparams_frame = ttk.Frame(act_filter_frame)
        act_freqparams_frame.grid(row=2,column=1,sticky='ew')
        
        #--Radial Buttons
        self.weekopt_date = tk.StringVar('')  #Variável da Decisão
        self.monthopt_date = tk.StringVar('')   #Variável da Decisão
        self.compopt_date = tk.StringVar('')   #Variável da Decisão

        
        if import_dict['date_freq'][0] == 'weekly':
            self.weekopt_date.set(import_dict['date_freq'][1])
            self.monthopt_date.set('   ')
            self.compopt_date.set('')
        elif import_dict['date_freq'][0] == 'monthly':
            self.weekopt_date.set('')
            self.compopt_date.set('')
            self.monthopt_date.set(import_dict['date_freq'][1])
        elif import_dict['date_freq'][0] == 'comparison':
            self.weekopt_date.set('')
            self.monthopt_date.set('   ')
            self.compopt_date.set(import_dict['date_freq'][1])
        else:
            self.weekopt_date.set('')
            self.monthopt_date.set('   ')
            self.compopt_date.set('Igual referência')
        
        #======================================================================
        
        #---Semanal
        #----Label
        act_freqparams_week_lbl = ttk.Label(act_freqparams_frame,text='Semanal',font='Times',anchor='center')
        act_freqparams_week_lbl.grid(row=0,column=0,padx=(5,5),pady=(5,5),sticky='nsew')
        
        #----Buttons
        act_week_frame = ttk.Frame(act_freqparams_frame)
        act_week_frame.grid(row=0,column=1,sticky='ew')
        
        #-----Domingo
        act_dom_lbl = ttk.Label(act_week_frame,text='D',anchor='center',font="Times")
        act_dom_lbl.grid(row=0,column=0,padx=(2,1),pady=(5,1),sticky='ew')
        act_dom_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='0',
                                     offvalue=''
                                     )
        act_dom_btt.grid(row=1,column=0,padx=(2,1),pady=(1,5),sticky='ew')
        
        #-----Segunda
        act_seg_lbl = ttk.Label(act_week_frame,text='S',anchor='center',font="Times")
        act_seg_lbl.grid(row=0,column=1,padx=(1,1),pady=(5,1),sticky='ew')
        act_seg_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='1',
                                     offvalue=''
                                     )
        act_seg_btt.grid(row=1,column=1,padx=(1,1),pady=(1,5),sticky='ew')
        
        #-----Terça
        act_ter_lbl = ttk.Label(act_week_frame,text='T',anchor='center',font="Times")
        act_ter_lbl.grid(row=0,column=2,padx=(1,1),pady=(5,1),sticky='ew')
        act_ter_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='2',
                                     offvalue=''
                                     )
        act_ter_btt.grid(row=1,column=2,padx=(1,1),pady=(1,5),sticky='ew')
        
        #-----Quarta
        act_qua_lbl = ttk.Label(act_week_frame,text='Q',anchor='center',font="Times")
        act_qua_lbl.grid(row=0,column=3,padx=(1,1),pady=(5,1),sticky='ew')
        act_qua_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='3',
                                     offvalue=''
                                     )
        act_qua_btt.grid(row=1,column=3,padx=(1,1),pady=(1,5),sticky='ew')
        
        #-----Quinta
        act_qui_lbl = ttk.Label(act_week_frame,text='Q',anchor='center',font="Times")
        act_qui_lbl.grid(row=0,column=4,padx=(1,1),pady=(5,1),sticky='ew')
        act_qui_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='4',
                                     offvalue=''
                                     )
        act_qui_btt.grid(row=1,column=4,padx=(1,1),pady=(1,5),sticky='ew')
        
        #-----Sexta
        act_sex_lbl = ttk.Label(act_week_frame,text='S',anchor='center',font="Times")
        act_sex_lbl.grid(row=0,column=5,padx=(1,1),pady=(5,1),sticky='ew')
        act_sex_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='5',
                                     offvalue=''
                                     )
        act_sex_btt.grid(row=1,column=5,padx=(1,1),pady=(1,5),sticky='ew')
        
        #-----Sabado
        act_sab_lbl = ttk.Label(act_week_frame,text='S',anchor='center',font="Times")
        act_sab_lbl.grid(row=0,column=6,padx=(1,10),pady=(5,1),sticky='ew')
        act_sab_btt = ttk.Checkbutton(act_week_frame,
                                     var=self.weekopt_date,
                                     onvalue='6',
                                     offvalue=''
                                     )
        act_sab_btt.grid(row=1,column=6,padx=(1,10),pady=(1,5),sticky='ew')
        
        #======================================================================
        
        #---Mensal
        #----Label
        act_freqparams_month_lbl = ttk.Label(act_freqparams_frame,text='Mensal',
                                            font='Times',anchor='center'
                                            )
        act_freqparams_month_lbl.grid(row=1,column=0,padx=(5,5),pady=(5,5),sticky='nsew')
        
        #----Options
        act_month_opt = ttk.Combobox(act_freqparams_frame,
                                     textvariable=self.monthopt_date,
                                     values=monthdays,
                                     )
        act_month_opt.config(width=35,
                             textvariable=self.monthopt_date)
        act_month_opt.grid(row=1,column=1,padx=(5,10),pady=(5,5),sticky='')
        
        #======================================================================
        
        #---Comparação
        #----Label
        act_freqparams_comp_lbl = ttk.Label(act_freqparams_frame,text='Comparação',
                                            font='Times',anchor='center'
                                            )
        act_freqparams_comp_lbl.grid(row=2,column=0,padx=(5,5),pady=(5,5),sticky='nsew')
        
        #----Options
        act_comp_opt = ttk.Combobox(act_freqparams_frame,
                                     textvariable=self.compopt_date,
                                     values=['',
                                             'Igual referência',
                                             'Antes da referência',
                                             'Após a referência'],
                                     )
        
        act_comp_opt.config(width=35,
                             textvariable=self.compopt_date)
        act_comp_opt.grid(row=2,column=1,padx=(5,10),pady=(5,5),sticky='')
        
        #------------------
        #Data de Referência
        #------------------
        
        #-Label
        act_ref_lbl = ttk.Label(act_filter_frame, text='Data\n de Referência',
                               anchor='w',font='Times'
                               )
        act_ref_lbl.grid(row=3,column=0,padx=(10,5),pady=(5,5),sticky='w')
        
        act_ref_cal = DateEntry(act_filter_frame,date_pattern='dd/mm/yyyy')
        act_ref_cal.grid(row=3,column=1)
        
        #---------------------
        #Indicador de Inclusão
        #---------------------
        
        #-Id da Coluna
        #--Label
        act_tag_lbl = ttk.Label(act_filter_frame,text='Coluna\n da Tag de Inluir:',anchor='w',font="Times")
        act_tag_lbl.grid(row=4,column=0,padx=(10,5),pady=(5,5),sticky='nw')
        
        #--Mensagem de ajuda
        tag_lbl_tip=('Letras correspondentes à coluna dos rodapés na planilha\n'+
                     'Ex. A, B, C...AA, AB')
        CreateToolTip(act_tag_lbl,tag_lbl_tip)
        
        #--Entradas
        
        act_tag_frame = ttk.Frame(act_filter_frame)
        act_tag_frame.grid(row=4,column=1,sticky='ew')
        
        id_tag = tk.StringVar('') 
        id_tag.set(import_dict['tag_var'][1])
        act_tag_ent = ttk.Entry(act_tag_frame,textvariable=id_tag,width=3)
        act_tag_ent.grid(row=0,column=0,padx=(5,10),pady=(5,5),sticky='w')
        
        #---Palavra Chave
        #----Label
        act_tag_lbl2 = ttk.Label(act_tag_frame,text='Incluir se\no Valor For:',anchor='w',font="Times")
        act_tag_lbl2.grid(row=0,column=1,padx=(5,5),pady=(5,5),sticky='nw')
        
        #----Mensagem de ajuda
        tag_lbl_tip2=("""Termo que, quando detctado 
em uma célula da coluna,
indica que a linha deve 
ser incluida na newsletter"""
                      )
        CreateToolTip(act_tag_lbl2,tag_lbl_tip2)
        
        #----Entrada
        key_tag = tk.StringVar('')
        key_tag.set(import_dict['tag_key'])
        
        act_tag_ent = ttk.Entry(act_tag_frame,textvariable=key_tag)
        act_tag_ent.grid(row=0,column=2,padx=(5,10),sticky='ew')

        
        #======================================================================
        
        """
        #=======
        #-Botões
        #=======
        """
        
        #-Frame
        
        bt_frame = ttk.Frame(self)
        bt_frame.grid(row=3,column=2,padx=10,pady=(0,10),sticky='sew')
        bt_frame.rowconfigure([0],weight=1)
        bt_frame.columnconfigure([0,1],weight=1)
        

        
        #-BOTÃO DE IMPORTAR
        bt_import = ttk.Button(bt_frame,text='Importar\ne sustituir',
                            width=10,
                            command= lambda: createNewsletter(news),
                            default='active'
                            )
        bt_import.grid(row=0,column=0,padx=10)
        
        bt_import = ttk.Button(bt_frame,text='Importar\ne adicionar ao fim',
                            width=10,
                            command= lambda: createNewsletter(news,reset=False),
                            default='active'
                            )
        bt_import.grid(row=0,column=1,padx=10)
        
        
        #-BOTÃO DE FORMATAÇÃO
        bt_format = ttk.Button(bt_frame,text='Formatação Avançada',
                              width=20,
                              command=lambda: controller.show_window(format_wd)
                              )
        bt_format.grid(row=0,column=3,padx=10,sticky='e')
        
        #-BOTÃO DE SALVAR CONFIGS
        bt_back = ttk.Button(bt_frame,text='Salvar\nConfigurações',
                             width=15,
                            command= lambda: save_profile()
                            )
        bt_back.grid(row=0,column=4,padx=10)
        
        #-BOTÃO DE IMPORTAR CONFIGS
        bt_back = ttk.Button(bt_frame,text='Importar\nConfigurações',
                             width=15,
                             command= lambda: load_profile()
                             )
        bt_back.grid(row=0,column=5,padx=10)   
        
        #-BOTÃO DE VOLTAR
        bt_back = ttk.Button(bt_frame,text='Voltar',
                            width=8,
                            command=lambda: controller.show_frame(self,adding_page))
        bt_back.grid(row=0,column=6,padx=10,sticky='e')
        
        """
        #-----------------------------------------------------------------
        #SEPARADORES
        #-----------------------------------------------------------------
        """
        
        pv_separtor=ttk.Separator(self,orient=tk.VERTICAL)
        pv_separtor.grid(row=0,column=1,rowspan=4,sticky='ns')
        
        """
        #----------------------------------------------------------------
        #REDIMENSIONAMENTO DINAMICO
        #----------------------------------------------------------------
        """
        
        self_col,self_row=self.size()

        self.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.columnconfigure([0,2], weight=1) #Faz com que a coluna de root expanda até a borda
        
        act_frame_col,act_frame_row=act_frame.size()
        act_frame.rowconfigure([i for i in range(act_frame_row)],weight=1)  
        act_frame.columnconfigure([i for i in range(act_frame_col)],weight=1)
        
        pv_frame_col,pv_frame_row=pv_frame.size()
        pv_frame.rowconfigure([i for i in range(pv_frame_row)],weight=1)
        pv_frame.columnconfigure([i for i in range(pv_frame_col)],weight=1)
        
        """
        #---------------------------------------------------------------
        #MENU DE ABAS
        #---------------------------------------------------------------
        """
        
        act_container.add(sheet_frame,text='Planilha')
        act_container.add(col_frame,text='Colunas')
        act_container.add(act_params_frame,text='Figuras')
        act_container.add(act_filter_frame,text='Filtro')
        
        act_container.grid(row=0,column=2,rowspan=4, sticky='nsew')