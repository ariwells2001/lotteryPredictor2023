import requests
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense, Bidirectional, Dropout
from tensorflow import keras
from tensorflow.keras.optimizers import Adam
from winning_history import webCrawling
import streamlit as st
import joblib
from keras.models import load_model

def trainingLSTM():
    file_name = 'lottery_2022_12_20.csv'
    df = pd.read_csv(file_name,index_col='number_of_round')

    scaler = StandardScaler()
    transformed_dataset = scaler.fit_transform(df)
    transformed_df = pd.DataFrame(data=transformed_dataset, index=df.index,columns=df.columns)

    number_of_rows = df.shape[0]
    window_length = 7
    number_of_features = df.shape[1]

    X = np.empty([number_of_rows - window_length,window_length,number_of_features],dtype=float)
    y = np.empty([number_of_rows - window_length,number_of_features],dtype=float)

    for i in range(0,number_of_rows-window_length):
        X[i] = transformed_df.iloc[i:i+window_length,0:number_of_features]
        y[i] = transformed_df.iloc[i+window_length:i+window_length+1,0:number_of_features]

    model = Sequential()

    model.add(Bidirectional(LSTM(240,input_shape = (window_length,number_of_features), return_sequences = True)))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features),return_sequences=True)))
    model.add(Bidirectional(LSTM(240, input_shape = (window_length, number_of_features), return_sequences = False)))
    model.add(Dense(59))
    model.add(Dense(number_of_features))



    model.compile(optimizer=Adam(learning_rate=0.001),loss='mse',metrics=['accuracy'])

    model.fit(x=X,y=y,batch_size=100,epochs=100,verbose=2)

    to_predict = df.tail(8)

    to_predict.drop([to_predict.index[-1]],axis=0,inplace=True)

    to_predict = np.array(to_predict)
    scaled_to_predict = scaler.transform(to_predict)
    y_pred = model.predict(np.array([scaled_to_predict]))
    scaler.inverse_transform(y_pred).astype(int)[0]

def showMyLSTM():
    initial_datetime = datetime.strptime('2002-12-07','%Y-%m-%d')
    delta = 7
    st.title("Lucky Numbers Predicted by LSTM")
    round_number_of_today = int((datetime.today() - initial_datetime).days/delta)+1
    start_round_number = round_number_of_today -6
    
    rescaler = joblib.load('scaler.save') 
    remodel = load_model('model_2022_12_22.h5')
    df = webCrawling(start_round_number,round_number_of_today)
    st.subheader("Input Data for Prediction: Previous 7 Week Data")
    st.table(df)
    df.drop(['bonus'],axis=1,inplace=True)
    df = np.array(df.values)
    scaled_to_predict = rescaler.transform(df)
    y_pred = remodel.predict(np.array([scaled_to_predict]))
    lucky_number= rescaler.inverse_transform(y_pred).astype(int)[0]
    st.title(f"Lucky Numbers for # {round_number_of_today+1} would be:")
    st.title(lucky_number)


