import requests
from datetime import datetime, timedelta
import streamlit as st
from PIL import Image
import pandas as pd

def showLatestWinningNumber(round=1000000):
    
    initial_datetime = datetime.strptime('2002-12-07','%Y-%m-%d')
    delta = 7
    round_number_of_today = int((datetime.today() - initial_datetime).days/delta)+1 # for latest round
    if round==1000000:
        val_input = round_number_of_today 
    else:
        val_input = round
    url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}'
    url = url.format(val_input)

    req_result = requests.get(url)
    json_result = req_result.json()
    
    val_return_success = json_result.get('returnValue', None)
    val_drw_dt = json_result.get('drwNoDate', None)
    val_no_1 = json_result.get('drwtNo1', None)
    val_no_1
    val_no_2 = json_result.get('drwtNo2', None)
    val_no_3 = json_result.get('drwtNo3', None)
    val_no_4 = json_result.get('drwtNo4', None)
    val_no_5 = json_result.get('drwtNo5', None)
    val_no_6 = json_result.get('drwtNo6', None)
    val_bonus_no = json_result.get('bnusNo', None)
    
    winning_number = [val_drw_dt,val_no_1,val_no_2,val_no_3,val_no_4,val_no_5,val_no_6,val_bonus_no,val_return_success]
    bonus_number = winning_number[7]
    winning_number = winning_number[1:7]
    if round ==1000000:
        st.header(f"The Latest Round: {round_number_of_today}")
        st.subheader(f"The Latest Winning Numbers: {winning_number}")
        st.subheader(f"The Bonus Number: [{bonus_number}]")
    # image = Image.open('congrats.gif')
    # st.image(image,width=300)
    return (winning_number,bonus_number)

def webCrawling(start,end):
    cum_round_numbers = []
    for r_number in range(start-1,end):
        url = 'https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={}'
        url = url.format(r_number+1)
        req_result = requests.get(url)
        json_result = req_result.json()
        
        val_return_success = json_result.get('returnValue', None)
        val_drw_dt = json_result.get('drwNoDate', None)
        val_no_1 = json_result.get('drwtNo1', None)
        val_no_2 = json_result.get('drwtNo2', None)
        val_no_3 = json_result.get('drwtNo3', None)
        val_no_4 = json_result.get('drwtNo4', None)
        val_no_5 = json_result.get('drwtNo5', None)
        val_no_6 = json_result.get('drwtNo6', None)
        val_bonus_no = json_result.get('bnusNo', None)
        
        temp = (r_number+1,val_drw_dt,val_no_1,val_no_2,val_no_3,val_no_4,val_no_5,val_no_6,val_bonus_no,val_return_success)
        
        cum_round_numbers.append(temp)
    

    df = pd.DataFrame(data=cum_round_numbers,columns=
                    ['number_of_round','date_of_lottery',
                    'number1','number2','number3','number4','number5','number6','bonus','return_value'])

    df = df[['number_of_round','number1','number2','number3','number4','number5','number6','bonus']]
    df.set_index('number_of_round',inplace=True)
    return df



def showWinningNumber():
    initial_datetime = datetime.strptime('2002-12-07','%Y-%m-%d')
    delta = 7
    st.title("Search History")
    number = st.number_input("Please type a round that you want to see. For example, 1000",1)
    winning_number,bonus_number = showLatestWinningNumber(number)
    st.header(f"The Chosen Round: {number}")
    st.subheader(f"The Winning Numbers: {winning_number}")
    st.subheader(f"The Bonus Number: [{bonus_number}]")
    st.header('')
    st.header('Period Selection')
    start_date = st.date_input("Start Date",value= datetime.strptime('2022-01-01','%Y-%m-%d'))
    end_date = st.date_input("End Date")

    start_date = str(start_date) + ' 00-00-00'
    start_date = datetime.strptime(start_date,'%Y-%m-%d %H-%M-%S')
    end_date = str(end_date) + ' 00-00-00'
    end_date = datetime.strptime(end_date,'%Y-%m-%d %H-%M-%S')
    
    # st.write(int((start_date - initial_datetime).days/delta)+1)
    start_round_number = int((start_date - initial_datetime).days/delta)+1
    end_round_number = int((end_date - initial_datetime).days/delta)+1
    # st.write(start_round_number)
    # st.write(end_round_number)
    df = webCrawling(start_round_number,end_round_number)
    st.table(df)


        
