# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 15:43:16 2022

@author: valter.gonzaga
"""

import PyInstaller.__main__

PyInstaller.__main__.run(['InfoConstructor.py',
                          '--noconsole',
                          '--noconfirm',
                          '--hidden-import=babel.numbers',
                          '--hidden-import=Tkhtml',
                          '--hidden-import=Tkcalendar',
                          '--collect-all=tkinterweb',
                          '--icon=Media/icon.ico',
                          ]
                         )