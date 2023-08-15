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




############################

# Dashboard Page Title

# Streamlit UI

###########################

st.set_page_config(
    page_title="Ore Type Definitions Dashboard",
    page_icon='./Extras/favicon-32x32.png',
    layout="wide", initial_sidebar_state='expanded'
)

image= Image.open('./Extras/R.jpg')
st.image(image, use_column_width=True)

#customizing the dashboard header

color = "blue" # Replace with the desired color hex/RGB code
title_html = f"<h1 style='color: {color}; text-align: center;'>Freeport-McMoRan Ore Type Validation Dashboard</h1>"
st.markdown(title_html, unsafe_allow_html=True)

label = "<h2 style='text-align: left; font-size: 24px;'>Welcome to Freeport-McMoRan Ore Type Validation dashboard</h2>"
st.markdown(label, unsafe_allow_html=True)


# Add CSS style to increase font size of file uploader text
label = "<h2 style='text-align: left; font-size: 20px;'>Upload Input Files</h2>"
st.markdown(label, unsafe_allow_html=True)

matplotlib.rc_context(rc={"interactive":False})


#plot function
def PXCU_PQLT_PLOT(data_plot, x_col, y_col, plot_title):
    if x_col=='PXCU' and y_col=='PQLT':
        cols_ = ["ORTP", "LITH"]
        for col_ in cols_:
            idx3 = data_plot[col_].isin([-2147483648])
            data_plot.loc[idx3, col_] = np.nan
    
    
        colors = dict({10: '#6C3600', 21: '#005900', 22: '#00FF00', 27: '#FF8000', 31: '#00FFFF', 32: '#FF0000', 33: '#00008B', 34:
                       '#B22222', 37: '#A1A0FF', 41: '#FFB6C1', 42: '#6F00DD', 46: '#FEFE00', 50: '#CCFF66', 51: '#4E00FF', 52: '#FFFFB7',
                       53: '#808040', 54: '#008080', 55: '#FF69B4'})
    
        plt.figure(figsize=(20, 15))
        major_ticks = np.arange(0, 100, 5)
        minor_ticks = np.arange(0, 100, 5)
    
        sns.scatterplot(x=x_col, y=y_col, hue="ORTP",
                        data=data_plot, palette=colors,
                        legend='full', alpha=1.0)
    
        plt.legend(loc='lower right')
        plt.xlabel(x_col, fontweight='bold', size=14)
        plt.ylabel(y_col, fontweight='bold', size=14)
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.grid()
        plt.title(plot_title, fontweight='bold', size=25)
        plt.xticks(major_ticks)
        plt.yticks(major_ticks)
    
        # Drawing oretype rectangles
        left, bottom, width, height = (50, 60, 100, 40)
        rect = mpatches.Rectangle((left, bottom), width, height,
                                  fill=True,
                                  alpha=0.1,
                                  linewidth=4,
                                  color="#00FF00")
        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect)
        plt.gca().annotate("OT 22", (0.5 * (left + right), 0.5 * (bottom + top)),
                           color='black', weight='bold', fontsize=20, ha='right', va='center')

        # add second rectangle with patches
        left, bottom, width, height = (20, 60, 30, 40)
        rect1=mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                          
                               linewidth=4,
                               color='#00FFFF')

        right= left + width
        top = bottom + height
        plt.gca().add_patch(rect1)
        plt.gca().annotate("OT 31",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='center',va='center')




        # add third rectangle with patches
        left, bottom, width, height = (0, 57, 20, 42.5)
        rect3 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                         
                               linewidth=4,
                               color='#B22222')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect3)
        plt.gca().annotate("OT 34",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,ha='center',va='center')



        # add fourth rectangle with patches
        left, bottom, width, height = (20, 30, 40, 30)
        rect4 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                        
                               linewidth=4,
                               color='#005900')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect4)
        plt.gca().annotate("OT 21",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='center',va='center')




        # add fifth rectangle with patches
        left, bottom, width, height = (0,35,20,22)
        rect5 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                          
                               linewidth=4,
                               color='#FF0000')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect5)
        plt.gca().annotate("OT 32:",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,ha='center',va='center')


        # add sixth rectangle with patches
        left, bottom, width, height = (0,15,20,20)
        rect6=mpatches.Rectangle((left,bottom),width,height, 
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect6)
        plt.gca().annotate("OT 27/42",(0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='right',va='bottom')



        # add seventh rectangle with patches
        left, bottom, width, height = (20,0,10, 30)
        rect7 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                         
                               linewidth=4,
                               color='#FF8000')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect7)
        plt.gca().annotate("OT 27", 
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=15,ha='center',va='center')





        # add eight rectangle with patches
        left, bottom, width, height = (20,50,30,10)
        rect8=mpatches.Rectangle((left,bottom),width,height,                          
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect8)
        plt.gca().annotate("OT 21/31", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')
                   
                   

        # add ninth rectangle with patches
        left, bottom, width, height = (0,0,15,15)
        rect9=mpatches.Rectangle((left,bottom),width,height, 
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect9)
        plt.gca().annotate("OT 27/41", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')



        # add tenth rectangle with patches
        left, bottom, width, height = (15,0,5, 25)
        rect10 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                       
                               linewidth=4,
                               hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect10)
        plt.gca().annotate("" , (0.4*(right+left), 0.4*(bottom+top)),color='black', weight='bold', fontsize=15, ha='center',va='center')


        # add eleventh rectangle with patches
        left, bottom, width, height = (0,15,20,10)
        rect_=mpatches.Rectangle((left,bottom),width,height,                          
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect_)
        plt.gca().annotate("OT 27/37", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')
                   

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
    
    
        st.write("Note: Interactive dashboard is displayed above.")
        plt.show()
    else:
        cols_1 = ["ORTP","LITH"]
        for col_1 in cols_1:
            idx_= data_plot[col_1].isin([-2147483648])
            data_plot.loc[idx_, col_1]=np.nan
   

        colors =dict({10:'#6C3600',21:'#005900',22:'#00FF00',27:'#FF8000',31:'#00FFFF',32:'#FF0000',33:'#00008B',34:'#B22222',
             37:'#A1A0FF',41:'#FFB6C1', 42:'#6F00DD',46:'#FEFE00',50:'#CCFF66',51:'#4E00FF',52:'#FFFFB7',53:'#808040', 
             54:'#008080', 55:'#FF69B4'})
        fig = plt.gcf()

        fig.set_size_inches(20, 15)
        major_ticks = np.arange( 0, 100,5 ) # major tick for every 4 units
        minor_ticks = np.arange( 0, 100, 5 ) # minor tick for every 2 units
        sns.scatterplot(x=x_col, y=y_col, hue="ORTP",
                        data=data_plot, palette=colors, 
                        legend='full', alpha=1.0)
        plt.legend(loc='upper left')
        plt.xlabel(x_col, fontweight ='bold', size=14)
        plt.ylabel(y_col, fontweight ='bold', size=14)
        plt.xlim(0,100)
        plt.ylim(0,100)
        plt.grid()
        plt.title(plot_title, fontweight ='bold', size=25)
        plt.xticks( major_ticks )
        plt.yticks( major_ticks )




        # add first rectangle with patches
        left, bottom, width, height = (50, 20, 50, 30)
        rect1=mpatches.Rectangle((left,bottom),width,height, 
                                 fill=True,
                                 alpha=0.1,                          
                                 linewidth=4,
                                 color='#00FFFF')

        right= left + width
        top = bottom + height
        plt.gca().add_patch(rect1)
        plt.gca().annotate("OT 31",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='center',va='center')




        # add second rectangle with patches
        left, bottom, width, height = (57, 0, 42.5, 20)
        rect2 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                         
                               linewidth=4,
                               color='#B22222')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect2)
        plt.gca().annotate("OT 34",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,ha='center',va='center')



        # add third rectangle with patches
        left, bottom, width, height = (30, 20, 30, 40)
        rect3 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                        
                               linewidth=4,
                               color='#005900')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect3)
        plt.gca().annotate("OT 21",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='center',va='center')


        # add fourth rectangle with patches

        left, bottom, width, height = (60, 50, 40, 50)
        rect4=mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1, 
                               linewidth=4,
                               color="#00FF00")
        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect4)
        plt.gca().annotate("OT 22", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='right',
                           va='center')

        # add eight rectangle with patches
        left, bottom, width, height = (50,20,10,30)
        rect8=mpatches.Rectangle((left,bottom),width,height,                          
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect8)
        plt.gca().annotate("OT 21/31", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')

        # add fifth rectangle with patches
        left, bottom, width, height = (35,0,22,20)
        rect5 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                          
                               linewidth=4,
                               color='#FF0000')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect5)
        plt.gca().annotate("OT 32:",
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,ha='center',va='center')

                
        # add sixth rectangle with patches
        left, bottom, width, height = (15,0,20,20)
        rect6=mpatches.Rectangle((left,bottom),width,height, 
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect6)
        plt.gca().annotate("OT 27/42",(0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20, ha='left',va='top')

        # add seventh rectangle with patches
        left, bottom, width, height = (0,0,15,15)
        rect7=mpatches.Rectangle((left,bottom),width,height, 
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect7)
        plt.gca().annotate("OT 27/41", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')

        # add eleventh rectangle with patches
        left, bottom, width, height = (0,15,20, 5)
        rect11 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                       
                               linewidth=4,
                               hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect11)
        plt.gca().annotate("" , (0.4*(right+left), 0.4*(bottom+top)),color='black', weight='bold', fontsize=15, ha='left',va='center')


        # add ninth rectangle with patches
        left, bottom, width, height = (0,20,30, 10)
        rect9 =mpatches.Rectangle((left,bottom),width,height, 
                                fill=True,
                                alpha=0.1,                         
                               linewidth=4,
                               color='#FF8000')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect9)
        plt.gca().annotate("OT 27", 
                           (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=15,ha='center',va='center')

        # add tenth rectangle with patches
        left, bottom, width, height = (15,0,10,20)
        rect_=mpatches.Rectangle((left,bottom),width,height,                          
                                fill=False,
                                linewidth=2,
                                hatch='/')

        right = left + width
        top = bottom + height
        plt.gca().add_patch(rect_)
        plt.gca().annotate("OT 27/37", (0.5*(left+right), 0.5*(bottom+top)),color='black', weight='bold', fontsize=20,
                           ha='center',va='center')
                   

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
        st.write("Note: Interactive dashboard is displayed above.")
        plt.show()
#function to download dataframe to excel
def outliers_download(dataframes, filename):
    doc_writer = pd.ExcelWriter(filename, engine='xlsxwriter')

    for sheet_name, df in dataframes.items():
        df.to_excel(doc_writer, sheet_name=sheet_name, index=False)

    doc_writer.save()
    

    
# Application body
def main():
    #st.title('Ore-Type Validation Data plotter')
    # Upload data from user's local machine
    uploaded_file = st.file_uploader("", type=["csv", "xlsx"], accept_multiple_files=True, label_visibility="visible")

    if uploaded_file is not None:
        for files in uploaded_file:
            # Process the uploaded file here
            data = pd.read_csv(files)
        
            st.write("File uploaded successfully!")
    
            x_options = data.columns.tolist()
            y_options = data.columns.tolist()
            st.header("Plot Settings")
    
            x_col = st.selectbox("Select X Column", x_options)
            y_col = st.selectbox("Select Y Column", y_options)
            plot_title = st.text_input("Enter Plot Title")
            
            #default filtering option
            data_plot=data.loc[data['TCU']>=0.1]
            
            data_plot = data_plot.drop(data_plot[(data_plot.ORTP == 10) | (data_plot.ORTP == 54) |
                                                 (data_plot.ORTP == 50) | (data_plot.ORTP == 51) | (data_plot.ORTP == 52) |
                                                 (data_plot.ORTP == 53)].index)
            #user input for data filtering
            filtering=st.number_input('Default TCU-Cutoff value', value=0.1)
            st.write("change default TCU-Cutoff value if needed")
            if filtering !=0.1:
                #default filtring option
                data_plot=data.loc[data['TCU']>=filtering]
               
            #graphical visualization plot button
            if st.button("Plot"):
                with st.spinner("Generating plot..."):
                    plot=PXCU_PQLT_PLOT(data_plot, x_col, y_col, plot_title)
                    st.pyplot(plot)
                    #st.set_option('deprecation.showPyplotGlobalUse', False)
                    st.write("Note: Interactive dashboard is displayed above.")
                    plt.show()
            #creating outliers dataframe        
            #Find OT21  Outliers
            idx=(~(data_plot['PQLT'].between(30, 60))&(data_plot['ORTP']==21) | ~(data_plot['PXCU'].between(20, 60))&
                 (data_plot['ORTP']==21))
            
            OT21_Outliers=data_plot.loc[idx].reset_index(drop=True)

            #Find OT22  Outliers
            idx1=(~(data['PQLT'].between(60, 100))&(data['ORTP']==22) | ~(data['PXCU'].between(50, 100))&(data['ORTP']==22))
            OT22_Outliers=data.loc[idx1].reset_index(drop=True)

            #Find OT27  Outliers
            idx2=(~(data_plot['PQLT'].between(0, 35))&(data_plot['ORTP']==27) | ~(data_plot['PXCU'].between(0, 35))&
                  (data_plot['ORTP']==27))
            OT27_Outliers=data_plot.loc[idx2].reset_index(drop=True)

            #Find OT31  Outliers
            idx3=(~(data_plot['PQLT'].between(50, 100))&(data_plot['ORTP']==31) | ~(data_plot['PXCU'].between(20, 50))&
                  (data_plot['ORTP']==31))
           
            OT31_Outliers=data_plot.loc[idx3].reset_index(drop=True)

            #Find OT32  Outliers
            idx8=(~(data_plot['PQLT'].between(35, 57))&(data_plot['ORTP']==32) | ~(data_plot['PXCU'].between(0, 20))&
                  (data_plot['ORTP']==32))
            OT32_Outliers=data_plot.loc[idx8].reset_index(drop=True)


            #Find OT34  Outliers
            idx4=(~(data_plot['PQLT'].between(57, 100))&(data_plot['ORTP']==34) | ~(data_plot['PXCU'].between(0, 20))&
                  (data_plot['ORTP']==34))
            
            OT34_Outliers=data_plot.loc[idx4].reset_index(drop=True)

            #Find OT37  Outliers
            idx5=(~(data_plot['PQLT'].between(15, 25))&(data_plot['ORTP']==37) | ~(data_plot['PXCU'].between(0, 20))&
                  (data_plot['ORTP']==37))
            
            OT37_Outliers=data_plot.loc[idx5].reset_index(drop=True)

            #Find OT41  Outliers
            idx6=(~(data_plot['PQLT'].between(0, 15))&(data_plot['ORTP']==41) | ~(data_plot['PXCU'].between(0, 15))&
                  (data_plot['ORTP']==41))
           
            OT41_Outliers=data_plot.loc[idx6].reset_index(drop=True)

            #Find OT42  Outliers
            idx7=(~(data_plot['PQLT'].between(15, 35))&(data_plot['ORTP']==42) | ~(data_plot['PXCU'].between(0, 15))&
                  (data_plot['ORTP']==42))
           
            OT42_Outliers=data_plot.loc[idx7].reset_index(drop=True)
            
            #put all outliers into dataframe
            dataframes = {'OT21_Outliers': OT21_Outliers, 'OT22_Outliers': OT22_Outliers, 'OT27_Outliers': OT27_Outliers, 
                          'OT31_Outliers': OT31_Outliers, 'OT32_Outliers': OT32_Outliers,
                          'OT34_Outliers': OT34_Outliers, 'OT37_Outliers': OT37_Outliers, 'OT41_Outliers': OT41_Outliers, 
                          'OT42_Outliers': OT42_Outliers}

                    
            #outlier execution button       
            if st.button("Download Outliers"):
                download_filename = "Outliers.xlsx"
                outliers_download(dataframes, download_filename)
                st.write(f'there are {idx.sum():,} OT21 Outliers  of the {len(idx):,} holes')
                st.write(f'there are {idx1.sum():,} OT22 Outliers  of the {len(idx1):,} holes')
                st.write(f'there are {idx2.sum():,} OT27 Outliers  of the {len(idx2):,} holes')
                st.write(f'there are {idx3.sum():,} OT31 Outliers of the {len(idx3):,} holes')
                st.write(f'there are {idx8.sum():,} OT32 Outliers of the {len(idx8):,} holes')
                st.write(f'there are {idx4.sum():,} OT34 Outliers of the {len(idx4):,} holes')
                st.write(f'there are {idx5.sum():,} OT37 Outliers of the {len(idx5):,} holes')
                st.write(f'there are {idx6.sum():,} OT41 Outliers of the {len(idx6):,} holes')
                st.write(f'there are {idx7.sum():,} OT42 Outliers of the {len(idx7):,} holes')
                st.success("Outliers successfully downloaded to your PC")
            

if __name__ == "__main__":
    main()

    







    