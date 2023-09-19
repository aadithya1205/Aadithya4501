#!/usr/bin/env python
# coding: utf-8

# In[159]:


import streamlit as st
import pandas as pd
from pymongo.mongo_client import MongoClient
import plotly.express as px
st.set_page_config(page_title= "AIR_BNB",
                   layout= "wide",
                   initial_sidebar_state= "expanded")
df=pd.read_csv("airbnb.csv")
tab1,tab2,tab3,tab4=st.tabs([":red[HOME]",":red[TOP 10 CHARTS]",":orange[AIRBNBS ALL OVER THE WORLD]",":red[FIND YOUR SUITABLE AIRBNB IN YOUR COUNTRY]"])
with tab1:
    st.header("AIRBNB ANALYSIS")
    st.header("You can analyse the prices and availibity of rooms,beds and amenities and all other details here")
    st.subheader("Technologies Used:")
    st.markdown(" --> python")
    st.markdown(" --> streamlit")
    st.markdown(" --> Mongodb")
    st.markdown(" --> Tableau")
with tab2:
    st.header("TOP 10 airbnbs in your country ")
    country=st.selectbox("select your country",options=sorted(df.Country.unique()),key="1")
    col1,col2=st.columns(2,gap="medium")
    with col1:
        Room_type=st.selectbox("select your Room Type",options=sorted(df.Room_type.unique()),key="2")
        query=f"Country in '{country}' and Room_type in '{Room_type}' and Review_scores==100"
        df1=df.query(query).sort_values(by="Price",ascending=True,ignore_index=True)[:10]
        if not df1.empty:
            fig = px.bar(df1[["Name","Price"]],
                         title='Top 10 based on room type',
                         x='Name',
                         y='Price',
                         orientation='v',
                         color='Price',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 
        else:
            st.info("Sorry there are no airbnbs available in this category")
    with col2:
        Accomodates=st.selectbox("select your Accomodates",options=sorted(df.Accomodates.unique()),key="3")
        query1=f"Country in '{country}' and Accomodates=={Accomodates} and Review_scores==100"                    
        df2=df.query(query1).sort_values(by="Price",ascending=True,ignore_index=True)[:10]
        if not df2.empty:
            fig = px.bar(df1[["Name","Price"]],
                         title='Top 10 based on Accomodates',
                         x='Name',
                         y='Price',
                         orientation='v',
                         color='Price',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True) 
        else:
            st.info("Sorry there are no airbnbs available in this category")
   
    col3,col4=st.columns(2,gap="medium")
    with col3:
        property_type=st.selectbox("Select your property type",options=sorted(df.Property_type.unique()),key="4")
        query2=f"Country in '{country}' and  Property_type in '{property_type}' and Review_scores==100"
        df3=df.query(query2).sort_values(by="Price",ascending=True,ignore_index=True)[:10]
        if not df3.empty:
            fig = px.bar(df3[["Name","Price"]],
                         title='Top 10 based on Property type',
                         x='Name',
                         y='Price',
                         orientation='v',
                         color='Price',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        else:
            st.info("Sorry there are no airbnbs available in this category")
    with col4:
        Total_beds=st.selectbox("Select your Total_beds",options=sorted(df.Total_beds.unique()),key="5")
        query3=f"Country in '{country}' and Total_beds == {Total_beds} and Review_scores==100"
        df4=df.query(query3).sort_values(by="Price",ascending=True,ignore_index=True)[:10]
        if not df4.empty:
            fig = px.bar(df3[["Name","Price"]],
                         title='Top 10 based on Total_beds',
                         x='Name',
                         y='Price',
                         orientation='v',
                         color='Price',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)
        
      
    with tab3:
        df_data=df.query("Is_location_exact==True")
        fig = px.scatter_geo(df_data, lat='Latitude',lon="Longitude", title="airbnbs around the world",
                             size='Price', locationmode='country names',
                             color="Country",template="plotly_dark",
                             projection="natural earth")
        st.plotly_chart(fig,use_container_width=True)
        country_df = df.groupby(['Country'],as_index=False)['Name'].count().rename(columns={'Name' : 'Total_Listings'})
        fig = px.choropleth(country_df,
                    title='Total Listings in each Country',
                    locations='Country',
                    locationmode='country names',
                    color='Total_Listings',
                    template="plotly_dark",
                    color_continuous_scale=px.colors.sequential.Plasma
                               )
    
        st.plotly_chart(fig,use_container_width=True)
        country_df = df.groupby('Country',as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                                       locations='Country',
                                       color= 'Price', 
                                       hover_data=['Price'],
                                       locationmode='country names',
                                       size='Price',
                                       title= 'Avg Price in each Country',
                                       template="plotly_dark",
                                       color_continuous_scale='agsunset'
                            )

        
        
        st.plotly_chart(fig,use_container_width=True)
    with tab4:
        country=st.selectbox("select your Country",options=sorted(df["Country"].unique()),key="6")
        with st.spinner("please wait"):
            property_type=st.selectbox("select a property type",options=sorted(df["Property_type"].unique()),key="7")
            query11=f"Country=='{country}'and Property_type=='{property_type}'"
            df11=df.query(query11)
            if not df11.empty:
                with st.spinner("please wait"):
                    bed_type=st.selectbox("Enter a bed type",options=sorted(df["Bed_type"].unique()),key="8")
                    query22=f"Country=='{country}'and Property_type=='{property_type}' and Bed_type=='{bed_type}'"
                    df22=df.query(query22)
                    if not df22.empty:
                        with st.spinner("please wait"):
                            total_beds=st.selectbox("Select your total_beds",options=sorted(df["Total_beds"].unique()),key="9")
                            query33=f"Total_beds == {total_beds}"
                            df33=df22.query(query33)
                            if not df33.empty:
                                with st.spinner("please wait"):
                                    Availbility=st.selectbox("Select Availibity",options=sorted(df["Availability_365"].unique()),key="10")
                                    query44=f"Availability_365=={Availbility}"
                                    df44=df33.query(query44)
                                    if not df44.empty:
                                        with st.spinner("please wait"):
                                            Review=st.selectbox("Review scores",options=sorted(df["Review_scores"].unique()),key="11")
                                            query55=f"Review_scores=={Review}"
                                            df55=df44.query(query55)
                                            if not df55.empty:
                                                with st.spinner("please wait"):
                                                    Price=st.selectbox("sortby",("lowest to highest","highest to lowest"),key="12")
                                                    df66=df55.sort_values(by="Price",ascending=True,ignore_index=True)[:10]
                                                    if Price=="lowest to highest":
                                                        fig = px.bar(df66[["Name","Price"]],
                                                        title='Recommended airbnb',
                                                        x='Name',
                                                        y='Price',
                                                        orientation='v',
                                                        color='Price',
                                                        color_continuous_scale=px.colors.sequential.Agsunset)
                                                        st.plotly_chart(fig,use_container_width=True)
                                                        st.dataframe(df66[["Name","Price","Cancellation_policy","Min_nights","Max_nights","Accomodates",'Security_deposit','Guests_included','Amenities']])
                                                    else:
                                                        df77=df55.sort_values(by="Price",ascending=False,ignore_index=True)[:10]
                                                        fig = px.bar(df77[["Name","Price"]],
                                                        title='Recommended airbnb',
                                                        x='Name',
                                                        y='Price',
                                                        orientation='v',
                                                        color='Price',
                                                        color_continuous_scale=px.colors.sequential.Agsunset)
                                                        st.plotly_chart(fig,use_container_width=True)
                                                        st.dataframe(df77[["Name","Price","Cancellation_policy","Min_nights","Max_nights","Accomodates",'Security_deposit','Guests_included','Amenities']])
                                            else:
                                                st.info("NO airbnbs under this Review,try again with another Review")
                                    else:
                                        st.info("NO airbnbs under this Availibility,try again with another  Availibility")
                            else:
                                 st.info("NO airbnbs under this category,Try it with another")
                    else:
                        st.info("No air_bnbs under this bed_type,try to change the bed_type")
            else:
                st.info("No_airbnbs under this property,try to change the property type")
        
                                            

        
        
        
        
        
        
        
        


# In[ ]:





# In[ ]:




