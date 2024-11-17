import pandas as pd
import os
import json
import requests
from time import sleep
import random
from unicodedata import normalize
import base64, struct
from datetime import datetime, timedelta

# Carga la data de los archivos
GOOGLE_PATH = "data/google"
DATA_PATH = "data/libros.csv"
API_KEY = "AIzaSyARZ0__vzi64hmmlMBbAAG6dqUFFiSmmOg"
BASE_URL = "https://www.googleapis.com/books/v1/volumes?q=+isbn:"
ERROR_ID = 2998
LEN = 20000 - ERROR_ID
SQL_FILE_PATH = "data/insert_queries.sql"

# Languages map 
LANGUAGES = {
    "en": "Inglés",
    "es": "Español",
    "fr": "Francés",
    "de": "Alemán",
    "it": "Italiano",
    "pt": "Portugués",
    "nl": "Holandés",
    "ja": "Japonés",
    "ru": "Ruso",
    "ca": "Catalán",
    "eo": "Esperanto",
}

# Data csv
csvs = {
    "author": "data/output/1_author.",
    "publisher": "data/output/2_publisher.",
    "genre": "data/output/3_genre.",
    "books": "data/output/4_books.",
    "authors_books": "data/output/5_authors_books.",
    "genre_books": "data/output/6_genre_books.",
    "image": "data/output/7_image.",
    "lang": "data/output/8_lang.",
    "books_lang": "data/output/9_books_lang."
}

# Diccionarios para almacenar autores, editoriales y categorías existentes con sus IDs
existing_authors = {}
existing_publishers = {}
existing_categories = {}
existing_langs = {}

# Contadores para los IDs simulados (esto simula lo que la base de datos haría)
author_id_counter = 1
publisher_id_counter = 1
category_id_counter = 1
lang_id_counter = 1
book_id_counter = 1
images_id_counter = 1

authors_pd = pd.DataFrame(columns=["id_author", "name", "created_at", "updated_at"])
publishers_pd = pd.DataFrame(columns=["id_publisher", "name", "created_at", "updated_at"])
categories_pd = pd.DataFrame(columns=["id_category", "name", "created_at", "updated_at"])
books_pd = pd.DataFrame(columns=["id_book", "depth", "height", "isbn_10", "isbn_13", "pages", "price", "rating", "release_date", "synopsis", "title", "weight", "width", "id_publisher", "created_at", "updated_at"])
authors_books_pd = pd.DataFrame(columns=["id_author", "id_book", "created_at", "updated_at"])
categories_books_pd = pd.DataFrame(columns=["id_category", "id_book", "created_at", "updated_at"])
images_pd = pd.DataFrame(columns=["id_image", "url", "alt", "id_book", "created_at", "updated_at"])
lang_pd = pd.DataFrame(columns=["id_lang", "name", "abbr", "created_at", "updated_at"])
books_lang_pd = pd.DataFrame(columns=["id_book", "id_lang", "created_at", "updated_at"])

def random_pages():
    return random.randint(1, 500)

def random_price():
    # return random float between 1 and 100
    return round(random.uniform(1, 100), 2)

def random_rating():
    # return random float between 1 and 5
    return round(random.uniform(1, 5), 2)

def random_weight():
    # return random float between 1 and 10
    return round(random.uniform(1, 10), 2)

def random_width():
    # return random float between 1 and 10
    return round(random.uniform(1, 10), 2)

def random_height():
    # return random float between 1 and 10
    return round(random.uniform(1, 10), 2)

def random_depth():
    # return random float between 1 and 10
    return round(random.uniform(1, 10), 2)


def main():
    data = pd.read_csv(DATA_PATH)
    data_LEN = data[ERROR_ID:LEN].reset_index(drop=True)
    #get_data_from_google(data_LEN)
    clean_data()
    #process_google_data()
    add_sql()

def get_data_from_google(data_LEN):
    books_not_found = []
    count = ERROR_ID
    for i in range(len(data_LEN)):
        isbn = data_LEN["isbn"][i]
        url = BASE_URL + isbn + "&key=" + API_KEY
        try:
            response = requests.get(url)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching book with ISBN {isbn}")
            continue

        rjson = response.json()
        
        # Verificar si el libro fue encontrado
        if rjson["totalItems"] == 0:
            print(f"{count}/{LEN} Book with ISBN {isbn} not found")
            count += 1
            books_not_found.append(isbn)
            sleep(1)  # Respeto a las limitaciones de la API
            continue
        
        with open(f"{GOOGLE_PATH}/google_book_{isbn}.json", "w", encoding='utf8') as f:
            f.write(response.text)
            
            print(f"{count}/{LEN} Book with ISBN {isbn} created")
            count += 1
        
        sleep(1)  # Respeto a las limitaciones de la API

    data_clean = data_LEN[~data_LEN["isbn"].isin(books_not_found)]
    data_clean.to_csv("data/libros_clean.csv", index=False)
    print("Data fetching completed")

def clean_data():
    isbn_in_data = []
    # read isbn in files in google folder
    for file in os.listdir("data/google"):
        filename = os.fsdecode(file)
        isbn = filename.split("_")[2].split(".")[0]
        isbn_in_data.append(isbn)
    
    data = pd.read_csv(DATA_PATH)
    data_clean = data[data["isbn"].isin(isbn_in_data)]
    data_clean.to_csv("data/libros_clean.csv", index=False)

def process_google_data():
    global images_id_counter
    global author_id_counter
    global publisher_id_counter
    global category_id_counter
    global lang_id_counter
    global book_id_counter
    global authors_pd
    global publishers_pd
    global categories_pd
    global books_pd
    global authors_books_pd
    global categories_books_pd
    global images_pd
    global lang_pd
    global books_lang_pd

    clean_data = pd.read_csv("data/libros_clean.csv")
    clean_data['isbn'] = clean_data['isbn'].astype(str)

    for file in os.listdir("data/google"):
        filename = os.fsdecode(file)
        with open(f"data/google/{filename}", "r", encoding='utf8') as f:
            print(f"Processing file {filename}")
            rjson = json.load(f)
            item = rjson.get("items", [{}])[0]
            book_in_data = None

            # Check len of item.get("volumeInfo", {}).get("industryIdentifiers", [{}])
            len_industryIdentifiers = len(item.get("volumeInfo", {}).get("industryIdentifiers", [{}]))
            
            if len_industryIdentifiers == 0:
                continue
            elif len_industryIdentifiers == 1:
                continue
            else:
                isbn_13 = item.get("volumeInfo", {}).get("industryIdentifiers", [{}])[0].get("identifier", "")
                isbn_10 = item.get("volumeInfo", {}).get("industryIdentifiers", [{}])[1].get("identifier", "")
    

            for i in range(len(clean_data)):
                if clean_data["isbn"][i] == isbn_13 or clean_data["isbn"][i] == isbn_10:
                    print(f"Matched {clean_data['isbn'][i]} with {isbn_13}")
                    book_in_data = clean_data.iloc[i]
                    break
            
            # Procesar autores
            authors = item.get("volumeInfo", {}).get("authors", [])
            author_ids = []
            for author in authors:
                if author is None:
                    continue
                author_id = add_author_to_pd(author)
                author_ids.append(author_id)
            
            # Procesar editoriales
            publisher = item.get("volumeInfo", {}).get("publisher", "")
            publisher_id = None
            if publisher != "" and publisher is not None:
                publisher_id = add_publisher_to_pd(publisher)

            # Procesar categorías
            categories = item.get("volumeInfo", {}).get("categories", [])
            category_ids = []
            for category in categories:
                category_id = add_category_to_pd(category)
                category_ids.append(category_id)
            if len(categories) == 0:
                category_id = add_category_to_pd("Sin categoría")
                category_ids.append(category_id)
            
            # Procesar idiomas
            langs_ids = []
            language = item.get("volumeInfo", {}).get("language", "")
            if language != "" and language is not None:
                lang_id = add_lang_to_pd(language)  
                langs_ids.append(lang_id)
            if len(langs_ids) == 0:
                lang_id = add_lang_to_pd("N/A")
                langs_ids.append(lang_id)

            # Procesar libro
            book = item.get("volumeInfo", {})
            book_id = book_id_counter
            book_id_counter += 1
            page_count = book.get("pageCount", book_in_data["cantidad_paginas"] if book_in_data is not None else random.randint(100, 500))
            books_pd = books_pd._append({
                "id_book": book_id,
                "depth": book.get("dimensions", {}).get("thickness", random_depth()),
                "height": book.get("dimensions", {}).get("height", random_height()),
                "isbn_10": isbn_10,
                "isbn_13": isbn_13,
                "pages": page_count,
                "price": book.get("retailPrice", {}).get("amount", random_price()),
                "rating": book.get("averageRating", random_rating()),
                "release_date": book.get("publishedDate", book_in_data["anio"] if book_in_data is not None else "N/A"),
                "synopsis": book.get("description", book_in_data["descripcion"] if book_in_data is not None else "Sin descripción disponible"),
                "title": book.get("title", book_in_data["nombre"] if book_in_data is not None else "Título desconocido"),
                "weight": book.get("dimensions", {}).get("weight", random_weight()),
                "width": book.get("dimensions", {}).get("width", random_width()),
                "id_publisher": publisher_id if publisher_id is not None else random.randint(1, 10),
                "created_at": "NOW()",
                "updated_at": "NOW()"
            }, ignore_index=True)

            # Procesar autores-libros
            for author_id in author_ids:
                authors_books_pd = authors_books_pd._append({
                    "id_author": author_id,
                    "id_book": book_id,
                    "created_at": "NOW()",
                    "updated_at": "NOW()"
                }, ignore_index=True)
            
            # Procesar categorías-libros
            for category_id in category_ids:
                categories_books_pd = categories_books_pd._append({
                    "id_category": category_id,
                    "id_book": book_id,
                    "created_at": "NOW()",
                    "updated_at": "NOW()"
                }, ignore_index=True)

            # Procesar idiomas-libros
            for lang_id in langs_ids:
                books_lang_pd = books_lang_pd._append({
                    "id_book": book_id,
                    "id_lang": lang_id,
                    "created_at": "NOW()",
                    "updated_at": "NOW()"
                }, ignore_index=True)

            # Procesar imágenes
            images = book.get("imageLinks", {})
            image_smallThumbnail = images.get("smallThumbnail", "")
            image_thumbnail = images.get("thumbnail", "")
            image_small = images.get("small", "")
            image_medium = images.get("medium", "")
            image_large = images.get("large", "")
            image_extraLarge = images.get("extraLarge", "")
            image_book_in_data = book_in_data["imagen_url"] if book_in_data is not None else ""
            images = [image_smallThumbnail, image_thumbnail, image_small, image_medium, image_large, image_extraLarge, image_book_in_data]

            for image in images:
                if image == "":
                    continue
                images_pd = images_pd._append({
                    "id_image": images_id_counter,
                    "url": image,
                    "alt": book.get("title", ""),
                    "id_book": book_id,
                    "created_at": "NOW()",
                    "updated_at": "NOW()"
                }, ignore_index=True)
                images_id_counter += 1

            # Guardar los dataframes en csv
            authors_pd.to_csv('data/output/csv/1_author.csv', index=False)
            publishers_pd.to_csv('data/output/csv/2_publisher.csv', index=False)
            categories_pd.to_csv('data/output/csv/3_genre.csv', index=False)
            books_pd.to_csv('data/output/csv/4_books.csv', index=False)
            authors_books_pd.to_csv('data/output/csv/5_authors_books.csv', index=False)
            categories_books_pd.to_csv('data/output/csv/6_genre_books.csv', index=False)
            images_pd.to_csv('data/output/csv/7_image.csv', index=False)
            lang_pd.to_csv('data/output/csv/8_lang.csv', index=False)
            books_lang_pd.to_csv('data/output/csv/9_books_lang.csv', index=False)
            
def add_author_to_pd(author_name):
    global author_id_counter
    global authors_pd

    if author_name not in existing_authors:
        existing_authors[author_name] = author_id_counter
        authors_pd = authors_pd._append({"id_author": author_id_counter, "name": author_name, "created_at": "NOW()", "updated_at": "NOW()"}, ignore_index=True)
        author_id_counter += 1

    return existing_authors[author_name]

def add_publisher_to_pd(publisher_name):
    global publisher_id_counter
    global publishers_pd

    if publisher_name not in existing_publishers:
        existing_publishers[publisher_name] = publisher_id_counter
        publishers_pd = publishers_pd._append({"id_publisher": publisher_id_counter, "name": publisher_name, "created_at": "NOW()", "updated_at": "NOW()"}, ignore_index=True)
        publisher_id_counter += 1

    return existing_publishers[publisher_name]

def add_category_to_pd(category_name):
    global category_id_counter
    global categories_pd

    if category_name not in existing_categories:
        existing_categories[category_name] = category_id_counter
        categories_pd = categories_pd._append({"id_category": category_id_counter, "name": category_name, "created_at": "NOW()", "updated_at": "NOW()"}, ignore_index=True)
        category_id_counter += 1

    return existing_categories[category_name]

def add_lang_to_pd(lang_name):
    global lang_id_counter
    global lang_pd

    if lang_name not in existing_langs:
        existing_langs[lang_name] = lang_id_counter
        lang_pd = lang_pd._append({"id_lang": lang_id_counter, "name": LANGUAGES[lang_name], "abbr": lang_name, "created_at": "NOW()", "updated_at": "NOW()"}, ignore_index=True)
        lang_id_counter += 1

    return existing_langs[lang_name]

def add_sql():
    #remove files in sql folder
    for file in os.listdir("data/output/sql"):
        os.remove(f"data/output/sql/{file}")
    authors_to_sql()
    publishers_to_sql()
    categories_to_sql()
    books_to_sql()
    authors_books_to_sql()
    categories_books_to_sql()
    images_to_sql()
    lang_to_sql()
    books_lang_to_sql()
    generate_randoms_users(1000)
    posts = generate_posts()
    generate_state_history_with_logic(posts)

def authors_to_sql():
    authors = pd.read_csv("data/output/csv/1_author.csv")
    authors_sql_path = "data/output/sql/1_author.sql"
    with open(authors_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(authors)):
            # Escapar comillas simples
            author_name = authors['name'][i].replace("'", "''")
            f.write(f"INSERT INTO public.author (name, created_at, updated_at) VALUES ('{author_name}', {authors['created_at'][i]}, {authors['updated_at'][i]});\n")

def publishers_to_sql():
    publishers = pd.read_csv("data/output/csv/2_publisher.csv")
    publishers_sql_path = "data/output/sql/2_publisher.sql"
    with open(publishers_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(publishers)):
            name = publishers['name'][i].replace("'", "''")
            f.write(f"INSERT INTO public.publisher (name, created_at, updated_at) VALUES ('{name}', {publishers['created_at'][i]}, {publishers['updated_at'][i]});\n")

def categories_to_sql():
    categories = pd.read_csv("data/output/csv/3_genre.csv")
    categories_sql_path = "data/output/sql/3_genre.sql"
    with open(categories_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(categories)):
            name = categories['name'][i].replace("'", "''")
            f.write(f"INSERT INTO public.genre (name, created_at, updated_at) VALUES ('{name}', {categories['created_at'][i]}, {categories['updated_at'][i]});\n")

def books_to_sql():
    books = pd.read_csv("data/output/csv/4_books.csv")
    # transform date to yyyy-mm-dd
    books['synopsis'] = books['synopsis'].fillna('')
    books['synopsis'] = books['synopsis'].astype(str)
    books_sql_path = "data/output/sql/4_books.sql"
    with open(books_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(books)):
            # Escapar comillas simples en todos los valores de texto
            synopsis = books['synopsis'][i].replace("'", "''")
            title = books['title'][i].replace("'", "''")
            release_date = format_date(books['release_date'][i])
            f.write(f"INSERT INTO public.book (depth, height, isbn_10, isbn_13, pages, price, rating, release_date, synopsis, title, weight, width, id_publisher, created_at, updated_at) VALUES ({books['depth'][i]}, {books['height'][i]}, '{books['isbn_10'][i]}', '{books['isbn_13'][i]}', {books['pages'][i]}, {books['price'][i]}, {books['rating'][i]}, '{release_date}', '{synopsis}', '{title}', {books['weight'][i]}, {books['width'][i]}, {books['id_publisher'][i]}, {books['created_at'][i]}, {books['updated_at'][i]});\n")

def format_date(date):
    # Convertir a cadena si no lo es
    if not isinstance(date, str):
        date = str(date)

    # Verificar valores no válidos
    if date in ('', 'nan', 'NaN', 'None') or len(date.split('-')) != 3:
        return random_date()  # Usar una fecha aleatoria como predeterminado

    return date

def random_date():
    date = f"{random.randint(1935, 2024)}-{random.randint(1, 12)}-{random.randint(1, 28)}"
    # add leading zero to month and day
    return '-'.join([f"{int(x):02d}" for x in date.split('-')])

def authors_books_to_sql():
    authors_books = pd.read_csv("data/output/csv/5_authors_books.csv")
    authors_books_sql_path = "data/output/sql/5_authors_books.sql"
    with open(authors_books_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(authors_books)):
            f.write(f"INSERT INTO public.book_author (id_author, id_book) VALUES ({authors_books['id_author'][i]}, {authors_books['id_book'][i]});\n")

def categories_books_to_sql():
    categories_books = pd.read_csv("data/output/csv/6_genre_books.csv")
    categories_books_sql_path = "data/output/sql/6_genre_books.sql"
    with open(categories_books_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(categories_books)):
            f.write(f"INSERT INTO public.book_genre (id_genre, id_book) VALUES ({categories_books['id_category'][i]}, {categories_books['id_book'][i]});\n")

def images_to_sql():
    images = pd.read_csv("data/output/csv/7_image.csv")
    images_sql_path = "data/output/sql/7_image.sql"
    with open(images_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(images)):
            alt = images['alt'][i].replace("'", "''")
            f.write(f"INSERT INTO public.image (url, alt, id_book) VALUES ('{images['url'][i]}', '{alt}', {images['id_book'][i]});\n")

def lang_to_sql():
    lang = pd.read_csv("data/output/csv/8_lang.csv")
    lang_sql_path = "data/output/sql/8_lang.sql"
    with open(lang_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(lang)):
            f.write(f"INSERT INTO public.lang (name, abbr, created_at, updated_at) VALUES ('{lang['name'][i]}', '{lang['abbr'][i]}', {lang['created_at'][i]}, {lang['updated_at'][i]});\n")

def books_lang_to_sql():
    books_lang = pd.read_csv("data/output/csv/9_books_lang.csv")
    books_lang_sql_path = "data/output/sql/9_books_lang.sql"
    with open(books_lang_sql_path, "a", encoding='utf-8') as f:
        for i in range(len(books_lang)):
            f.write(f"INSERT INTO public.book_lang (id_book, id_lang) VALUES ({books_lang['id_book'][i]}, {books_lang['id_lang'][i]});\n")

def generate_randoms_users(n):
    #INSERT INTO public."user" (created_at, deleted_at, updated_at, birth_date, email, genre, hashed_password, last_name, name, role, user_site_name, id_municipality, id_province, phone_number, address, instagram) VALUES
    names = ["Juan", "Pedro", "Pablo", "María", "José", "Ana", "Luis", "Carlos", "Andrea", "Marta", "Laura", "Sofía", "Lucía", "Javier", "David", "Miguel", "Rosa", "Elena", "Carmen", "Antonio", "Manuel", "Rafael", "Francisco", "Jorge", "Alberto", "Diego", "Fernando", "Sara", "Isabel", "Cristina", "Patricia", "Natalia", "Eva", "Raquel", "Beatriz", "Silvia", "Gloria", "Victoria", "Marina", "Mónica", "Teresa", "Rocío", "Celia", "Clara", "Julia", "Paula", "Alicia", "Lorena", "Miriam", "Nerea", "Irene", "Carmen", "María", "Ángela", "María", "Ángeles", "María", "José", "María", "Carmen", "María", "Pilar", "María", "Isabel", "María", "Dolores", "María", "Teresa", "Ana", "María", "María", "Luisa", "María", "Laura", "María", "Victoria", "María", "Elena", "María", "África", "María", "Ángela", "María", "Rosa", "María", "Nieves", "María", "Soledad", "María", "Cristina", "María", "Paz", "María", "Milagros", "María", "Carmen", "María", "Ángeles", "María", "Luz", "María", "Consuelo", "María", "José", "María", "Antonia", "María", "Lourdes", "María", "Mercedes", "María", "Rosario", "María", "Pilar", "María", "Isabel", "María", "Dolores", "María", "Teresa", "Ana", "María", "María", "Luisa", "María", "Laura", "María", "Victoria", "María", "Elena", "María", "África", "María", "Ángela", "María", "Rosa", "María", "Nieves", "María", "Soledad", "María", "Cristina", "María", "Paz", "María", "Milagros", "María", "Carmen", "María", "Ángeles", "María", "Luz", "María", "Consuelo", "María", "José", "María", "Antonia", "María", "Lourdes", "María", "Mercedes", "María", "Rosario", "María", "Pilar", "María", "Isabel", "María", "Dolores", "María", "Teresa", "Ana", "María", "María", "Luisa", "María", "Laura", "María", "Victoria", "María", "Elena", "María", "África", "María", "Ángela", "María", "Rosa", "María", "Nieves", "María", "Soledad", "María", "Cristina", "María", "Paz", "María", "Milagros", "María", "Carmen", "María", "Ángeles", "María", "Luz", "María", "Consuelo", "María", "José", "María", "Antonia", "María", "Lourdes", "María", "Mercedes", "María", "Rosario", "María", "Pilar", "María", "Isabel", "María", "Dolores", "María", "Teresa", "Ana"]
    last_names = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina", "Morales", "Ortega", "Delgado", "Suárez", "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias", "Nuñez", "Medina", "Garrido", "Cortés", "Redondo", "Castillo", "Santos", "Lozano", "Guerrero", "Cano", "Prieto", "Méndez", "Calvo", "Pascual", "Vidal", "León", "Herrero", "Peña", "Flores", "Cruz", "Carrasco", "Esteban", "Parra", "Bravo", "Aguilar", "Santana", "Hidalgo", "Lorenzo", "Montero", "Ibáñez", "Vega", "Fuentes", "Cabrera", "Rey", "Mora", "Vicente", "Arias", "Carmona", "Moya", "Santiago", "Salas", "Soto", "Rojas", "Bermúdez", "Giménez", "Pardo", "Estévez", "Bravo", "Aguilar", "Santana", "Hidalgo", "Lorenzo", "Montero", "Ibáñez", "Vega", "Fuentes", "Cabrera", "Rey", "Mora", "Vicente", "Arias", "Carmona", "Moya", "Santiago", "Salas", "Soto", "Rojas", "Bermúdez"]
    emails = ["gmail.com", "hotmail.com", "outlook.com"]
    genres = ["male", "female", "N/A"]
    address_names = ["Primavera", "Avenida del Sol", "Plaza Mayor", "Paseo de los Álamos", "Camino Real", "Travesía del Río", "Cuesta de la Luz", "Ronda de San Pedro", "Carretera de la Sierra", "Rambla del Mar", "Callejón del Gato", "Avenida de las Estrellas", "Plaza de la Libertad", "Paseo de los Pinos", "Camino de la Esperanza", "Travesía del Olivo", "Cuesta del Molino", "Ronda de los Abedules", "Carretera de los Cipreses", "Rambla de los Sueños", "Calle de la Paz", "Avenida del Amanecer", "Plaza de la Fuente", "Paseo de la Amistad", "Camino de la Loma", "Travesía del Alba", "Cuesta del Castillo", "Ronda del Parque", "Carretera de la Flor", "Rambla de los Encantos", "Calle de los Tulipanes", "Avenida de la Luna", "Plaza del Mirador", "Paseo de los Cedros", "Camino de las Rosas", "Travesía de la Montaña", "Cuesta de los Vientos", "Ronda del Bosque", "Carretera del Cielo", "Rambla del Horizonte", "Calle de la Aurora", "Avenida del Sauce", "Plaza de las Campanas", "Paseo del Horizonte", "Camino de los Aromas", "Travesía del Valle", "Cuesta del Lago", "Ronda de los Nogales", "Carretera del Alba", "Rambla de los Jazmines"]

    users_sql_path = "data/output/sql/15_users.sql"

    with open(users_sql_path, "a", encoding='utf-8') as f:
        for i in range(n):
            name = random.choice(names)
            last_name = random.choice(last_names)
            # remove accents and special characters from name and last_name and lowercase
            name_for_email = normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8')
            last_name_for_email = normalize('NFD', last_name).encode('ascii', 'ignore').decode('utf-8')
            birth_date = random_date()            
            email = f"{name_for_email.lower()}{last_name_for_email.lower()}{random_chars_for_email(birth_date)}@{random.choice(emails)}"
            role = "USER"
            site_name = f"{name_for_email.lower()}{last_name_for_email.lower()}"
            genre = random.choice(genres)
            id_municipality = random.randint(1, 10)
            id_province = random.randint(1, 10)
            phone_number = f"{random.randint(351, 370)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            address = f"{random.choice(address_names)} {random.randint(1, 100)}"
            birth_date_arr = birth_date.split('-')
            instagram = f"@{name_for_email.lower()}{last_name_for_email.lower()}{random.choice(birth_date_arr)}"
            rand_float = random.SystemRandom().random()
            password = base64.b64encode((struct.pack('!d', rand_float))).decode('utf-8').replace('=', '').replace("'", '')
            f.write(f"INSERT INTO public.\"user\" (created_at, updated_at, birth_date, email, genre, hashed_password, last_name, name, role, user_site_name, id_municipality, id_province, phone_number, address, instagram) VALUES (NOW(), NOW(), '{birth_date}', '{email}', '{genre}', '{password}', '{last_name}', '{name}', '{role}', '{site_name}', {id_municipality}, {id_province}, '{phone_number}', '{address}', '{instagram}');\n")

def random_chars_for_email(birth_date):
    birth_array = birth_date.split('-')
    char_ = ["", ".", "_", "-"]
    return f"{random.choice(char_)}{random.choice(birth_array)}{random.choice(char_)}"

def generate_posts():
    books_size = 719
    users_size = 1000
    posts_sql_path = "data/output/sql/16_posts.sql"
    posts = []  # Para almacenar los datos de los posts generados

    book_conditions_description = [
        "Nuevo", "Usado", "Buen estado", "Muy buen estado", "Excelente estado",
        "Libro en perfecto estado", "Libro en buen estado", "Con algunas marcas de uso",
        "Nunca usado, en empaque original", "Usado, pero en buen estado"
    ]
    book_states = ["COMO_NUEVO", "MUY_BUENO", "BUENO", "ACEPTABLE", "NUEVO"]
    types = ["EXCHANGE", "PURCHASE"]

    with open(posts_sql_path, "a", encoding='utf-8') as f:
        for i in range(2234):
            created_at = "NOW()"
            updated_at = "NOW()"
            description = random.choice(book_conditions_description)
            image = f"image_{random.randint(1, 1000)}.jpg"
            price = round(random.uniform(5000, 90000), 2)
            type_ = random.choice(types)
            book_state = random.choice(book_states)
            id_book = random.randint(1, books_size)
            id_user = random.randint(1, users_size)

            f.write(
                f"INSERT INTO public.post (created_at, updated_at, book_state, description, image, price, type, id_book, id_user) "
                f"VALUES ({created_at}, {updated_at}, '{book_state}', '{description}', '{image}', {price}, '{type_}', {id_book}, {id_user});\n"
            )
            # Guardar post en la lista
            posts.append({
                "id_post": i + 1,
                "id_user": id_user,
                "type": type_,
                "created_at": created_at
            })
    return posts

def generate_state_history_with_logic(posts):
    state_history_sql_path = "data/output/sql/19_state_history.sql"
    exchange_offer_sql_path = "data/output/sql/17_exchange_offer.sql"
    exchange_sql_path = "data/output/sql/18_exchange.sql"
    exchange_users_sql_path = "data/output/sql/20_exchange_users.sql"

    # Transiciones de estados
    transitions_posts = {
        1: [2, 4, 5],  # PUBLICADA -> CON OFERTA, PAUSADA, CANCELADA
        2: [1, 3, 4, 5],  # CON OFERTA -> PUBLICADA, OFERTA PARCIALMENTE ACEPTADA, PAUSADA, CANCELADA
        3: [2, 4, 5],  # OFERTA PARCIALMENTE ACEPTADA -> CON OFERTA, PAUSADA, CANCELADA
        4: [3, 2, 1, 5],  # PAUSADA -> OFERTA PARCIALMENTE ACEPTADA, CON OFERTA, PUBLICADA, CANCELADA
        5: [],  # CANCELADA -> Sin transición
        6: [7, 5],  # EN INTERCAMBIO -> INTERCAMBIADA, CANCELADA
        7: []  # INTERCAMBIADA -> Sin transición
    }
    transitions_offers = {
        8: [9, 11, 12],  # PENDIENTE -> PARCIALMENTE ACEPTADA, RECHAZADA, CANCELADA
        9: [10, 11, 12],  # PARCIALMENTE ACEPTADA -> ACEPTADA, RECHAZADA, CANCELADA
        10: [],  # ACEPTADA -> Sin transición
        11: [],  # RECHAZADA -> Sin transición
        12: []  # CANCELADA -> Sin transición
    }
    transitions_exchange = {
        13: [14, 15, 17],  # NOTIFICADO -> CANCELADO, PENDIENTE DE ENVIO, CONCRETADO
        14: [],  # CANCELADO -> Sin transición
        15: [16, 17],  # PENDIENTE DE ENVIO -> EN ENVIO, CONCRETADO
        16: [17],  # EN ENVIO -> CONCRETADO
        17: []  # CONCRETADO -> Sin transición
    }

    # Variables para manejar IDs internos
    current_offer_id = 1
    current_exchange_id = 1

    with open(state_history_sql_path, "a", encoding='utf-8') as f_state, \
         open(exchange_offer_sql_path, "a", encoding='utf-8') as f_offer, \
         open(exchange_sql_path, "a", encoding='utf-8') as f_exchange, \
         open(exchange_users_sql_path, "a", encoding='utf-8') as f_exchange_users:
        
        for i in range(0, len(posts), 2):
            if i + 1 >= len(posts):
                break

            post_a = posts[i]
            post_b = posts[i + 1]

            if post_a["type"] != "EXCHANGE" or post_b["type"] != "EXCHANGE":
                continue

            # Paso 1: Estado inicial de los posts
            initial_date_a = datetime(2024, 4, 1, random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
            initial_date_b = initial_date_a + timedelta(days=random.randint(1, 5))

            f_state.write(
                f"INSERT INTO public.state_history (initial_date, final_date, id_post, id_state) "
                f"VALUES ('{initial_date_a}', NULL, {post_a['id_post']}, 1);\n"
            )
            f_state.write(
                f"INSERT INTO public.state_history (initial_date, final_date, id_post, id_state) "
                f"VALUES ('{initial_date_b}', NULL, {post_b['id_post']}, 1);\n"
            )

            # Paso 2: Crear una oferta de intercambio
            offer_date = initial_date_b + timedelta(days=random.randint(1, 5))
            f_state.write(
                f"UPDATE public.state_history SET final_date = '{offer_date}' WHERE id_post = {post_a['id_post']} AND final_date IS NULL;\n"
            )
            f_state.write(
                f"INSERT INTO public.state_history (initial_date, final_date, id_post, id_state) "
                f"VALUES ('{offer_date}', NULL, {post_a['id_post']}, 2);\n"
            )

            f_offer.write(
                f"INSERT INTO public.exchange_offer (offer_date, offered_post_id, post_id, user_id) "
                f"VALUES ('{offer_date}', {post_b['id_post']}, {post_a['id_post']}, {post_b['id_user']});\n"
            )
            offer_id = current_offer_id
            current_offer_id += 1

            # Paso 3: Transiciones de la oferta
            current_offer_state = 8
            while transitions_offers[current_offer_state]:
                next_offer_state = random.choice(transitions_offers[current_offer_state])
                state_date = offer_date + timedelta(days=random.randint(1, 5), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                f_state.write(
                    f"UPDATE public.state_history SET final_date = '{state_date}' WHERE id_exchange_offer = {offer_id} AND final_date IS NULL;\n"
                )
                f_state.write(
                    f"INSERT INTO public.state_history (initial_date, final_date, id_exchange_offer, id_state) "
                    f"VALUES ('{state_date}', NULL, {offer_id}, {next_offer_state});\n"
                )
                current_offer_state = next_offer_state

            # Paso 4: Crear intercambio si la oferta es aceptada
            if current_offer_state == 10:
                exchange_date = state_date + timedelta(days=random.randint(1, 5), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                f_exchange.write(
                    f"INSERT INTO public.exchange (exchange_date, shipping_type, exchange_offer_id) "
                    f"VALUES ('{exchange_date}', 'DELIVERY', {offer_id});\n"
                )
                f_state.write(
                    f"INSERT INTO public.state_history (initial_date, final_date, id_exchange, id_state) "
                    f"VALUES ('{exchange_date}', NULL, {current_exchange_id}, 13);\n"
                )

                # Paso 5: Agregar ambos usuarios a la tabla exchange_users
                f_exchange_users.write(
                    f"INSERT INTO public.exchange_users (exchange_id, user_id) VALUES ({current_exchange_id}, {post_a['id_user']});\n"
                )
                f_exchange_users.write(
                    f"INSERT INTO public.exchange_users (exchange_id, user_id) VALUES ({current_exchange_id}, {post_b['id_user']});\n"
                )

                current_exchange_id += 1

                # Paso 6: Transiciones del intercambio
                current_exchange_state = 13
                while transitions_exchange[current_exchange_state]:
                    next_exchange_state = random.choice(transitions_exchange[current_exchange_state])
                    exchange_state_date = exchange_date + timedelta(days=random.randint(1, 5), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                    f_state.write(
                        f"UPDATE public.state_history SET final_date = '{exchange_state_date}' WHERE id_exchange = {current_exchange_id - 1} AND final_date IS NULL;\n"
                    )
                    f_state.write(
                        f"INSERT INTO public.state_history (initial_date, final_date, id_exchange, id_state) "
                        f"VALUES ('{exchange_state_date}', NULL, {current_exchange_id - 1}, {next_exchange_state});\n"
                    )
                    current_exchange_state = next_exchange_state

            f_state.write("\n")
            f_offer.write("\n")
            f_exchange.write("\n")
            f_exchange_users.write("\n")

if __name__ == "__main__":
    main()
