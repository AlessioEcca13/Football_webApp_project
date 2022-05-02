from highlight_text import HighlightText
from pywaffle import Waffle
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.image as image
import matplotlib.font_manager
import streamlit as st


font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))





def waffle_plot(df, lista_attaccanti):
    df['goal'] = (df.outcome == 'goal').astype(int)

    df_prova = df[(df['goal']==1)]
    df_prova = df_prova[['player','goal','body_part']]
    df_Waffle = df_prova.groupby(['body_part','player']).sum().reset_index().pivot(index='body_part', columns='player', values='goal').fillna(0)

    df_test = df_Waffle[lista_attaccanti].copy()
    my_list = df_test.columns.values.tolist()
    
        #Different colors so we don't have to type them in every time
    background = "#313332"
    text_color = 'w'
    primary = 'red'
    secondary = 'lightblue'
    mpl.rcParams['xtick.color'] = text_color
    mpl.rcParams['ytick.color'] = text_color
    
    fig = plt.figure(
        FigureClass = Waffle,
        plots={
            331: {                              #refer matplotlib subplot grids, '331' means 3 x 3 grid, first subplot
                'values': df_test.iloc[:,0],
                'title': {
                    'label': my_list[0],
                    'color': 'white'
                },
                },
            332: {                             
                'values': df_test.iloc[:,1],
                'title': {
                    'label': my_list[1],
                    'color': 'white'
                },
                },
            333: {                           #Line 20   
                'values': df_test.iloc[:,2],
                'title': {
                    'label': my_list[2],
                    'color': 'white'
                }
                },
            334:{                              
                'values': df_test.iloc[:,3],
                'title': {
                    'label': my_list[3],
                    'color': 'white'
                },
                }
            ,
            335: {                              
                'values': df_test.iloc[:,4],
                'title': {
                    'label': my_list[4],
                    'color': 'white'
                },
                },
            336: {
                'values': df_test.iloc[:,5],                              
                'title': {
                    'label': my_list[5],
                    'color': 'white'
                },
                },
            337: {                              
                'values': df_test.iloc[:,6],
                'title': {
                    'label': my_list[6],
                    'color': 'white'
                },
                },
            338: {                             
                'values': df_test.iloc[:,7],
                'title': {
                    'label': my_list[7],
                    'color': 'white'
                    ''
                },
                },
            339: {
                'values': df_test.iloc[:,8],
                'title': {
                    'label': my_list[8],
                    'color': 'white'
                },
                },
        },
        rows=5,
        figsize=(11, 9),
        rounding_rule='floor',
        colors=("#a3a3c2", "#75a3a3", "#ff4d4d",'#00cc99'),
        facecolor=background
    )


    #Create the text and highlight the different points
    HighlightText(
                    x=-3,y=4,
                    s = "Scorer comparison in Serie A + how they scored their goals \n<HEAD>, <LEFT>, <RIGHT>, + <OTHER>",
                    fontfamily='Andale Mono',
                    fontsize=25,
                    color=text_color,
                    highlight_textprops=[{"color": '#a3a3c2'},{"color": '#75a3a3'},{"color": '#00cc99'},{"color": '#ff4d4d'}])
                    #highlight_colors=['#a3a3c2','#75a3a3','#ff4d4d','#00cc99'])
    fig.patch.set_facecolor(background)


def waffle_plot_one_player(df, lista_attaccanti):
    df['goal'] = (df.outcome == 'goal').astype(int)

    df_prova = df[(df['goal']==1)]
    df_prova = df_prova[['player','goal','body_part']]
    df_Waffle = df_prova.groupby(['body_part','player']).sum().reset_index().pivot(index='body_part', columns='player', values='goal').fillna(0)

    df_test = df_Waffle[lista_attaccanti].copy()
    #my_list = df_test.columns.values.tolist()
    
        #Different colors so we don't have to type them in every time
    background = "#313332"
    text_color = 'w'
    primary = 'red'
    secondary = 'lightblue'
    mpl.rcParams['xtick.color'] = text_color
    mpl.rcParams['ytick.color'] = text_color
    
    fig = plt.figure(
        FigureClass = Waffle,
        plots={
            331: {                              #refer matplotlib subplot grids, '331' means 3 x 3 grid, first subplot
                'values': df_test.iloc[:,0],
              #  'title': {
              #      'label': my_list[0],
               #     'color': 'white'
               # },
                }
        },
        rows=5,
        figsize=(11, 9),
        rounding_rule='floor',
        colors=("#a3a3c2", "#75a3a3", "#ff4d4d",'#00cc99'),
        facecolor=background
    )


    #Create the text and highlight the different points
    HighlightText(
                    x=-0.1,y=1.35,
                    s = "SCORES\n<HEAD>, <LEFT>, <RIGHT>, + <OTHER>\n",
                    fontfamily='Andale Mono',
                    fontsize=25,
                    color=text_color,
                    highlight_textprops=[{"color": '#a3a3c2'},{"color": '#75a3a3'},{"color": '#00cc99'},{"color": '#ff4d4d'}])
    
     ### Add StatsBomb 360 logo
    ax3 = fig.add_axes([0.3575, 0.62, 0.20, 0.20])
    ax3.axis('off')
    img = image.imread('data/img/logos/Italian-Serie-A-logo-1.png')
    ax3.imshow(img)
    
    fig.patch.set_facecolor(background)