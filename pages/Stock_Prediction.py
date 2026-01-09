import streamlit as st
from pages.Utils.model_train import get_data, get_rolling_mean, get_differencing_order, scalling, evaluate_model, get_forecast, inverse_scaling, fit_model, stationery_check
import pandas as pd
from pages.Utils.plotly_figure import plotly_table, Moving_average_forecast
import numpy as np

st.set_page_config(
    page_title="Stock Prediction",
    page_icon="chart_with_downwards_trend",
    layout="wide",
    )

col1, col2, col3 = st.columns(3)

with col1:
    ticker = st.text_input('Stock Ticker', 'AAPL')

rmse = 0

st.subheader('Predicting Next 30 days close Price for: '+ ticker)

close_price = get_data(ticker)
rolling_price = get_rolling_mean(close_price)

differencing_order = get_differencing_order(rolling_price)
scaled_data, scalar = scalling(rolling_price)

rmse = evaluate_model(scaled_data, differencing_order)

st.write("**Model RSME Score:**",rmse)

forecast = get_forecast(scaled_data, differencing_order)

forecast['Close'] = inverse_scaling( scalar, forecast['Close'])

st.write('#### Forecast Data (Next 30 days)')
fig_tail = plotly_table(forecast.sort_index(ascending = True).round(3))
fig_tail.update_layout(height = 220)
st.plotly_chart(fig_tail, use_container_width=True)

forecast = pd.concat([rolling_price, forecast])

# st.plotly_chart(fig_tail, width='stretch')
# st.plotly_chart(Moving_average_forecast(forecast.iloc[150:]), width='stretch') 

st.plotly_chart(
    fig_tail,
    width='stretch',
    key='forecast_table_chart'
)
st.plotly_chart(
    Moving_average_forecast(forecast.iloc[150:]),
    width='stretch',
    key='moving_average_forecast_chart'
)
