# How to run:  python -m streamlit run main.py

import streamlit as st
import heicToJPEG

st.title("Heic to JPG conversion utility")

st.markdown("<strong style='color:#1E90FF;font-size: 25px'>🎯 Welcome. Pick a task to continue:</strong>", unsafe_allow_html=True)
userChoice = st.selectbox("Task Choice", [".heic to .jpg conversion", "Something else"], label_visibility="collapsed")

if userChoice == ".heic to .jpg conversion":
    with st.form("heicToJPG_input_form"):
        st.markdown("<strong style='color:#1E90FF;'>You can either provide a folder with multiple .heic files, or can provide a single .heic file.</strong>", unsafe_allow_html=True)
        # st.write("You can either provide a folder with multiple .heic files, or can provide a single .heic file.")
        folderOrImage = st.selectbox("Are you providing a folder or a single image file?",["Folder","Image"])
        providedPath = st.text_input("Enter Folder Path or Full Image Path:")
        targetFolder = st.text_input("Target Folder Path (Default: Same as source folder/image):")
        compressionPercentage = st.slider("If you require compression, pls specify a value between 0 and 1 (Default: 1 - No compression). Ex: If the chosen value is 0.5; the image will be spatially compressed to 0.5 times of the original image", 
                                                                        min_value=0.0,
                                                                        max_value=1.0,
                                                                        value=1.0,
                                                                        step=0.1
                                                                    )
        imageQuality = st.selectbox("Select image quality (Default: High)",["Low","Moderate","High"])
        submitted = st.form_submit_button("Submit form")

        if submitted:
            if providedPath is None or providedPath.strip() == "":
                st.error("Please provide Folder Path or Full Image Path to use the utility.")
            else:
                # st.write("Provided Input--> " + folderOrImage + ": " + providedPath)
                st.write("Thanks for providing your input.")
                st.markdown("<strong style='color:#1E90FF;'>Task in progress. Please wait.....</strong>", unsafe_allow_html=True)
                status = heicToJPEG.wrapperHeicToJPG(folderOrImage = folderOrImage, sourcePath = providedPath, targetFolder = targetFolder, compressionPercentage=compressionPercentage, imageQuality=imageQuality)
                if status == "Success":
                    st.markdown("<strong style='color:#1E90FF;'>Task completed successfully. Please change the values in the form and resubmit to perform more similar operations.</strong>", unsafe_allow_html=True)

else:
    st.markdown("<strong style='color:#1E90FF;'>I am not capable to do this. Please choose a different option.</strong>", unsafe_allow_html=True)


