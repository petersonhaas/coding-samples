# Author: Peterson Haas
# Description: This program uses FRED APIs to search for economic data

import streamlit as st
import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta
import requests 
import json
from io import BytesIO
import io
import plotly.graph_objs as go

# Set up the keys
FREDAPIKey = "150fdf7814c5596d0e8baeb1c5ad7636"
#FREDAPIKey = st.secrets["fedKey"]

tab1, tab2 = st.tabs(["Snapshot", "Finder"])


with tab2:

    # Add a title
    st.title("Economic Data Finder", anchor = False)

    # Add a description
    st.write("Explore a wide range of global economic indicators. Easily search for indicators by browsing titles, country names, currencies, specific IDs, and more. Whether interested in GDP, job numbers, or prices, this platform simplifies access to crucial information, helping you to make well-informed decisions. It currently supports data from the US Federal Reserve database (FRED).", anchor = False)

    # Create columns to display the search bar, filter bar, and color picker
    colA1, colA2, colA3 = st.columns([4,9,1])                     

    # Add search bar
    with colA1: 
        search_field = st.text_input("Search:",placeholder = "E.g. US GDP, M2 Brazil... ")

    # Load and extract economic series from FRED
    FREDresponse = requests.get(f"https://api.stlouisfed.org/fred/series/search?search_text={search_field}&api_key={FREDAPIKey}&file_type=json")
    FREDDict = json.loads(FREDresponse.content.decode('utf-8'))
    series_data = FREDDict.get('seriess', [])

    # Extract titles for the dropdown filter bar
    sorted_titles = sorted(series_data, key=lambda x: x['popularity'], reverse=True)
    titles = []
    titles = titles+[series['title'] for series in sorted_titles]   


    # Get series ID based on the selected title
    selected_id = None
    selected_id_2 = None
        
    if search_field:
        
        # Display dropdown filter bar
        if search_field:
            with colA2: 
                selected_title = st.selectbox("Select an Indicator:", titles)

        # Get and display economic data from the selected series
        selected_series = next((series for series in series_data if series['title'] == selected_title), None)
        if selected_series:
            selected_id = selected_series.get('id')
            
            # Add color picker
            with colA3:
                line_color = st.color_picker('Color', '#346FD0',label_visibility='hidden')
            
            # Get the response from the API and convert to dictionary
            JSONResponse = requests.get(f"https://api.stlouisfed.org/fred/series/observations?series_id={selected_id}&api_key={FREDAPIKey}&file_type=json").text
            DictResponse = json.loads(JSONResponse)
            
            # Parse the dictionary and print information
            listOfData = DictResponse['observations']
            for theData in listOfData:
                theDate = theData['date']
                theValue = theData['value']
                
            # Create dataframe with date and value columns
            df = pd.DataFrame(listOfData)
            df = df[['date','value']]
                
            # Replace empty strings with NaN
            df['value'] = df['value'].replace('.', np.nan)
            df['date'] = df['date'].replace('.', np.nan)

            # Convert variables into the appropriate types
            df['date'] = df['date'].astype('datetime64[ns]')
            df['value'] = df['value'].astype('float')

            # Sort and round values
            df = df.sort_values(by='date', ascending=False)
            df['value'] = df['value'].round(1)
            df = df.reset_index(drop=True)

            # Define filtered dataframe and timeseries 
            df_filtered = df

            timeseries = ""
        
        
            # Repeat the same process for the second indicator (optional input)
            with colA1: 
                search_field_2 = st.text_input("Compare:", placeholder = 'Optional')
                
            FREDresponse_2 = requests.get(f"https://api.stlouisfed.org/fred/series/search?search_text={search_field_2}&api_key={FREDAPIKey}&file_type=json")
            FREDDict_2 = json.loads(FREDresponse_2.content.decode('utf-8'))
            series_data_2 = FREDDict_2.get('seriess', [])
            
            sorted_titles_2 = sorted(series_data_2, key=lambda x: x['popularity'], reverse=True)
            titles_2 = []
            titles_2 = titles_2+[series['title'] for series in sorted_titles_2] 
            
            with colA2:
                selected_title_2 = st.selectbox("",titles_2, placeholder = 'Optional')
            
            if selected_title_2:
                selected_series_2 = next((series for series in series_data_2 if series['title'] == selected_title_2), None)
                selected_id_2 = selected_series_2.get('id')

                with colA3:
                    st.write("\n\n")
                    line_color_2 = st.color_picker('', '#FF8600',label_visibility='hidden')
                    
                JSONResponse_2 = requests.get(f"https://api.stlouisfed.org/fred/series/observations?series_id={selected_id_2}&api_key={FREDAPIKey}&file_type=json").text
                DictResponse_2 = json.loads(JSONResponse_2)
                listOfData_2 = DictResponse_2['observations']
                
                for theData_2 in listOfData_2:
                    theDate_2 = theData_2['date']
                    theValue_2 = theData_2['value']
                    
                df_2 = pd.DataFrame(listOfData_2)
                df_2 = df_2[['date','value']]
                df_2['value'] = df_2['value'].replace('.', np.nan)
                df_2['date'] = df_2['date'].replace('.', np.nan)
                df_2['date'] = df_2['date'].astype('datetime64[ns]')
                df_2['value'] = df_2['value'].astype('float')
                df_2 = df_2.sort_values(by='date', ascending=False)
                df_2['value'] = df_2['value'].round(1)
                df_2 = df_2.reset_index(drop=True)
                df_filtered_2 = df_2

            
            # Create columns for the expander
            colA, colB, colC, colD, colE, colF = st.columns(6)
            
            def generate_plot(df, timeseries):
                """
                Generates a personalized chart based on an expander with advanced settings
                Arguments:
                    df: dataframe with dates and values for the selected economic indicator
                    timeseries: selected time range to be displayed in the chart
                Returns:
                    fig: line chart
                """
                
                # define time ranges
                current_date = datetime.now()
                one_year_ago = current_date - timedelta(days=365)
                five_years_ago = current_date - timedelta(days=5*365)
                ten_years_ago = current_date - timedelta(days=10*365)

                # Create and expander with multiple options to personalize the chart                
                with st.expander("Advanced Settings"):
                    # Create columns for the expander
                    colC1, colC2, colC3 = st.columns([1,2,4])
                    # Create radio button with time series and chart style options
                    with colC1:
                        timeseries = st.radio("Time series", ["Max","10Y", "5Y", "1Y"])
                        chart_style = st.radio('Chart Style',('Gray', 'Blue','White'))
                        if chart_style == "White":
                            chart_style_color = "white"
                        elif chart_style == "Blue":
                            chart_style_color = "rgb(224,235,255)"
                        elif chart_style == "Gray":
                            chart_style_color = 'rgb(240,242,246)'
                            
                    # Create toggles to add data labels, grids, US recession bars, area fill, autoscale,y=0 line
                    with colC2:
                        data_labels = st.toggle('Data labels')
                        vertical_grid = st.toggle('Vertical Grid')
                        horizontal_grid = st.toggle('Horizontal Grid')
                        recession_bars = st.toggle('US Recession Bars',value = True)
                        chart_area = st.toggle('Chart Area')
                        autoscale = st.toggle('Autoscale')
                        y_zero = st.toggle('y = 0',value = True)

                    # Create text bars to include a chart title and y-axis title
                    with colC3:
                        chart_title = st.text_input("Title:")
                        colD1, colD2 = st.columns([1,1])
                        with colD1:
                            series_name = st.text_input("1st Series Name",value=f"{selected_series.get('title')}")
                            if selected_title_2:
                                series_name_2 = st.text_input("2nd Series Name",value=f"{selected_series_2.get('title')}")
                        with colD2:
                            y_axis_units = st.text_input("Units:",value=f"{selected_series.get('units')}",key="units1")
                            if selected_title_2:
                                y_axis_units_2 = st.text_input("Units:",value=f"{selected_series_2.get('units')}",key="units2")

                # Filter dataframe based on selected time range
                if timeseries == "1Y":
                    df_filtered = df[df['date'] >= one_year_ago]
                elif timeseries == "5Y":
                    df_filtered = df[df['date'] >= five_years_ago]
                elif timeseries == "10Y":
                    df_filtered = df[df['date'] >= ten_years_ago]
                else:
                    df_filtered = df
                
                if selected_title_2:
                    if timeseries == "1Y":
                        df_filtered_2 = df_2[df_2['date'] >= one_year_ago]
                    elif timeseries == "5Y":
                        df_filtered_2 = df_2[df_2['date'] >= five_years_ago]
                    elif timeseries == "10Y":
                        df_filtered_2 = df_2[df_2['date'] >= ten_years_ago]
                    else:
                        df_filtered_2 = df_2

                # Create a line chart to display the first indicator
                fig = px.line(template='simple_white')
                fig.add_scatter(
                    x=df_filtered['date'], 
                    y=df_filtered['value'], 
                    mode='lines', 
                    name=selected_title, 
                    line=dict(color=line_color),
                    yaxis='y1')
                    
                fig.update_traces(name=series_name)
                fig.update_layout(yaxis_title=f"{y_axis_units}")
                fig.update_layout(xaxis_title="")
                fig.update_yaxes(tickformat=',') 
                fig.update_layout(title=f"{chart_title}",title_x=0.5,title_xanchor='center')
                
                # Add second indicator in the chart
                if selected_title_2:
                    y_axis_units_2=f"{selected_series_2.get('units')}"
                    fig.add_scatter(
                        x=df_filtered_2['date'], 
                        y=df_filtered_2['value'], 
                        mode='lines', 
                        name=series_name_2, 
                        line=dict(color=line_color_2),
                        yaxis='y2')
                    
                    fig.update_layout(yaxis2=dict(title=y_axis_units,overlaying='y',side='right'))

                # Add a legend
                fig.update_layout(
                    legend=dict(
                        orientation="v", 
                        yanchor="top", 
                        y=-0.1, 
                        xanchor="left",  
                        x=0),
                        margin=dict(l=40, r=40, t=40, b=40), 
                        xaxis=dict(showline=True, linecolor='black'), 
                        yaxis=dict(showline=True, linecolor='black'),  
                        paper_bgcolor=chart_style_color)
                
                # Set hover mode
                fig.update_layout(hovermode="x unified")
                if not selected_title_2:
                    fig.update_yaxes(showspikes=True)
                
                # Define horizontal and vertical grids
                if horizontal_grid:
                    horizontal_grid2 = True
                else:
                    horizontal_grid2 = False
                    
                if vertical_grid:
                    vertical_grid2 = True
                else:
                    vertical_grid2 = False
                fig.update_layout(xaxis_showgrid=vertical_grid2, yaxis_showgrid=horizontal_grid2)

                # Define data labels
                if data_labels:
                    fig.update_traces(mode='lines+markers+text', text=df_filtered['value'], textposition='top center')
                    
                # Define not autoscale
                if autoscale == False:
                    if not selected_title_2:
                        y_min = df_filtered['value'].min()
                        y_max = df_filtered['value'].max()
                        fig.update_yaxes(range=[y_min,y_max])
                    else:
                        y_min = min([df_filtered['value'].min(),df_filtered_2['value'].min()])
                        y_max = max([df_filtered['value'].max(),df_filtered_2['value'].max()])
                        fig.update_yaxes(range=[y_min,y_max])

                else:
                    if not selected_title_2:
                        y_min = df_filtered['value'].min()
                        y_max = df_filtered['value'].max()
                    else:
                        y_min = min([df_filtered['value'].min(),df_filtered_2['value'].min()])
                        y_max = min([df_filtered['value'].max(),df_filtered_2['value'].max()])
                
                # Define y = 0
                if y_zero:
                    y_min = 0
                    
                # Get dates and define US recession bars
                if recession_bars:
                    recessions =requests.get('https://data.nber.org/data/cycles/business_cycle_dates.json')
                    economic_cycles = recessions.json()
                    
                    # Convert 'peak' and 'trough' dates to datetime 
                    for period in economic_cycles:
                        period['peak'] = pd.to_datetime(period['peak'])
                        period['trough'] = pd.to_datetime(period['trough'])

                    # Filter recession periods that fall within the date range
                    filtered_cycles = []
                    for period in economic_cycles:
                        if period['peak'] >= df_filtered['date'].min():
                            filtered_cycles.append(period)

                    # Add recession bars to the chart layout
                    for period in filtered_cycles:
                        fig.add_shape(
                            type='rect',
                            x0=period['peak'],
                            y0= y_min,
                            x1=period['trough'],
                            y1=y_max,
                            fillcolor='rgba(0, 0, 0, 0.3)',
                            layer='below',
                            line=dict(width=0))
                
                # Define chart footnote    
                fig.add_annotation(
                    text="Source: FRED",
                    xref='paper', yref='paper',
                    x=1, y=-0.175, 
                    showarrow=False,
                    font=dict(size=10, color='grey'))
                
                # Define chart area
                if chart_area:
                    fig.update_traces(fill='tozeroy')
                    
                # Add a red line at y=0 
                if (df_filtered['value'] < 0).any():
                    fig.add_shape(type="line", x0=min(df_filtered['date']), x1=max(df_filtered['date']), y0=0, y1=0,line=dict(color="red", width=2))
                
                return fig
            
            # Return function to generate plot
            fig = generate_plot(df_filtered, timeseries)
    
            # Create sidebar to display the dataframe
            st.sidebar.header(selected_title)
            
            # Display 1st dataframe in the sidebar
            df_sidebar = df
            df_sidebar['date'] = pd.to_datetime(df_sidebar['date']).dt.date
            df_sidebar['date'] = pd.to_datetime(df_sidebar['date'], format='%Y-%m-%d')
            df_sidebar['date'] = df_sidebar['date'].dt.strftime('%m/%d/%Y')
            df_sidebar_display = df_sidebar.head(5).reset_index(drop=True)
            df_sidebar_display.index += 1
            st.sidebar.write(df_sidebar_display)

            # Create 2 columns in the sidebar
            colB1, colB2 = st.sidebar.columns(2)

            # Display option to dowload the 1st dataframe
            with colB1:
                file_format_df = st.selectbox("",["CSV"],format_func=lambda x: x,label_visibility = "collapsed", key='bb1')
            
            with colB2:
                if file_format_df == "CSV":
                    file_df = df_filtered.to_csv(index=False)
                    st.download_button("Download", file_df, file_name='data',key = 'b1')

            # Display 2nd dataframe in the sidebar
            if selected_title_2:    
                st.sidebar.header(selected_title_2)
                df_sidebar_2 = df_2
                df_sidebar_2['date'] = pd.to_datetime(df_sidebar_2['date']).dt.date
                df_sidebar_2['date'] = pd.to_datetime(df_sidebar_2['date'], format='%Y-%m-%d')
                df_sidebar_2['date'] = df_sidebar_2['date'].dt.strftime('%m/%d/%Y')
                df_sidebar_2_display = df_sidebar_2.head(5).reset_index(drop=True)
                df_sidebar_2_display.index += 1
                st.sidebar.write(df_sidebar_2_display)

                # Create 2 columns in the sidebar
                colBB1, colBB2 = st.sidebar.columns(2)

                # Display option to dowload the 2nd dataframe
                with colBB1:
                    file_format_df_2 = st.selectbox("",["CSV"],format_func=lambda x: x,label_visibility = "collapsed",key='bb2')

                with colBB2:
                    if file_format_df_2 == "CSV":
                        file_df_2 = df_filtered_2.to_csv(index=False)
                        st.download_button("Download", file_df_2, file_name='data',key = 'b2')

            # Display information regarding the selected economic series
            if selected_title_2:
                st.markdown("<hr>", unsafe_allow_html=True) # Horizontal line
                st.markdown(f"<h3 style='text-align: center;'>{selected_title} vs. {selected_title_2}</h3>", unsafe_allow_html=True)
                colNull, col0, col1, col2, col3, col4 = st.columns([2,2,10,8,9,3])
                with col0:
                    st.markdown(f"<b style='text-align: left;'>1.</b>", unsafe_allow_html=True)
                    st.markdown(f"<b style='text-align: left;'>2.</b>", unsafe_allow_html=True)
                with col1:
                    st.write("ID:", selected_series.get('id'))
                    st.write("ID:", selected_series_2.get('id'))
                with col2:
                    st.write("Frequency:", selected_series.get('frequency'))
                    st.write("Frequency:", selected_series_2.get('frequency'))
                with col3:
                    st.write("Units:", selected_series.get('units_short'))
                    st.write("Units:", selected_series_2.get('units_short'))
                with col4:
                    st.write(f"{selected_series.get('seasonal_adjustment_short')}")
                    st.write(f"{selected_series_2.get('seasonal_adjustment_short')}")
                st.write(fig) 
                
                st.markdown("<hr>", unsafe_allow_html=True) # Horizontal line
                st.markdown(f"<h5 style='text-align: left;'>{selected_title}</h3>", unsafe_allow_html=True)
                st.write("Last Updated:", selected_series.get('last_updated'))
                st.write("Notes:", selected_series.get('notes'))

                st.markdown("<hr>", unsafe_allow_html=True) # Horizontal line
                st.markdown(f"<h5 style='text-align: left;'>{selected_title_2}</h3>", unsafe_allow_html=True)
                st.write("Last Updated:", selected_series_2.get('last_updated'))
                st.write("Notes:", selected_series_2.get('notes'))
                st.markdown("Source: [FRED](https://fred.stlouisfed.org/)")

                st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
                st.markdown(f"<h6 style='text-align: center;'>© 2023 Peterson Haas. All rights reserved.</h6>",unsafe_allow_html=True)
                
            else:
                st.markdown("<hr>", unsafe_allow_html=True) # Horizontal line
                st.markdown(f"<h3 style='text-align: center;'>{selected_title}</h3>", unsafe_allow_html=True)
                colNull, col0, col1, col2, col3, col4 = st.columns([2,2,10,8,9,3])
                with col1:
                    st.write("ID:", selected_series.get('id'))
                with col2:
                    st.write("Frequency:", selected_series.get('frequency'))
                with col3:
                    st.write("Units:", selected_series.get('units_short'))
                with col4:
                    st.write(f"{selected_series.get('seasonal_adjustment_short')}")
                st.write(fig) 
                st.markdown("<hr>", unsafe_allow_html=True) # Horizontal line
                st.write("Last Updated:", selected_series.get('last_updated'))
                st.write("Notes:", selected_series.get('notes'))
                st.markdown("Source: [FRED](https://fred.stlouisfed.org/)")

                st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
                st.markdown(f"<h6 style='text-align: center;'>© 2023 Peterson Haas. All rights reserved.</h6>",unsafe_allow_html=True)


with tab1:

    series_id = {"GDP": {"title": "GDP",
                         "sub": None,
                         "description":"Nominal GDP (Quarterly)",
                         "source":"U.S. Bureau of Economic Analysis",
                         "link":"https://www.bea.gov/data/gdp/gross-domestic-product"},
                 "GDPC1": {"title": "Real GDP",
                           "sub": None,
                           "description":"Real GDP (Quarterly)",
                           "source":"U.S. Bureau of Economic Analysis",
                           "link":"https://www.bea.gov/data/gdp/gross-domestic-product"},
                 "A191RL1Q225SBEA": {"title": "GDP Growth",
                                     "sub": None,
                                     "description":"Real GDP Growth (Quarterly)",
                                     "source":"U.S. Bureau of Economic Analysis",
                                     "link":"https://www.bea.gov/data/gdp/gross-domestic-product"},
                 "M2SL": {"title": "M2 Money Supply",
                          "sub": "M2",
                          "description":"M2 Money Supply (Monthly, SA)",
                          "source":"Federal Reserve",
                          "link":"https://www.federalreserve.gov/releases/h6/current/default.htm"},
                 "M1SL": {"title": "M1 Money Supply",
                          "sub": "M1",
                          "description":"M1 Money Supply (Monthly, SA)",
                          "source":"Federal Reserve",
                          "link":"https://www.federalreserve.gov/releases/h6/current"},
                 "BOGMBASE": {"title": "Monetary Base",
                          "sub": "M0",
                          "description":"M0 - Monetary Base (Monthly, NSA)",
                          "source":"Federal Reserve",
                          "link":"https://www.federalreserve.gov/releases/h6/current"},
                 "BOGMBBM": {"title": "Reserve Balances",
                          "sub": "Reserve Balances",
                          "description":"Reserve Balances with Federal Reserve Banks (Monthly, NSA)",
                          "source":"Federal Reserve",
                          "link":"https://www.federalreserve.gov/releases/h6/current"},
                 "MBCURRCIR": {"title": "In Circulation",
                          "sub": "Currency in Circulation",
                          "description":"Currency in Circulation (Monthly, NSA)",
                          "source":"Federal Reserve",
                          "link":"https://www.federalreserve.gov/releases/h6/current"},
                 "UNRATE": {"title": "Unemployment",
                            "sub": "Unemployment Rate",
                            "description":"Unemployment Rate (Monthly, SA)",
                            "source":"U.S. Bureau of Labor Statistics",
                            "link":"https://data.bls.gov/timeseries/LNS14000000"},
                 "CIVPART": {"title": "Participation Rate",
                            "sub": "Labor Force Participation Rate",
                            "description":"Labor Force Participation Rate (Monthly)",
                            "source":"U.S. Bureau of Labor Statistics",
                            "link":"https://data.bls.gov/timeseries/LNS11300000"},
                 "EMRATIO": {"title": "Emp-Pop Ratio",
                            "sub": "Employment-Population Ratio",
                            "description":"Employment-Population Ratio (Monthly)",
                            "source":"U.S. Bureau of Labor Statistics",
                            "link":"https://data.bls.gov/timeseries/LNS12300000"},
                 "ICSA": {"title": "Jobless Claims",
                            "sub": "Initial Unemployment Claims",
                            "description":"Unemployment Initial Claims (Weekly, SA)",
                            "source":"U.S. Department of Labor",
                            "link":"https://www.dol.gov/newsroom/releases"},
                 "CPIAUCSL": {"title": "Inflation",
                              "sub": "Headline CPI",
                              "description":"Headline CPI - All Items (Monthly, NSA)",
                              "source":"U.S. Bureau of Labor Statistics",
                              "link":"https://www.bls.gov/cpi/home.htm"},
                 "CPILFESL": {"title": "Inflation",
                              "sub": "Core CPI",
                              "description":"Core CPI - All Items Less Food and Energy (Monthly, NSA)",
                              "source":"U.S. Bureau of Labor Statistics",
                              "link":"https://www.bls.gov/cpi/home.htm"},
                 "PPIFIS": {"title": "PPI",
                              "sub": "PPI",
                              "description":"Producer Price Index (Monthly, NSA)",
                              "source":"U.S. Bureau of Labor Statistics",
                              "link":"https://www.bls.gov/ppi/home.htm"},
                 "FEDFUNDS": {"title": "Interest Rate",
                              "sub": "Fed Funds Rate",
                              "description":"Effective Federal Funds Rate (EFFR)",
                              "source":"Federal Reserve",
                              "link":"https://www.federalreserve.gov/releases/h15/"},
                 "PCEPI": {"title": "Inflation",
                              "sub": "Headline PCE",
                              "description":"PCE Price Index (Monthly, SA)",
                              "source":"U.S. Bureau of Economic Analysis (BEA)",
                              "link":"https://www.bea.gov/data/personal-consumption-expenditures-price-index"},
                 "PCEPILFE": {"title": "Inflation",
                              "sub": "Core PCE",
                              "description":"PCE Price Index Excluding Food and Energy (Monthly, SA)",
                              "source":"U.S. Bureau of Economic Analysis (BEA)",
                              "link":"https://www.bea.gov/data/personal-consumption-expenditures-price-index"},
                 "POPTHM": {"title": "Population",
                              "sub": "Population",
                              "description":"Population (Monthly, NSA)",
                              "source":None,
                              "link":None},
                 "HOUST": {"title": "Housing Starts",
                              "sub": "Housing Starts",
                              "description":"New Residential Construction (Monthly, SAAR)",
                              "source":"Census",
                              "link":"https://www.census.gov/economic-indicators/"},
                 "MORTGAGE30US": {"title": "30Y FRM",
                              "sub": "Mortgage Rates (30Y)",
                              "description":"30-Year Fixed Mortgage Rate (Weekly, NSA)",
                              "source":"Freddie Mac",
                              "link":"https://www.freddiemac.com/pmms"},
                 "MORTGAGE15US": {"title": "15Y FRM",
                              "sub": "Mortgage Rates (15Y)",
                              "description":"15-Year Fixed Mortgage Rate (Weekly, NSA)",
                              "source":"Freddie Mac",
                              "link":"https://www.freddiemac.com/pmms"}}


    data_dict = {}
    

    for i in series_id:
        FREDresponse = requests.get(f"https://api.stlouisfed.org/fred/series/observations?series_id={i}&api_key={FREDAPIKey}&file_type=json").text
        DictResponse = json.loads(FREDresponse)
        listOfData = DictResponse['observations']

        curr_value = float(listOfData[-1]['value']) 
        prev_value = float(listOfData[-2]['value']) 
        prev_value_3 = float(listOfData[-3]['value']) 
        year_ago_value = float(listOfData[-13]['value']) 
        year_ago_value_2 = float(listOfData[-14]['value']) 
        period1 = ((curr_value-prev_value)/prev_value)*100  
        period2= ((prev_value-prev_value_3)/prev_value_3)*100
        curr_date=datetime.strptime(listOfData[-1]['date'], '%Y-%m-%d').date()
        curr_date2 = curr_date.strftime("%b %Y")
        annual_change = float(f"{(((curr_value - year_ago_value)/year_ago_value)*100):.1f}")
        annual_change_2 = float(f"{(((prev_value - year_ago_value_2)/year_ago_value_2)*100):.1f}")
       

        data_dict[i] = {
            "id": series_id[i],
            "title": series_id[i]['title'],
            "sub": series_id[i]['sub'],
            "source": series_id[i]['source'],
            "link": series_id[i]['link'],
            "curr_value": curr_value,
            "curr_date": curr_date,
            "prev_value": prev_value,
            "prev_date": datetime.strptime(listOfData[-2]['date'], '%Y-%m-%d').date(),
            "perc_change": str(float(f"{(((curr_value - prev_value)/prev_value)*100):.1f}"))+"%",
            "nominal_change": round(curr_value - prev_value,1),
            "annual_change": str(annual_change)+"%",
            "annual_change_2": str(annual_change_2)+"%",
            "period_change": str(float(f"{(period1-period2):.1f}")),
            "period_change_2": str(float(f"{(annual_change-annual_change_2):.1f}")),
            "period1": str(f"{period1:.1f}%"),
            "period2": str(f"{period2:.1f}%"),
            "help":f"{series_id[i]['description']} \n\nLast Updated: {curr_date2}\n\nSource: [{series_id[i]['source']}]({series_id[i]['link']}) \n\n ID: {i}"
            }


    st.title("Economic Outlook", anchor = False)

    st.subheader('Overview', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["A191RL1Q225SBEA"]["title"], str(data_dict["A191RL1Q225SBEA"]["curr_value"])+"%", str(data_dict["A191RL1Q225SBEA"]["nominal_change"])+" (QoQ)",help=data_dict["A191RL1Q225SBEA"]["help"])
    col2.metric(data_dict["GDP"]["title"], str(round(data_dict["GDP"]["curr_value"]/1000,2))+"T", str(data_dict["GDP"]["perc_change"])+" (QoQ)",help=data_dict["GDP"]["help"])
    col3.metric(data_dict["FEDFUNDS"]["title"], str(round(data_dict["FEDFUNDS"]["curr_value"],1))+"%", str(data_dict["FEDFUNDS"]["nominal_change"])+" (MoM)",delta_color="inverse",help=data_dict["FEDFUNDS"]["help"])
    col4.metric(data_dict["PCEPILFE"]["title"], data_dict["PCEPILFE"]["annual_change"], str(data_dict["PCEPILFE"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["PCEPILFE"]["help"])
    col5.metric(data_dict["UNRATE"]["title"], str(data_dict["UNRATE"]["curr_value"])+"%", str(data_dict["UNRATE"]["nominal_change"])+" (MoM)",delta_color="inverse",help=data_dict["UNRATE"]["help"])

    st.subheader('Prices', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["PCEPILFE"]["sub"], data_dict["PCEPILFE"]["period1"], str(data_dict["PCEPILFE"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["PCEPILFE"]["help"])
    col2.metric(data_dict["PCEPILFE"]["sub"], data_dict["PCEPILFE"]["annual_change"], str(data_dict["PCEPILFE"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["PCEPILFE"]["help"])
    col3.metric(data_dict["PCEPI"]["sub"], data_dict["PCEPI"]["period1"], str(data_dict["PCEPI"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["PCEPI"]["help"])
    col4.metric(data_dict["PCEPI"]["sub"], data_dict["PCEPI"]["annual_change"], str(data_dict["PCEPI"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["PCEPI"]["help"])

    col1.metric(data_dict["CPILFESL"]["sub"], data_dict["CPILFESL"]["period1"], str(data_dict["CPILFESL"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["CPILFESL"]["help"])
    col2.metric(data_dict["CPILFESL"]["sub"], data_dict["CPILFESL"]["annual_change"], str(data_dict["CPILFESL"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["CPILFESL"]["help"])
    col3.metric(data_dict["CPIAUCSL"]["sub"], data_dict["CPIAUCSL"]["period1"], str(data_dict["CPIAUCSL"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["CPIAUCSL"]["help"])
    col4.metric(data_dict["CPIAUCSL"]["sub"], data_dict["CPIAUCSL"]["annual_change"], str(data_dict["CPIAUCSL"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["CPIAUCSL"]["help"])

    col1.metric(data_dict["PPIFIS"]["sub"], data_dict["PPIFIS"]["period1"], str(data_dict["PPIFIS"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["PPIFIS"]["help"])
    col2.metric(data_dict["PPIFIS"]["sub"], data_dict["PPIFIS"]["annual_change"], str(data_dict["PPIFIS"]["period_change_2"])+" (YoY)",delta_color="inverse",help=data_dict["PPIFIS"]["help"])

    st.subheader('Money', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["FEDFUNDS"]["sub"], str(round(data_dict["FEDFUNDS"]["curr_value"],1))+"%", str(data_dict["FEDFUNDS"]["nominal_change"])+" (MoM)",delta_color="inverse",help=data_dict["FEDFUNDS"]["help"])
    col2.metric(data_dict["M2SL"]["sub"], data_dict["M2SL"]["period1"], str(data_dict["M2SL"]["period_change"])+" (MoM)",delta_color="inverse",help=data_dict["M2SL"]["help"])
    col3.metric(data_dict["M2SL"]["sub"], str(round(data_dict["M2SL"]["curr_value"]/1000,2))+"T", str(data_dict["M2SL"]["annual_change"])+" (YoY)",delta_color="inverse",help=data_dict["M2SL"]["help"])
    col4.metric(data_dict["M1SL"]["sub"], str(round(data_dict["M1SL"]["curr_value"]/1000,2))+"T", str(data_dict["M1SL"]["annual_change"])+" (YoY)",delta_color="inverse",help=data_dict["M1SL"]["help"])
    
    col1.metric(data_dict["BOGMBASE"]["title"], str(round(data_dict["BOGMBASE"]["curr_value"]/1000000,2))+"T", str(data_dict["BOGMBASE"]["annual_change"])+" (YoY)",delta_color="inverse",help=data_dict["BOGMBASE"]["help"])
    col2.metric(data_dict["MBCURRCIR"]["title"], str(round(data_dict["MBCURRCIR"]["curr_value"]/1000000,2))+"T", str(data_dict["MBCURRCIR"]["annual_change"])+" (YoY)",delta_color="inverse",help=data_dict["MBCURRCIR"]["help"])
    col3.metric(data_dict["BOGMBBM"]["title"], str(round(data_dict["BOGMBBM"]["curr_value"]/1000000,2))+"T", str(data_dict["BOGMBBM"]["annual_change"])+" (YoY)",delta_color="normal",help=data_dict["BOGMBBM"]["help"])

    st.subheader('Labor', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["UNRATE"]["title"], str(data_dict["UNRATE"]["curr_value"])+"%", str(data_dict["UNRATE"]["nominal_change"])+" (MoM)",delta_color="inverse",help=data_dict["UNRATE"]["help"])
    col2.metric(data_dict["CIVPART"]["title"], str(data_dict["CIVPART"]["curr_value"])+"%", str(data_dict["CIVPART"]["nominal_change"])+" (MoM)",delta_color="normal",help=data_dict["CIVPART"]["help"])
    col3.metric(data_dict["EMRATIO"]["title"], str(data_dict["EMRATIO"]["curr_value"])+"%", str(data_dict["EMRATIO"]["nominal_change"])+" (MoM)",delta_color="normal",help=data_dict["EMRATIO"]["help"])
    col4.metric(data_dict["ICSA"]["title"], str(int(data_dict["ICSA"]["curr_value"]/1000))+"k", str(data_dict["ICSA"]["perc_change"])+" (WoW)",delta_color="inverse",help=data_dict["ICSA"]["help"])

    st.subheader('Housing', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["HOUST"]["title"], str(round(data_dict["HOUST"]["curr_value"]/1000,2))+"M", str(data_dict["HOUST"]["perc_change"])+" (MoM)",delta_color="normal",help=data_dict["HOUST"]["help"])
    col2.metric(data_dict["MORTGAGE30US"]["title"], str(data_dict["MORTGAGE30US"]["curr_value"])+"%", str(data_dict["MORTGAGE30US"]["nominal_change"])+" (WoW)",delta_color="inverse",help=data_dict["MORTGAGE30US"]["help"])
    col3.metric(data_dict["MORTGAGE15US"]["title"], str(data_dict["MORTGAGE15US"]["curr_value"])+"%", str(data_dict["MORTGAGE15US"]["nominal_change"])+" (WoW)",delta_color="inverse",help=data_dict["MORTGAGE15US"]["help"])


    st.subheader('Demographics', divider='red')
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(data_dict["POPTHM"]["title"], str(int(data_dict["POPTHM"]["curr_value"]/1000))+"M", str(data_dict["POPTHM"]["annual_change"])+" (YoY)",delta_color="inverse",help=data_dict["POPTHM"]["help"])

    st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align: center;'></h1>", unsafe_allow_html=True)
    st.markdown(f"<h6 style='text-align: center;'>© 2023-{datetime.now().year} Peterson Haas. All rights reserved.</h6>",unsafe_allow_html=True)
