import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
from soccerplots.radar_chart import Radar
import streamlit as st



font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))





def get_player_camparision_radar(df,player_1_name, player_2_name):
    
    """
    Function to create a two player radar, based on the soccerplots
    library.
    """

    
    list_for_percentiles = [ 'xA_p90',
                             'opxG_p90',
                             'Dribbling vincenti_p90',
                   
                   
                             'Third pass vincenti_p90',
                             'Passaggi Chiave_p90',
                             'xT_p90',
                           
                        
                   
                               'PSV-99_p90',
                 
                             'HI Distance_p90',
                               'Count Sprint_p90',
                   
                            'Duelli vinti_p90',
                             'Duelli tackle vinti_p90',
                             'Interventi decisivi +_p90'
                        
                        ]
    for metric in list_for_percentiles:
        df[metric+'_perc'] = df[metric].rank(pct=True)
    
    percentiles = [ 'xA_p90_perc',
                             'opxG_p90_perc',
                             'Dribbling vincenti_p90_perc',
                          
                   
                             'Third pass vincenti_p90_perc',
                             'Passaggi Chiave_p90_perc',
                             'xT_p90_perc',
                           
                        
                   
                               'PSV-99_p90_perc',
                           
                             'HI Distance_p90_perc',
                               'Count Sprint_p90_perc',
                   
                            'Duelli vinti_p90_perc',
                             'Duelli tackle vinti_p90_perc',
                             'Interventi decisivi +_p90_perc',
                            
                        ]
    ## Select only the players we wish to compare
    lst_players = [player_1_name, player_2_name]
    
    
    ## Filter DataFrame to only have the two players of interest
    
    ### Player 1 
    df_radar_player_1 = df[df['full_name'] == player_1_name]
    
    ### Player 2 
    df_radar_player_2 = df[df['full_name'] == player_2_name]
    
    ### Union two DataFrames together
    df_radar = pd.concat([df_radar_player_1, df_radar_player_2])
    
    
    info = ['full_name']
    
    ## Select only columns of interest for radar
    df_radar = df_radar[info + percentiles]

    
    df_radar.columns=['player_name',
                        'Expected Assists (xA)',
                      'open play xG ',
                      'Dribbling Win%',
                      'Key passes',
                        'Expected Threat',
                      'xOVA',
                      'PSV-99 (velocity)',
                       'HI Distance',
                   'Count Sprint',
                    'Aerial Win%',
                      'Tackle Win%',
                        'Decisive Int.',
                       ]
    
    ## Reset index
    df_radar = df_radar.reset_index(drop=True)

    
    ## Radar visualisation
    
    ### Get parameters
    params = list(df_radar.columns)
    params = params[1:]
    
    ### Add ranges to list of tuple pairs
    ranges = []
    a_values = []
    b_values = []
    
    ###
    for x in params:
        a = min(df_radar[params][x])
        a = a - (a*.25)

        b = max(df_radar[params][x])
        b = b + (b*.25)

        ranges.append((a, b))

    ###
    for x in range(len(df_radar['player_name'])):
        if df_radar['player_name'][x] == player_1_name:
            a_values = df_radar.iloc[x].values.tolist()
        if df_radar['player_name'][x] == player_2_name:
            b_values = df_radar.iloc[x].values.tolist()
    
    ###
    a_values = a_values[1:]
    b_values = b_values[1:]

    ###
    values = [a_values, b_values]
    season= '2020/2021'
    ###
    title = dict(title_name = player_1_name,
                 title_color = '#B6282F',
                 subtitle_name = season,
                 subtitle_color = 'black',
                 title_name_2 = player_2_name,
                 title_color_2 = '#344D94',
                 subtitle_name_2 = season,
                 subtitle_color_2 = 'black',
                 title_fontsize = 16,
                 subtitle_fontsize=13
                )


    ### Define fonts and colours
    background='#f7f7f7'    #'#313233'
    mpl.rcParams.update(mpl.rcParamsDefault)
    
    
     ### End note
    endnote = 'player comparision'
    ###
    radar = Radar()

    ### Create figure
    fig, ax = radar.plot_radar(ranges=ranges,
                               params=params,
                               values=values,
                               radar_color=['#B6282F', '#344D94'],
                               alphas=[0.5, 0.5],
                               title=title,
                               endnote=endnote,
                               compare=True,
                               image='data/img/logos/Italian-Serie-A-logo-1.png', image_coord=[0.442, 0.805, 0.14, 0.1])
                              
    
   
    plt.show()
    
    
    
    
    
    

def plot_player_pyPizza(df,player):
    
    
    #df_radar = df[df['full_name'] == player]
    
    list_for_percentiles = ['PSV-99_p90',
                            'M/min_p90',
                            'HI Distance_p90',
                            'Count Sprint_p90',
                            'Duelli vinti_p90',
                            'Duelli tackle vinti_p90',
                            'Interventi decisivi +_p90',
                            'Falli fatti_p90',
                            'xA_p90',
                            'opxG_p90',
                            'Dribbling vincenti_p90',
                            'opgoals_p90',
                            'Third pass vincenti_p90',
                            'Passaggi Chiave_p90',
                            'xT_p90',
                            'xOVA_p90']
    
    
    list_for_percentiles = [ 'xA_p90',
                             'opxG_p90',
                             'Dribbling vincenti_p90',
                             'opgoals_p90',
                   
                             'Third pass vincenti_p90',
                             'Passaggi Chiave_p90',
                             'xT_p90',
                             'xOVA_p90',
                        
                   
                               'PSV-99_p90',
                             'M/min_p90',
                             'HI Distance_p90',
                               'Count Sprint_p90',
                   
                            'Duelli vinti_p90',
                             'Duelli tackle vinti_p90',
                             'Interventi decisivi +_p90',
                             'Falli fatti_p90'
                        ]
    for metric in list_for_percentiles:
        df[metric+'_perc'] = df[metric].rank(pct=True)
    
    percentiles = [ 'xA_p90_perc',
                             'opxG_p90_perc',
                             'Dribbling vincenti_p90_perc',
                             'opgoals_p90_perc',
                   
                             'Third pass vincenti_p90_perc',
                             'Passaggi Chiave_p90_perc',
                             'xT_p90_perc',
                             'xOVA_p90_perc',
                        
                   
                               'PSV-99_p90_perc',
                             'M/min_p90_perc',
                             'HI Distance_p90_perc',
                               'Count Sprint_p90_perc',
                   
                            'Duelli vinti_p90_perc',
                             'Duelli tackle vinti_p90_perc',
                             'Interventi decisivi +_p90_perc',
                             'Falli fatti_p90_perc'
                        ]
 
    df_radar = df[df['full_name'] == player]
    df_radar = df_radar[percentiles]
    df_radar = df_radar.reset_index(drop=True)
  


    df_radar.columns=['Expected Assists (xA)',
                      'open play xG ',
                      'Dribbling Win%',
                      'open play goals',
                        
                      'Third pass win%',
                      'Key passes',
                        'Expected Threat',
                      'xOVA',
                     
                        
                      'PSV-99 (velocity)',
                      'Distance/min',
                             'HI Distance',
                   'Count Sprint',
                        
                    'Aerial Win%',
                      'Tackle Win%',
                        'Decisive Int.',
                        'Fouls']

    ## Radar visualisation

    ### Get parameters
    params = list(df_radar.columns)
    values = df_radar.iloc[0].values.tolist()

    values = [int(i * 100) for i in values]
    


    # color for the slices and text
    slice_colors = ["#1A78CF"] * 4 + ["#FF9300"] * 4 + ["#D70232"] * 4 + ["green"] *4
    text_colors = ["#F2F2F2"] * 4 + ["#F2F2F2"] * 4 + ["#F2F2F2"] * 4 + ["#F2F2F2"] * 4

    # instantiate PyPizza class
    baker = PyPizza(
        params=params,                  # list of parameters
        background_color="#FFFFFF",     # background color
        straight_line_color="#000000",  # color for straight lines
        straight_line_lw=1,             # linewidth for straight lines
        last_circle_color="#000000",    # color for last line
        last_circle_lw=1,               # linewidth of last circle
        other_circle_lw=0,              # linewidth for other circles
        inner_circle_size=20            # size of inner circle
    )

    # plot pizza
    fig, ax = baker.make_pizza(
        values,                          # list of values
        figsize=(8, 8.5),                # adjust the figsize according to your need
        color_blank_space="same",        # use the same color to fill blank space
        slice_colors=slice_colors,       # color for individual slices
        value_colors=text_colors,        # color for the value-text
        value_bck_colors=slice_colors,   # color for the blank spaces
        blank_alpha=0.6,                 # alpha for blank-space colors
        kwargs_slices=dict(
            edgecolor="#000000", zorder=2, linewidth=1
        ),                               # values to be used when plotting slices
        kwargs_params=dict(
            color="#F2F2F2", fontsize=11,
            fontproperties=font_normal.prop, va="center"
        ),                               # values to be used when adding parameter labels
        kwargs_values=dict(
            color="#000000", fontsize=11,
            fontproperties=font_normal.prop, zorder=3,
            bbox=dict(
                edgecolor="#000000", facecolor="cornflowerblue",
                boxstyle="round,pad=0.2", lw=1
            )
        )                                # values to be used when adding parameter-values labels
    )



    # add subtitle
    fig.text(
        0.515, 0.965,
        "Percentile Rank vs Serie A | Season 2020-21",
        size=13,
        ha="center", fontproperties=font_bold.prop, color="#F2F2F2"
    )


    # add text
    fig.text(
        0.21, 0.93, "Attacking          Possession         Defending          Phisycal", size=14,
        fontproperties=font_bold.prop, color="#F2F2F2"
    )

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.17, 0.9225), 0.025, 0.025, fill=True, color="#1a78cf",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.332, 0.9225), 0.025, 0.025, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.512, 0.9225), 0.025, 0.025, fill=True, color="green",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.69, 0.9225), 0.025, 0.025, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])


    plt.show()