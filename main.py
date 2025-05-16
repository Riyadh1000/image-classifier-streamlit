import streamlit as st
import requests
from PIL import Image
import io

st.title("Классификатор изображений (ShuffleNet)")
st.write("Загрузите изображение для классификации с использованием ShuffleNetV2")

# URL API (заменить на ваш URL при деплое)
API_URL = "https://image-classifier-ruadh3001.amvera.io/classify/"

uploaded_file = st.file_uploader(
    "Выберите изображение",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    try:
        # Отображение загруженного изображения
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, caption="Загруженное изображение", use_column_width=True)
        
        # Правильное форматирование файла для отправки
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
        
        # Кнопка для запуска классификации
        if st.button("Классифицировать"):
            with st.spinner('Обработка изображения...'):
                response = requests.post(API_URL, files=files)
            
            if response.status_code == 200:
                predictions = response.json()["predictions"]
                st.subheader("Результаты классификации:")
                
                # Создаем таблицу для более красивого отображения
                for pred in predictions:
                    st.write(
                        f"{pred['rank']}. Класс {pred['class_name']} - "
                        f"{pred['probability']*100:.2f}%"
                    )
                    
                # Показываем визуализацию вероятностей
                chart_data = {
                    "Класс": [p["class_name"] for p in predictions],
                    "Вероятность (%)": [p["probability"]*100 for p in predictions]
                }
                st.bar_chart(chart_data, x="Класс", y="Вероятность (%)")
                
            else:
                st.error(f"Ошибка при получении предсказания: {response.status_code}")
                st.error(f"Детали ошибки: {response.text}")

    except Exception as e:
        st.error(f"Ошибка обработки изображения: {str(e)}")
