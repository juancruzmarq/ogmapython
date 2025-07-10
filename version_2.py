# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta
from unicodedata import normalize

RANDOM_GENRES = ["M", "F", "N/A"]
RANDOM_NAMES = ["Juan", "Pedro", "Pablo", "María", "José", "Ana", "Luis", "Carlos", "Andrea", "Marta", "Laura", "Sofía", "Lucía", "Javier", "David", "Miguel", "Rosa", "Elena", "Carmen", "Antonio", "Manuel", "Rafael", "Francisco", "Jorge", "Alberto", "Diego", "Fernando", "Sara", "Isabel", "Cristina", "Patricia", "Natalia", "Eva", "Raquel", "Beatriz", "Silvia", "Gloria", "Victoria", "Marina", "Mónica", "Teresa", "Rocío", "Celia", "Clara", "Julia", "Paula", "Alicia", "Lorena", "Miriam", "Nerea", "Irene"]
RANDOM_LAST_NAMES = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina", "Morales", "Ortega", "Delgado", "Suárez", "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias", "Nuñez", "Medina", "Garrido"]
RANDOM_EMAIL_SERVICE = ["gmail.com", "hotmail.com", "outlook.com"]
RANDOM_ADDRESS_NAMES = ["Primavera", "Avenida del Sol", "Plaza Mayor", "Paseo de los Álamos", "Camino Real", "Travesía del Río", "Cuesta de la Luz", "Ronda de San Pedro", "Carretera de la Sierra", "Rambla del Mar", "Callejón del Gato", "Avenida de las Estrellas"]
USER_DISTRIBUTION_BY_MONTH = {
    8: 100,   # agosto
    9: 200,  # septiembre
    10: 500, # octubre
    11: 100, # noviembre
    12: 100  # diciembre 
}

def generate_random_password():
    password = ""
    for i in range(12):
        password += random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    return password

def generate_random_phone():
    phone = "+34"
    for i in range(9):
        phone += random.choice("0123456789")
    return phone

def generate_random_timestamp():
    year = 2024
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    # Add 0 to month, day, hour, minute and second if they are less than 10
    month = f"0{month}" if month < 10 else month
    day = f"0{day}" if day < 10 else day
    hour = f"0{hour}" if hour < 10 else hour
    minute = f"0{minute}" if minute < 10 else minute
    second = f"0{second}" if second < 10 else second
    return f"{year}-{month}-{day} {hour}:{minute}:{second}"

def generate_logical_timestamp():
    months = list(USER_DISTRIBUTION_BY_MONTH.keys())
    weights = list(USER_DISTRIBUTION_BY_MONTH.values())
    
    # Elige el mes según la distribución dada
    selected_month = random.choices(months, weights=weights, k=1)[0]

    # Define días válidos evitando fines de semana (más lógico)
    year = 2024
    first_day = datetime(year, selected_month, 1)
    if selected_month == 12:
        next_month_first_day = datetime(year + 1, 1, 1)
    else:
        next_month_first_day = datetime(year, selected_month + 1, 1)
    
    valid_days = []
    current_day = first_day
    while current_day < next_month_first_day:
        if current_day.weekday() < 5:  # de lunes(0) a viernes(4)
            valid_days.append(current_day)
        current_day += timedelta(days=1)

    # Elige un día más lógico (menos probable en los extremos del mes)
    selected_day = random.choice(valid_days)

    # Hora más lógica: usuarios suelen registrarse en horario laboral (8-18hs)
    hour = random.randint(8, 18)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    timestamp = selected_day.replace(hour=hour, minute=minute, second=second)
    return timestamp.strftime("%Y-%m-%d %H:%M:%S")

def generate_random_birth_date():
    year = random.randint(1950, 2009)
    month = random.randint(1, 12)
    day = random.randint(1, 28)
    # Add 0 to month and day if they are less than 10
    month = f"0{month}" if month < 10 else month
    day = f"0{day}" if day < 10 else day
    return f"{year}-{month}-{day}"

class User:
    def __init__(self, id_user, id_province, id_municipality, valid_emails, email="", name="", last_name="", genre=""):
        self.id_user = id_user
        self.name = name
        self.last_name = last_name
        self.email = email
        self.genre = genre
        self.hashed_password = generate_random_password()
        self.phone_number = generate_random_phone()
        self.created_at = generate_logical_timestamp()
        self.instagram = f"@{self.name.lower()}{self.last_name.lower()}"
        self.user_site_name = f"{self.name.lower()}.{self.last_name.lower()}"
        self.id_province = id_province
        self.id_municipality = id_municipality
        self.address = f"{random.choice(RANDOM_ADDRESS_NAMES)}, {random.randint(1, 4000)}"
        self.birth_date = generate_random_birth_date()
        self.posts = []
        self.reviews = []
        self.literary_routes = []
        

        if self.genre == "":
            self.genre = random.choice(RANDOM_GENRES)
        if self.name == "":
            self.name = random.choice(RANDOM_NAMES)
        if self.last_name == "":
            self.last_name = random.choice(RANDOM_LAST_NAMES)
        if self.email == "":
            self.generate_valid_email(valid_emails)
        
    
    def __str__(self):
        return f"User({self.id_user}, {self.name}, {self.last_name}, {self.email}, {self.genre}, {self.hashed_password}, {self.phone}, {self.created_at}, {self.id_province}, {self.id_municipality}, {self.address}, {self.birth_date})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_user = (
            f"INSERT INTO public.user (name, last_name, email, genre, hashed_password, phone_number, created_at, instagram, user_site_name, id_province, id_municipality, address, birth_date, role) \n"
            f"VALUES ('{self.name}', '{self.last_name}', '{self.email}', '{self.genre}', '{self.hashed_password}', '{self.phone_number}', '{self.created_at}', '{self.instagram}', '{self.user_site_name}', {self.id_province}, {self.id_municipality}, '{self.address}', '{self.birth_date}', 'USER'); \n"
        )
        return insert_in_user
    
    def generate_valid_email(self, valid_emails):
        name_for_email = normalize('NFD', self.name).encode('ascii', 'ignore').decode('utf-8').lower()
        lastname_for_email = normalize('NFD', self.last_name).encode('ascii', 'ignore').decode('utf-8').lower()
        random_sufix = random.randint(1, 9999)
        if self.email in valid_emails:   
            self.email = f"{name_for_email}.{lastname_for_email}{random_sufix}@{random.choice(RANDOM_EMAIL_SERVICE)}"
            self.generate_valid_email(valid_emails)
        elif self.email == "":
            self.email = f"{name_for_email}.{lastname_for_email}@{random.choice(RANDOM_EMAIL_SERVICE)}"
            self.generate_valid_email(valid_emails)
        else:
            valid_emails.append(self.email)

    def add_review(self, review):
        self.reviews.append(review)

    def add_literary_route(self, literary_route):
        self.literary_routes.append(literary_route)

    def add_post(self, post):
        self.posts.append(post)

    def append_post(self, post):
        self.posts.append(post)
    
    def get_posts(self):
        return self.posts

class StateMachine:
    def __init__(self, initial_state, states, transitions, id_column_name, object_id):
        self.state = initial_state
        self.states = states
        self.transitions = transitions
        self.id_column_name = id_column_name
        self.object_id = object_id

    def can_transition(self, new_state):
        return new_state in self.transitions.get(self.state, [])

    def transition_to(self, new_state, date):
        if self.can_transition(new_state):
            self.state = new_state
            return (
                f"UPDATE public.state_history SET final_date = '{date}' WHERE {self.id_column_name} = {self.object_id} AND final_date IS NULL;\n"
                f"INSERT INTO public.state_history (initial_date, final_date, {self.id_column_name}, id_state) \n"
                f"VALUES ('{date}', NULL, {self.object_id}, {new_state});\n"
            )
        else:
            raise ValueError(f"Invalid transition from {self.state} to {new_state}")

class Post(StateMachine):
    def __init__(self, id_post, id_user, id_book, type_, created_at):
        states = {
            1: "PUBLICADA",
            2: "CON OFERTA",
            3: "OFERTA PARCIALMENTE ACEPTADA",
            4: "PAUSADA",
            5: "CANCELADA",
            6: "EN INTERCAMBIO",
            7: "INTERCAMBIADA"
        }
        transitions = {
            1: [2, 4, 5],
            2: [1, 3, 4, 5],
            3: [2, 4, 5, 6],
            4: [1, 2, 3, 5],
            5: [],
            6: [7, 5],
            7: []
        }
        super().__init__(initial_state=1, states=states, transitions=transitions, id_column_name="id_post", object_id=id_post)
        
        self.id_post = id_post
        self.id_user = id_user
        self.id_book = id_book
        self.type = type_
        self.created_at = created_at
        self.updated_at = created_at
        self.book_received = "NULL"
        self.book_send = "False"
        self.book_state = random.choice(BOOK_STATES)
        self.description = random.choice(BOOK_STATE_DESCRIPTIONS)
        self.image = "NULL"
        self.price = round(random.uniform(5000, 120000), 2)
        self.exchange_offer = []

    def change_state(self, new_state, date):
        return self.transition_to(new_state, date)
    
    def __str__(self):
        return f"Post({self.id_post}, {self.id_user}, {self.id_book}, {self.type}, {self.created_at}, {self.updated_at}, {self.book_state}, {self.description}, {self.image}, {self.price}, {self.book_send}, {self.book_received})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_post = (
            f"INSERT INTO public.post (created_at, updated_at, book_state, description, image, price, type, id_book, id_user, book_send, book_received)  \n"
            f"VALUES ('{self.created_at}', '{self.updated_at}', '{self.book_state}', '{self.description}', '{self.image}', {self.price}, '{self.type}', {self.id_book}, {self.id_user}, {self.book_send}, {self.book_received}); \n"
        )
        insert_in_state_history = (
            f"INSERT INTO public.state_history (initial_date, final_date, id_post, id_state)  \n"
            f"VALUES ('{self.created_at}', NULL, {self.id_post}, 1); \n"
        )
        return insert_in_post, insert_in_state_history
    
    def change_to_con_oferta(self, date):
        return self.change_state(2, date)
    
    def change_to_oferta_parcialmente_aceptada(self, date):
        return self.change_state(3, date)
    
    def change_to_pausada(self, date):
        return self.change_state(4, date)
    
    def change_to_cancelada(self, date):
        return self.change_state(5, date)
    
    def change_to_en_intercambio(self, date):
        return self.change_state(6, date)
    
    def change_to_intercambiada(self, date):
        return self.change_state(7, date)
    
    def append_exchange_offer(self, exchange_offer):
        return self.exchange_offer.append(exchange_offer)

    def get_exchange_offers(self):
        return self.exchange_offer
    
    def get_exchange_offer(self, id_exchange_offer):
        for exchange_offer in self.exchange_offer:
            if exchange_offer.offered_post_id == id_exchange_offer:
                return exchange_offer
        return None
