import streamlit as st
import requests
from PIL import Image

st.title("Классификация изображений (ResNet-50)")
st.write("Загрузите изображение для классификации")

# изменить на реальные url
API_URL = "http://api:8000/predict"  
# API_URL = "http://localhost:8000/predict" 

uploaded_file = st.file_uploader(
    "Выберите изображение",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="Загруженное изображение", use_column_width=True)
        
        files = {"file": uploaded_file.getvalue()}
        response = requests.post(API_URL, files=files)
        
        if response.status_code == 200:
            predictions = response.json()["predictions"]
            st.subheader("Топ-5 предсказаний:")
            for i, pred in enumerate(predictions):
                st.write(
                    f"{i+1}. Класс {pred['class']} - "
                    f"{pred['probability']*100:.2f}%"
                )
        else:
            st.error("Ошибка при получении предсказания")

    except Exception as e:
        st.error(f"Ошибка обработки изображения: {str(e)}")
