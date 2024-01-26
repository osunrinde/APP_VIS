import altair as alt
import streamlit as st
from PIL import Image
import io
import os
import base64
import urllib.request
import xlsxwriter
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import subprocess
from io import BytesIO
import streamlit_authenticator as stauth
import pickle
from pathlib import Path
import time
from datetime import datetime

############################

# Dashboard Page Title

# Streamlit UI

###########################

st.set_page_config(
    page_title="Ore Type Visalization Dashboard",
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
names  = ["Freeport-McMoRan"]
usernames = ["freeport"]

# load hashed passwords
file_path = Path(__file__).parent / "Freeport_password.pkl"
with file_path.open("rb") as file:
    hashed_passwords = pickle.load(file)

authenticator = stauth.Authenticate(names, usernames, hashed_passwords, "ore type dashboard", "abcdef", cookie_expiry_days=1)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:
    #plot function
    #@st.cache_data
   
    def PXCU_PQLT_PLOT(data_plot, x_col, y_col, Ore_Type, LITH, plot_title):
        rectangles=[]
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
            rectangle = [
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
                                        facecolor=color if color else 'none',
                                        hatch=hatch
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

# Function to check if the list is empty
    def is_list_empty(lst):
        return not lst 




    # Application body
    def main():

    #setting background color for the sidebar
        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: black;
            }
        </style>
        """, unsafe_allow_html=True)
        # create logout button
  
        authenticator.logout("Logout", "sidebar")
        st.sidebar.title(f"Welcome {name}")
        
       # creating upload button and plot buttons

        #upload button
        st.sidebar.header("Upload input files")
        uploaded_file = st.sidebar.file_uploader("", type=["csv", "xlsx"], accept_multiple_files=True)

        # plot buttons

        if uploaded_file is not None:
            for files in uploaded_file:
                # Process the uploaded file here
                try:
                    data_ = pd.read_csv(files)
                   
                # Continue processing the DataFrame
                except UnicodeDecodeError:
                    data_ = pd.read_csv(files, encoding='ISO-8859-1')  # or encoding='cp1252'  
                # Copy DataFrame
                #data_C = data_.copy()

                st.sidebar.write("File uploaded successfully!")

                # Sidebar with filtering options
                st.sidebar.header("Filter Options")
                
                # Select column to filter
                column_to_filter = st.sidebar.selectbox("Select column to filter:", data_.columns)
                filter_input = st.sidebar.text_input("Enter the holes to be filtered (comma-separated):")
                filter_list = [x.strip() for x in filter_input.split(',')]

                #user input for data filtering
                filtering=st.sidebar.number_input('Default TCU-Cutoff value', value=0.1)
                st.sidebar.write("change the default TCU-Cutoff value if needed")
                
                if 'session_state' not in st.session_state:
                    st.session_state.session_state = {
                    'x_col': None,
                    'y_col': None,
                    'Ore_Type': None,
                    'LITH':None,
                    }
                columns = data_.columns.tolist()
                #create plot settings
                st.sidebar.header("Plot Settings")
                plot_title = st.sidebar.text_input("Enter Plot Title")
                st.session_state.x_col= st.sidebar.selectbox("Select X Column",columns)
                st.session_state.y_col= st.sidebar.selectbox("Select Y Column",columns)
                st.session_state.Ore_Type=st.sidebar.selectbox("Select Ore_type Column", columns, index=0)
                st.session_state.LITH=st.sidebar.selectbox("Select Lithology Column", columns, index=0)
                #data check 
                #drop rows with ortp==99 and not having grades in it. This is because they are not needed for plotting or modelling
                data_C=data_[~((data_[st.session_state.Ore_Type] == 99) & (data_['TCU'].isin([-1,-2])))]

                #check if assay data has ore type 99 and has grade present in it. This is to help geologists know what holes to fix in the database

                if (data_C[st.session_state.Ore_Type]==99).any() and (data_C['TCU'] >=0).any():
                    data_N=data_C[(data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0)]
                    st.subheader("ORTP 99 Assay Data:")
                    st.dataframe(data_N)
                    st.warning('please check assay data and correct as needed. This data will automatically be filtered out and would not be considered in the plot')
                # Apply filtering logic
                if is_list_empty(filter_list):
                    data = data_C[~((data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0))]
                    data_plot=data.loc[data['TCU']>=0.1]
                    data_plot = data_plot[~data_plot[st.session_state.Ore_Type].isin([10,50,51,52,53,54])]
                    st.subheader("Filtered Assay Data:")
                    st.dataframe(data_plot)
                else:
                    data = data_C[~((data_C[st.session_state.Ore_Type] == 99) & (data_C['TCU'] >= 0))]
                    data = data.loc[data[column_to_filter].str.startswith(tuple(filter_list))]
                    data_plot=data.loc[data['TCU']>=0.1]
                    data_plot = data_plot[~data_plot[st.session_state.Ore_Type].isin([10,50,51,52,53,54])]
                    st.subheader("Filtered Assay Data:")
                    st.dataframe(data_plot)
                    

            
                if (st.session_state.x_col and st.session_state.y_col and st.session_state.Ore_Type)== "":
                    pass
                else:

                    if filtering !=0.1:
                        #default filtring option
                        data_plot=data.loc[data['TCU']>=filtering]
                        data_plot = data_plot[~data_plot[st.session_state.Ore_Type].isin([10,50,51,52,53,54])]
                     
                    if st.session_state.x_col and st.session_state.y_col and st.session_state.Ore_Type and plot_title != None:
                        st.write('proceed to plot graph')
                    else:
                        st.warning('select all necessary variable')
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


                    #creating columns for the plot and download buttons
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

   
