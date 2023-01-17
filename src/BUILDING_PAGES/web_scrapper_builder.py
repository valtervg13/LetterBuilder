# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:43:05 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import datetime as dt
import pickle as pk
import newsapi as napi
import webbrowser as wb

from cfg import news,format_dict,newsapi_dict
import Utilities.util as util
from SUPPORT_PAGES.Preview_Window import pvWidget
from tkinter import Tk, ttk
from tkinter.font import Font
from functools import partial

news_q = tk.StringVar()
news_lang = tk.StringVar()
news_country = tk.StringVar()
news_src = tk.StringVar()
news_from = tk.StringVar()
news_to = tk.StringVar()
news_sort_by = tk.StringVar()

class web_scrapper_page(tk.Frame):
    def __init__(self, parent, controller):
        
        from SUPPORT_PAGES.single_entry import single_entry
        from HOME_PAGES.adding_page import adding_page
        from SUPPORT_PAGES.format_wd import format_wd
        from SUPPORT_PAGES.html_viewport import HTML_viewport
        
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
        def get_newsapi_params(newsapi_dict):
            
            #subfunction that changes date format from dd/mm/yyyy to yyyy-mm-dd
            def date_format(date):
                return date[6:10] + '-' + date[3:5] + '-' + date[0:2]

            params = newsapi_dict
            
            params['q'] = news_q.get()
            params['language'] = news_lang.get()
            params['country'] = news_country.get()
            params['sources'] = news_src.get()
            params['from'] = date_format(news_from.get())
            params['to'] = date_format(news_to.get())
            params['sort_by'] = news_sort_by.get()
            
            return params

        #Function that takes a dictionary from get_newsapi_params and 
        #makes an http request through newsapi using the parameters
        def get_newsapi(params):
                
                http_params = {'q' : params['q'],
                               'language' : params['language'],
                               'from_param' : params['from'],
                               'to' : params['to'],
                               'sort_by' : params['sort_by']
                               }
                    
                http_params = {k:v for k,v in http_params.items() if v != ''}
                
                newsapi = napi.NewsApiClient(api_key=params['api_key'])
                
                news_results = newsapi.get_everything(**http_params)

                pk.dump(news_results,open('Data/news_results.pk','wb'))

        #Function that imports pickled newsapi results and creates list 
        # containing info for each article
        def get_newsapi_results():
            
            news_results = pk.load(open('Data/news_results.pk','rb'))
            
            newsapi_list = []
            
            for article in news_results['articles']:
                newsapi_list.append([article['title'],
                                    article['description'],
                                    article['url'],
                                    article['publishedAt']
                                    ]
                                    )
                
            return newsapi_list

        #function to wrap cells of result table
        def motion_handler(tree, event):
            f = Font(font='TkDefaultFont')
            # A helper function that will wrap a given value based on column width
            def adjust_newlines(val, width, pad=10):
                if not isinstance(val, str):
                    return val
                else:
                    words = val.split()
                    lines = [[],]
                    for word in words:
                        line = lines[-1] + [word,]
                        if f.measure(' '.join(line)) < (width - pad):
                            lines[-1].append(word)
                        else:
                            lines[-1] = ' '.join(lines[-1])
                            lines.append([word,])

                    if isinstance(lines[-1], list):
                        lines[-1] = ' '.join(lines[-1])

                    return '\n'.join(lines)

            if (event is None) or (tree.identify_region(event.x, event.y) == "separator"):
                # You may be able to use this to only adjust the two columns that you care about
                # print(tree.identify_column(event.x))

                col_widths = [tree.column(cid)['width'] for cid in tree['columns']]

                for iid in tree.get_children():
                    new_vals = []
                    for (v,w) in zip(tree.item(iid)['values'], col_widths):
                        new_vals.append(adjust_newlines(v, w))
                    tree.item(iid, values=new_vals)


                    act_results.bind('<B1-Motion>', partial(motion_handler, act_results))
                    motion_handler(act_results, None)   # Perform initial wrapping
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

        act_import_legend_q = ttk.Label(act_import_frame,text='Pesquisa:')
        act_import_legend_q.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)

        global news_q
        news_q.set(newsapi_dict['q'])
        act_import_q = ttk.Entry(act_import_frame,textvariable=news_q,width=80)
        act_import_q.grid(row=0,column=1,sticky='nsew',padx=5,pady=5)

        #Language
        act_import_legend_lang = ttk.Label(act_import_frame,text='Língua:')
        act_import_legend_lang.grid(row=1,column=0,sticky='nsew',padx=5,pady=5)

        global news_lang
        news_lang.set(newsapi_dict['language'])
        act_import_lang = ttk.Entry(act_import_frame,textvariable=news_lang,width=5)
        act_import_lang.grid(row=1,column=1,sticky='nsew',padx=5,pady=5)

        #Country
        act_import_legend_country = ttk.Label(act_import_frame,text='País:')
        act_import_legend_country.grid(row=2,column=0,sticky='nsew',padx=5,pady=5)

        global news_country
        news_country.set(newsapi_dict['country'])
        act_import_country = ttk.Entry(act_import_frame,textvariable=news_country,width=10)
        act_import_country.grid(row=2,column=1,sticky='nsew',padx=5,pady=5)

        #Date From
        act_import_legend_from = ttk.Label(act_import_frame,text='De:')
        act_import_legend_from.grid(row=3,column=0,sticky='nsew',padx=5,pady=5)

        global news_from
        news_from.set(newsapi_dict['from'])
        act_import_from = DateEntry(act_import_frame,
                                    date_pattern='dd/mm/yyyy',
                                    textvariable=news_from)
        act_import_from.grid(row=3,column=1,sticky='nsew',padx=5,pady=5)

        #Date To
        act_import_legend_to = ttk.Label(act_import_frame,text='Até:')
        act_import_legend_to.grid(row=4,column=0,sticky='nsew',padx=5,pady=5)

        global news_to
        news_to.set(newsapi_dict['to'])
        act_import_to = DateEntry(act_import_frame,
                                    date_pattern='dd/mm/yyyy',
                                    textvariable=news_to
                                    )
        act_import_to.grid(row=4,column=1,sticky='nsew',padx=5,pady=5)

        #Sort By
        act_import_legend_sort_by = ttk.Label(act_import_frame,text='Ordenar por:')
        act_import_legend_sort_by.grid(row=5,column=0,sticky='nsew',padx=5,pady=5)

        global news_sort_by
        news_sort_by.set(newsapi_dict['sort_by'])
        act_import_sort_by = ttk.Combobox(act_import_frame,textvariable=news_sort_by)
        act_import_sort_by['values'] = ('relevancy','popularity','publishedAt')
        act_import_sort_by.grid(row=5,column=1,sticky='nsew',padx=5,pady=5)

        #Button to call the API

        act_import_bt = ttk.Button(act_import_frame,
                                    text='Buscar',
                                    command=lambda: get_newsapi(get_newsapi_params(newsapi_dict))
                                    )
        act_import_bt.grid(row=6,column=1,sticky='nsew',padx=5,pady=5)

        act_frame.add(act_import_frame, text = 'Parâmetros da API')

        #---------------------------------------------------------------
        # IMPORT RESULTS
        #---------------------------------------------------------------

        act_results_frame = ttk.Frame(act_frame)
        act_results_frame.grid(row=0,column=0,sticky='nsew')

        #Results

        act_results_legend = ttk.Label(act_results_frame,text='Resultados:')
        act_results_legend.grid(row=0,column=0,sticky='nsew',padx=5,pady=5)

        act_results = ttk.Treeview(act_results_frame,columns=('title','description'))
        act_results.heading('#0',text='ID')
        act_results.heading('title',text='Título')
        act_results.heading('description',text='Descrição')
        act_results.column('#0',width=25)
        act_results.column('title',width=400)
        act_results.column('description',width=400)
        act_results.grid(row=1,column=0,sticky='nsew',padx=5,pady=5)

        act_frame.add(act_results_frame, text = 'Resultados')

        act_results_scroll = ttk.Scrollbar(act_results_frame,orient='vertical',command=act_results.yview)
        act_results_scroll.grid(row=1,column=1,sticky='nsew')
        act_results['yscroll'] = act_results_scroll.set

        act_results.bind('<Double-1>',
                         lambda event: wb.open(act_results.item(act_results.selection())['values'][2]))

        news_results = get_newsapi_results()
        for id,result in enumerate(news_results):
            act_results.insert('','end',text=id,values=result[0:2])
        
        act_results.bind('<B1-Motion>', partial(motion_handler, act_results))
        motion_handler(act_results, None)   # Perform initial wrapping

        
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