import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def classify_variable(column):
    unique_values = df[column].nunique()
    if pd.api.types.is_numeric_dtype(df[column]):
        if unique_values > 20:
            return 'Continuous'
        else:
            return 'Categorical'
    else:
        return 'Categorical'

# Streamlit App
st.title("Variable Type Selection and Visualization")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Load the data
    df = pd.read_csv(uploaded_file)

    # Classify all variables
    variable_types = {col: classify_variable(col) for col in df.columns}

    # Select variable type
    var_type = st.radio("Select Variable Type", ['Categorical', 'Continuous'])

    # Get list of variables of the selected type
    if var_type == 'Categorical':
        variables = [var for var, vtype in variable_types.items() if vtype == 'Categorical']
    else:
        variables = [var for var, vtype in variable_types.items() if vtype == 'Continuous']

    # Select a variable
    selected_variable = st.selectbox("Select Variable", variables)

    if st.button('Get Graph'):
        # Plot the data
        fig, axs = plt.subplots(1, 2, figsize=(14, 6))

        if var_type == 'Categorical':
            df[selected_variable].value_counts().plot(kind='bar', color='skyblue', ax=axs[0])
            axs[0].set_title(f'Bar Graph of {selected_variable}')
            axs[0].set_xlabel(selected_variable)
            axs[0].set_ylabel('Count')
            
            df[selected_variable].value_counts().plot(kind='hist', bins=30, color='skyblue', ax=axs[1])
            axs[1].set_title(f'Histogram of {selected_variable}')
            axs[1].set_xlabel(selected_variable)
            axs[1].set_ylabel('Frequency')
        else:
            df[selected_variable].plot(kind='hist', bins=30, color='skyblue', ax=axs[0])
            axs[0].set_title(f'Histogram of {selected_variable}')
            axs[0].set_xlabel(selected_variable)
            axs[0].set_ylabel('Frequency')
            
            df[selected_variable].plot(kind='line', color='skyblue', ax=axs[1])
            axs[1].set_title(f'Line Plot of {selected_variable}')
            axs[1].set_xlabel('Index')
            axs[1].set_ylabel(selected_variable)

        for ax in axs:
            ax.grid(axis='y')

        st.pyplot(fig)
