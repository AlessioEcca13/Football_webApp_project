import matplotlib.patches as mpatches
from mplsoccer.pitch import Pitch, VerticalPitch
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Arc
import matplotlib.image as image
import streamlit as st
import matplotlib.font_manager
@st.cache
def draw_pitch(x_min=0,
                   x_max=106,
                   y_min=0,
                   y_max=68,
                   pitch_color="w",
                   line_color="grey",
                   line_thickness=1.5,
                   point_size=20,
                   orientation="horizontal",
                   aspect="full",
                   ax=None
                  ):

    if not ax:
        raise TypeError("This function is intended to be used with an existing fig and ax in order to allow flexibility in plotting of various sizes and in subplots.")


    if orientation.lower().startswith("h"):
        first = 0
        second = 1
        arc_angle = 0

        if aspect == "half":
            ax.set_xlim(x_max / 2, x_max + 5)

    elif orientation.lower().startswith("v"):
        first = 1
        second = 0
        arc_angle = 90

        if aspect == "half":
            ax.set_ylim(x_max / 2, x_max + 5)

    
    else:
        raise NameError("You must choose one of horizontal or vertical")

    
    ax.axis("off")

    rect = plt.Rectangle((x_min, y_min),
                         x_max, y_max,
                         facecolor=pitch_color,
                         edgecolor="none",
                         zorder=-2)

    ax.add_artist(rect)

    x_conversion = x_max / 100
    y_conversion = y_max / 100

    pitch_x = [0,5.8,11.5,17,50,83,88.5,94.2,100] # pitch x markings
    pitch_x = [x * x_conversion for x in pitch_x]

    pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100] # pitch y markings
    pitch_y = [x * y_conversion for x in pitch_y]

    goal_y = [45.2, 54.8] # goal posts
    goal_y = [x * y_conversion for x in goal_y]

    # side and goal lines
    lx1 = [x_min, x_max, x_max, x_min, x_min]
    ly1 = [y_min, y_min, y_max, y_max, y_min]

    # outer boxed
    lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
    ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    lx3 = [0, pitch_x[3], pitch_x[3], 0]
    ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    # goals
    lx4 = [x_max, x_max+2, x_max+2, x_max]
    ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    lx5 = [0, -2, -2, 0]
    ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    # 6 yard boxes
    lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
    ly6 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]

    lx7 = [0, pitch_x[1], pitch_x[1], 0]
    ly7 = [pitch_y[2],pitch_y[2], pitch_y[4], pitch_y[4]]


    # Halfway line, penalty spots, and kickoff spot
    lx8 = [pitch_x[4], pitch_x[4]]
    ly8 = [0, y_max]

    lines = [
        [lx1, ly1],
        [lx2, ly2],
        [lx3, ly3],
        [lx4, ly4],
        [lx5, ly5],
        [lx6, ly6],
        [lx7, ly7],
        [lx8, ly8],
        ]

    points = [
        [pitch_x[6], pitch_y[3]],
        [pitch_x[2], pitch_y[3]],
        [pitch_x[4], pitch_y[3]]
        ]

    circle_points = [pitch_x[4], pitch_y[3]]
    arc_points1 = [pitch_x[6], pitch_y[3]]
    arc_points2 = [pitch_x[2], pitch_y[3]]


    for line in lines:
        ax.plot(line[first], line[second],
                color=line_color,
                lw=line_thickness,
                zorder=-1)

    for point in points:
        ax.scatter(point[first], point[second],
                   color=line_color,
                   s=point_size,
                   zorder=-1)

    circle = plt.Circle((circle_points[first], circle_points[second]),
                        x_max * 0.088,
                        lw=line_thickness,
                        color=line_color,
                        fill=False,
                        zorder=-1)

    ax.add_artist(circle)

    arc1 = Arc((arc_points1[first], arc_points1[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=128.75,
               theta2=231.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc1)

    arc2 = Arc((arc_points2[first], arc_points2[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=308.75,
               theta2=51.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc2)

    ax.set_aspect("equal")

    return ax


def create_shot_map_player(df, player_name):

    """
    Function to create a shot map for individual players.
    """

   


    ### Exclude penalties
    df = df[df.situation != 'penalty']
    
        
    df['x_no'] = df['x'] + 20.5
    df['y_no'] = df['y'] - 7.5
    
    ### Select only shots from the DataFrame if full events dataset passed through
    df_shots = df[(df['outcome'] != 'goal') & (df['player'] == player_name)]
    df_goals = df[(df['outcome'] == 'goal') & (df['player'] == player_name)]
    df_shots_and_goals =  df[df['player'] == player_name]

    ### Determine the total number of shots
    total_shots = str(len(df_shots))
    total_goals = str(len(df_goals))

    ### Determine the total nxG
    df_shots_and_goals = df_shots_and_goals.reset_index(drop=True)
    total_xg = str(round(df_shots_and_goals['xG'][0],2))

    
    y_shots = df_shots['x_no'].tolist()
    x_shots = df_shots['y_no'].tolist()
    y_goals = df_goals['x_no'].tolist()
    x_goals = df_goals['y_no'].tolist()


    ## Data Visualisation

    ### Define fonts and colours
    title_font = 'Alegreya Sans'
    main_font = 'Open Sans'
    background='#F7F7F7'
    title_colour='black'
    text_colour='black'
    mpl.rcParams.update(mpl.rcParamsDefault)
    mpl.rcParams['xtick.color'] = text_colour
    mpl.rcParams['ytick.color'] = text_colour
    mpl.rcParams.update({'font.size': 18})
    
    
    
    ### Create figure 
    fig, ax = plt.subplots(figsize=(16.5, 10.5))
    fig.set_facecolor(background)
    ax.patch.set_facecolor(background)



    ### Draw the pitch using the 
    draw_pitch(x_min=0,
               x_max=120,
               y_min=0,
               y_max=85,
               orientation='vertical',
               aspect='half',
               pitch_color=background,
               line_color='#3B3B3B',
               ax=ax
              )

    ## Add Z variable for xG
    z1 = df_shots['xG_calc'].tolist()
    z1 = [1000 * i for i in z1]
    z2 = df_goals['xG_calc'].tolist()
    z2 = [1000 * i for i in z2]

    ### Define Z order
    zo = 12
    
    ## Add small legend in the bottom corner
    mSize = [0.05, 0.10, 0.2, 0.4, 0.6, 1]
    mSizeS = [1000 * i for i in mSize]
    mx = [1.5, 3.0, 5.0, 7.5, 10.625, 14.25]
    my = [115, 115, 115, 115, 115, 115]
    ax.text(7.875,110.5,'xG',color='#3B3B3B',ha='center',va='center',zorder=zo,fontsize=16)

    ### Create scatter plot of shots
    ax.scatter(x_shots,y_shots,marker='o',color='red',edgecolors='black',s=z1,alpha=0.7,zorder=zo,label='Shots')

    ### Create scatter plot of goals
    ax.scatter(x_goals,y_goals, marker='*', color='green', edgecolors='black',s=z2,alpha=0.7,zorder=zo,label='Goals')

    ax.scatter(mx, my,s=mSizeS, facecolors='#3B3B3B', edgecolor='#3B3B3B', zorder=zo)
    ax.plot([1.5, 14.25], [112.25,112.25], color='#3B3B3B', lw=2, zorder=zo)

    ### 
    i = 0
    for i in range(len(mx)):
        ax.text(mx[i], my[i], mSize[i], fontsize=mSize[i]*14, color='white', zorder=zo, ha='center', va='center')


    ### Show Legend
    plt.legend(loc='best', bbox_to_anchor=(0.1, 0., 0.5, 0.5),fontsize=25)
    

    plt.title(f"Shot Map of {player_name} | Serie A 2020/2021 ", color = "black", fontweight = "bold", size = 35, pad = -25)



    ### Add logo
    ax2 = fig.add_axes([0.75, 0.7, 0.15, 0.15])
   
    ax2.axis('off')
    img = image.imread('data/img/logos/Italian-Serie-A-logo-1.png')
    ax2.imshow(img)


    ax3 = fig.add_axes([0.6, -0.018, 0.25, 0.25])
    ax3.axis('off')
    img = image.imread('data/img/logos/loghi.png')
    ax3.imshow(img)




    plt.tight_layout()
    plt.show()
    
    
    
    

def get_Shotmap(df,name):

    df = df[df['player']==name]

    df = df[df.situation != 'penalty']

    gls = {'goal':"Goal", 'miss': "NoGoal", 'saved': "NoGoal", 
           'blocked': "NoGoal", 'post': "NoGoal"}
    colours = {'Goal':"#E74C3C", 'NoGoal': "#1B2631"}
    df["result"] = df["outcome"].map(gls)

    finaldata = df.copy()

    player_name = finaldata["player"].values[0]
    res = {"Goal": 1, "NoGoal": 0} 
    finaldata["isGoal"] = finaldata["result"].map(res)
    finaldata["col"] = finaldata["result"].map(colours)
    finaldata = finaldata.dropna()
    finaldata = finaldata.reset_index(drop=True)


    xG = finaldata["xG"][0]
    xG = str(round(xG, 2))
    xgst = (finaldata["xG"][0]) / len(finaldata.index)
    xgst = str(round(xgst, 2))
    gls = sum(finaldata["isGoal"])

    g = mpatches.Patch(color = "#E74C3C", label = "Goal")
    ss = mpatches.Patch(color = "#ffffff", label = "No Goal")
    pitch = VerticalPitch(pitch_type = 'opta',pitch_color='#1B2631', line_color = "#707B7C", stripe=False, half = True, 
                          constrained_layout = True)
    fig, ax = pitch.draw()
    plt.scatter(x = finaldata["y"], y = finaldata["x"], s = finaldata["xG_calc"] * 600, c = finaldata["col"], 
                edgecolors="white")
    plt.gca().invert_xaxis()
    plt.text(35.5, 51, '2020/2021', color="white", size= 30, fontweight = "bold")
    plt.text(73, 51, f"Total xG = {xG}\nxG/Shot = {xgst}\nGoals = {gls}", size = 20, color = "white")
    #plt.text(79, 56.5, "Created by @AlessioEcca\nData from Understat", color = "white", size = 12)
    plt.title(f"{player_name}", color = "white", fontweight = "bold", size = 30, pad = -25)
    leg = plt.legend(handles = [g, ss], frameon = False, loc = "center left", 
                     bbox_to_anchor=(0.05,0.1), prop={'size': 12})

    for text in leg.get_texts():
        text.set_color("white")

    fig.set_size_inches(10, 8)

    plt.show()
    

def get_Shotmap_color2(df, name):
    df = df[df['player'] == name]

    df = df[df.situation != 'penalty']

    colours = {'goal': '#229954', 'saved': '#CB4335', 'miss': '#F1C40F',
               'blocked': '#3498DB', 'post': '#76448A'}
    player_name = df["player"].values[0]
    res = {"goal": 1, "saved": 0, "blocked": 0, "post": 0,
           "miss": 0}
    markers = {"goal": '*', "saved": 'o', "blocked": 'o', "post": 'o', "miss": 'o'}

    finaldata = df.copy()
    finaldata["isGoal"] = finaldata["outcome"].map(res)
    finaldata["col"] = finaldata["outcome"].map(colours)
    finaldata['marker'] = finaldata['outcome'].map(markers)
    finaldata = finaldata.dropna()
    finaldata = finaldata.reset_index(drop=True)
    xG_p90 = finaldata["xG_p90"][0]
    xG = finaldata["xG"][0]
    xG = str(round(xG, 2))
    xgst = (finaldata["xG"][0]) / len(finaldata.index)
    xgst = str(round(xgst, 2))
    gls = sum(finaldata["isGoal"])

    final_goal = finaldata[finaldata['goal'] == 1]
    final_Nogoal = finaldata[finaldata['goal'] == 0]
    saved = final_Nogoal[final_Nogoal['outcome'] == 'saved']
    miss = final_Nogoal[final_Nogoal['outcome'] == 'miss']
    block = final_Nogoal[final_Nogoal['outcome'] == 'blocked']
    post = final_Nogoal[final_Nogoal['outcome'] == 'post']

    g = mpatches.Patch(color="#229954", label="Goal", hatch='*')
    ss = mpatches.Patch(color="#CB4335", label="Saved Shot")
    ms = mpatches.Patch(color="#F1C40F", label="Missed Shot")
    bs = mpatches.Patch(color="#3498DB", label="Blocked Shot")
    sop = mpatches.Patch(color="#76448A", label="Shot on Post")

    pitch = VerticalPitch(pitch_type='opta', pitch_color='#1B2631', line_color="#707B7C", stripe=False, half=True,
                          constrained_layout=True)
    fig, ax = pitch.draw()

    plt.scatter(x=saved["y"], y=saved["x"], s=saved["xG_calc"] * 600, c=saved["col"], marker='s',
                edgecolors="white")

    plt.scatter(x=miss["y"], y=miss["x"], s=miss["xG_calc"] * 600, c=miss["col"], marker='^',
                edgecolors="white")

    plt.scatter(x=block["y"], y=block["x"], s=block["xG_calc"] * 600, c=block["col"], marker='x',
                edgecolors="white")

    plt.scatter(x=post["y"], y=post["x"], s=post["xG_calc"] * 600, c=post["col"], marker='o',
                edgecolors="white")

    plt.scatter(x=final_goal["y"], y=final_goal["x"], s=final_goal["xG_calc"] * 600, c=final_goal["col"], marker='*',
                edgecolors="white")

    plt.gca().invert_xaxis()

    plt.text(73, 51, f"Total xG = {xG}\nxG/Shot = {xgst}\nGoals = {gls}", size=20, color="white")

    leg = plt.legend(handles=[g, ss, ms, bs, sop], frameon=False, loc="center left",
                     bbox_to_anchor=(0.043, 0.15), prop={'size': 12})

    for text in leg.get_texts():
        text.set_color("white")



    fig.set_size_inches(10, 8)

    plt.show()


def get_Shotmap_color(df, name):
    df = df[df['player']==name]

    df = df[df.situation != 'penalty']

    colours = {'goal':'#229954', 'saved':'#CB4335', 'miss':'#F1C40F', 
               'blocked':'#3498DB', 'post':'#76448A'}
    player_name = df["player"].values[0]
    res = {"goal": 1, "saved": 0, "blocked": 0, "post": 0, 
           "miss": 0}
    markers = {"goal": '*', "saved": 'o', "blocked": 'o', "post": 'o',"miss": 'o'}

    finaldata = df.copy()
    finaldata["isGoal"] = finaldata["outcome"].map(res)
    finaldata["col"] = finaldata["outcome"].map(colours)
    finaldata['marker'] = finaldata['outcome'].map(markers)
    finaldata = finaldata.dropna()
    finaldata = finaldata.reset_index(drop=True)

    xG_p90 = finaldata["xG_p90"][0]
    xG = finaldata["xG"][0]
    xG = str(round(xG, 2))
    xgst = (finaldata["xG"][0]) / len(finaldata.index)
    xgst = str(round(xgst, 2))
    gls = sum(finaldata["isGoal"])


    g = mpatches.Patch(color = "#229954", label = "Goal")
    ss = mpatches.Patch(color = "#CB4335", label = "Saved Shot")
    ms = mpatches.Patch(color = "#F1C40F", label = "Missed Shot")
    bs = mpatches.Patch(color = "#3498DB", label = "Blocked Shot")
    sop = mpatches.Patch(color = "#76448A", label = "Shot on Post")


    pitch = VerticalPitch(pitch_type = 'opta',pitch_color='#1B2631', line_color = "#707B7C", stripe=False, half = True, 
                      constrained_layout = True)
    fig, ax = pitch.draw()
    plt.scatter(x = finaldata["y"], y = finaldata["x"], s = finaldata["xG_calc"] * 600, c = finaldata["col"],marker = finaldata['marker'].value,
                edgecolors="white")
    plt.gca().invert_xaxis()
    plt.text(35.5, 51, '2020/2021', color="white", size= 30, fontweight = "bold")
    plt.text(73, 51, f"Total xG = {xG}\nxG/Shot = {xgst}\nGoals = {gls}", size = 20, color = "white")
    plt.title(f"{player_name}", color = "white", fontweight = "bold", size = 30, pad = -25)
    leg = plt.legend(handles = [g, ss, ms, bs, sop], frameon = False, loc = "center left", 
                 bbox_to_anchor=(0.043,0.15), prop={'size': 12})

    for text in leg.get_texts():
        text.set_color("white")
        
    fig.set_size_inches(10, 8)

    plt.show()