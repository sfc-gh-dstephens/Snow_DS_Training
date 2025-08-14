# Import python packages
from snowflake.snowpark.context import get_active_session
from snowflake.ml.utils.connection_params import SnowflakeLoginOptions
from snowflake.snowpark import Session
import streamlit as st
import sys
import time

# Configure page
st.set_page_config(layout="wide")

@st.cache_resource
def get_snowflake_session():
    """Cache the Snowflake session to avoid recreating it on every run."""
    try:
        if sys._xoptions.get("snowflake_import_directory"):
            return get_active_session()
        else:
            return Session.builder.configs(SnowflakeLoginOptions()).getOrCreate()
    except Exception as e:
        st.error(f"Failed to create Snowflake session: {str(e)}")
        return None

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_survival_prediction(sibsp, parch, fare, pclass, who, town):
    """Cache prediction results with proper error handling."""
    session = get_snowflake_session()
    
    if session is None:
        return None, None
    
    try:
        # Execute the prediction query
        start_time = time.time()
        
        result = session.sql(
            f"""
            select TITANIC_PIPE_PREDICTION_SERVICE!predict_proba(
            {sibsp},
            {parch},
            {fare},
            '{pclass}',
            '{who}',
            '{town}'
            ):output_feature_1 AS surv_prob
            """
        ).collect()

        end_time = time.time()
        runtime = end_time - start_time
        
        # Check if we got results
        if not result or len(result) == 0:
            st.error("No prediction result returned from the model")
            return None, runtime
            
        # Extract the prediction value
        prediction_value = result[0][0]
        
        # Handle None values
        if prediction_value is None:
            st.error("Prediction service returned None. Please check if the model is properly deployed.")
            return None, runtime
            
        # Convert to float and percentage
        try:
            return round(float(prediction_value) * 100, 2), runtime
        except (ValueError, TypeError) as e:
            st.error(f"Invalid prediction value returned: {prediction_value}. Error: {str(e)}")
            return None, runtime
            
    except Exception as e:
        st.error(f"Error executing prediction query: {str(e)}")
        return None, None

# Initialize session
session = get_snowflake_session()

if session is None:
    st.stop()

st.title("Will you survive the titanic?")

# Use a form to prevent reruns on every input change
with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        pclass = st.selectbox("What class is your ticket?", ["FIRST", "SECOND", "THIRD"])
        town = st.selectbox("What town did you embark from?", ["SOUTHAMPTON", "CHERBOURG", "QUEENSTOWN"])
    
    with col2:
        fare = st.number_input("What was the cost of your ticket?", min_value=0.00, max_value=512.00, value=50.0)
        who = st.selectbox("Are you a Man, Woman, or Child?", ("MAN", "WOMAN", "CHILD"))
    
    with col3:
        sibsp = st.number_input("How many siblings/spouses are traveling with you?", min_value=0, max_value=8, value=0, step=1)
        parch = st.number_input("How many parents/children are traveling with you?", min_value=0, max_value=6, value=0, step=1)
    
    # Form submit button
    submitted = st.form_submit_button("Get your chance of survival")

# Process prediction when form is submitted
if submitted:
    with st.spinner('Calculating your survival chances...'):
        # Debug: Show the inputs being sent
        # with st.expander("Debug Info (click to expand)"):
        #     st.write("Input parameters:")
        #     st.json({
        #         "sibsp": sibsp,
        #         "parch": parch, 
        #         "fare": fare,
        #         "pclass": pclass,
        #         "who": who,
        #         "town": town
        #     })
        
        surv_pred, runtime = get_survival_prediction(sibsp, parch, fare, pclass, who, town)
        
        if surv_pred is not None:
            st.session_state['surv_pred'] = surv_pred
            st.session_state['runtime'] = runtime
            #st.success(f"Prediction successful: {surv_pred}%")
        else:
            st.error("Failed to get prediction. Please check the debug info above and try again.")
            # Still store runtime even if prediction failed
            if runtime is not None:
                st.session_state['runtime'] = runtime

# Display result if available
if 'surv_pred' in st.session_state and st.session_state['surv_pred'] is not None:
    st.metric(value=f"{st.session_state['surv_pred']}%", label="Chance of surviving the Titanic")

# Display runtime at the bottom
if 'runtime' in st.session_state and st.session_state['runtime'] is not None:
    st.markdown("---")
    st.caption(f"Prediction service runtime: {st.session_state['runtime']:.3f} seconds")