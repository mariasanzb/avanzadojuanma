import streamlit as st
import pickle
import pandas as pd
import os

# Cargar el modelo y los datos
#with open('.../Datos/similarity_matrix.pkl', 'rb') as f:
#   similarity_matrix = pickle.load(f)

model_path = os.path.join(os.path.dirname(__file__), '../Datos/similarity_matrix.pkl')

# Cargar el modelo desde el archivo .pkl
with open(model_path, 'rb') as file:
    similarity_matrix = pickle.load(file)


# Cargar los datos de negocios (restaurantes) agrupados por reseñas
#business_reviews_grouped = pd.read_csv('business_reviews_grouped.csv')
import os
import pandas as pd

# Ruta relativa al archivo Parquet
data_path = os.path.join(os.path.dirname(__file__), '../business.parquet')
business_reviews_grouped = pd.read_parquet(data_path)


# Función de recomendación
def recommend_restaurants_based_on_reviews(restaurant_id, n=15):
    if restaurant_id not in business_reviews_grouped['business_id'].values:
        raise ValueError(f"El restaurante con ID '{restaurant_id}' no se encuentra en los datos.")
    restaurant_index = business_reviews_grouped[business_reviews_grouped['business_id'] == restaurant_id].index[0]
    similarity_score = list(enumerate(similarity_matrix[restaurant_index]))
    similarity_score = sorted(similarity_score, key=lambda x: x[1], reverse=True)
    similarity_score = similarity_score[1:n+1]
    restaurant_indices = [i[0] for i in similarity_score]
    return business_reviews_grouped.iloc[restaurant_indices][['business_id', 'name', 'categories', 'city']]

# Título y descripción
st.title("Recomendador de Restaurantes")
st.markdown("Ingresa un `restaurant_id` para obtener recomendaciones personalizadas de restaurantes similares.")

# Entrada de texto para el restaurant_id
restaurant_id = st.text_input("Ingrese un Restaurant ID", "Bf87HcPERF9yiSjb2tQBqw")

# Botón para obtener recomendaciones
if st.button('Obtener Recomendaciones'):
    try:
        recommendations = recommend_restaurants_based_on_reviews(restaurant_id)
        st.subheader(f"Restaurantes recomendados para el usuario {restaurant_id}:")
        for index, row in recommendations.iterrows():
            st.write(f"**{row['name']}** - {row['categories']} - {row['city']}")
    except ValueError as e:
        st.error(f"Error: {e}")
