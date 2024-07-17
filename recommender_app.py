import streamlit as st
import pandas as pd
import time
import backend as backend
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode

# Basic webpage setup with emojis and HTML/CSS
st.set_page_config(
    page_title="📚 Course Recommender System",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Centered Title
st.markdown(
    """
    <h1 style='text-align: center; color: #4A90E2;'>📚 Course Recommender System</h1>
    """, 
    unsafe_allow_html=True
)

# ------- Functions ------
# Load datasets
@st.cache_data
def load_ratings():
    try:
        return backend.load_ratings()
    except Exception as e:
        st.error(f"Error loading ratings: {e}")
        return pd.DataFrame()

@st.cache_data
def load_course_sims():
    try:
        return backend.load_course_sims()
    except Exception as e:
        st.error(f"Error loading course similarities: {e}")
        return pd.DataFrame()

@st.cache_data
def load_courses():
    try:
        return backend.load_courses()
    except Exception as e:
        st.error(f"Error loading courses: {e}")
        return pd.DataFrame()

@st.cache_data
def load_bow():
    try:
        return backend.load_bow()
    except Exception as e:
        st.error(f"Error loading bag-of-words data: {e}")
        return pd.DataFrame()

# Initialize the app by first loading datasets
def init_recommender_app():
    with st.spinner('Loading datasets...'):
        ratings_df = load_ratings()
        sim_df = load_course_sims()
        course_df = load_courses()
        course_bow_df = load_bow()

    if ratings_df.empty or sim_df.empty or course_df.empty or course_bow_df.empty:
        st.error("Failed to load datasets. Please check the data files.")
        return pd.DataFrame()

    st.success('Datasets loaded successfully.')

    st.markdown("""---""")
    st.markdown(
        """
        <h2 style='text-align: center; color: #FF6347;'>Select courses that you have audited or completed:</h2>
        """, 
        unsafe_allow_html=True
    )

    # Build an interactive table for `course_df`
    gb = GridOptionsBuilder.from_dataframe(course_df)
    gb.configure_default_column(enablePivot=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    gb.configure_side_bar()
    grid_options = gb.build()

    # Create a grid response
    response = AgGrid(
        course_df,
        gridOptions=grid_options,
        enable_enterprise_modules=True,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
        fit_columns_on_grid_load=False,
    )

    results = pd.DataFrame(response["selected_rows"], columns=['COURSE_ID', 'TITLE', 'DESCRIPTION'])
    results = results[['COURSE_ID', 'TITLE']]
    st.markdown(
        """
        <h3 style='text-align: center; color: #FF6347;'>Your courses:</h3>
        """, 
        unsafe_allow_html=True
    )
    st.table(results)
    return results

def train(model_name, params):
    if model_name == backend.models[0]:
        with st.spinner('Training...'):
            try:
                backend.train(model_name)
                st.success('Model training finished successfully! 🎉')
            except Exception as e:
                st.error(f"Error during model training: {e}")
    else:
        st.warning('Training for selected model is not implemented yet.')

def predict(model_name, user_ids, params):
    res = None
    with st.spinner('Generating course recommendations...'):
        try:
            res = backend.predict(model_name, user_ids, params)
            if res.empty:
                st.warning('No recommendations found. 😕')
            else:
                st.success('Recommendations generated successfully! 🎉')
        except Exception as e:
            st.error(f"Error during prediction: {e}")
    return res

# ------ UI ------
# Sidebar
st.sidebar.title('Personalized Learning Recommender')
# Initialize the app
selected_courses_df = init_recommender_app()

# Model selection selectbox
st.sidebar.subheader('1. Select recommendation models')
model_selection = st.sidebar.selectbox(
    "Select model:",
    backend.models
)

# Hyper-parameters for each model
params = {}
st.sidebar.subheader('2. Tune Hyper-parameters:')
if model_selection == backend.models[0]:
    top_courses = st.sidebar.slider('Top courses', min_value=1, max_value=100, value=10, step=1)
    course_sim_threshold = st.sidebar.slider('Course Similarity Threshold %', min_value=0, max_value=100, value=50, step=10)
    params['top_courses'] = top_courses
    params['sim_threshold'] = course_sim_threshold
elif model_selection == backend.models[1]:
    profile_sim_threshold = st.sidebar.slider('User Profile Similarity Threshold %', min_value=0, max_value=100, value=50, step=10)
elif model_selection == backend.models[2]:
    cluster_no = st.sidebar.slider('Number of Clusters', min_value=1, max_value=50, value=20, step=1)

# Training
st.sidebar.subheader('3. Training:')
training_button = st.sidebar.button("Train Model")
if training_button:
    train(model_selection, params)

# Prediction
st.sidebar.subheader('4. Prediction:')
pred_button = st.sidebar.button("Recommend New Courses")
if pred_button and not selected_courses_df.empty:
    new_id = backend.add_new_ratings(selected_courses_df['COURSE_ID'].values)
    user_ids = [new_id]
    res_df = predict(model_selection, user_ids, params)
    if res_df is not None and not res_df.empty:
        res_df = res_df[['COURSE_ID', 'SCORE']]
        course_df = load_courses()
        res_df = pd.merge(res_df, course_df, on=["COURSE_ID"]).drop('COURSE_ID', axis=1)
        st.markdown(
            """
            <h2 style='text-align: center; color: #4A90E2;'>Recommended Courses</h2>
            """, 
            unsafe_allow_html=True
        )
        st.table(res_df)
