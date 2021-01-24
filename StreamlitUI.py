import streamlit as st
import base64
from TwitterBot import TwitterBot


st.set_page_config(page_title='Twitter Bot',  # Alternate names: setup_page, page, layout
                    layout="wide",  # Can be "centered" or "wide". In the future also "dashboard", etc.
                    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                    page_icon=None,  # String, anything supported by st.image, or None.
                    )

cols_title = st.beta_columns((1, 2, 1, 1, 1, 1, 1, 1))
cols_title[0].image('Images/Bot.png', width=150)
cols_title[1].title('Twitter Bot')

st.sidebar.header('Enter Trend')
search = st.sidebar.text_input("e.g., 'Tesla'")

st.sidebar.header('Total Tweets')
total_tweets = st.sidebar.text_input("e.g., 10")

progress_bar = st.sidebar.progress(0)

done = st.sidebar.empty()
done.text('')

col_side = st.sidebar.beta_columns(2)
with col_side[0]:
    enter = st.button('Enter')
with col_side[1]:
    reset = st.button('Reset')

st.sidebar.markdown('''<h3>Created By: Ameer Tamoor Khan</h3>
                    <h4>Github : <a href="https://github.com/AmeerTamoorKhan" target="_blank">Click Here </a></h4> 
                    <h4>Email: drop-in@atkhan.info</h4> ''', unsafe_allow_html=True)

if enter:
    bot = TwitterBot(search, int(total_tweets), progress_bar)
    df = bot.scrap_tweets()
    st.balloons()
    done.success('Done')
    cols = st.beta_columns(1)
    cols[0].header('The Collected Tweets')
    cols[0].table(df[['Id', 'Tweet', 'Time', 'Retweet Count', 'Likes Count']])
    csv = df.to_csv(index=False)
    b4 = base64.b64encode(csv.encode()).decode()
    st.subheader('Download CSV File:')
    st.markdown(f'''<a href="data:file/csv;base64,{b4}" download="tweets.csv">Download Tweets</a>''', unsafe_allow_html=True)
elif reset:
    st.empty()
else:
    pass




