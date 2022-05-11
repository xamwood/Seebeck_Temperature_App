#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  1 20:14:48 2022

@author: maxwood
"""
import streamlit as st
import pandas as pd
import numpy as np
import copy
import matplotlib.pyplot as plt
import csv


ke = 8.617333262145*10**(-5)

st.write(
    """
#  Seebeck Temperature Checker
Upload your seebeck data to see if it strays from a single parabolic band model
"""
)

uploaded_file = st.file_uploader("Upload CSV", type=".csv")

df = pd.read_csv('Seeb_example.csv')
example_data = df.to_csv(index = False)

st.download_button('Download Example Data To Try!',example_data, file_name = 'example_seebeck.csv')

ab_default = None
result_default = None



if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.markdown("### Data preview")
    st.dataframe(df.head())

    st.markdown("### Select columns for analysis")
    with st.form(key="my_form"):
        ab = st.multiselect(
            "Temperature (K)",
            options=df.columns,
            help="Select which column refers to the temperature you want to analyze",
            default=ab_default,
        )

        result = st.multiselect(
            "Seebeck (uV/K)",
            options=df.columns,
            help="Select which Seebeck values you want to anlayze",
            default=result_default,
        )


        with st.expander("Adjust test parameters"):
            st.write("### Parameters")
            aps = st.checkbox('λ = 0 (APS)', value = True)
            iis = st.checkbox('λ = 2 (IIS)')

        submit_button = st.form_submit_button(label="Submit")

    if not ab or not result:
        st.warning("Please select which column is Seebeck and which column is temperature")
        st.stop()
    
        
    with open('data3.npy', 'rb') as f: data = np.load(f)
    data_aps = data[:,:,:] # the high cc values aren't realistic and messing with plotting
    data_iis = data[:,:,:]
    Tlow = np.float(df[ab].min())
    Tmax = np.float(df[ab].max())
    Tsel = st.number_input('Temperature to base Seebeck',
                           value = Tlow, 
                           min_value = Tlow,
                           max_value = Tmax)
    Tsel_loc = np.argmin(abs(df[ab]-Tsel))
    Seebsel= np.float(df[result].iloc[Tsel_loc])
    Tsel_really = np.float(df[ab].iloc[Tsel_loc]) # this grabs the closest temp to what the user inputs
    
    T_loc = np.argmin(abs(data[0,:,0]-Tsel_really))
    T_loc_min = np.argmin(abs(data[0,:,0]-Tlow))
    T_loc_max = np.argmin(abs(data[0,:,0]-Tmax))
    st.write(T_loc)    
    n_loc_aps = np.argmin(abs(data_aps[:,T_loc,4]*10**6-Seebsel))
    n_loc_iis = np.argmin(abs(data_iis[:,T_loc,3]*10**6-Seebsel))


    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.scatter(
        df[ab],
        df[result],
        label = 'experimental data'
    )
    if aps:
        ax.plot(
            data[n_loc_aps,T_loc_min-5:T_loc_max+5,0],
            data[n_loc_aps,T_loc_min-5:T_loc_max+5,4]*10**6,
            label = 'λ = 0 (APS)')
    if iis:
        ax.plot(
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,0],
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,3]*10**6,
            label = 'λ = 2 (IIS)')
    ax.legend()

    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Seebeck (uV/K)")

    st.write(fig)
        

    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    if aps:
        ax.plot(
            data[n_loc_aps,T_loc_min-20:T_loc_max+20,0],
            data[n_loc_aps,T_loc_min-20:T_loc_max+20,2],
            label = 'λ = 0 (APS)')
    
    if iis:
        ax.plot(
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,0],
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,2],
            label = 'λ = 2 (IIS)')
    ax.legend()
    
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("η reduced chemical potential (Ef-E)/kT")

    st.write(fig)
        

    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    
    
    if aps:
        ax.plot(
            data[n_loc_aps,T_loc_min-20:T_loc_max+20,0],
            data[n_loc_aps,T_loc_min-20:T_loc_max+20,2]*data[n_loc_aps,T_loc_min-20:T_loc_max+20,0]*ke,
            label = 'λ = 0 (APS)')
    
    if iis:
        ax.plot(
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,0],
            data[n_loc_iis,T_loc_min-20:T_loc_max+20,2]*data[n_loc_aps,T_loc_min-20:T_loc_max+20,0]*ke,
            label = 'λ = 2 (IIS)')
    ax.legend()
    ax.set_xlabel("Temperature (K)")
    ax.set_ylabel("Fermi Level distance from band edge (eV) (Ef-E)")

    st.write(fig)

        



