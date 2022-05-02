import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mplsoccer import PyPizza, add_image, FontManager
import matplotlib.image as image
import matplotlib.font_manager
import matplotlib.patheffects as pe
from highlight_text import htext, fig_text

font_normal = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Regular.ttf?raw=true"))
font_italic = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                           "Roboto-Italic.ttf?raw=true"))
font_bold = FontManager(("https://github.com/google/fonts/blob/main/apache/roboto/static/"
                         "Roboto-Medium.ttf?raw=true"))






def plot_scatterplot_from_metrics(df, metric1,metric2):
    
    
    
    df_team_grouped = df.copy()

    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 15})


    ### Create figure 
    fig, ax = plt.subplots(figsize=(16.5, 10.5))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)

    ax.grid(linestyle='dotted',linewidth=0.25,color='#3B3B3B',axis='y',zorder=1)


    spines = ['top', 'right', 'bottom', 'left']

    for s in spines:
        if s in ['top', 'right', 'bottom', 'left']:
            ax.spines[s].set_visible(False)
        else:
            ax.spines[s].set_color(text_colour)


    ### Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')

    ax.xaxis.set_tick_params(pad=2)
    ax.yaxis.set_tick_params(pad=20)

    ### Add X, Y gridlines
    ax.grid(b=True,
            color='grey',
            linestyle='-.',
            linewidth=0.5,
            alpha=0.2
           )


    ### Define X and Y values
    v_metric1 = df_team_grouped[metric1].tolist()
    v_metric2 = df_team_grouped[metric2].tolist() 
    teams = df_team_grouped['full_name'].tolist()
    xg_diff_p90 = df_team_grouped[metric2].tolist()


    ### Label the nodes
    for i, label in enumerate(teams):
        plt.annotate(label,(v_metric1[i], v_metric2[i] +0.01))


    ### Define Z order
    zo = 12
    colour_scale='RdBu'

    ### Create scatter plot of shots
    ax.scatter(v_metric1,
               v_metric2,
               marker='o',
              #color=point_colour,
               edgecolors='black',
               c=xg_diff_p90,
               cmap=colour_scale,
              #linewidths=0.5,
               s=200,
               alpha=0.7,
               zorder=zo
              )


    ### Show Legend
    #plt.legend(loc='upper left')     # commented out as not required
    ### Add Plot Title
    plt.figtext(0.045,
                1.04,
                f'Players {metric1} vs. {metric2}',
                fontsize=30,
                fontweight='bold', 
                color=text_colour
               )


    ### Add Plot Subtitle
    fig.text(0.045, 1.00, f'Serie A 2020/2021', fontweight='regular', fontsize=20, fontfamily=title_font, color=text_colour)


    ### Add X and Y labels
    plt.xlabel(metric1, color=text_colour, fontsize=18)
    plt.ylabel(metric2, color=text_colour, fontsize=18)
    #plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2])
    #plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6])
    #plt.xlim([1, 2.6])
    #plt.ylim([1, 2.2])


    ### Invert x axis - less xGA is better
    #ax.invert_xaxis()


    ### Remove pips
    ax.tick_params(axis='both', length=0)


    ### Add UEFA EURO 2020 logo
    ax2 = fig.add_axes([0.99, 0.95, 0.15, 0.15])
    ax2.axis('off')
    img = image.imread('data/img/logos/Italian-Serie-A-logo-1.png')
    ax2.imshow(img)



    ### Add StatsBomb 360 logo
    ax3 = fig.add_axes([0.9175, -0.0535, 0.16, 0.16])
    ax3.axis('off')
    img = image.imread('data/img/logos/loghi.png')
    ax3.imshow(img)


    ### Save figure
    #if not os.path.exists(fig_dir + f'/xg_diff_scatter_plot_teams.png'):
    #    plt.savefig(fig_dir + f'/xg_diff_scatter_plot_teams.png', bbox_inches='tight', dpi=300)
    #else:
    #    pass


    ### Show plt
    plt.tight_layout()
    plt.show()



def barplot_score_goals(df):
    g = df.query("outcome=='goal'").groupby(["player", "situation"])\
                                  .agg({"outcome":"count"})\
                                  .reset_index()\
                                  .pivot(index="player", columns="situation", values="outcome")\
                                  .fillna(0)
    g["total"] = g[g.columns].sum(axis=1)
    g = g.sort_values("total", ascending=False).head(10)
    g = g[['set_piece', 'open_play', 'free_kick', 'from_corner', 'fast_break', 'penalty','total']]


    line_color = "k"
    column_color_dict = {'open_play': "royalblue",
                         'penalty': "teal",
                         'free_kick': "darkorchid",
                         'from_corner': "magenta",
                         'set_piece': "gold",
                         'fast_break':'gold',
           


                        }

    #with plt.style.context("Solarize_Light2"):
    plt.rcParams['font.family'] = 'Palatino Linotype' ##set global font

    fig, ax = plt.subplots(figsize=(13, 10))
    ax = g[column_color_dict.keys()].iloc[::-1].plot.barh(stacked=True, ax=ax, color=column_color_dict, 
                                               ec="silver", legend=None)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)  

    ax.grid(False)    
    ax.set_position([0.08, 0.08, 0.82, 0.74]) ## make space for the title on top of the axes

    for num, total in enumerate(g["total"].iloc[::-1]):
        ax.text(total+2, num, int(total), va='center_baseline', ha='left', fontsize=20)

    ## labels, titles and subtitles
    ax.set(ylabel=" ", xlabel="Goals")     
    ax.xaxis.label.set(fontsize=12, fontweight='bold', color=line_color)    

    for label in ax.get_yticklabels():
        label.set(color=line_color, fontsize=12)
    for t in ax.xaxis.get_ticklabels():
        t.set_color(line_color)

  
    fig.text(x=0.14, y=1, s="How are strikers scoring their goals? - Serie A | 2020-2021", 
            ha='left', fontsize=25, fontweight='bold', color=line_color,
            path_effects=[pe.Stroke(linewidth=1.1, foreground='0.1'),
                       pe.Normal()])  

    fig_text(x=0.14, y=0.985, ha='left',
             fontsize=20, fontweight='bold',
             color=line_color,
             s='<Open Play> | <Penalty> | <Direct Freekick> | <Corner> | <Other Set-pieces>',
             highlight_textprops=[{"color": "royalblue"},
                                  {"color": "teal"}, 
                                  {"color": "darkorchid"}, 
                                  {"color": "magenta"}, 
                                  {"color": "gold"}]
            )

    #fig.savefig("shooter-bar-chart", dpi=180)
    
    ### Show plt
    plt.tight_layout()
    plt.show()
