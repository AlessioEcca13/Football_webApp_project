import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.colors as mcolors
import streamlit as st
import matplotlib



font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))


def get_barchart_attacking(df,
                        player_name,
                        player_colour='#1B4094'
                       ):
    
    """
    Function to create a 11-metric Attacking percentile rank bar chart for 
    an individual player.
    """
    
    list_for_percentiles = ['xG_p90',
                                    'Dribbling_p90',
                                 'Dribbling vincenti_p90',
                                 
                                 'goals_p90',
                                 'xOVA_p90',
                                 'xT_p90',
                                 'xT_carry_p90',
                                 'goals_p90',
                                 'Precisione da area',
                                 'Precisione da fuori area',
                                 'opshots_p90']
    
    

    for metric in list_for_percentiles:
        df[metric+'_perc'] = df[metric].rank(pct=True)
    
    percentiles = ['xG_p90_perc',
        
                    'Dribbling_p90_perc',
                     'Dribbling vincenti_p90_perc',
                     'goals_p90_perc',
                     'xOVA_p90_perc',
                     'xT_p90_perc',
                     'xT_carry_p90_perc',
                     'goals_p90_perc',
                     'Precisione da area_perc',
                     'Precisione da fuori area_perc',
                     'opshots_p90_perc']
 
    df_player_pr = df[df['full_name'] == player_name]
    df_player_pr = df_player_pr[percentiles]
    df_player_pr = df_player_pr.reset_index(drop=True)
  


    df_player_pr.columns=['Expected goals (xG)',
                     'Dribbling',
                     'Dribbling won%',
                     'Goals',
                     'xOVA',
                     'Expected threat (xT)',
                     'xT from carries',
                     'Goals',
                     'Precisione da area',
                     'Precisione da fuori area',
                     'Open play shots']

    # Transpose DataFrame
    df_player_pr_t = df_player_pr.T

    # Reset index
    df_player_pr_t = df_player_pr_t.reset_index(drop=False)

    # Rename Columns
    df_player_pr_t.columns = ['Metric', 'PR']

      


    # Percentile Rank Bar Chart

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='white'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    # Define labels and metrics
    metric = df_player_pr_t['Metric']
    pr = df_player_pr_t['PR']

    ## Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    # Create Horizontal Bar Plot
    clist = [(0, "red"), (0.125, "red"), (0.25, "red"), (0.4, "orange"),
             (0.55, "orange"), (0.70, "green"), (1, "green")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)

    ax.barh(metric,
            pr,
            color=rvb(pr),

            #cmap = "Reds",#player_colour,
            alpha=0.95)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20, labelsize=27)

    # Add X, Y gridlines
    ax.grid(b=True,
            color='white',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((100* i.get_width()), 1)) + '%',
                 fontsize=21,
                 fontweight='regular',
                 color ='white'
                )


    # Verticle line
    ax.axvline(0.5,
               0,
               0.952,
               color='gold',
               linestyle='--',
               linewidth=3
              )



    # Convert X axis to percentages
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])


    ## Save figure
  #  plt.savefig(fig_dir + f'/{player_name}_pr.png', bbox_inches='tight', dpi=300)

    ## Show plt
    plt.tight_layout()


    plt.tight_layout()
    plt.show()
    

def get_barchart_passing(df,
                        player_name,
                        player_colour='#1B4094'
                       ):
    
    """
    Function to create a 11-metric Passing percentile rank bar chart for 
    an individual player.
    """
    
    list_for_percentiles = ['Assist Vincenti_p90',
                   'Cut Back riusciti_p90',
                   'Cut Back vincenti_p90',
                   'xA_p90',
                   'assists_p90',
                   'opxA_p90',
                   'opassists_p90',
                   'xT_pass_p90',
                   'Third pass vincenti_p90',
                   'Cross vincenti_p90',
                   'Triangolazioni fatte_p90']
    
 

    for metric in list_for_percentiles:
        df[metric+'_perc'] = df[metric].rank(pct=True)
    
    percentiles = ['Assist Vincenti_p90_perc',
                   'Cut Back riusciti_p90_perc',
                   'Cut Back vincenti_p90_perc',
                   'xA_p90_perc',
                   'assists_p90_perc',
                   'opxA_p90_perc',
                   'opassists_p90_perc',
                   'xT_pass_p90_perc',
                   'Third pass vincenti_p90_perc',
                   'Cross vincenti_p90_perc',
                   'Triangolazioni fatte_p90_perc']
 
    df_player_pr = df[df['full_name'] == player_name]
    df_player_pr = df_player_pr[percentiles]
    df_player_pr = df_player_pr.reset_index(drop=True)
  


    df_player_pr.columns=['Assist Won%',
                   'Successful Cut Back',
                   'Cut Back won%',
                   'Expected Assists (xA)',
                   'Assists',
                   'Open play xA',
                   'Open play assists',
                   'Expected Threat passes',
                   'Third pass',
                   'Winning crosses',
                   'Triangulations']

    # Transpose DataFrame
    df_player_pr_t = df_player_pr.T

    # Reset index
    df_player_pr_t = df_player_pr_t.reset_index(drop=False)

    # Rename Columns
    df_player_pr_t.columns = ['Metric', 'PR']

      


    # Percentile Rank Bar Chart

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='white'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    # Define labels and metrics
    metric = df_player_pr_t['Metric']
    pr = df_player_pr_t['PR']

    ## Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    # Create Horizontal Bar Plot
    clist = [(0, "red"), (0.125, "red"), (0.25, "red"), (0.4, "orange"),
             (0.55, "orange"), (0.70, "green"), (1, "green")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)

    ax.barh(metric,
            pr,
            color=rvb(pr),
            #cmap = "Reds",#player_colour,
            alpha=0.95)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20, labelsize=27)

    # Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((100* i.get_width()), 1)) + '%',
                 fontsize=22,
                 fontweight='regular',
                 color ='white'
                )


    # Verticle line
    ax.axvline(0.5,
               0,
               0.952,
               color='gold',
               linestyle='--',
               linewidth=3
              )



    # Convert X axis to percentages
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])

    ## Save figure
  #  plt.savefig(fig_dir + f'/{player_name}_pr.png', bbox_inches='tight', dpi=300)

    ## Show plt
    plt.tight_layout()
    plt.show()
    

def get_barchart_defending(df,
                        player_name,
                        player_colour='#1B4094'
                       ):
    
    """
    Function to create a 11-metric Attacking percentile rank bar chart for 
    an individual player.
    """
    
    list_for_percentiles = ['Duelli_p90',
                             'Duelli di gioco_p90',
                             'Duelli vinti_p90',
                             'Duelli aerei_p90',
                             'Duelli aerei vinti_p90',
                             'Duelli tackle_p90',
                             'Duelli tackle vinti_p90',
                             'Recupera palla_p90',
                             'Dribbling perdenti subiti_p90',
                                              'Interventi decisivi +_p90',
                             'Falli fatti_p90']
    
 

    for metric in list_for_percentiles:
        df[metric+'_perc'] = df[metric].rank(pct=True)
    
    percentiles = ['Duelli_p90_perc',
                             'Duelli di gioco_p90_perc',
                             'Duelli vinti_p90_perc',
                             'Duelli aerei_p90_perc',
                             'Duelli aerei vinti_p90_perc',
                             'Duelli tackle_p90_perc',
                             'Duelli tackle vinti_p90_perc',
                             'Recupera palla_p90_perc',
                             'Dribbling perdenti subiti_p90_perc',
                                              'Interventi decisivi +_p90_perc',
                             'Falli fatti_p90_perc']
 
    df_player_pr = df[df['full_name'] == player_name]
    df_player_pr = df_player_pr[percentiles]
    df_player_pr = df_player_pr.reset_index(drop=True)
  


    df_player_pr.columns=['Duels',
                             'Open play duels ',
                             'Duels won%',
                             'Aerial duels',
                             'Aerial duels won%',
                             'Tackle',
                             'Tackle won%',
                             'Ball recovery',
                             'Dribble stopped',
                                              'Decisive Interventions',
                             'Fouls']

    # Transpose DataFrame
    df_player_pr_t = df_player_pr.T

    # Reset index
    df_player_pr_t = df_player_pr_t.reset_index(drop=False)

    # Rename Columns
    df_player_pr_t.columns = ['Metric', 'PR']

      


    # Percentile Rank Bar Chart

    ## Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    #background='#f7f7f7'    #'#313233'
    title_colour='black'
    text_colour='white'
   # mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})

    # Define labels and metrics
    metric = df_player_pr_t['Metric']
    pr = df_player_pr_t['PR']

    ## Create figure 
    fig, ax = plt.subplots(figsize =(16, 16))
    fig.set_facecolor(color=None)
    ax.patch.set_facecolor(color=None)

    # Create Horizontal Bar Plot
    clist = [(0, "red"), (0.125, "red"), (0.25, "red"), (0.4, "orange"),
             (0.55, "orange"), (0.70, "green"), (1, "green")]
    rvb = mcolors.LinearSegmentedColormap.from_list("", clist)

    ax.barh(metric,
            pr,
            color=rvb(pr),
            #cmap = "Reds",#player_colour,
            alpha=0.95)

    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)

    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20, labelsize=27)

    # Add X, Y gridlines
    ax.grid(b=True,
            color='white',
            linestyle='-.',
            linewidth=0.5,
            alpha=0
           )

    # Show top values
    ax.invert_yaxis()

    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.015, i.get_y()+0.4,
                 str(round((100* i.get_width()), 1)) + '%',
                 fontsize=22,
                 fontweight='regular',
                 color ='white'
                )



    # Verticle line
    ax.axvline(0.5,
               0,
               0.952,
               color='gold',
               linestyle='--',
               linewidth=3
              )



    # Convert X axis to percentages
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:,.0%}'.format(x) for x in vals])

    ## Save figure
  #  plt.savefig(fig_dir + f'/{player_name}_pr.png', bbox_inches='tight', dpi=300)

    ## Show plt
    plt.tight_layout()
   # plt.show()