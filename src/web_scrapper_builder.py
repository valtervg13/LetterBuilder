# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:43:05 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
import newsapi as napi
from cfg import news,format_dict,newsapi_dict
import util
from Preview_Window import pvWidget

news_q = tk.StringVar()
news_lang = tk.StringVar()
news_country = tk.StringVar()

class web_scrapper_page(tk.Frame):
    def __init__(self, parent, controller):
        
        from single_entry import single_entry
        from adding_page import adding_page
        from format_wd import format_wd
        from html_viewport import HTML_viewport
        
        ttk.Frame.__init__(self,
                           parent,
                           height=parent.winfo_height(),
                           width=parent.winfo_width())
        self.controller = controller
        
        def browseFiles(option='banner'):
            #nonlocal banner_url
            #nonlocal footer_url
            filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File")
            
            """
            if option == 'banner':
                banner_url.set(filename)
            else:
                footer_url.set(filename)
            """
        #---------------------------------------------------------------
        #FUNÇÃO: CRIA O DICIONÁRIO DE INFORMAÇÕES DO CARD
        #---------------------------------------------------------------
        def InfoDict():
            
            info_dict = {}
            
            info_dict['header'] = header_var.get()
            info_dict['title'] = act_title.get()
            info_dict['banner'] = act_banner.get()
            info_dict['banner_link'] = act_banner_link.get()
            info_dict['banner_mode'] = banner_mode.get()
            info_dict['banner_caption']= bn_cpt_var.get()
            info_dict['body'] = act_body.get('1.0','end-1c').split('\n')
            info_dict['footer'] = act_footer.get()
            info_dict['footer_link'] = act_footer_link.get()
            info_dict['footer_mode'] = footer_mode.get()
            info_dict['footer_caption']= ft_cpt_var.get()
            
            return info_dict

            
        def Insert(popup_output,
                   popup_window,
                   newsletter='',
                   **kwargs):
            
            Create(newsletter, pos=int(popup_output))
            
            popup_window.close()            
            
        def get_pos(newsletter):
            
            single_entry(parent=self,
                         parent_func=Insert,
                         master = controller,
                         label_text='Posição: (1,2...)',
                         f_kwargs={'newsletter':newsletter})
            
        
        def Create(newsletter,pos='end',**kwargs):
            
            controller.createCard(newsletter,
                                  InfoDict(),
                                  pos=pos)
            
            display = open('display_text.html',encoding="utf8")
            pv_text.load_html(display.read())
            pv_text.update()
            display.close()
            

        #Function to get news api parameters as dictionary
        def get_newsapi_params():
            
            params = {}
            
            params['q'] = news_q.get()
            params['language'] = news_lang.get()
            params['country'] = news_country.get()
            params['category'] = news_cat.get()
            params['sources'] = news_src.get()
            params['page_size'] = news_pg_size.get()
            params['page'] = news_pg.get()
            params['sort_by'] = news_sort.get()
            
            return params

        #---------------------------------------------------------------
        #JANELA DE VIZUALISAÇÃO
        #---------------------------------------------------------------
        
        pv_widget = pvWidget(window_obj=self, 
                             parent=parent, 
                             controller=self.controller,
                             width=0.4,
                             height=0.9)
        
        pv_frame = pv_widget.pv_frame
        pv_text = pv_widget.pv_text
        
        #---------------------------------------------------------------
        #FRAME DAS AÇÕES
        #---------------------------------------------------------------
        act_frame = ttk.Notebook(self)
        act_frame.grid(row=0,rowspan=3,column=2,sticky='nsew',padx=5,pady=(2,5))
        #act_frame.grid_propagate(0)
        act_frame.update()
        act_frame.columnconfigure([0],weight=1)
        
        #---------------------------------------------------------------
        # IMPORT PARAMETERS
        #---------------------------------------------------------------

        act_import_frame = ttk.Frame(act_frame)
        act_import_frame.grid(row=0,column=0,sticky='nsew')

        #Query

        act_import_legend_q = ttk.Label(act_import_frame,text='Query:')
        act_import_legend_q.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)

        global news_q
        news_q.set(newsapi_dict['q'])
        act_import_q = ttk.Entry(act_import_frame,textvariable=news_q,width=80)
        act_import_q.grid(row=0,column=1,sticky='nsew',padx=5,pady=5)

        #Language
        act_import_legend_lang = ttk.Label(act_import_frame,text='Language:')
        act_import_legend_lang.grid(row=1,column=0,sticky='nsew',padx=5,pady=5)

        global news_lang
        news_lang.set(newsapi_dict['language'])
        act_import_lang = ttk.Entry(act_import_frame,textvariable=news_lang,width=5)
        act_import_lang.grid(row=1,column=1,sticky='nsew',padx=5,pady=5)

        #Country
        act_import_legend_country = ttk.Label(act_import_frame,text='Country:')
        act_import_legend_country.grid(row=2,column=0,sticky='nsew',padx=5,pady=5)

        global news_country
        news_country.set(newsapi_dict['country'])
        act_import_country = ttk.Entry(act_import_frame,textvariable=news_country,width=10)
        act_import_country.grid(row=2,column=1,sticky='nsew',padx=5,pady=5)


        act_frame.add(act_import_frame, text = 'Parâmetros da API')
        
        
        #---------------------------------------------------------------
        #FRAME DOS BOTÕES
        #---------------------------------------------------------------
        
        bt_frame = ttk.Frame(self)
        bt_frame.grid(row=3,column=2,padx=10,pady=(10,10),sticky='sew')
        bt_frame.rowconfigure([0],weight=1)
        bt_frame.columnconfigure([0,1],weight=1)
        
        #--------------------
        #-BOTÃO DE CRIAR CARD
        #--------------------
        bt_back = ttk.Button(bt_frame,
                             text='Adicionar',
                             width=15,
                             command= lambda: Create(news)
                             )
        bt_back.grid(row=0,column=0,padx=10)
        
        #--------------------
        #-BOTÃO DE CRIAR CARD
        #--------------------
        bt_back = ttk.Button(bt_frame,
                             text='Inserir',
                             width=15,
                             command= lambda: get_pos(news)
                             )
        bt_back.grid(row=0,column=1,padx=10)   
        
        #----------------
        #-BOTÃO DE VOLTAR
        #----------------
        bt_back = ttk.Button(bt_frame,
                             text='Voltar',
                             width=15,
                             command=lambda: controller.show_frame(self,adding_page)
                             )
        bt_back.grid(row=0,column=2,padx=10)
        
        #--------------------
        #-BOTÃO DE FORMATAÇÃO
        #--------------------
        
        bt_format = ttk.Button(bt_frame,
                               text='Formatação\nAvançada',
                               width=25,
                               command=lambda: controller.show_window(format_wd)
                               )
        bt_format.grid(row=0,column=3,padx=10)
        
        
        #-----------------------------------------------------------------
        #SEPARADORES
        #-----------------------------------------------------------------
        
        pv_separtor=ttk.Separator(self,orient=tk.VERTICAL)
        pv_separtor.grid(row=0,column=1,rowspan=4,sticky='nsew')
        
        
        #----------------------------------------------------------------
        #REDIMENSIONAMENTO DINAMICO
        #----------------------------------------------------------------
        
        self_col,self_row=self.size()

        self.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        
        
        pv_frame_col,pv_frame_row=pv_frame.size()
        pv_frame.rowconfigure([i for i in range(pv_frame_row)],weight=1)
        pv_frame.columnconfigure([i for i in range(pv_frame_col)],weight=1)   