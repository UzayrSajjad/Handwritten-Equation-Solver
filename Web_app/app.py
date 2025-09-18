import streamlit as st      
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2 
from predict import predict
import base64

def display_results(eq, res):
    """Helper function to display prediction results"""
    st.write(f"#### Equation: **{eq}**")
    x = str(res)
    res_length = len(x)
    width = 100
    font_size = 35
    if res_length > 3:
        width = 150
        font_size = 25

    padding_top = max(5, (40 - font_size) / 2)
    padding_bottom = max(5, (40 - font_size) / 2)
    style = f"background-color: grey; height: 70px; width: {width}px; border-radius: 5px; padding-top: {padding_top}px; padding-bottom: {padding_bottom}px; margin-left: 150px; text-align: center;"

    label_style = "font-weight: bold; color: white; font-size: {font_size}px;"
    label_style = label_style.format(font_size=font_size)

    st.subheader("Result")
    st.markdown(f"<div style='{style}'><label style='{label_style}'>{res}</label></div>", unsafe_allow_html=True)
st.set_page_config(page_title="Equation Solver",initial_sidebar_state="auto")


st.markdown(
    """
    <style>
    .container {
        display: flex;
    }
    .logo-text {
        font-weight:700;
        font-size:50px ;
        color: black ;
        margin-left:-15px;
        padding: 15px ;
    }
    .logo-img {
        float:right;
        width: 100px;
        height:100px;
    }

    /* Custom icon colors: white by default, red on hover */
    /* Target common Streamlit button/icon classes and svg icons inside buttons */
    .stButton>button, .stDownloadButton>button, .stFileUploader, .stSidebar button {
        color: white !important;
    }

    /* For svg icons inside buttons */
    .stButton>button svg, .stSidebar button svg, .stToolbar button svg, button svg {
        fill: white !important;
        stroke: white !important;
    }

    /* Hover state: turn icons red */
    .stButton>button:hover svg, .stSidebar button:hover svg, button:hover svg, .stButton>button:hover, .stSidebar button:hover {
        fill: red !important;
        stroke: red !important;
        color: red !important;
    }

    /* Additional specific selectors for back/forward/delete icons if they have aria-labels or titles */
    button[title~="Back"] svg, button[aria-label~="Back"] svg,
    button[title~="Forward"] svg, button[aria-label~="Forward"] svg,
    button[title~="Delete"] svg, button[aria-label~="Delete"] svg {
        fill: white !important;
        stroke: white !important;
    }
    button[title~="Back"]:hover svg, button[aria-label~="Back"]:hover svg,
    button[title~="Forward"]:hover svg, button[aria-label~="Forward"]:hover svg,
    button[title~="Delete"]:hover svg, button[aria-label~="Delete"]:hover svg {
        fill: red !important;
        stroke: red !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


stroke_color = "black"
bg_color = "white"
drawing_mode = "freedraw"
realtime_update = True


# Create tabs for different input methods
tab1, tab2 = st.tabs(["📝 Draw Equation", "📷 Upload Image"])

with tab1:
    st.subheader("Draw your equation on the canvas below:")
    
    with st.sidebar:
        stroke_width=st.slider(label="Adjust Stroke Width",value=5,min_value=3,max_value=10)

        
    data = st_canvas(
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        update_streamlit=realtime_update,
        height=300,
        width=700,
        drawing_mode=drawing_mode,
        key="canvas_app",
    )

    if st.button('Predict from Drawing', key="predict_canvas"):
        if data.image_data is not None:
            path='temp/temp.png'
            cv2.imwrite(path, data.image_data)
            try:
                eq, res = predict(path)
                display_results(eq, res)
            except Exception as e:
                st.error(f"Error predicting equation: {str(e)}")
        else:
            st.warning("Please draw an equation first!")

with tab2:
    st.subheader("Upload an image containing a handwritten equation:")
    
    uploaded_file = st.file_uploader(
        "Choose an image file", 
        type=['png', 'jpg', 'jpeg', 'bmp'],
        help="Upload an image containing a handwritten mathematical equation"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        # Convert PIL image to OpenCV format and save
        image_array = np.array(image)
        if len(image_array.shape) == 3:
            image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        else:
            image_cv = image_array
            
        # Save the uploaded image
        upload_path = 'temp/uploaded_image.png'
        cv2.imwrite(upload_path, image_cv)
        
        if st.button('Predict from Image', key="predict_upload"):
            try:
                eq, res = predict(upload_path)
                display_results(eq, res)
            except Exception as e:
                st.error(f"Error predicting equation: {str(e)}")
