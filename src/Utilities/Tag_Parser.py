# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 13:59:18 2022

@author: valter.gonzaga
"""

def parse_string(s:str):

    
    tag_data = []
    
    s_len = len(s)
    tag_flag = 0 #Indica se o algoritimo encontra-se em uma tag
    tag_code = ''
    
    for idx,char in enumerate([c for c in s]):
        
        
        trail = s[idx-3:idx] # Three last characters in the text
        
        
        idx_max = (idx + 4 if idx+4 <= s_len
                   else s_len)
        
        lead = s[idx+1:idx_max]
        
        
        if trail[1:3] == '{{' and trail[0] != '\\': #checks for oppening brackets
            tag_flag = 1 # text aftwards is treated as tag code
            
            init_pos = idx-2
        
        if tag_flag == 1:
            
            tag_code += char
            
            try:
                if char != '\\' and lead[0:2] == '}}': #checks for closing brackets
                    tag_flag = 0 # text is treated as normal text aftwards
                    end_pos = idx+2
                    
                    code_split = tag_code.split(' ')
                    
                    tag_id = code_split[0]
                    tag_args = code_split[1:]
                    
                    tag_data.append({'idx_0': init_pos,
                                     'idx_f': end_pos,
                                     'id': tag_id,
                                     'args': tag_args})
                    
                    tag_code = ''
                    
                    
            except:
                #String has ended before a closing brackets could be found
                raise SyntaxError('EOF after opening {{')
    
    return tag_data
        

                


          
test_s = """
Heed the warning the sound of the drums
Set the {{I www.imageprovider.com\cool-praph}} beacons on fire for them all
Call to arms who remains, far and wide
"""

tag_data = parse_string(test_s)
