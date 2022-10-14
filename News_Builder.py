# -*- coding: utf-8 -*-
"""
Created on Thu Dec 23 09:06:32 2021

@author: valter.gonzaga
"""

import base64 as bs64
from urllib.request import urlopen
import random as rd


"============================ NEWS  ========================================"
#Funções
def bol2bold(boldopt): #Transforma opções denegrito em instruções HTML
    if boldopt==True:
        font_weight  = 'bold'
    else:
        font_weight  = 'normal'
        
        return font_weight

def fig2bs64(fig_path,mode):
    if mode == 'url':
        return bs64.b64encode(urlopen((fig_path)).read())
    else:
        with open(fig_path,'rb') as fig:
            return bs64.b64encode(fig.read()).decode('utf-8')

def styleBuilder(css_dict):
    style_string = ('style="'
                    +';'.join([f'{key}:{value}' for key,value in css_dict.items()])
                    +'"' )
    
    return style_string

#Parse text lines for tags and returns their type and position
def parseTags(textblock:str):
    tags = {'T':'title',
            '-':'tab',
            't':'tab',
            'I':'image'}
    
    lines = textblock.split('\n')
    for i,line in enumerate(lines):
        for j,char in enumerate(line):
            return None
    
    


#Classes
class HTML():
    
     def __init__(self,
                  text:str,
                  sectitle:str='',
                  text_css:dict={},
                  sectitle_css:dict={},
                  tab_handler:str='bullet'):
         
        """
        ============================================================================================
        DEFINIÇÕES INICIAIS
        ============================================================================================
        """
        #===============================================
        #ESTILOS
        #===============================================
        text_style = styleBuilder(text_css)
        sectitle_style = styleBuilder(sectitle_css)
        
        tab_dict={'bullet':'ul',
                  'enumerada':'ol',
                  'descrição':'dl'}
        tab_tag=tab_dict[tab_handler]
        
        
        #===============================================
        #HTML TAGS
        #===============================================
        par = (f'<p {text_style}>')
        self.par = par
        
        heading = (f'<h2 {sectitle_style}>')
        self.heading = heading
        
        html_list = (f'<{tab_tag} {text_style}>')
        self.list = html_list
        
        
        """
        ============================================================================================
        DEFINIÇÕES INICIAIS
        ============================================================================================
        """
        
        #===============================================
        #HTML
        #===============================================
        
        title2html = self.heading+sectitle+'</h2>\n'
        
        text2html = ''
        
        #Formatação em html linha-por-linha

        t = 0 #gatilho que indica quanto uma linha é parte de uma lista ou não
        textlines = text.split('\n')
        for i in range(len(textlines)):
            line = textlines[i]
            
            #'\\placeholders substituem tabulações '<tab>' para demarcar onde estavam, de modo que possam ser
            #substituidos por uma quebra de linha '\n' ao reconstruir o texto
            if line[0:5] == '<tab>' and t==0: #Checa pelo início de uma lista
                
                line = line.replace('<tab>','\\placeholder'+html_list+'\\placeholder<li>') 
                line = line + '</li>'
                
                line = '</p>' + line if i!= 0 else line
                t=1
            
            elif line[0:5] == '<tab>' and t==1 and i!=len(textlines)-1: #Checa por itens de uma lista
                line = line.replace('<tab>', '\\placeholder<li>')
                line = line+'</li>'
            
            elif line[0:5] !='<tab>' and t==1: #Checa pela linha seguinte à uma lista
                line = f'\\placeholder</{tab_tag}>\n'+line
                t=0
            
            elif line[0:5] == '<tab>' and i==len(textlines)-1: #Checa pelo caso onde a linha final é um item de lista
                line = line.replace('<tab>', '\\placeholder<li>')
                line = line+'</li>'
                line = line+f'\\placeholder</{tab_tag}>'
                t=0
            
            else: #Caso para linhas que não fazem parte de uma lista
                line = '\n'+line
                t=0
                
            
        
            #Substitui tags <I=url;x> por elementos html de imagem:
            if '<I' in line:
                img_pre,post_tag = line.split('<I')
                img_cfg,img_post = post_tag.split('>')
                if ';' in img_cfg:
                    img_url,img_wd = ''.join(img_cfg.replace(' ','').split('=')[1:]).split(';')
                else:
                    img_url = ''.join(img_cfg.replace(' ','').split('=')[1:])
                    img_wd = '100'
                
                
                line = (img_pre
                        + f'\\placeholder\t<div style="display:block;text-align:center;width:{img_wd}%">\\placeholder\t\t<img src="{img_url}" width="{img_wd}%">\\placeholder\t</div>'
                        + img_post
                        )
                
                
            text2html = text2html+line
                
        #Para adcionar as tags finais, é nescessário  checar se a linha final é uma lista.
        text2html = (par+text2html.replace('\n','</p>\n'+par)+'\n</p>' #caso não seja, finaliza-se com </p>
                     if not text2html[len(text2html)-5:len(text2html)] in  ('</ul>','</ol>','</dl>') 
                     else par+text2html.replace('\n','</p>\n'+par)) #caso seja, a última tag já se encontra fechada com o tipo apropriado de lista
        
        text2html = text2html.replace('\\placeholder','\n') #adiciona as quebras de linhas
            
        
        html_text = title2html+text2html #constrói o código html
        
        self.html_text=html_text
        return None
     


        
class Newsletter():
    def __init__(self,
                 default_header_size:int=16,
                 default_header_font:str='Times New Roman',
                 default_header_bold:bool=False,
                 default_header_color:str='black',
                 default_font:str='Times New Roman',
                 default_size:int=12,
                 default_sectitle_font:str='Times New Roman',
                 default_sectitle_size:int=13,
                 default_sectitle_bold:bool=False,
                 default_title_size:int=16,
                 default_title_font:str='Times New Roman',
                 default_title_bold:bool=False,
                 default_footer_size:int=10,
                 deafult_border_color:str='black',
                 default_border_size:str='2px',
                 default_border_radius:str='20px',
                 default_tab_handler:str='bullet',
                 default_padx:str='2',
                 default_pady:str='1',
                 max_width:int=600,
                 ):
        
        cards = []
        
        self.default_size = default_size
        self.default_header_size = default_header_size
        self.default_header_font= default_header_font
        self.default_header_bold = default_header_bold
        self.default_header_color = default_header_color
        self.default_title_size = default_title_size
        self.default_sectitle_size = default_sectitle_size
        self.default_sectitle_bold = default_sectitle_bold
        self.default_font = default_font
        self.default_title_bold = default_title_bold
        self.default_footer_size = default_footer_size
        self.default_border_size=default_border_size
        self.default_border_radius=default_border_radius    
        self.cards = cards
        self.default_padx = default_padx
        self.default_pady = default_pady
        self.max_width = max_width
        
        return None
    
    
    def reset(self):
        self.cards = []
    
    def add_card(self,card,pos='end'): 
        """
        Função para adicionar  ao gerenciador de newsletter
        
        Parameters
        ----------
        card : card 
            O objeto card a ser adicionado a lista de  da newsletter.
        
        """
        
        
        
        def insert(val,lst,idx):

            idx = idx-1
            return [lst[i] if i < idx
                    else 
                    val if i == idx
                    else
                    lst[i-1]
                    for i in range(len(lst)+1)]
        
        
        if pos in ('end','e'):
            self.cards.append(card)
            
        elif pos in ('start','strt','s'):
            self.cards = [card,*self.cards]
            
        elif pos == 'replace':
            self.cards.pop(pos)
            self.cards.insert(card,
                              self.cards,
                              pos
                              )
            
        elif type(pos)==int:
            if pos > len(self.cards):
                self.cards.append(card)
            
            else:
                
                self.cards = insert(card,
                                    self.cards,
                                    pos
                                    )
                
    def delete_card(self,pos):
        self.cards.pop(pos)
        return
            
            
    
    def build_letter(self):
        """    
        Constrói o código final em html
        
        Returns
        -------
        
        MIME_message: 
            código MIME/html para e-mail 
            
        HTML_message: 
            código HTML puro
        """
        
        """
        ======================================================================
        CÓDIGOS MIME
        ======================================================================
        """
        
        #==========================================
        #PREÂMBULO
        #==========================================
        
        preamble = """--outer_boundary
Content-Type: multipart/related;
    boundary = "inner_boundary"

--inner_boundary
Content-Type: multipart/alternative;
    boundary = "body_boundary"

--body_boundary
Content-Type: text/html;
    charset = "utf-8"
Content-Transfer-Encoding: 7bit
                    
                    """
                    
        #==========================================
        #POST-SCRIPTUM
        #==========================================
        
        #Para cada imagem base64 é nescessário uma seção no 'post-scriptum' (a seção após o HTML)
        post_scriptum = '' 
        for card_obj in self.cards:
            if card_obj.banner_cid != 'n/a' or card_obj.footer_cid != 'n/a': #Checa se o card possui imagens em base 64
                
                for cid,ext,img in [(card_obj.banner_cid,card_obj.banner_extension.lower(),card_obj.banner_image),
                                    (card_obj.footer_cid,card_obj.footer_extension.lower(),card_obj.footer_image)]:
                    
                    if cid != 'n/a': #Checa por imagem no banner e/ou no footer
                        post_mime = f"""
--inner_boundary
Content-Type: image/{ext}; name="{cid}.{ext}"
charset=utf-8
Content-Disposition: inline; filename="{cid}.{ext}"
Content-Transfer-Encoding: base64
Content-ID: <{cid}>
Content-Location: {cid}.{ext}

{img}
"""
                        post_scriptum = post_scriptum + post_mime #Adciona o código referente à imagem
        
        if post_scriptum != '':
            post_scriptum = '\n--body_boundary--\n'+post_scriptum + '\n--inner_boundary--\n--outer_boundary--'
        

        """
        ============================================================================================
        CÓDIGOS DEFINITIVOS
        ============================================================================================
        """
        
        #===============================================
        #MIME + HTML
        #===============================================
        
        MIME_message = (
"""MIME-Version: 1.0;
Content-Type: multipart/mixed;
    boundary = "outer_boundary"
                
"""
+preamble+
f"""
<!doctype html><HTML lang="pt-br">
    <HEAD> 
    <meta http-equiv="content-type"  name="viewport" content="text/html;width=device-width, initial-scale=1.0" charset="UTF-8"/>
    </head>
    
    <body>
        <table align="center" width="100%" style="width:100%;table-layout:fixed">
            <tr>
                <td></td>
                <td width="{self.max_width}">
                
"""
                +'\n<br>'.join([card.mime_text for card in self.cards])
                +"""
                </td>
                <td></td>
            </tr>
        </table>
    </body>
    </HTML>
                """
                +post_scriptum)
        
    
        #===============================================
        #HTML PURO
        #===============================================
        
        HTML_message = ("""
<!doctype html><HTML lang="pt-br">
    <HEAD>
        <meta charset="utf8">
    </HEAD>
    
    <body style="max-width:950px">    
        """
+'\n<br><br>'.join([card.html_text for card in self.cards])
+"""
    </body>
    </HTML>""")
    
    
    
        
        return MIME_message, HTML_message
                    



class card():
    """
    Classe que constrói os  em HTML que compoem o objeto Newsletter
    
    
    Parameters
    ----------
    
    newsletter : Newsletter
        Objeto Newsletter no qual o card é incorporado.
        
    
    banner : str, default = ''
        A imagem de banner localiza-se no topo do card.
    
        O conteúdo de `banner` pode ser (1) a URL da imagem hospedada online ou (2) o caminho para a imagem local.
        
        1. O e-mail utilizara a tag HTML <img source="[URL]">, de modo que as imagens serão carregadas via web para o corpo da mensagem;
        
        2. o e-mail utilizara a tag HTML  <img source="cid:[tag]">, de modo que a imagem será salva no corpoda mensagem, em formato base64, o que pode tornar o e-mail mais pesado.
        
    banner_mode : str, default = 'url'
        Indica se o conteúdo de `banner` é uma (1) URL ou (2) um caminho.
        
        1. Entrada: 'url'
        
        2. Entrada: 'path'
    
    banner_extension: str, default = 'png'
        Indica a extensão da imagem. Recomenda-se: 'png','jpg','jpeg' e 'gif'.
        
        A extensão deve ser a mesma da imagem original.
    
    banner_hyperlink : str, default = ''
        Indica a url a ser acessado ao clicar na imagem do banner.
        
    footer : str, default = ''
        Conteúdo do rodapé que localiza-se na base do card.
    
        O conteúdo de `footer` pode ser (1) a URL da imagem hospedada online ou (2) o caminho para a imagem local (3) uma string de texto.
        
        
        1. O e-mail utilizara a tag HTML <img source="[URL]">, de modo que as imagens serão carregadas via web para o corpo da mensagem;
        
        2. o e-mail utilizara a tag HTML  <img source="cid:[tag]">, de modo que a imagem será salva no corpoda mensagem, em formato base64, o que pode tornar o e-mail mais pesado.
        
        3. o rodapé será composto de texto simples centralizado.
        
    footer_mode : str, default = 'url'
        Indica se o conteúdo de `footer` é uma (1) URL, (2) um caminho (3) texto.
        
        1. Entrada: 'url';
        
        2. Entrada: 'path';
        
        3. Etntrada: 'text';
    
    footer_extension: str, default = 'png'
        Indica a extensão da imagem. Recomenda-se: 'png','jpg','jpeg' e 'gif'.
        
        A extensão deve ser a mesma da imagem original.
    
    footer_hyperlink : str, default = ''
        Indica a url a ser acessado ao clicar no conteúdo do rodapé.  
        
    footer_font: str, default = None
        Indica a família de fonte a ser inserida na tag HTML do rodapé, no campo "font-family: [`footer_font`]".
        
        Quando None, o valor padrão, `default_font`, da newsletter é utilizado.
    
    footer_size: int, default = None
        Indica o tamanhp da fonte do rodapé.
        
        Quando None, o valor padrão, `default_footer_size`, da newsletter é utilizado.
    """
    
    
    def __init__(self, newsletter,
                 header:str='',
                 header_size=None,
                 header_font=None,
                 header_bold=None,
                 header_color=None,
                 header_padx= None,
                 header_pady= None,
                 banner:str='', 
                 banner_mode:str='url',
                 banner_extension:str='png',
                 banner_hyperlink: str='',
                 banner_caption: str='',
                 banner_padx = None,
                 banner_pady = None,
                 footer:str='',
                 footer_mode:str='url',
                 footer_extension:str='png',
                 footer_hyperlink:str='',
                 footer_font = None,
                 footer_size = None,
                 footer_caption:str = '',
                 footer_padx = None,
                 footer_pady = None,
                 title:str='',  
                 title_font= None,
                 title_size = None,
                 title_bold = None,
                 sectitle_size = None,
                 sectitle_font = None,
                 sectitle_bold = None,
                 date = None,
                 body:list=[],
                 body_font = None,
                 body_size = None,
                 body_padx = None,
                 body_pady = None,
                 tab_handler=None,
                 border_color = None,
                 border_thickness = None,
                 border_corner_radius = None,
                 border_padx = None,
                 border_pady = None,
                 border_toggle = None,
                 max_width = None):

        """
        ============================================================================================
        CONFIGURAÇÕES DE ESTILO CSS
        ============================================================================================
        """
        #===============================================
        #Importação das configurações padrão do objeto Newsletter, 
        #a menos que esepcificado o contrário
        #===============================================
        
        body_font = (newsletter.default_font if body_font == None else body_font)
        body_size = (newsletter.default_size if body_size == None else body_size)
        body_padx = (newsletter.default_padx if body_padx == None else body_padx)
        body_pady = (newsletter.default_pady if body_pady == None else body_pady)
        
        tab_handler = (newsletter.default_tab_handler if tab_handler == None else tab_handler)
        
        header_size = (newsletter.default_header_size if header_size == None else header_size)
        header_font = (newsletter.default_header_font if header_font == None else header_font)
        header_bold = (newsletter.default_header_bold if header_bold == None else header_bold)
        header_color = (newsletter.default_header_color if header_color == None else header_color)
        header_padx = (newsletter.default_padx if header_padx == None else header_padx)
        header_pady = (newsletter.default_pady if header_pady == None else header_pady)
        
        banner_padx = (newsletter.default_padx if banner_padx == None else banner_padx)
        banner_pady = (newsletter.default_pady if banner_pady == None else banner_pady)
        
        title_size = (newsletter.default_title_size if title_size == None else title_size)
        title_font = (newsletter.default_title_font if title_font == None else title_font)
        title_bold = (newsletter.default_title_bold if title_bold == None else title_bold)

        
        sectitle_size = (newsletter.default_sectitle_size if sectitle_size == None else sectitle_size)
        sectitle_font = (newsletter.default_sectitle_font if sectitle_font == None else sectitle_font)
        sectitle_bold = (newsletter.default_sectitle_bold if sectitle_bold == None else sectitle_bold)
        
        footer_font = (newsletter.default_font if footer_font == None else footer_font)
        footer_size = (newsletter.default_footer_size if footer_size == None else footer_size)   
        footer_padx = (newsletter.default_padx if footer_padx == None else footer_padx)
        footer_pady = (newsletter.default_pady if footer_pady == None else footer_pady)
        
        border_color = (newsletter.default_border_color if border_color == None else border_color)
        border_thickness = (newsletter.default_border_size if border_thickness == None else border_thickness)
        border_corner_radius = (newsletter.default_border_radius if border_corner_radius == None else border_corner_radius)
        
        #===============================================
        #Dicionários de estilo CSS
        #===============================================
        
        
        border_css = {'display':'inline-block',
                      'border':f'{border_thickness} solid {border_color}',
                      'border-radius':border_corner_radius,
                      'width':'100%',
                      'max-width':max_width,
                      'height': 'auto',
                      'horizontal-align': 'center'}
        
        header_css = {'font-family':header_font,
                     'font-size':header_size,
                     'color':header_color,
                     'text-align':'left',
                     'font-weight':bol2bold(header_bold)}
        
        title_css = {'font-family':title_font,
                     'font-size':title_size,
                     'font-weight':bol2bold(title_bold)}
        
        sectitle_css = {'font-family':body_font,
                        'font-size':sectitle_size,
                        'font-weight':'bold'}
        
        body_css = {'font-family':body_font,
                    'font-size':body_size,
                    'text-align':'justify',
                    'text-justify':'inter-word'}
        
        footer_css = {'display':'inline-block',
                      'font-size': footer_size,
                      'font-family':footer_font,
                      'text-align':'center'}
        
        caption_css = {'display':'block',
                      'font-size': footer_size,
                      'font-family':footer_font,
                      'text-align':'center'}
        
        
        #===============================================
        #Larguras e Alturas
        #===============================================

        #Header
        hd_padx_list = list(map(float,header_padx.split(','))) #Separa os valores entre padding esquerdo e direito, se houverem
        hd_lcellw = hd_padx_list[0] 
        hd_rcellw = (hd_lcellw 
                     if len(hd_padx_list) == 1
                     else hd_padx_list[1]
                     )
        hd_cellw = 100-(hd_lcellw+hd_rcellw)
        
        hd_pady_list = list(map(float,header_pady.split(','))) #Separa os valores entre padding superior e inferior, se houverem
        hd_tcellh = hd_pady_list[0]

        
        #Banner
        bn_padx_list = list(map(float,banner_padx.split(','))) #Separa os valores entre padding esquerdo e direito, se houverem
        bn_lcellw = bn_padx_list[0] 
        bn_rcellw = (bn_lcellw 
                     if len(bn_padx_list) == 1
                     else bn_padx_list[1]
                     )
        bn_cellw = 100-(bn_lcellw+bn_rcellw)
        
        bn_pady_list = list(map(float,banner_pady.split(','))) #Separa os valores entre padding superior e inferior, se houverem
        bn_tcellh = bn_pady_list[0]
        bn_bcellh = (bn_tcellh
                     if len(bn_pady_list) == 1
                     else bn_pady_list[1]
                     )

        #body
        bd_padx_list = list(map(float,body_padx.split(',')))
        bd_lcellw = bd_padx_list[0]
        bd_rcellw = (bd_lcellw 
                     if len(bd_padx_list) == 1
                     else bd_padx_list[1]
                     )
        bd_cellw = 100-(bd_lcellw+bd_rcellw)
        
        bd_pady_list = list(map(float,body_pady.split(',')))


        
        #footer
        ft_padx_list = list(map(float,footer_padx.split(',')))
        ft_lcellw = ft_padx_list[0]
        ft_rcellw = (ft_lcellw 
                     if len(ft_padx_list) == 1
                     else ft_padx_list[1]
                     )
        ft_cellw = 100-(ft_lcellw+ft_rcellw)
        
        ft_pady_list = list(map(float,footer_pady.split(',')))
        ft_tcellh = ft_pady_list[0]
        ft_bcellh = (ft_tcellh 
                     if len(ft_pady_list) == 1
                     else ft_pady_list[1]
                     )
        
        
        """
        ============================================================================================
        CONSTRUÇÃO DO HTML
        ============================================================================================
        """
        
        caption_style = styleBuilder(caption_css)
        
        #===========================================================
        #HEADER
        #===========================================================
        
        header_style = styleBuilder(header_css)
        
        mime_header = (f"""

<table align="center" width="100%" style=";width:100%;table-layout:fixed">
    <tr style="width:100%;height:{hd_tcellh}%">
        <td></td>
        <td></td>
    </tr>
    <tr style="width:100%">
        <td style="width:{hd_lcellw}%"></td>
        <td style="width:{hd_cellw+hd_rcellw}%">
            <div {header_style}>
                {header}
            </div>
        </td>
    </tr>        
</table>

        """
                        if header != ''
                        else ''
                        )
        
        
        html_header = (f"""
    <div style="width:100%;padding: {hd_tcellh}% {hd_rcellw}% 0 {hd_lcellw}%">
        <div {header_style}>
            {header}
        </div>
    </div>
        """
                        if header != ''
                        else ''
                        )
        
        #===========================================================
        #BANNER
        #===========================================================

        banner_img=''
        banner_src = ''
        cid = 'n/a'
        if banner != '':
            
            if banner_mode == 'url':
                banner_src = banner
                
            elif banner_mode == 'path':
                banner_img = fig2bs64(banner,mode=banner_mode) #converte a imagem do  banner para base 64
                
                cid = rd.randint(100000, 999999)
                
                banner_src = f'cid:{cid}'
          
        banner_caption = (banner_caption
                          if banner_src != ''
                          else ''
                          )
                
        if banner_hyperlink != '':
            banner_hyperlink = f'href="{banner_hyperlink}"'
        mime_banner = (f"""

        <table align="center" width="100%" style="width:100%;table-layout:fixed">
            <tr style="width:100%;height:{bn_tcellh}%"></tr>
            <tr>
                <td style="width:{bn_lcellw}%"></td>
                <td style="width:{bn_cellw}%">
                     <a {banner_hyperlink}>
                         <img src="{banner_src}" width="100%"/>
                     </a>
                     <div {caption_style}>{banner_caption}</div>
                 </td>
                 <td style="width:{bn_rcellw}%"></td>
             </tr>
             <tr style="width:100%;height:{bn_bcellh}%"></td>
         </table>
                        """ 
                       if banner!= ''
                       else '')
        
    
        html_banner = (f"""
        <div style="width:100%;text-align:center">
                 <a {banner_hyperlink}>
                     <img style="display:block;width:{bn_cellw}%;margin-left:auto;margin-right:auto;" src="{banner_src}"  width="100%"/>
                 </a>    
                 <div {caption_style}>{banner_caption}</div>
        </div>
                       """ 
                       if banner_mode == 'url' and banner != ''
                       else f"""
        <div style="width:100%;text-align:center">
            <a {banner_hyperlink}>
                <img style="display:block;width:{bn_cellw}%;margin-left:auto;margin-right:auto;" src="data:image/{banner_extension};base64, {banner_img}" />
            </a>
            <div {caption_style}>{banner_caption}</div>
        </div>"""
                       if banner_mode == 'path' and banner != ''
                       else ''
                       )
        
        #===========================================================
        #TÍTULO
        #===========================================================
        
        title_style = styleBuilder(title_css)
        html_title = f'\n<h1 {title_style}> {title} </h1>\n'
        
        #===========================================================
        #CORPO DO TEXTO
        #===========================================================
        
        sectitle_tag = '<T>' #Indicador de que o texto em seguida é um título de seção
        body_list =[] # Armazena os pedaços de texto com indicadores de titulo de seção
        for chunk in body:
            sectitle_indicator = False
            if chunk[0:3] == sectitle_tag:
                sectitle_indicator = True #Indica que o pedaço de texto é um totulo de seção
            body_list.append((chunk,sectitle_indicator))
        
        text_string ='' #Armazena o texto a ser transformado em HTML
        sectitle ='' # Armazena o título de seção, se houver
        html_body_list = []
        for chunk in body_list:
            if chunk[1] == True and chunk[0] != sectitle: # Gera a seção anterior quando detecta um novo título de seção
                html_body_list.append(HTML(text=text_string,
                                           sectitle=sectitle,
                                           text_css=body_css,
                                           sectitle_css=sectitle_css,
                                           tab_handler=tab_handler).html_text
                                      ) #Transforma o trecho em HTMl e o salva na lista
                text_string= '' #Reseta o armazenamento
                
                sectitle = chunk[0] #Define o título de seão da seção seguinte
     
            else:
                text_string = text_string+'\n'+chunk[0] #Monta os paragrafos da seção
        
    
        html_body_list.append(HTML(text=text_string,
                                   sectitle=sectitle,
                                   text_css=body_css,
                                   sectitle_css=sectitle_css).html_text) # Gera a seção final
         

        html_body = (''
                    if body == ['']
                    else '\n\n'.join(html_body_list)
                    )#Constroi código HTML do corpo do texto
        
        mime_body =('' 
                    if html_body == ''
                    else
                    f""" 
            <table align="center" width="100%" style="width:100%;table-layout:fixed">
            <tr>
            	<td width="{bd_lcellw}%"></td>
            	<td width="{bd_cellw}%">
            
                              """ 
                             +html_title
                             +html_body
                             +"""
                             
                             
                </td>
            	<td width="{bd_rcellw}%"></td>
            </tr>
            </table>
            """)
        
        
        #===========================================================
        #FOOTER
        #===========================================================
        
        footer_img=''
        footer_src=''
        footer_cid = 'n/a'
        if footer_mode != 'text' and footer != '':
            
            if footer_mode == 'url':
                footer_src = footer
            
            elif footer_mode == 'path':
                footer_img = fig2bs64(footer,mode=footer_mode) #converte a imagem do  banner para base 64
        
                footer_cid = rd.randint(100000, 999999)
        
                footer_src = f'cid:{footer_cid}'
                
        footer_style = styleBuilder(footer_css)
        
        footer_caption = (footer_caption
                          if footer_src != ''
                          else ''
                          )
        
        if footer_hyperlink != '':
            footer_hyperlink = f'href="{footer_hyperlink}"'
            
            
        mime_footer = ('' 
                       if footer==''
                       else f"""
    <table align="center" width="100%" style="width:100%;table-layout:fixed">
        <tr style="width:100%;height:{ft_tcellh}"></tr>
        <tr style="width:{ft_cellw}%">
            <td style="width:{ft_lcellw}%"></td>
            <td style="width:{ft_cellw}%">
                <div style="text-align:center">
                <a {footer_hyperlink}>
                    <img src="{footer_src}" width="100%">
                </a>
                </div>
                <div {caption_style}>{footer_caption}</div>
            </td>
            <td style="width:{ft_rcellw}%"></td>
        </tr>
        <tr style="width:100%;height:{ft_bcellh}"></tr>
    </table>
                        """ 
                        if footer_mode != 'text'
                        else f"""
    <table align="center" width="100%" style="width:100%;table-layout:fixed">
    <tr width="100%">
        <td width="{ft_lcellw}%"></td>
        <td width={ft_cellw}%>
        <center>
            <p {footer_style}>
        """ 
                             + footer 
                             +"""
            </p>
            </center>
        </td>
        <td width="{ft_rcellw}%"></td>
    </tr>
    </table>
    """)
    
        html_footer = (f"""
   <div style="width:100%;text-align:center">
        <a {footer_hyperlink}>
            <img src={footer_src} style = "display:block;
                                            text-align:center;
                                            font-family={title_font};
                                            width:100%;
                                            max-width:50%;
                                            margin-left:auto;
                                            margin-right:auto;" >
        </a>
        <div {caption_style}> {footer_caption}</div>    
    </div>
                        """ 
                        if footer_mode == 'url'
                        else f"""
    <div style="width:100%;text-align:center">
         <a {footer_hyperlink}>
             <img style="display:block;text-align:center;font-family={title_font};max-width:80%; margin-left:auto;margin-right:auto;"  src="data:image/{footer_extension};charset:UTF-8;base64,{footer_img}">
        </a>
        <div {caption_style}>{footer_caption}</div>
    </div>
                                        """ 
                        if footer_mode == 'path'
                        else f"""
    <div width="100%" style="width:100%;padding:2%">
    <div width="100%" {footer_style}>
        """ 
                             + footer 
                             +"""
    </div>
    </div>""")
        
        #===========================================================
        #BORDA
        #===========================================================
        
        border_style = styleBuilder(border_css)

        mime_border = (f"""
    <table align="center" width="100%" {border_style}>
        <tr width="100%">
        <td width="1%"></td>
        <td width="98%"  style = "display:inline-block; height: auto">
            <div>
                """ 
                        if border_toggle==True
                        else ''
                        )
        mime_wrap = ("""
          </div>
        </td>
        <td width="1%"></td>
    </tr>
    </table>"""
                    if border_toggle==True
                    else ''
                    )
    
        html_border = (f"""
    <div width="98%" {border_style}>
                """
                        if border_toggle==True
                        else ''
                        )
        
        html_wrap = ('\n</div>'
                     if border_toggle==True
                     else '')
        
        
        
        
        """       
        ==============================================================================================
        MONTAGEM DO TEXTO
        ==============================================================================================
        """    

        #===================================================================
        #-MIME
        #===================================================================
        
        mime_text = ("""
<!--======================================/////======================================-->

<!--=================================BORDER CODE=====================================-->
                     """
                     +mime_border
                     +"""
                     
     <!--=================================HEADER CODE=====================================-->
                     """
                     +mime_header
                     +"""
                     
     <!--=================================BANNER CODE=====================================-->
     
                                  """
                     +mime_banner
                     +"""
         <!--=================================BODY CODE=====================================-->
                     """
                     +mime_body
                     +"""
            <!--=================================FOOTER CODE=====================================-->
                       """
                     +mime_footer
                     +"""
                      
    <!--=================================BORDER WRAPPING=====================================-->     
                         """
                     +mime_wrap
                     )#Constrói o MIME e HTML do card
        
        #================================================================================
        #-HTML
        #===============================================================================
        
        html_text = (html_border
                     +html_header
                     +html_banner
                     +f'<div style="padding: 0 {bd_lcellw}% 0 {bd_rcellw}%">'
                     +html_title
                     +html_body
                     +'</div>'
                     +html_footer
                     +html_wrap
                     +'\n\n\n') # Constrói HTML do card
        
        
        """
        ============================================================================================
        ORGANIZAÇÃO DOS DADOS
        ============================================================================================
        """
        #dados do cabeçalho
        self.header = header
        self.header_font = header_font
        self.header_bold = header_bold
        self.header_color = header_color
        
        #Dados do Banner
        self.banner_path = banner
        self.banner_mode = banner_mode
        self.banner_image = banner_img
        self.banner_extension = banner_extension
        self.banner_link = banner_hyperlink
        self.banner_path = footer
        self.banner_mode = footer_mode
        self.banner_cid = cid           
        
        #Dados do Título
        self.title = title
        self.title_font = title_font
        self.title_bold = title_bold
        
        #Dados do Corpo
        self.body = body
        self.body_size = body_size
        self.body_font = body_font
        
        #Dados do Rodapé
        self.footer_path = footer
        self.footer_mode = footer_mode
        self.footer_image = footer_img
        self.footer_extension = footer_extension
        self.footer_link = footer_hyperlink
        self.footer_cid = footer_cid
        
        
        #Texto em formato MIME/HTML
        self.mime_text = mime_text
        #Texto em formato HTML
        self.html_text = html_text
        
        self.info = ''
        return None
    
    def set_info(self,info):
        self.info = info
        
    def get_info(self,info):
        return self.info
    
