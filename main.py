import streamlit as st
import requests
from PIL import Image

st.title("Классификация изображений (ResNet-50)")
st.write("Загрузите изображение для классификации")

# URL API на хостинге Amvera
API_URL = "https://image-api-ruadh3001.amvera.io/predict"

uploaded_file = st.file_uploader(
    "Выберите изображение",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        # Отображение загруженного изображения
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="Загруженное изображение", use_column_width=True)
        
        # Правильное форматирование файла для отправки через requests
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        # Добавляем кнопку для отправки запроса
        if st.button("Классифицировать"):
            with st.spinner('Обработка изображения...'):
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
                st.error(f"Ошибка при получении предсказания: {response.status_code}")
                st.error(f"Информация об ошибке: {response.text}")

    except Exception as e:
        st.error(f"Ошибка обработки изображения: {str(e)}")
