import plotly.graph_objects as go
import dateutil
import pandas_ta as pta
import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd


def plotly_table(dataframe):
    headerColor = "grey"
    rowEvenColor ='#f8fafd'
    rowOddColor = '#90d5FF'

    fig = go.Figure(
    data=go.Table(
        header=dict(
            values=["<b><b>"] + ["<b>" + str(i)[:10] + "<b>" for i in dataframe.columns],
            line_color='#0078ff',
            fill_color='#0078ff',
            align='center',
            font=dict(color='white', size=15),height =35,
        ),
        cells=dict(
            values=[["<b>"+str(i)+"<b>" for i in dataframe.index]] +
            [dataframe[i] for i in dataframe.columns],
            fill_color=[
                [
                    rowOddColor if i % 2 == 0 else rowEvenColor
                    for i in range(len(dataframe))
                ]
            ] * (len(dataframe.columns) + 1),
            align='left',
            line_color='white',
            font=dict(color='black', size=15)
        )

    )
)
    fig.update_layout( height= 400, margin=dict(l=0, r=0, t=0, b=0))
    return fig


def filter_data(dataframe, numperiod):

    # Ensure DatetimeIndex
    dataframe.index = pd.to_datetime(dataframe.index)

    last_date = dataframe.index[-1]

    if numperiod == '1mo':
        date = last_date - relativedelta(months=1)

    elif numperiod == '5d':
        date = last_date - relativedelta(days=5)

    elif numperiod == '6mo':
        date = last_date - relativedelta(months=6)

    elif numperiod == '1y':
        date = last_date - relativedelta(years=1)

    elif numperiod == '5y':
        date = last_date - relativedelta(years=5)

    elif numperiod == 'yth':  # Year Till Today
        date = datetime.datetime(last_date.year, 1, 1)

    else:
        date = dataframe.index[0]

    df = dataframe.reset_index()
    return df[df['Date'] > date]

def close_chart(dataframe, num_period = False):
    if num_period:
        dataframe = filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open',line = dict( width=2,color = "#90d5FF")))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close',line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict( width=2,color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='High', line=dict( width=2,color='red')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white',paper_bgcolor='#90d5FF', legend=dict(
        yanchor="top",
        xanchor="right"
    ))
    return fig
def candlestick(datafram, numperiod):
    datafram = filter_data(datafram,numperiod)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(
        x=datafram['Date'],
        open=datafram['Open'],
        high=datafram['High'],
        low=datafram['Low'],
        close=datafram['Close']
        ))
    
    fig.update_layout(showlegend= False,height = 500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white',paper_bgcolor='#90d5FF')
    return fig
def RSI(dataframe, num_period):
    dataframe['RSI'] = pta.rsi(dataframe['Close'])
    dataframe= filter_data(dataframe,num_period)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, name = 'RSI', marker_color="orange",line=dict(width=2,color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe.RSI, name='RSI', marker_color='orange',line=dict(width=2,color='orange'),
    ))
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[70]*len(dataframe), name='Overbought', marker_color='red',line=dict(width=2,color='red',dash='dash'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=[30]*len(dataframe),
        fill='tonexty',
        name='Oversold',
        marker_color='#79da84',
        line=dict(width=2,color='#79da84',dash='dash')
        ))

    fig.update_layout(yaxis_range=[0,100],
        height=200,plot_bgcolor='white',paper_bgcolor='#90d5FF',margin=dict(l=0, r=0, b=0),legend=dict(orientation="h",
    yanchor="top",
    y=1.02,
    xanchor="right",
    
    x=1
    )
    )
    return fig

def Moving_average(dataframe,num_period):

    dataframe['SMA_50'] = pta.sma(dataframe['Close'], 50)
    dataframe=filter_data(dataframe,num_period)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Open'],
                             mode='lines',
                             name='Open',line = dict( width=2,color = '#5ab7ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Close'],
                             mode='lines',
                             name='Close',line = dict( width=2,color = 'black')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['High'],
                             mode='lines', name='High', line=dict( width=2,color='#0078ff')))
    fig.add_trace(go.Scatter(x=dataframe['Date'], y=dataframe['Low'],
                             mode='lines', name='High', line=dict( width=2,color='red')))
    fig.add_trace(go.Scatter(x=dataframe['Date'],  y=dataframe['SMA_50'],
                             mode='lines', name='SMA 50', line=dict(width=2,color='purple')))
    
    fig.update_xaxes(rangeslider_visible=True)
    fig.update_layout(height=500,margin=dict(l=0, r=20, t=20, b=0), plot_bgcolor='white',paper_bgcolor='#90d5FF', legend=dict(
        yanchor="top",
        xanchor="right"
    ))
    return fig

def MACD(dataframe, num_period):
    macd = pta.macd(dataframe['Close']).iloc[:,0]
    macd_signal = pta.macd(dataframe['Close']).iloc[:,1]
    macd_hist = pta.macd(dataframe['Close']).iloc[:,2]
    dataframe['MACD'] = macd
    dataframe['MACD Signal'] = macd_signal
    dataframe['MACD Hist'] = macd_hist
    dataframe= filter_data(dataframe,num_period)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD'], name = 'MACD', marker_color="orange",line=dict(width=2,color='orange'),
    ))

    fig.add_trace(go.Scatter(
        x=dataframe['Date'],
        y=dataframe['MACD Signal'],name='Overbought', marker_color='red',line=dict(width=2,color='red',dash='dash'),
    ))
    c = ['red' if cl <0 else "green" for cl in macd_hist]
    
    fig.update_layout(
    height=200,
    plot_bgcolor='white',        # background for plot
    paper_bgcolor='#90d5FF',     # correct hex, single #
    margin=dict(l=0, r=0, b=0),
    legend=dict(
        orientation="h",
        yanchor="top",
        y=1.02,
        xanchor="right",
        x=1
        )
        )
    
    return fig

# def Moving_average_forecast(forecast):
#     fig = go.Figure()

#     fig.add_trace(go.Scatter(x=forecast.index[:-30], y=forecast['Close'].iloc[:-30],
#                              mode='lines',
#                              name='Close Price', line=dict(width=2,color='black')))
#     fig.update_xaxes(rangeslider_visible=True)
#     fig.update_layout(height=500,margin=dict(l=0, t=20, b=0), plot_bgcolor='white', paper_bgcolor='#fffd8d',
#                       legend=dict(
#                           yanchor="top",
#                           xanchor="right",
#                           ))
#     return fig 

def Moving_average_forecast(data):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',  # 'lines+markers' also works
        name='Close Price'
    ))
    fig.update_layout(
        title='Stock Close Price Forecast',
        xaxis_title='Date',
        yaxis_title='Close Price',
        template='plotly_white'
    )
    return fig