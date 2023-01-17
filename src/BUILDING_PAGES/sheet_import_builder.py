# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:43:05 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
from cfg import news,format_dict
import Utilities.util as util
from SUPPORT_PAGES.Preview_Window import pvWidget

class card_builder(tk.Frame):
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
            nonlocal banner_url
            nonlocal footer_url
            filename = tk.filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File")
            if option == 'banner':
                banner_url.set(filename)
            else:
                footer_url.set(filename)
        
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
        

        #-------
        #-Título
        #-------
        act_title_frame = ttk.Frame(act_frame,width=act_frame.winfo_width())
        act_title_frame.grid(padx=15,pady=15,sticky='nsew')  
        
        act_title_lbl = ttk.Label(act_title_frame,text='TÍTULO',font='Times')
        act_title_lbl.grid(row=1,column=0,padx=10,pady=10,sticky='ws')
        
        title_var = tk.StringVar()
        title_var.set('')
        act_title = ttk.Entry(act_title_frame,textvariable=title_var)
        act_title.grid(row=2,column=0,sticky='ew',padx=10,pady=10)
        
        act_header_lbl = ttk.Label(act_title_frame,text='CABEÇALHO',font='Times')
        act_header_lbl.grid(row=3,column=0,padx=10,pady=10,sticky='ws')
        
        header_var = tk.StringVar()
        header_var.set('')
        act_header = ttk.Entry(act_title_frame,textvariable=header_var)
        act_header.grid(row=4,column=0,sticky='ew',padx=10,pady=10)
        
        act_title_frame.columnconfigure([0],weight=1)
        
        #------
        #-Corpo
        #------
        act_body_frame = ttk.Frame(act_frame,width=act_frame.winfo_width())
        act_body_frame.grid(padx=15,pady=15,sticky='nsew')
        
        
        act_body_lbl = ttk.Label(act_body_frame,text='CORPO',font='Times')
        act_body_lbl.grid(row=0,column=0,sticky='ws')
        
        bodyvar_frame = ttk.Frame(act_body_frame)
        bodyvar_frame.grid(row=1,column=0,sticky='nsew')
        
        act_body_scroll = ttk.Scrollbar(bodyvar_frame,
                                        orient=tk.VERTICAL
                                        )
        act_body_scroll.pack(side=tk.RIGHT,fill=tk.Y,padx=(0,10),pady=10)
        
        act_body = tk.Text(bodyvar_frame,
                           height=30,
                           yscrollcommand=act_body_scroll.set
                           )
        act_body.pack(side=tk.LEFT,fill=tk.BOTH,padx=(10,0),pady=10)
        
        act_body_frame.columnconfigure([0,1],weight=1)

        act_body_scroll.configure(command=act_body.yview)
        
        #-------
        #-Banner
        #-------
        act_banner_frame = ttk.Frame(act_frame,width=act_frame.winfo_width())
        act_banner_frame.grid(padx=15,pady=15,sticky='nsew')
        
        
        #--label
        act_banner_lbl = ttk.Label(act_banner_frame,text='BANNER',font='Times')
        act_banner_lbl.grid(row=0,column=0,padx=10,pady=10,sticky='ws')
        
        #--modos
        act_banner_modeframe = ttk.Frame(act_banner_frame)
        act_banner_modeframe.grid(row=1,column=0,padx=10,pady=10,sticky='ew')
        
        act_banner_modelbl = ttk.Label(act_banner_modeframe,text='Tipo de Endereço:',font='Times')
        act_banner_modelbl.grid(row=0,column=0,sticky='w')
        
        
        banner_mode = tk.StringVar()
        banner_mode.set('Caminho')
        
        act_banner_modeurl = ttk.Radiobutton(act_banner_modeframe,text='URL',
                                            var=banner_mode,value='url')
        act_banner_modeurl.grid(row=0,column=1,sticky='ew')
        
        act_banner_modepath = ttk.Radiobutton(act_banner_modeframe,text='Caminho',
                                             var=banner_mode,value='path')
        act_banner_modepath.grid(row=0,column=2,sticky='ew')
        
        act_banner_modeframe.rowconfigure([0],weight=1)
        act_banner_modeframe.columnconfigure([0,1,2],weight=1)
        
        #--imagem
        banner_url = tk.StringVar()
        banner_url.set('')
        act_banner = ttk.Entry(act_banner_frame,textvariable=banner_url)
        act_banner.grid(row=2,column=0,sticky='ew',padx=10,pady=(2,5))
        
        act_banner_search = ttk.Button(act_banner_modeframe,
                                       text='Buscar Imagem',
                                       command=browseFiles
                                       )
        act_banner_search.grid(row=1,column=2,padx=5,pady=2.5,sticky='w')
        
        #--Legenda
        
        bn_cpt_var = tk.StringVar()
        bn_cpt_var.set('')
        
        banner_cpt_frame = ttk.Frame(act_banner_frame)
        banner_cpt_frame.grid(row=3,column=0,padx=10,pady=10,sticky='nsew')
        banner_cpt_frame.rowconfigure([0],weight=1)
        banner_cpt_frame.columnconfigure([0],weight=1)
        banner_cpt_frame.columnconfigure([1],weight=2)
        
        banner_cpt_label = ttk.Label(banner_cpt_frame,text='Legenda:',font='Times')
        banner_cpt_label.grid(row=0,column=0,sticky='w')
        
        banner_caption = ttk.Entry(banner_cpt_frame,textvariable=bn_cpt_var)
        banner_caption.grid(row=0,column=1,sticky='ew')
        
        
        #--hyperlink
        banner_hyperlink_frame= ttk.Frame(act_banner_frame)
        banner_hyperlink_frame.grid(row=4,column=0,sticky='ew',padx=10,pady=10)   
        banner_hyperlink_frame.rowconfigure([0],weight=1)
        banner_hyperlink_frame.columnconfigure([0],weight=1)
        banner_hyperlink_frame.columnconfigure([1],weight=2)
        
        banner_link_label = ttk.Label(banner_hyperlink_frame,text='Hyperlink:',font='Times')
        banner_link_label.grid(row=0,column=0,sticky='w',padx=0,pady=0)
        banner_link = tk.StringVar()
        banner_link.set('')
        
        act_banner_link = ttk.Entry(banner_hyperlink_frame,textvariable=banner_link)
        act_banner_link.grid(row=0,column=1,sticky='ew',padx=0,pady=0)        
        
        act_banner_frame.columnconfigure([0],weight=1)
        
        #-------
        #-footer
        #-------
        act_footer_frame = ttk.Frame(act_frame,width=act_frame.winfo_width())
        act_footer_frame.grid(padx=15,pady=15,sticky='nsew')
        
        
        act_footer_lbl = ttk.Label(act_footer_frame,text='RODAPÉ',font='Times')
        act_footer_lbl.grid(row=0,column=0,sticky='ws')
        
        
        #--modos
        act_footer_modeframe = ttk.Frame(act_footer_frame)
        act_footer_modeframe.grid(row=1,column=0,padx=10,pady=10,sticky='ew')
        
        act_footer_modelbl = ttk.Label(act_footer_modeframe,text='Tipo de Endereço:',font='Times')
        act_footer_modelbl.grid(row=0,column=0,sticky='w')
        
        
        footer_mode = tk.StringVar()
        footer_mode.set('Texto')
        
        act_footer_modeurl = ttk.Radiobutton(act_footer_modeframe,text='URL',
                                            var=footer_mode,value='url')
        act_footer_modeurl.grid(row=0,column=1,sticky='ew')
        
        act_footer_modepath = ttk.Radiobutton(act_footer_modeframe,text='Caminho',
                                             var=footer_mode,value='path')
        act_footer_modepath.grid(row=0,column=2,sticky='ew')
        
        act_footer_modepath = ttk.Radiobutton(act_footer_modeframe,text='Texto',
                                             var=footer_mode,value='text')
        act_footer_modepath.grid(row=0,column=3,sticky='ew')
        
        act_footer_modeframe.rowconfigure([0],weight=1)
        act_footer_modeframe.columnconfigure([0,1,2,3],weight=1)
        
        
        #--conteúdo
        footer_url = tk.StringVar()
        footer_url.set('')
        act_footer = ttk.Entry(act_footer_frame,textvariable=footer_url)
        act_footer.grid(row=2,column=0,sticky='ew',padx=5,pady=5)
        
        act_footer_search = ttk.Button(act_footer_modeframe,
                                       text='Buscar Imagem',
                                       command= lambda: browseFiles('footer'))
        act_footer_search.grid(row=1,column=2,padx=5,pady=2.5,sticky='w')        
        
        #--Legenda
        
        ft_cpt_var = tk.StringVar()
        ft_cpt_var.set('')
        
        footer_cpt_frame = ttk.Frame(act_footer_frame)
        footer_cpt_frame.grid(row=3,column=0,padx=10,pady=10,sticky='nsew')
        footer_cpt_frame.rowconfigure([0],weight=1)
        footer_cpt_frame.columnconfigure([0],weight=1)
        footer_cpt_frame.columnconfigure([1],weight=2)
        
        footer_cpt_label = ttk.Label(footer_cpt_frame,text='Legenda:',font='Times')
        footer_cpt_label.grid(row=0,column=0,sticky='w',padx=(5,0),pady=5)
        
        footer_caption = ttk.Entry(footer_cpt_frame,textvariable=ft_cpt_var)
        footer_caption.grid(row=0,column=1,sticky='ew',padx=(5,0),pady=5)
        
        #--hyperlink
        footer_hyperlink_frame= ttk.Frame(act_footer_frame)
        footer_hyperlink_frame.grid(row=4,column=0,sticky='ew',padx=10,pady=10)   
        footer_hyperlink_frame.rowconfigure([0],weight=1)
        footer_hyperlink_frame.columnconfigure([0],weight=1)
        footer_hyperlink_frame.columnconfigure([1],weight=2)
        
        footer_link_label = ttk.Label(footer_hyperlink_frame,text='Hyperlink (Apenas para Imagens):',font='Times')
        footer_link_label.grid(row=0,column=0,sticky='w',padx=0,pady=0)
        footer_link = tk.StringVar()
        footer_link.set('')
        
        act_footer_link = ttk.Entry(footer_hyperlink_frame,textvariable=footer_link)
        act_footer_link.grid(row=0,column=1,sticky='ew',padx=0,pady=0)        
        
        act_footer_frame.columnconfigure([0],weight=1)
        #----------------------------------------------------------------------

        act_frame.add(act_title_frame, text='Título e Cabeçalho')
        act_frame.add(act_body_frame, text = 'Corpo')
        act_frame.add(act_banner_frame, text = 'Banner')
        act_frame.add(act_footer_frame, text = 'Rodapé')
        
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