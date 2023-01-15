import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime,timedelta
from tqdm import tqdm
from PIL import Image
from winning_history import showLatestWinningNumber,showWinningNumber
from winning_ml import showMyLSTM


# Setting up sidebar menu

image = Image.open('ariwells-logo.png')
st.sidebar.image(image,width = 100)
st.sidebar.title("Korean Lotto Predictor-LSTM")

page=st.sidebar.selectbox("",("Choose a menu","Latest Winning No.","Search History","Lucky Numbers","Extra") )
if page == "Latest Winning No.":
    showLatestWinningNumber()
elif page == "Choose a menu":
    st.title("Welcome to Korean Lotto Predictor")
    st.header("Programmed by Ariwells")
    st.image(image,width = 400)
elif page == 'Search History':
    showWinningNumber()
elif page == 'Lucky Numbers':
    showMyLSTM()
