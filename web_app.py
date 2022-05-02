import streamlit as st
import pandas as pd
import io
import matplotlib.font_manager
from PIL import Image, ImageOps
import numpy as np
from PIL import Image, ImageOps
import requests
from IPython.display import display, clear_output
from src.utils import calculate_xg
from src.viz_functions_shotmap import draw_pitch,create_shot_map_player, get_Shotmap_color2, get_Shotmap
from src.viz_functions_plotting_generic import plot_scatterplot_from_metrics, barplot_score_goals
from src.viz_functions_evaluation_player import get_player_camparision_radar, plot_player_pyPizza
from src.viz_functions_metrics import get_barchart_attacking,get_barchart_passing, get_barchart_defending
from src.viz_functions_waffle_plot import waffle_plot, waffle_plot_one_player
import pickle
from pathlib import Path

import base64






name1='data/dataset_corso&bioScraping_cst.csv'
name2= 'data/database_tiri_serieA_2020-21.csv'


def load_dataset(name1,name2):
    df = pd.read_csv(name1).iloc[:,1:]
    df_shots = pd.read_csv(name2)
    return df,df_shots



df,df_shots= load_dataset(name1,name2)

@st.cache
def add_varables_shots(df,df_shots):
    df_xG = df[['player_id','xG_p90','xG']]

    df_shots = df_shots.merge(df_xG, on= 'player_id')
    df_shots = calculate_xg(df_shots)
    return df_shots


mapping = {'FW':'Forward','FB':'Full-back','CB':'Center Back','CM':'Central Midfielder','DMC':'Defensive Midfielder','CAM':'Central Attacking Midfielder', 'WAM':'Outside Forward' }
mapping_foot = {'destro': 'Right','sinistro':'Left','entrambi':'Ambidextrous'}
df['foot'] = df['foot'].map(mapping_foot)
@st.cache
def get_and_display_player_image(df, player):
    image_url = df[df['full_name'] == player]['PlayerImgURL'].values[0]
    image = ImageOps.expand(Image.open(requests.get(image_url, stream=True).raw),border=5,fill='black')
    image = image.resize((400, 400))
    return image
@st.cache
def get_logo_image(df, player):
    team = df[df['full_name'] == player]['team'].values[0]
    logo = ImageOps.expand(Image.open(f'data/img/logos/{team}.png'))
    #logo_serieA = ImageOps.expand(Image.open('data/img/logos/Italian-Serie-A-logo-1.png'))
    logo = logo.resize((60, 60))

    return logo

@st.cache
def get_logo_image_static(logo_name):

    logo = ImageOps.expand(Image.open(f'data/img/logos/{logo_name}.png'))

    logo = logo.resize((60, 60))

    return logo

@st.cache
def get_parameter(df,player, mapping):

    team = df[df['full_name'] == player]['team'].values[0]

    ruolo = df[df['full_name'] == player]['soccRole'].map(mapping).values[0]
    altezza = df[df['full_name'] == player]['height'].values[0]
    altezza = altezza.split()[0]
    foot = df[df['full_name'] == player]['foot'].values[0]
    country = df[df['full_name'] == player]['Country'].values[0]
    stipendio = df[df['full_name'] == player]['Annual Gross'].values[0]
    anni = df[df['full_name'] == player]['Età'].values[0]
    birth_date = df[df['full_name'] == player]['birth_date'].values[0]
    goals = df[df['full_name'] == player]['goals'].values[0]
    assists = df[df['full_name'] == player]['assists'].values[0]
    cluster_def = df[df['full_name'] == player]['cluster_def'].values[0]

    return team,ruolo,altezza,foot,country,stipendio,anni, birth_date, goals, assists,cluster_def
@st.cache
def add_varables_shots(df,df_shots):
    df_xG = df[['player_id','xG_p90','xG']]

    df_shots = df_shots.merge(df_xG, on= 'player_id')
    df_shots = calculate_xg(df_shots)
    return df_shots

@st.cache
def get_salary(x):
    try:
        res = x[2:].split(',')
    except:
        return None
    try:
        res = float('.'.join([res[0].replace('.', ''), res[1]]))
        if len(x) > 10:
            res = res * 1000000
        else:
            res = res * 1000
    except:
        return None
    return res


@st.cache
def return_list_roles(df,mapping):

    list_roles = list(df['soccRole'].map(mapping).unique())
    list_roles.insert(0, 'All')
    return list_roles

@st.cache
def get_salary_default(df,sal_mln1,sal_mln2):
    df['Annual Gross_float'] = df['Annual Gross'].apply(lambda x: get_salary(x))
    df_salary = df.dropna(subset=['Annual Gross_float'])
    list_tmp = list(df_salary[(df_salary['Annual Gross_float'] >= sal_mln1) & (
                df_salary['Annual Gross_float'] <= sal_mln2)].full_name)
    df = df.query('full_name in @list_tmp')
    return df


#########################################SETTINGS#######################################################################################




def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_bg(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = """
        <style>
        .stApp {
        background-image: url("data:image/png;base64,%s");
        background-size: cover;
        }
        </style>
    """ % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


st.set_page_config(
    page_title="Football Analytics Serie A",
    page_icon=":soccer:",
    layout="wide"
)

set_bg('data/img//background.png')



st.set_option('deprecation.showPyplotGlobalUse', False)





######################################################################## SIDEBAR ###################################################################################


with st.sidebar:
    st.sidebar.markdown( "**Select the parameters you consider important to filter your search for the characteristics of the ideal player or scroll down and select the player directly.** 👇")


    c1, c2 = st.columns((2, 2))
    with c1:
        st.text('')
        age_default = (min(df['Età']), max(df['Età']))
        p_age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default,
         help='Age range. Drag the sliders on either side. \'All\' ages by default.')
        list_clst = list(df['cluster_def'].unique())
        list_clst.insert(0,'All')
        c_clst_role = st.selectbox('Select Cluster Skills', list_clst)

        teams = list(df['team'].unique())
        teams.insert(0, 'All')
        p_team = st.selectbox('Select team',teams)

    with c2:
        st.text('')

        list_roles = return_list_roles(df, mapping)
        role = st.selectbox('Select Role', list_roles)

        salary_default =(float(0.4), float(60))
        salarys = st.slider('Salary( 400k -- 60M )', min_value=salary_default[0], max_value=salary_default[1], value=salary_default,
                          help='Salary range. Select a range from 400k to 60 million in annual salary')
        sal_mln1 = salarys[0] * 1000000
        sal_mln2 = salarys[1] * 1000000
        salary_tuple = (sal_mln1, sal_mln2)

        p_foot = st.selectbox('Preferred foot', ['All', 'Right', 'Left', 'Ambidextrous'])


@st.cache(suppress_st_warning=True)
def filter_df_for_select_players(df,p_age, role, p_foot,p_team,salary_tuple,mapping):

    if p_age == age_default:
        pass
    else:
        df = df[(df['Età'] >= p_age[0]) & (df['Età'] <= p_age[1])]

    if role == 'All':
        pass
    else:
        df['soccRole_ext'] = df['soccRole'].map(mapping)
        df = df[df['soccRole_ext'] == role]


    if salary_tuple == salary_default:
        pass
    else:
        df = get_salary_default(df,salary_tuple[0],salary_tuple[1])


    if p_foot == 'All':
        pass
    elif p_foot == 'Right':

        df = df[df['foot'] == p_foot]
    elif p_foot == 'Left':
        df = df[df['foot'] == p_foot]
    elif p_foot == 'Ambidextrous':
        df = df[df['foot'] == p_foot]
    else:
        pass


    if c_clst_role == 'All':
        pass
    else:
        df = df[df['cluster_def'] == c_clst_role]

    if p_team == 'All':
        pass
    else:
        df = df[df['team'] == p_team]

    return df

df_filter = filter_df_for_select_players(df,p_age,role, p_foot,p_team,salary_tuple,mapping)

player = st.sidebar.selectbox('', list(df_filter['full_name'].unique()),help='Type without deleting a character. To search from a specific team, just type in the club\'s name.')

try:
    team, ruolo, altezza, foot, country, stipendio, anni, birth_date, goals, assists, cluster_def = get_parameter(df, player, mapping)
except:
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')

    st.text('')
    st.text('')
    st.text('')
    st.markdown(f"<h1 style='text-align: center;color:white '> Your search returned no results, please select the paremeters again </h1>", unsafe_allow_html=True)
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')
    st.text('')


image = get_and_display_player_image(df, player)
logo = get_logo_image(df, player)
logo_socc = get_logo_image_static(logo_name='loghi')



header = st.container()
core = st.container()

st.markdown("""
<style>
.big-font {
    font-size:50px !important;
}
.medium-font {
    font-size:30px !important;
}
</style>
""", unsafe_allow_html=True)






with header:
    c1, c2, c3, c4, = st.columns((7, 1, 1, 3))
    with c1:
        st.markdown('Based on the 2020/21 season data for the **Serie A**  league :soccer:')

        def read_info(path):
            return Path(path).read_text(encoding='utf8')

        st.markdown(read_info('info.md'), unsafe_allow_html=True)
        st.title(f'{player} - {team} ')
    with c4:
        st.image('data/img/logos/soccsics.png')

   # data / img / logos / {logo_name}.png
    st.markdown("""<hr style="height:2px;border:none;color:white;background-color:gold;" /> """,
                unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns((1, 1, 2, 1, 2))
    with c1:
        st.image(image)

    with c2:
        st.image(logo)

    with c3:
        st.markdown(f"<h3 style='text-align: center ;'>  {ruolo} </h3>",
                    unsafe_allow_html=True)
        st.markdown(f"<h5 style='text-align: center;color:gold '> Skills:  {cluster_def} </h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center; '> Nationality: {country} </h4>", unsafe_allow_html=True)


    with c4:

        st.text('')

        st.markdown(f"<h6 style='text-align: center; '>Age: {anni} </h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center;'>Goals: {goals} </h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center;'>Assists: {assists} </h4>", unsafe_allow_html=True)

    with c5:
        st.text('')

        #st.markdown(f"<h6 style='text-align: center; color: black;'>Contracted to {team} </h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center;'> Salary: {stipendio}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center;'> Heiht: {altezza}cm </h4>", unsafe_allow_html=True)
        st.markdown(f"<h6 style='text-align: center;'> Foot: {foot}</h4>", unsafe_allow_html=True)

       # st.markdown("""<hr style="height:10px;border:none;color:white;background-color:white;" /> """, unsafe_allow_html=True)




with core:
    st.markdown("""<hr style="height:2px;border:none;color:white;background-color:gold;" /> """,
                unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
    #st.header("Attacking Metrics")
        st.markdown("<h3 style='text-align: center; '> Attacking Metrics</h3>", unsafe_allow_html=True)

        attck = get_barchart_attacking(df=df, player_name=player, player_colour='red')
        st.pyplot(attck,transparent=True)
    with col2:
        st.markdown("<h3 style='text-align: center;'> Passing Metrics</h3>", unsafe_allow_html=True)

        passing = get_barchart_passing(df=df, player_name=player, player_colour='red')
        st.pyplot(passing,transparent=True)
    with col3:
        st.markdown("<h3 style='text-align: center;'> Defending Metrics</h3>", unsafe_allow_html=True)

        defending = get_barchart_defending(df=df, player_name=player, player_colour='red')
        st.pyplot(defending, transparent=True)

st.markdown("""<hr style="height:2px;border:none;color:white;background-color:gold;" /> """,
            unsafe_allow_html=True)



df_shots = add_varables_shots(df,df_shots)

with st.container():

    cc1, cc2 = st.columns((3,2))
    with cc1:
        fig_pizz = plot_player_pyPizza(df,player)
        st.pyplot(fig_pizz, transparent=True)

    with cc2:


        try:
            st.markdown("<h3 style='text-align: center;'> Map shots no penalty</h3>", unsafe_allow_html=True)
            fig_shot = get_Shotmap_color2(df_shots,player)
            st.pyplot(fig_shot,transparent=True)

            waffle = waffle_plot_one_player(df_shots, [player])
            st.pyplot(waffle, transparent=True)
        except:
            st.markdown("<h3 style='text-align: center;'> The selected player has no shots to show</h3>", unsafe_allow_html=True)




with st.container():
    st.markdown("""
    <style>
    r { color: Red }
    o { color: Orange }
    g { color: Green }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""<hr style="height:2px;border:none;color:white;background-color:gold;" /> """,
                unsafe_allow_html=True)
    st.markdown(f" ##### Which soccer players are more similar to ${player}$ ? ")
    st.markdown("**Set the parameters that you think more appropriate to filter your search.** 👇")

   # @st.cache(allow_output_mutation=True)
    def getData():

        player_df = pd.read_csv('data/dataset_corso&bioScraping.csv')

        with open(r'data/player_ID.pkl', 'rb') as file:
            player_ID = pickle.load(file)
        with open(r'data/engine.pickle', 'rb') as file:
            engine = pickle.load(file)
        return [player_df, player_ID, engine]


    outfield_data = getData()
    df2, player_ID, engine = outfield_data
    print(df2)
    print(df2.head())
    print('###############################################################')
    print(df.shape)
    print(df)

    df2['cluster_def'] =df['cluster_def']
    #df2 = df2.merge(df_merg, on='full_name')
    players = sorted(list(player_ID.keys()))
    age_default = (min(df2['Età']), max(df2['Età']))

    players_ = []
    for idx in range(len(df2)):
        players_.append(df2['full_name'][idx] + f"({df2['team'][idx]})")

    df2['player_dict'] = players_

    query = df2[df2['full_name'] == player]['player_dict'].values[0]

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        comparison = st.selectbox('Comparison with', ['All positions', 'Same position'],
                                  help='Whether to compare the selected player with all positions or just the same defined position in the dataset. \'All \
               positions\' by default.')

        res, val, step = (3, 20), 10, 3
        count = st.slider('Number of results', min_value=res[0], max_value=res[1], value=val, step=step)


    with col2:
        age = st.slider('Age bracket', min_value=age_default[0], max_value=age_default[1], value=age_default,
                        help='Age range to get recommendations from. Drag the sliders on either side. \'All\' ages by default.')
        clst_role2 = st.selectbox(f'Compare only with the same skills? ( {cluster_def} )', ['All Skills','Same skills Cluster' ],
                                  help='Whether to compare the selected player with all skills from cluster analysis. \'All \
               positions\' by default.')

        list_clst2 = list(df2['cluster_def'].unique())
        list_clst2.insert(0, 'All')
       # clst_role2 = st.selectbox('Select Ability Skills-Cluster Analysis', list_clst2)



    with col3:
        c_foot = st.selectbox('Foot', ['All', 'Right', 'Left', 'Ambidextrous'])
        salary_default = (float(0.4), float(60))
        salarys = st.slider(' Salary ( 400k -- 60M )', min_value=salary_default[0], max_value=salary_default[1],
                            value=salary_default,
                            help='Salary range. Select a range from 400k to 60 million in annual salary')
        sal_mln1 = salarys[0] * 1000000
        sal_mln2 = salarys[1] * 1000000
        salary_tuple = (sal_mln1, sal_mln2)








with st.container():
    st.text(' \n')
    st.text(' \n')
    st.text(' \n')
    st.markdown('_showing recommendations for_ **{}**'.format(query))


    @st.cache(suppress_st_warning=True)
    def getRecommendations(metric,  foot, comparison, age, count, clst_role2):

        df_res = df2[['full_name',  'soccRole', 'Età', 'team', 'Annual Gross','height','foot','player_dict','cluster_def']].copy()

        df_res['foot'] = df_res['foot'].map(mapping_foot)

        df_res['Player'] = list(player_ID.keys())
        df_res.insert(1, 'Similarity', metric)
        df_res = df_res.sort_values(by=['Similarity'], ascending=False)
        metric = [str(num) + '%' for num in df_res['Similarity']]
        df_res['Similarity'] = metric

      #  if clst_role2 == 'All':
      #      pass
      #  else:
      #      df_res = df_res[df_res['cluster_def'] == clst_role2]

        if p_team == 'All':
            pass
        else:
            df_res = df_res[df_res['team'] == p_team]
       # 'All Skills', 'Same skills Cluster'
        if clst_role2 == 'Same skills Cluster':
            q_pos = list(df_res[df_res['Player'] == query].cluster_def)[0]
            df_res = df_res[df_res['cluster_def'] == q_pos]




        if comparison == 'Same position':
            q_pos = list(df_res[df_res['Player'] == query].soccRole)[0]
            df_res = df_res[df_res['soccRole'] == q_pos]

            df_res = df_res.iloc[1:, :]

        if age == age_default:
            pass
        else:
            df_res = df_res[(df_res['Età'] >= age[0]) & (df_res['Età'] <= age[1])]

        if foot == 'All':
            pass
        elif foot == 'Right':

            df_res = df_res[df_res['foot'] == foot]
        elif foot == 'Left':
            df_res = df_res[df_res['foot'] == foot]
        elif foot == 'Ambidextrous':
            df_res = df_res[df_res['foot'] == foot]
        else:
            pass


        if salary_tuple == salary_default:
            pass
        else:
            df_res = get_salary_default(df_res, salary_tuple[0], salary_tuple[1])


        df_res =  df_res[df_res['Player']!= query]
        df_res = df_res.iloc[:count, :].reset_index(drop=True)
        df_res.index = df_res.index + 1



        df_res = df_res[['full_name', 'Similarity', 'soccRole', 'Età', 'team', 'Annual Gross','height','foot']]
        df_res.rename(columns={'full_name': 'Player Name', 'soccRole': 'Position', 'Età': 'Age','team':'Team','height':'Height','foot':'Foot'}, inplace=True)

        return df_res

    sims = engine[query]

    df_type = 'outfield'
    @st.cache
    def return_results(sims,c_foot,comparison,age,count,clst_role2):
        result = getRecommendations(sims, foot=c_foot, comparison=comparison, age=age, count=count,clst_role2=clst_role2)
        return result


    recoms= return_results(sims,c_foot,comparison,age,count,clst_role2)



    st.table(recoms)

    list_comp = list(recoms['Player Name'].unique())

    with st.container():
        st.text(' \n')
        st.text(' \n')
        st.text(' \n')
        col1, col2, col3 = st.columns([1, 6, 1])

        with col2:
            st.markdown(f"**Select from the drop-down menu the player you want to compare with {player}.** 👇")
            player_comp = st.selectbox('', list_comp,
                                   help='Type without deleting a character. To search from a specific team, just type in the club\'s name.')



            with st.expander("View comparison"):

                fig = get_player_camparision_radar(df, player,player_comp)
                st.pyplot(fig)
