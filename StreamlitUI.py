import streamlit as st
import base64
from TwitterBot import TwitterBot


st.set_page_config(page_title='Twitter Bot',  # Alternate names: setup_page, page, layout
                    layout="centered",  # Can be "centered" or "wide". In the future also "dashboard", etc.
                    initial_sidebar_state="auto",  # Can be "auto", "expanded", "collapsed"
                    page_icon=None,  # String, anything supported by st.image, or None.
                    )

cols_title = st.beta_columns((1, 2, 1, 1, 1))
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


def default():
    st.header('Working Demonstration')
    st.video('Images/Twitter.mp4')
    st.header('How It Works')
    st.markdown('''
        <p>As it is clear from the name, "Twitter Bot," extracts the tweets from Twitter based on the trend you are 
        searching for. For instance, you want to search on "Teslaa," you type it in the "Enter Trend" text box and
        also specifies the number of tweets (Total Tweets) you want and Voila. On right side, it will show you the
        tweets and essential info related. You can also download the tweets in .csv form.</p>
        <p>Scraping is a process of extracting information from the web. Big Data plays an important role in Machine 
        learning. And it happens that you are in search of particular data, which is not easily available, then 
        scraping comes into play. </p>
        <h4><strong>#scraping</strong> <strong>#selenium</strong> <strong>#python</strong> <strong>#numpy</strong>
        <strong>#pandas</strong> <strong>#machinelearning</strong></h4>
    ''', unsafe_allow_html=True)


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
    default()




