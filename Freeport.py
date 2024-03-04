# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 07:46:39 2024

@author: tosunrin
"""
import streamlit as st
import pandas as pd
from PIL import Image
import pyodbc
import xlsxwriter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import streamlit_authenticator as stauth
import time
from datetime import datetime
import yaml
from yaml.loader import SafeLoader

############################

# Dashboard Page Title

# Streamlit UI

###########################

st.set_page_config(
    page_title="Ore Type Visualization Dashboard",
    page_icon="./Extras/favicon-32x32.png",
    layout="wide", initial_sidebar_state='expanded'
)



#stlying the application logo

image= Image.open("./Extras/logo.png")
st.image(image, use_column_width=True)

#customizing the dashboard header

color = "white" # Replace with the desired color hex/RGB code
title_html = f"<h1 style='color: {color}; text-align: center;'>Freeport-McMoRan Ore Type Validation Dashboard</h1>"
st.markdown(title_html, unsafe_allow_html=True)



matplotlib.rc_context(rc={"interactive":False})
st.set_option('deprecation.showPyplotGlobalUse', False)



# --- USER AUTHENTICATION ---
with open('./Extras/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
        )

if st.session_state["authentication_status"] is False:
    st.write('please login')
elif st.session_state["authentication_status"] is None:
    choice = st.sidebar.selectbox('login/Signup', ['Login', 'Sign up'])
    if choice == 'Login':
        try:
            authenticator.login()
        except Exception as e:
            st.error(e)
        st.warning('Please enter your username and password')
    else:
        try:
            email_register_user, username_register_user, name_register_user = authenticator.register_user(preauthorization=False)
            if email_register_user:
                st.success('User registered successfully')
        except Exception as e:
            st.error(e)
    # Saving config file
    with open('./Extras/config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
elif st.session_state["authentication_status"]:
    st.sidebar.write(f'Welcome *{st.session_state["name"]}*')

    def PXCU_PQLT_PLOT(data_plot, x_col, y_col, Ore_Type, LITH, plot_title):
       if x_col=='PXCU' and y_col=='PQLT':
           cols_ = [Ore_Type, LITH]
           for col_ in cols_:
               idx3 = data_plot[col_].isin([-2147483648, -1,-2])
               data_plot.loc[idx3, col_] = np.nan
               
               
           colors = dict({10: '#6C3600', 21: '#005900', 22: '#00FF00', 27: '#FF8000', 31: '#00FFFF', 32: '#FF0000',
                          33: '#00008B', 34:
                              '#B22222', 37: '#A1A0FF', 41: '#FFB6C1', 42: '#6F00DD', 46: '#FEFE00', 50: '#CCFF66',
                          51: '#4E00FF', 52:
                              '#FFFFB7',
                          53: '#808040', 54: '#008080', 55: '#FF69B4'})


           fig, ax = plt.subplots(figsize=(10, 6))
           major_ticks = np.arange(0, 100, 5)

           sns.scatterplot(x=x_col, y=y_col, hue=Ore_Type,
                           data=data_plot, palette=colors,
                           legend='full', alpha=1.0)
           ax.legend(loc='lower right')
           ax.set_xlabel(x_col, fontweight='bold', size=14)
           ax.set_ylabel(y_col, fontweight='bold', size=14)
           ax.set_xlim(0, 100)
           ax.set_ylim(0, 100)
           ax.grid()
           ax.set_title(plot_title, fontweight='bold', size=25)
           ax.set_xticks(major_ticks)
           ax.set_yticks(major_ticks)

           # Drawing oretype rectangles
           rectangles = [
           (50, 60, 100, 40, "OT 22", "#00FF00", None, 'center'),  # Added hatch and va parameters
           (20, 60, 30, 40, "OT 31", '#00FFFF', None, 'center'),
           (0, 57, 20, 42.5, "OT 34", '#B22222', None, 'center'),
           (20, 30, 40, 30, "OT 21", '#005900', None, 'center'),
           (0, 35, 20, 22, "OT 32", '#FF0000', None, 'center'),
           (0, 15, 20, 20, "OT 27/42", None, '/', 'bottom'),
           (20, 0, 10, 30, "OT 27", '#FF8000', None, 'center'),
           (20, 50, 30, 10, "OT 21/31", None, '/', 'center'),
           (0, 0, 15, 15, "OT 27/41", None, "/", 'center'),
           (15, 0, 5, 25, "", None, "/", 'center'),
           (0, 15, 20, 10, "27/37", None, "/", 'center'),
       ]

           for rect_params in rectangles:
               left, bottom, width, height, label, color, hatch, va = rect_params
               rect = mpatches.Rectangle((left, bottom), width, height,
                                         fill=True,
                                         alpha=0.1,
                                         linewidth=2,
                                         edgecolor='black',
                                         facecolor=color,
                                         hatch=hatch if x_col == 'PXCU' else None,  # Set hatch parameter based on axes
                                         )
               ax.add_patch(rect)
               ax.annotate(label,
                           (0.5 * (left + left + width), 0.5 * (bottom + bottom + height)),
                           color='black', weight='bold', fontsize=12,
                           ha='center', va=va if x_col == 'PXCU' else 'center',  # Set va parameter based on axes
                           bbox=dict(facecolor='white', alpha=0.5, edgecolor='white'))
    
    
             # Legends
               OT22_patch = mpatches.Patch(color='#00FF00', label='22: Green Oxide')
               OT21_patch = mpatches.Patch(color='#005900', label='21: Black Oxide')
               OT27_patch = mpatches.Patch(color='#FF8000', label='27: Insoluble oxide')
               OT32_patch = mpatches.Patch(color='#FF0000', label='32: Secondary Chalcocite')
               OT34_patch = mpatches.Patch(color='#B22222', label='34: Mixed Native CU')
               OT31_patch= mpatches.Patch(color='#00FFFF', label='31:Mixed Oxide-Chalcocite')
               OT33_patch= mpatches.Patch(color='#00008B', label='33:Mixed Chalcocite-Sulphide')
               OT37_patch= mpatches.Patch(color='#A1A0FF', label='37:Mixed Chalcopyrite')
               OT41_patch= mpatches.Patch(color='#FFB6C1', label='41:Chalcopyrite')
               OT42_patch= mpatches.Patch(color='#6F00DD', label='42:Bornite')
               Overlap_patch= mpatches.Patch(hatch='/', label='Overlapping Zones',fill=False)
    
               plt.legend(handles=[OT21_patch, OT22_patch, OT27_patch, OT31_patch, OT32_patch, OT33_patch, OT34_patch,
                                   OT37_patch, OT41_patch, OT42_patch, Overlap_patch])
           
           
       else:
           cols_ = [Ore_Type, LITH]
           for col_ in cols_:
               idx3 = data_plot[col_].isin([-2147483648, -1,-2])
               data_plot.loc[idx3, col_] = np.nan
           colors = dict({10: '#6C3600', 21: '#005900', 22: '#00FF00', 27: '#FF8000', 31: '#00FFFF', 32: '#FF0000',
                   33: '#00008B', 34:
                       '#B22222', 37: '#A1A0FF', 41: '#FFB6C1', 42: '#6F00DD', 46: '#FEFE00', 50: '#CCFF66',
                   51: '#4E00FF', 52:
                       '#FFFFB7',
                   53: '#808040', 54: '#008080', 55: '#FF69B4'})
           
           
           fig, ax = plt.subplots(figsize=(10, 6))
           major_ticks = np.arange(0, 100, 5)

           sns.scatterplot(x=x_col, y=y_col, hue=Ore_Type,
                           data=data_plot, palette=colors,
                           legend='full', alpha=1.0, ax=ax)

           ax.legend(loc='lower right')
           ax.set_xlabel(x_col, fontweight='bold', size=14)
           ax.set_ylabel(y_col, fontweight='bold', size=14)
           ax.set_xlim(0, 100)
           ax.set_ylim(0, 100)
           ax.grid()
           ax.set_title(plot_title, fontweight='bold', size=25)
           ax.set_xticks(major_ticks)
           ax.set_yticks(major_ticks)

   
       # add first rectangle with patches
           rectangles = [
               (60, 50, 40, 50, "OT 22", "#00FF00", None, 'center'),  # Added hatch and va parameters
               (50, 20, 50, 30, "OT 31", '#00FFFF', None, 'center'),
               (57, 0, 42.5, 20, "OT 34", '#B22222', None, 'center'),
               (30, 20, 30, 40, "OT 21", '#005900', None, 'center'),
               (35, 0, 22, 20, "OT 32", '#FF0000', None, 'center'),
               (15, 0, 20, 20, "OT 27/42", None, '/', 'bottom'),
               (0, 20, 30, 10, "OT 27", '#FF8000', None, 'center'),
               (50, 20, 10, 30, "OT 21/31", None, '/', 'center'),
               (0, 0, 15, 15, "OT 27/41", None, "/", 'center'),
               (0, 15, 20, 5, "", None, "/", 'center'),
               (15, 0, 10, 20, "27/37", None, "/", 'center'),
               ]
           for rect_params in rectangles:
               left, bottom, width, height, label, color, hatch, va = rect_params
               rect = mpatches.Rectangle((left, bottom), width, height,
                                           fill=True,
                                           alpha=0.1,
                                           linewidth=2,
                                           edgecolor='black',
                                           facecolor=color,
                                           hatch=hatch if x_col == 'PXCU' else None,  # Set hatch parameter based on axes
                                           )
               ax.add_patch(rect)
               ax.annotate(label,
                           (0.5 * (left + left + width), 0.5 * (bottom + bottom + height)),
                           color='black', weight='bold', fontsize=12,
                           ha='center', va=va if x_col == 'PXCU' else 'center',  # Set va parameter based on axes
                           bbox=dict(facecolor='white', alpha=0.5, edgecolor='white'))
    
               #Legends
               # Creating legend with color box
               OT22_patch= mpatches.Patch(color='#00FF00', label='22:Green Oxide')
               OT21_patch= mpatches.Patch(color='#005900', label='21:Black Oxide')
               OT27_patch= mpatches.Patch(color='#FF8000', label='27:Insoluble oxide')
               OT32_patch= mpatches.Patch(color='#FF0000', label='32:Secondary Chalcocite')
               OT34_patch= mpatches.Patch(color='#B22222', label='34:Mixed Native CU')
               OT31_patch= mpatches.Patch(color='#00FFFF', label='31:Mixed Oxide-Chalcocite')
               OT33_patch= mpatches.Patch(color='#00008B', label='33:Mixed Chalcocite-Sulphide')
               OT37_patch= mpatches.Patch(color='#A1A0FF', label='37:Mixed Chalcopyrite')
               OT41_patch= mpatches.Patch(color='#FFB6C1', label='41:Chalcopyrite')
               OT42_patch= mpatches.Patch(color='#6F00DD', label='42:Bornite')
               Overlap_patch= mpatches.Patch(hatch='/', label='Overlapping Zones',fill=False)
    
    
               plt.legend(handles=[OT21_patch,OT22_patch, OT27_patch,OT31_patch,OT32_patch,OT33_patch, OT34_patch,
                               OT37_patch,OT41_patch,OT42_patch, Overlap_patch])
               #st.write("Note: Interactive dashboard is displayed above.")
               #plt.show()
           
           
                    
  
    #function to download dataframe to excel
    def outliers_download(dataframes, filename):
        with st.spinner("processing outliers....."):
            doc_writer = pd.ExcelWriter(filename, engine='xlsxwriter')
            for sheet_name, df in dataframes.items():
                df.to_excel(doc_writer, sheet_name=sheet_name, index=False)
                doc_writer.close()
            st.success("outliers has been processed successfully and read for download")
         
    #function to calculate PQLT and PXCU for DB
    def pqlt_pxcu_calculate_DB(file):
        if 'PQLT' not in file.columns and 'PXCU' not in file.columns:
     
            #Check if QLT is greater than TCU and update accordingly
            file['QLT'] = np.where(file['QLT'] > file['TCu'], 
                                             file['QLT'], file['TCu'])
            # Check if XCu is greater than TCU and update accordingly
            file['XCu'] = np.where(file['XCu']> file['TCu'],
                                             file['XCu'], file['TCu'])

             # Check if XCu is greater than QLT and update accordingly
            file['XCu'] = np.where(file['XCu'] > file['QLT'], 
                                           file['XCu'], file['QLT'] )
            # Evaluate PQLT if PQLT is not present in dataframe
     
            file['PQLT'] = round((file['QLT'] / file['TCu']) * 100)

             # Evaluate PXCU if 'PXCU' is not present in dataframe
     
            file['PXCU'] = file['XCu'] / file['TCu']
        return file
    
    
    
            
    #function to calculate PQLT and XDIVT for local PC
    def pqlt_pxcu_calculate_PC(file):
        if 'PQLT' not in file.columns and 'PXCU' not in file.columns:
     
            #Check if QLT is greater than TCU and update accordingly
            file['QLT'] = np.minimum(file['QLT'], file['TCU'])
            # Check if XCu is greater than TCU and update accordingly
            file['XCU'] = np.minimum(file['XCU'], file['TCU'])

             # Check if XCu is greater than QLT * 1.1 and update accordingly
            file['XCU'] = np.where(file['XCU'] <= file['QLT'] * 1.1, 
                                           file['XCU'], file['QLT'] * 1.1)
            # Evaluate PQLT if PQLT is not present in dataframe
     
            file['PQLT'] = round((file['QLT'] / file['TCU']) * 100)

             # Evaluate PXCU if 'PXCU' is not present in dataframe
     
            file['PXCU'] = file['XCU'] / file['TCU']
        return file
            
    # Function to check if the list is empty
    def is_list_empty(lst):
        return not lst 
        
        #plot function
        #@st.cache_data
            
        
        
        
############################

#APP LAYOUT

###########################
    #@st.cache_data(experimental_allow_widgets=True)  
    def main():
        if 'session_state' not in st.session_state or 'selected_data_source' not in st.session_state:
            st.session_state['selected_data_source'] = 'Local PC'
    
        authenticator.logout("Logout", "sidebar")
    
        selected_data_source = st.sidebar.radio("Select Data Source", ["Local PC", "Database"])
    
        if selected_data_source == "Local PC":
            st.sidebar.header("Upload input files")
            uploaded_file = st.sidebar.file_uploader("", type=["csv", "xlsx"], accept_multiple_files=True)
            data_a=None
            if uploaded_file is not None:
                data_a = pd.DataFrame()
                for files in uploaded_file:
                    file_name = files.name
                    file_extension = file_name.split('.')[-1].lower()
    
                    if file_extension == 'csv':
                        try:
                            data_ = pd.read_csv(files)
                            st.sidebar.success("Data successfully loaded")
                            data_=pqlt_pxcu_calculate_PC(data_)
                            data_a = data_.copy()
                            st.header('Original Data')
                            st.write(data_)
                            st.session_state.pop('x_col', None)
                            st.session_state.pop('y_col', None)
                            st.session_state.pop('Ore_Type', None)
                            st.session_state.pop('LITH', None)
                        # Hqandling exceptions error
                        except UnicodeDecodeError:
                            data_ = pd.read_csv(files, encoding='ISO-8859-1')  # or encoding='cp1252'
                            st.sidebar.success("Data successfully loaded from PC")
                            data_=pqlt_pxcu_calculate_PC(data_)
                            data_a=data_.copy()
                            st.header('Original Data')
                            st.write(data_)
                            st.session_state.pop('x_col', None)
                            st.session_state.pop('y_col', None)
                            st.session_state.pop('Ore_Type', None)
                            st.session_state.pop('LITH', None)
                        except KeyError:
                            st.warning('please check the column headers to meet safford mine format: LITH, ORTP, HOLEID')
                        except pd.errors.ParserError as e:
                        # Handle the parsing error
                            st.warning(f"ParserError: {e}")
                        except Exception as e:
                        # This block can catch any other exceptions that were not specifically caught above
                            st.warning(f"An unexpected error occurred: {e}")
                    elif file_extension=='xlsx':
                            try:
                                data_ = pd.read_excel(files)
                                st.sidebar.success("Data successfully loaded from PC")
                                data_=pqlt_pxcu_calculate_PC(data_)
                                data_a=data_.copy()
                                st.header('Original Data')
                                st.write(data_)
                                st.session_state.pop('x_col', None)
                                st.session_state.pop('y_col', None)
                                st.session_state.pop('Ore_Type', None)
                                st.session_state.pop('LITH', None)
                            # Continue processing the DataFrame
                            except UnicodeDecodeError:
                                data_ = pd.read_csv(files, encoding='ISO-8859-1')  # or encoding='cp1252'
                                st.sidebar.success("Data successfully loaded from PC")
                                data_=pqlt_pxcu_calculate_PC(data_)
                                data_a=data_.copy()
                                column_type=data_a.columns.dtype
                                st.header('Original Data')
                                st.write(data_)
                                st.session_state.pop('x_col', None)
                                st.session_state.pop('y_col', None)
                                st.session_state.pop('Ore_Type', None)
                                st.session_state.pop('LITH', None)
                            except KeyError:
                                st.warning('please check the column headers to meet safford mine format: LITH, ORTP, HOLEID')
                            except pd.errors.ParserError as e:
                            # Handle the parsing error
                                st.warning(f"ParserError: {e}")
                            except Exception as e:
                            # This block can catch any other exceptions that were not specifically caught above
                                st.warning(f"An unexpected error occurred: {e}")
                    else:
                        st.warning(f"This file is unsupported: {file_extension}")
            if data_a is not None:
                  st.session_state.data_a = data_a
         #user loading data from database
        if selected_data_source == "Database":
            data_a=None
            if 'data_a' not in st.session_state:
                st.session_state.data_a=pd.DataFrame
            #data_a = pd.DataFrame()  # Assign a default empty DataFrame
            server = st.sidebar.text_input("Server", value="your_server_name")
            database = st.sidebar.text_input("Database", value="your_database_name")
            driver = st.sidebar.text_input("ODBC Driver", value="{ODBC Driver 17 for SQL Server}")
    
            user_query = st.sidebar.text_area("Enter your SQL query")
            load_data = st.sidebar.checkbox("Load Data")
            if load_data and not st.session_state.get('data_loaded', False):
                conn = None
                try:
                    conn = pyodbc.connect(f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes")
                    st.success('connection successful')
                    data_ = pd.read_sql(user_query, conn)
                    
                    #call function to calculate pxcu and xdivt
                    data_=pqlt_pxcu_calculate_DB(data_)
                    
                    st.session_state.data_a = data_.copy()
                    
                    st.sidebar.success("Data successfully loaded from Database:")
                    st.header('Original Data')
                    st.dataframe(st.session_state.data_a)
                    
                    #st.session_state.data_loaded=True
                    #clearing drop downs once not in session
                    st.session_state.pop('x_col', None)
                    st.session_state.pop('y_col', None)
                    st.session_state.pop('Ore_Type', None)
                    st.session_state.pop('LITH', None)
                    
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
                finally:
                    if conn is not None:
                        conn.close()
            
        #if 'data_a' not in st.session_state:
            #st.session_state.data_a = pd.DataFrame()
    
        if data_a is not None:
            st.session_state.data_a = data_a
            

        column_ = st.session_state.data_a.columns.tolist() if 'data_a' in st.session_state else []
        
        if not column_:
            column_ = ['No columns available']
        if 'x_col' not in st.session_state or st.session_state.x_col not in column_:
            st.session_state.x_col = column_[0]
            
        if 'y_col' not in st.session_state or st.session_state.y_col not in column_:
            st.session_state.y_col = column_[0]
        if 'Ore_Type' not in st.session_state or st.session_state.Ore_Type not in column_:
            st.session_state.Ore_Type = column_[0]
        if 'LITH' not in st.session_state or st.session_state.LITH not in column_:
            st.session_state.LITH = column_[0]
        if 'column_to_filter' not in st.session_state or st.session_state.column_to_filter not in column_:
            st.session_state.column_to_filter = column_[0]
        if 'filter_input' not in st.session_state:
            st.session_state.filter_input = None
        if 'plot_title' not in st.session_state:
            st.session_state.plot_title = None
        
        st.sidebar.header("Plot Parameters")    
        x_col = st.sidebar.selectbox("Select X Column", column_, index=column_.index(st.session_state.x_col))
        y_col = st.sidebar.selectbox("Select Y Column", column_, index=column_.index(st.session_state.y_col))
        Ore_Type = st.sidebar.selectbox("Select Ore_Type Column", column_, index=column_.index(st.session_state.Ore_Type))
        LITH = st.sidebar.selectbox("Select LITH Column", column_, index=column_.index(st.session_state.LITH))
        plot_title = st.sidebar.text_input("Enter Plot Title")
    
        
        st.sidebar.header("Filter Options")
        # Select column to filter
        column_to_filter = st.sidebar.selectbox("Select column to filter:", column_, 
                                                index=column_.index(st.session_state.column_to_filter))
        
        filter_input = st.sidebar.text_input("Enter the holes to be filtered (comma-separated):")

        #user input for data filtering
        filtering=st.sidebar.number_input('Default TCU-Cutoff value', value=0.1)
        st.sidebar.write("change the default TCU-Cutoff value if needed")
        
        
        #updating columns after app rerun
        st.session_state.x_col = x_col
        st.session_state.y_col = y_col
        st.session_state.Ore_Type = Ore_Type
        st.session_state.LITH = LITH
        st.session_state.filtering = filtering
        st.session_state.filter_input= filter_input
        st.session_state.plot_title= plot_title
        
        
        if x_col == 'No columns available' or y_col == 'No columns available' or Ore_Type == 'No columns available' or LITH == 'No columns available':
            st.info('Please load data from Local PC or Database')
        else:
            # Drop rows with ORTP==99 and not having grades in it.
            data_C = data_a[~((data_a[st.session_state.Ore_Type] == 99) & (data_a['TCU'].isin([-1, -2])))]

            # Initialize data_plot to an empty DataFrame to ensure it's always defined
            data_plot = pd.DataFrame()
           
            # Check specific conditions and update data_N or data_plot as needed
            if (data_C[st.session_state.Ore_Type] == 99).any() and (data_C['TCU'] >= 0).any():
                data_N = data_C[(data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0)]
                st.subheader("ORTP 99 Assay Data:")
                st.dataframe(data_N)
                st.warning('Please check assay data and correct as needed. This data will automatically be filtered out and would not be considered in the plot.')
           
            # Apply filtering logic based on user input
            if filter_input:
                filter_list = [x.strip() for x in filter_input.split(',')]
                column_type = data_a[column_to_filter].dtype
               
                data = data_C[~((data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0))]
                if column_type == 'object':
                    data = data.loc[data[column_to_filter].str.startswith(tuple(filter_list))]
                elif column_type in ['int64', 'float']:
                    try:
                        filter_list = [int(x.strip()) for x in filter_input.split(',')] if filter_input else []
                        data = data[data[column_to_filter].isin(filter_list)]
                    except ValueError:
                        st.error('Enter valid numbers separated by comma')
                        data = pd.DataFrame()  # Initialize data to avoid further errors if the input is invalid
               
                if not data.empty:
                    data_plot = data.loc[data['TCU'] >= filtering]
                    data_plot = data_plot[~data_plot[st.session_state.Ore_Type].isin([10, 50, 51, 52, 53, 54])]
        
            # Display filtered data if data_plot has been defined and is not empty
            if not data_plot.empty:
                st.subheader("Filtered Assay Data:")
                st.dataframe(data_plot)
            else:
                st.info('No Filters applied. Apply filters if necessary or proceed to plot the graph.')
            if not data_plot.empty:                
                #creating outliers dataframe        
                #Find OT21  Outliers
                idx=(~(data_plot['PQLT'].between(30, 60))&(data_plot[st.session_state.Ore_Type]==21) | ~(data_plot['PXCU'].between(20, 60))&
                     (data_plot[st.session_state.Ore_Type]==21))
                data_plot.loc[idx, 'FLAGD'] = 5
                OT21_Outliers = data_plot.loc[idx].reset_index(drop=True)
    
                #Find OT22  Outliers
                idx1=(~(data['PQLT'].between(60, 100))&(data[st.session_state.Ore_Type]==22) | ~(data['PXCU'].between(50, 100))&
                      (data[st.session_state.Ore_Type]==22))
                data_plot.loc[idx1, 'FLAGD'] = 5
                OT22_Outliers = data_plot.loc[idx1].reset_index(drop=True)
                #Find OT27  Outliers
                idx2=(~(data_plot['PQLT'].between(0, 35))&(data_plot[st.session_state.Ore_Type]==27) | ~(data_plot['PXCU'].between(0, 35))&
                      (data_plot[st.session_state.Ore_Type]==27))
                
                data_plot.loc[idx2, 'FLAGD'] = 5
                OT27_Outliers = data_plot.loc[idx2].reset_index(drop=True)
            
    
                #Find OT31  Outliers
                idx3=(~(data_plot['PQLT'].between(50, 100))&(data_plot[st.session_state.Ore_Type]==31) | ~(data_plot['PXCU'].between(20, 50))&
                      (data_plot[st.session_state.Ore_Type]==31))
    
                data_plot.loc[idx3, 'FLAGD'] = 5
                OT31_Outliers = data_plot.loc[idx3].reset_index(drop=True)
            
                #Find OT32  Outliers
                idx8=(~(data_plot['PQLT'].between(35, 57))&(data_plot[st.session_state.Ore_Type]==32) | ~(data_plot['PXCU'].between(0, 20))&
                      (data_plot[st.session_state.Ore_Type]==32))
                data_plot.loc[idx8, 'FLAGD'] = 5
                OT32_Outliers = data_plot.loc[idx8].reset_index(drop=True)
            
                #Find OT34  Outliers
                idx4=(~(data_plot['PQLT'].between(57, 100))&(data_plot[st.session_state.Ore_Type]==34) | ~(data_plot['PXCU'].between(0, 20))&
                      (data_plot[st.session_state.Ore_Type]==34))
    
                data_plot.loc[idx4, 'FLAGD'] = 5
                OT34_Outliers = data_plot.loc[idx4].reset_index(drop=True)
    
                #Find OT37  Outliers
                idx5=(~(data_plot['PQLT'].between(15, 25))&(data_plot[st.session_state.Ore_Type]==37) | ~(data_plot['PXCU'].between(0, 20))&
                      (data_plot[st.session_state.Ore_Type]==37))
    
                data_plot.loc[idx5, 'FLAGD'] = 5
                OT37_Outliers = data_plot.loc[idx5].reset_index(drop=True)
    
    
                #Find OT41  Outliers
                idx6=(~(data_plot['PQLT'].between(0, 15))&(data_plot[st.session_state.Ore_Type]==41) | ~(data_plot['PXCU'].between(0, 15))&
                      (data_plot[st.session_state.Ore_Type]==41))
    
                data_plot.loc[idx6, 'FLAGD'] = 5
                OT41_Outliers = data_plot.loc[idx6].reset_index(drop=True)
        
    
                #Find OT42  Outliers
                idx7=(~(data_plot['PQLT'].between(15, 35))&(data_plot[st.session_state.Ore_Type]==42) | ~(data_plot['PXCU'].between(0, 15))&
                      (data_plot[st.session_state.Ore_Type]==42))
    
                data_plot.loc[idx7, 'FLAGD'] = 5
                OT42_Outliers = data_plot.loc[idx7].reset_index(drop=True)
                
    
                #ORTP 99 outliers
                id_=(data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0)
                data_plot.loc[id_, 'FLAGD'] = 5
                ORTP_99= data_plot.loc[id_].reset_index(drop=True)
    
                #put all outliers into dataframe
                dataframes = {'OT21_Outliers': OT21_Outliers, 'OT22_Outliers': OT22_Outliers, 'OT27_Outliers': OT27_Outliers, 
                              'OT31_Outliers': OT31_Outliers, 'OT32_Outliers': OT32_Outliers,
                              'OT34_Outliers': OT34_Outliers, 'OT37_Outliers': OT37_Outliers, 'OT41_Outliers': OT41_Outliers, 
                              'OT42_Outliers': OT42_Outliers,'ORTP_99_Outliers':ORTP_99}     
                
            plot_button, download_button=st.columns(2)
            #graphical visualization plot button
            if 'plot' not in st.session_state:
                st.session_state.plot=None
            with plot_button:
                if st.button("Plot"):
                    with st.spinner("Generating plot..."):
                        st.session_state.plot=PXCU_PQLT_PLOT(data_plot, st.session_state.x_col, st.session_state.y_col, st.session_state.Ore_Type, st.session_state.LITH, plot_title)
                        st.pyplot(st.session_state.plot)
                        st.set_option('deprecation.showPyplotGlobalUse', False)
                        st.write("Note: Interactive dashboard is displayed above.")
                if st.session_state.plot is not None:
                    st.pyplot(st.session_state.plot)
                       
                        #outlier execution button
                with download_button:
                    if 'clicked' not in st.session_state:
                        st.session_state.clicked = False

                    def click_button():
                        st.session_state.clicked = True
                    
                    if st.button("Process Outliers"):
                        time.sleep(3)
                        download_time=datetime.now().strftime("%m%d%y_%H_%M_%S")
                        download_filename = f"Outliers_{download_time}.xlsx"
                        outliers_download(dataframes, download_filename)
                        with open(download_filename, "rb") as file:
                            st.download_button(label="download", data=file.read(), file_name=download_filename, key="download_button", on_click=click_button)
                            if st.session_state.clicked:
                                st.success("Outliers successfully downloaded to your PC")
                            st.write(f'there are {idx.sum():,} OT21 Outliers  of the {len(idx):,} holes')
                            st.write(f'there are {idx1.sum():,} OT22 Outliers  of the {len(idx1):,} holes')
                            st.write(f'there are {idx2.sum():,} OT27 Outliers  of the {len(idx2):,} holes')
                            st.write(f'there are {idx3.sum():,} OT31 Outliers of the {len(idx3):,} holes')
                            st.write(f'there are {idx8.sum():,} OT32 Outliers of the {len(idx8):,} holes')
                            st.write(f'there are {idx4.sum():,} OT34 Outliers of the {len(idx4):,} holes')
                            st.write(f'there are {idx5.sum():,} OT37 Outliers of the {len(idx5):,} holes')
                            st.write(f'there are {idx6.sum():,} OT41 Outliers of the {len(idx6):,} holes')
                            st.write(f'there are {idx7.sum():,} OT42 Outliers of the {len(idx7):,} holes')
        
    
    if __name__ == "__main__":
        main()
