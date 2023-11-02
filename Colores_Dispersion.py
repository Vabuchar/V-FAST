# -*- coding: utf-8 -*-
"""
Created on Sun Jan 22 23:20:16 2023

@author: vabuc
"""

def color_dispersion_hazard(total_num_hazard):
    if total_num_hazard <= 7:
        color_graphs = ('darkviolet','darkblue','cyan',
                        'greenyellow','yellow','orange','darkred')
    elif total_num_hazard == 8:
        color_graphs = ('darkviolet','darkblue','blue','cyan',
                        'greenyellow','yellow','orange','darkred')
    elif total_num_hazard == 9:
        color_graphs = ('darkviolet','darkblue','blue','cyan',
                        'greenyellow','yellow','orange','red','darkred')
    elif total_num_hazard == 10:
        color_graphs = ('darkviolet','darkblue','blue','cyan','aquamarine',
                        'greenyellow','yellow','orange','red','darkred')
    elif total_num_hazard == 11:
        color_graphs = ('darkviolet','darkblue','blue','dodgerblue','cyan','aquamarine',
                        'greenyellow','yellow','orange','red','darkred')
    elif  total_num_hazard == 12:
        color_graphs = ('violet','darkviolet','darkblue','blue','dodgerblue','cyan','aquamarine',
                        'greenyellow','yellow','orange','red','darkred')
    elif  total_num_hazard == 13:
        color_graphs = ('violet','darkviolet','darkblue','blue','dodgerblue','cyan','aquamarine',
                        'greenyellow','yellow','orange','orangered','red','darkred')
    elif  total_num_hazard == 14:
        color_graphs = ('violet','darkviolet','darkblue','blue','dodgerblue','cyan','aquamarine',
                        'greenyellow','yellow','orange','goldenrod','orangered','red','darkred')    
    else:
        print('Add more colors to the variable called color_graphs')
    
    return color_graphs

def graphs_many_color():
    colors_python = [
        'blue',
        'green',
        'red',
        'cyan',
        'magenta',
        'yellow',
        'black',
        'gray',
        'purple',
        'orange',
        'brown',
        'pink',
        'teal',
        'navy',
        'olive',
        'maroon',
        'lime',
        'aqua',
        'silver',
        'indigo',
        'gold',
        'violet',
        'tan',
        'coral',
        'plum',
        'orchid',
        'salmon',
        'khaki',
        'peru',
        'turquoise',
        'crimson',
        'lavender',
        'sienna',
        'thistle',
        'chartreuse',
        'aquamarine',
        'wheat',
        'lightgray',
        'aliceblue',
        'azure',
        'beige',
        'bisque',
        'blanchedalmond',
        'burlywood',
        'cadetblue',
        'chocolate',
        'cornflowerblue',
        'cornsilk',
        'darkblue',
        'darkcyan',
        'darkgoldenrod',
        'darkgray',
        'darkgreen',
        'darkkhaki',
        'darkmagenta',
        'darkolivegreen',
        'darkorange',
        'darkorchid',
        'darkred',
        'darksalmon',
        'darkseagreen',
        'darkslateblue',
        'darkslategray',
        'darkturquoise',
        'darkviolet',
        'deeppink',
        'deepskyblue',
        'dimgray',
        'dodgerblue',
        'firebrick',
        'floralwhite',
        'forestgreen',
        'gainsboro',
        'ghostwhite',
        'goldenrod',
        'greenyellow',
        'honeydew',
        'hotpink',
        'indianred',
        'ivory',
        'khaki',
        'lavenderblush',
        'lawngreen',
        'lemonchiffon',
        'lightblue',
        'lightcoral',
        'lightcyan',
        'lightgoldenrodyellow',
        'lightgreen',
        'lightpink',
        'lightsalmon',
        'lightseagreen',
        'lightskyblue',
        'lightslategray',
        'lightsteelblue',
        'lightyellow',
        'linen',
        'mediumaquamarine',
        'mediumblue',
        'mediumorchid',
        'mediumpurple',
        'mediumseagreen',
        'mediumslateblue',
        'mediumspringgreen',
        'mediumturquoise',
        'mediumvioletred',
        'midnightblue',
        'mintcream',
        'mistyrose',
        'moccasin',
        'oldlace',
        'olivedrab',
        'orangered',
        'palegoldenrod',
        'palegreen',
        'paleturquoise',
        'palevioletred',
        'papayawhip',
        'peachpuff',
        'powderblue',
        'rosybrown',
        'royalblue',
        'saddlebrown',
        'sandybrown',
        'seagreen',
        'seashell',
        'skyblue',
        'slateblue',
        'slategray']
    
    return colors_python