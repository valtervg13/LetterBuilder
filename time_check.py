# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 15:38:57 2022

@author: valter.gonzaga
"""

import datetime as dt
import copy

class time_check():
    def __init__(self):
        return
    
    def week_bounds(reference,
                    weekday:int):
        for i in range(-8,7):
            date_delta =  dt.timedelta(abs(i))
            if i < 0:
                day = reference - date_delta
                if day.weekday() == weekday:
                    last_weekday = day
            else:
                day = reference + date_delta
                if day.weekday() == weekday:
                    next_weekday = day
                    
        return last_weekday,next_weekday
    
    def month_bounds(reference,
                     monthday:int):
        for i in range(-32,31):
            date_delta =  dt.timedelta(abs(i))
            if i < 0:
                day = reference - date_delta
                if day.days() == monthday:
                    last_monthday = day
            else:
                day = reference + date_delta
                if day.days() == monthday:
                    next_monthday = day
                    
        return last_monthday,next_monthday    
    
    def is_between(date,
                   lower_bound,
                   upper_bound,
                   include_lower = False,
                   include_upper = True):
        
        day_displace = dt.timedelta(1)
        if include_lower == False:
            lower = lower_bound
        else:
            lower = copy.deepcopy(lower_bound)
        
        if include_upper == False:
            upper = upper_bound-day_displace
        else:
            upper = copy.deepcopy(upper_bound)
        
        
        date_check = (date <= upper and date >= lower)

        return date_check
    
    def is_later(date,
                 reference,
                 equal_istrue = True):
        
        if equal_istrue:
            return date>=reference
        else:
            return date>reference
        
    def is_earlier(date,
                   reference,
                   equal_istrue = True):
        
        if equal_istrue:
            return date<=reference
        else:
            return date<reference
        
        