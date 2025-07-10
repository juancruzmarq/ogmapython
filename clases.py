import random
import os
from unicodedata import normalize
from datetime import datetime, timedelta

BOOK_STATES = ["COMO_NUEVO", "MUY_BUENO", "BUENO", "ACEPTABLE", "NUEVO"]
BOOK_STATE_DESCRIPTIONS = ["Nuevo", "Usado", "Excelente estado", "Bueno", "Aceptable"]
RANDOM_NAMES = ["Juan", "Pedro", "Pablo", "María", "José", "Ana", "Luis", "Carlos", "Andrea", "Marta", "Laura", "Sofía", "Lucía", "Javier", "David", "Miguel", "Rosa", "Elena", "Carmen", "Antonio", "Manuel", "Rafael", "Francisco", "Jorge", "Alberto", "Diego", "Fernando", "Sara", "Isabel", "Cristina", "Patricia", "Natalia", "Eva", "Raquel", "Beatriz", "Silvia", "Gloria", "Victoria", "Marina", "Mónica", "Teresa", "Rocío", "Celia", "Clara", "Julia", "Paula", "Alicia", "Lorena", "Miriam", "Nerea", "Irene"]
RANDOM_LAST_NAMES = ["García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Gómez", "Martín", "Jiménez", "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Muñoz", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres", "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Molina", "Morales", "Ortega", "Delgado", "Suárez", "Castro", "Ortiz", "Rubio", "Marín", "Sanz", "Iglesias", "Nuñez", "Medina", "Garrido"]
RANDOM_EMAIL_SERVICE = ["gmail.com", "hotmail.com", "outlook.com"]
RANDOM_GENRES = ["M", "F", "N/A"]
RANDOM_ADDRESS_NAMES = ["Primavera", "Avenida del Sol", "Plaza Mayor", "Paseo de los Álamos", "Camino Real", "Travesía del Río", "Cuesta de la Luz", "Ronda de San Pedro", "Carretera de la Sierra", "Rambla del Mar", "Callejón del Gato", "Avenida de las Estrellas"]
FOLDER_PATH = "./data/output/new"
USERS_PATH = f"{FOLDER_PATH}/15_user.sql"
POSTS_PATH = f"{FOLDER_PATH}/16_post.sql"
EXCHANGE_OFFERS_PATH = f"{FOLDER_PATH}/18_exchange_offer.sql"
EXCHANGES_PATH = f"{FOLDER_PATH}/19_exchange.sql"
STATE_HISTORIES_PATH = f"{FOLDER_PATH}/20_state_history.sql"
SURVEYS_PATH = f"{FOLDER_PATH}/23_surveys.sql"
REVIEWS_PATH = f"{FOLDER_PATH}/22_reviews.sql"
EXCHANGE_USERS_PATH = f"{FOLDER_PATH}/21_exchange_users.sql"
LITERARY_ROUTES_PATH = f"{FOLDER_PATH}/24_literary_routes.sql"
LITERARY_ROUTES_BOOK_PATH = f"{FOLDER_PATH}/25_literary_routes_books.sql"

BOOKS_SIZE = 719
BOOK_RATING_REVIEW = {
    1: ["Muy malo", "No lo recomiendo", "Pésimo", "Decepcionante", "No me gustó", "Muy aburrido", "No lo compren", "No lo vale", "No lo leería de nuevo", "No lo recomendaría", "No lo volvería a comprar"],
    2: ["Malo", "Regular", "No es lo que esperaba", "Podría mejorar", "No es tan bueno", "No es lo mejor", "No lo compraría de nuevo", "No lo recomendaría mucho", "No lo volvería a leer", "No lo volvería a comprar"],
    3: ["Aceptable", "Está bien", "Nada especial", "Es pasable", "Cumple, pero no destaca", "Normal", "No está mal", "No está tan bueno", "No es tan recomendable", "No es tan bueno como esperaba"],
    4: ["Bueno", "Me gustó", "Está bastante bien", "Recomendable", "Buena calidad", "Vale la pena leerlo", "Lo disfruté", "Lo volvería a comprar", "Lo recomendaría", "Lo volvería a leer"],
    5: ["Excelente", "Increíble", "Lo recomiendo mucho", "Maravilloso", "Muy bueno", "Me encantó", "Lo amé", "Lo mejor que he leído", "Lo volvería a comprar", "Lo volvería a leer"]
}
SURVEY_COMMENTS = {
    1: ["Muy insatisfecho", "Pésimo intercambio", "No volvería a hacer un intercambio aquí"],
    2: ["Insatisfecho", "No fue lo que esperaba", "Regular experiencia"],
    3: ["Aceptable", "Intercambio promedio", "No estuvo mal"],
    4: ["Satisfecho", "Buena experiencia", "Intercambio exitoso"],
    5: ["Muy satisfecho", "Excelente experiencia", "Lo recomendaría a otros"]
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

USER_DISTRIBUTION_BY_MONTH = {
    8: 100,   # agosto
    9: 200,  # septiembre
    10: 500, # octubre
    11: 100, # noviembre
    12: 100  # diciembre 
}

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

    
    def append_post(self, post):
        self.posts.append(post)
    
    def get_posts(self):
        return self.posts

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

class ExchangeOffer(StateMachine):
    def __init__(self, id_exchange_offer, offered_post_id, post_id, user_id, offer_date):
        states = {
            8: "PENDIENTE",
            9: "PARCIALMENTE ACEPTADA",
            10: "ACEPTADA",
            11: "RECHAZADA",
            12: "CANCELADA",
            13: "FINALIZADA"
        }
        transitions = {
            8: [9, 11, 12],
            9: [10, 11, 12],
            10: [13],
            11: [],
            12: []
        }
        super().__init__(initial_state=8, states=states, transitions=transitions, id_column_name="id_exchange_offer", object_id=id_exchange_offer)

        self.id_exchange_offer = id_exchange_offer
        self.offered_post_id = offered_post_id
        self.post_id = post_id
        self.user_id = user_id
        self.offer_date = offer_date

    def change_state(self, new_state, date):
        return self.transition_to(new_state, date)
    
    def __str__(self):
        return f"ExchangeOffer({self.offered_post_id}, {self.post_id}, {self.user_id}, {self.offer_date})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_exchange_offer = (
            f"INSERT INTO public.exchange_offer (offered_post_id, post_id, user_id, offer_date)  \n"
            f"VALUES ({self.offered_post_id}, {self.post_id}, {self.user_id}, '{self.offer_date}'); \n"
        )
        insert_in_state_history = (
            f"INSERT INTO public.state_history (initial_date, final_date, id_exchange_offer, id_state) \n"
            f"VALUES ('{self.offer_date}', NULL, {self.offered_post_id}, 8);"
        )
        return insert_in_exchange_offer, insert_in_state_history
    
    def change_to_parcialmente_aceptada(self, date):
        return self.change_state(9, date)
    
    def change_to_aceptada(self, date):
        return self.change_state(10, date)
    
    def change_to_rechazada(self, date):
        return self.change_state(11, date)
    
    def change_to_cancelada(self, date):
        return self.change_state(12, date)
    
    def change_to_finalizada(self, date):
        return self.change_state(13, date)
    
class Exchange(StateMachine):
    def __init__(self, id_exchange, id_exchange_offer, id_post, id_user, exchange_date):
        states = {
            14: "NOTIFICADO",
            15: "CANCELADO",
            16: "PENDIENTE DE ENVIO",
            17: "EN ENVIO",
            18: "CONCRETADO SATISFACTORIAMENTE",
            19: "CONCRETADO	NO SATISFACTORIAMENTE"
        }
        transitions = {
            14: [15, 16, 17],
            15: [],
            16: [17, 15],
            17: [18, 19],
            18: [],
            19: []
        }
        super().__init__(initial_state=14, states=states, transitions=transitions, id_column_name="id_exchange", object_id=id_exchange)

        self.id_exchange = id_exchange
        self.id_exchange_offer = id_exchange_offer
        self.id_post = id_post
        self.id_user = id_user
        self.send_book_date = None
        self.shipping_type = "DELIVERY"
        self.exchange_date = exchange_date

    def change_state(self, new_state, date):
        return self.transition_to(new_state, date)
    
    def __str__(self):
        return f"Exchange({self.id_exchange}, {self.id_exchange_offer}, {self.id_post}, {self.id_user}, {self.exchange_date})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_exchange = (
            f"INSERT INTO public.exchange (exchange_date, shipping_type, exchange_offer_id, send_book_date) \n"
            f"VALUES ('{self.exchange_date}', 'DELIVERY', {self.id_exchange_offer}, NULL);"
        )
        insert_in_state_history = (
            f"INSERT INTO public.state_history (initial_date, final_date, id_exchange, id_state) \n"
            f"VALUES ('{self.exchange_date}', NULL, {self.id_exchange}, 14);"
        )
        return insert_in_exchange, insert_in_state_history

    def change_to_cancelado(self, date):
        return self.change_state(15, date)
    
    def change_to_pendiente_de_envio(self, date):
        return self.change_state(16, date)
    
    def change_to_en_envio(self, date):
        return self.change_state(17, date)
    
    def change_to_concretado_satisfactoriamente(self, date):
        return self.change_state(18, date)
    
    def change_to_concretado_no_satisfactoriamente(self, date):
        return self.change_state(19, date)
    
    def generate_exchage_users(self, id_user_a, id_user_b):
        return (
            f"INSERT INTO public.exchange_users (exchange_id, user_id) \n"
            f"VALUES ({self.id_exchange}, {id_user_a}); \n"
            f"INSERT INTO public.exchange_users (exchange_id, user_id) \n"
            f"VALUES ({self.id_exchange}, {id_user_b});"
        )
 
class Survey:
    def __init__(self, id_survey, id_exchange, id_user, id_book, id_user_rated):
        self.id_survey = id_survey
        self.id_exchange = id_exchange
        self.id_user = id_user
        self.survey_date = generate_random_timestamp()
        self.book_rating = random.randint(1, 5)
        self.user_rating = random.randint(1, 5)
        self.comment = random.choice(SURVEY_COMMENTS[self.user_rating])
        self.type = "EXCHANGE"
        self.id_book = id_book
        self.id_user_rated = id_user_rated

        # El 90% de las encuestas recomiendan ogma
        self.recommendation = random.choices([True, False], weights=[90, 10])[0]

    def __str__(self):
        return f"Survey({self.id_survey}, {self.id_exchange}, {self.id_user}, {self.survey_date}, {self.book_rating}, {self.user_rating}, {self.comment}, {self.type}, {self.id_book}, {self.id_user_rated})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_survey = (
            f"INSERT INTO public.survey (book_rating, user_rating, comment, type, id_book, id_user_rated, id_user, id_exchange, recommendation) \n"
            f"VALUES ({self.book_rating}, {self.user_rating}, '{self.comment}', '{self.type}', {self.id_book}, {self.id_user_rated}, {self.id_user}, {self.id_exchange}, {self.recommendation}); \n"
        )
        return insert_in_survey

class Review:
    def __init__(self, rating, id_book, id_user):
        self.rating = rating
        self.id_book = id_book
        self.id_user = id_user
        self.comment = self.generate_random_comment()
    
    def __str__(self):
        return f"Review({self.id_review}, {self.comment}, {self.rating}, {self.review_date})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_review = (
            f"INSERT INTO public.review (comment, rating, id_book, id_user, created_at, updated_at, deleted_at) \n"
            f"VALUES ('{self.comment}', {self.rating}, {self.id_book}, {self.id_user}, '{generate_random_timestamp()}', NULL, NULL); \n"

        )
        return insert_in_review
    
    def generate_random_comment(self):
        return random.choice(BOOK_RATING_REVIEW[self.rating])

class LiteraryRoute:
    def __init__(self, id_literary_route, books, id_user, created_at, name="", description=""):
        self.id_literary_route = id_literary_route
        self.books = books
        self.rating = random.randint(1, 5)
        self.id_user = id_user
        self.created_at = created_at
        self.name = name
        self.description = description

    def __str__(self):
        return f"LiteraryRoute({self.id_literary_route}, {self.id_user}, {self.name}, {self.description})"
    
    def __repr__(self):
        return str(self)
    
    def create_sql(self):
        insert_in_literary_route = (
            f"INSERT INTO public.literary_route (id_user, name, description, rating, created_at) \n"
            f"VALUES ({self.id_user}, '{self.name}', '{self.description}', {self.rating}, '{self.created_at}'); \n"
        )
        insert_in_literary_route_book = ""
        for book in self.books:
            insert_in_literary_route_book += (
                f"INSERT INTO public.literary_route_book (id_literary_route, id_book) \n"
                f"VALUES ({self.id_literary_route}, {book}); \n"
            )
            
        return insert_in_literary_route, insert_in_literary_route_book

class Writer:
    def __init__(self, user_path, post_path, exchange_offer_path, exchange_path, survey_path, review_path, state_history_path, exchange_users_path, exchange_confirmed_needed, literary_route_path, literary_route_book_path):
        self.user_path = user_path
        self.post_path = post_path
        self.exchange_offer_path = exchange_offer_path
        self.exchange_path = exchange_path
        self.survey_path = survey_path
        self.review_path = review_path
        self.state_history_path = state_history_path
        self.exchange_users_path = exchange_users_path
        self.users = []
        self.posts = []
        self.exchange_offers = []
        self.exchanges = []
        self.surveys = []
        self.reviews = []
        self.valid_emails = []
        self.literary_routes = []
        self.exchanges_confirmed = 0
        self.exchange_confirmed_needed = exchange_confirmed_needed
        self.literary_route_path = literary_route_path
        self.literary_route_book_path = literary_route_book_path
        
    def generate_users(self, n):
        for i in range(n):
            user = User(i + 1, random.randint(1, 24), random.randint(1, 100), self.valid_emails)
            self.users.append(user)
            self.valid_emails.append(user.email)

            # Write user to file
            self.write(self.user_path, user.create_sql())
    
    def get_users(self):
        return self.users

    def generate_n_post_per_user(self, min, max, porcentage_of_users):
        users_len = len(self.users)
        n = int((porcentage_of_users * users_len) / 100)
        users_reduced = random.sample(self.users, n)
        print(f"Generating posts for {n} users")
        print(f"Total users: {users_len}")
        print(f"Total users reduced: {len(users_reduced)}")
        print(f"Distinct users ids: {len(set([user.id_user for user in users_reduced]))}")

        id_post = 1
        for user in users_reduced:
            for i in range(random.randint(min, max)):
                id_book = random.randint(1, BOOKS_SIZE)
                type_ = random.choice(["PURCHASE", "EXCHANGE"])
                # al created_at del usuario sumarle de 1 a 5 dias
                created_at = datetime.strptime(user.created_at, "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(1, 5))
                post = Post(id_post, user.id_user, id_book, type_, created_at)
                
                # Check if the user already created a post with the same book
                if not self.check_if_post_exists(post):
                    user.append_post(post)
                    self.posts.append(post)
                    insert_in_post, insert_in_state_history = post.create_sql()
                    self.write(self.post_path, insert_in_post)
                    self.write(self.state_history_path, insert_in_state_history)
                    id_post += 1
                else:
                    i -= 1          

    def find_post_not_in_user_id(self, user_id):
        posts_without_user_id = [post for post in self.posts if post.id_user != user_id]
        return random.choice(posts_without_user_id)

    def generate_exchanges(self):
        for post in self.posts:
            if post.state == 1 and post.type == "EXCHANGE":
                num_offers = random.randint(1, 3)
                offers_for_this_post = []

                for _ in range(num_offers):
                    other_post = self.find_post_not_in_user_id(post.id_user)
                    timestamp = post.created_at + timedelta(days=random.randint(1, 2))

                    exchange_offer = ExchangeOffer(
                        id_exchange_offer=len(self.exchange_offers) + 1,
                        offered_post_id=other_post.id_post,
                        post_id=post.id_post,
                        user_id=other_post.id_user,
                        offer_date=timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    )

                    post.append_exchange_offer(exchange_offer)
                    self.exchange_offers.append(exchange_offer)

                    insert_offer_sql, insert_offer_state = exchange_offer.create_sql()
                    self.write(self.exchange_offer_path, insert_offer_sql)
                    self.write(self.state_history_path, insert_offer_state)

                    if post.state == 1:
                        sql = post.change_to_con_oferta(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                    offers_for_this_post.append((exchange_offer, other_post))

                if self.exchanges_confirmed >= self.exchange_confirmed_needed or not offers_for_this_post:
                    continue

                selected_offer, other_post = random.choice(offers_for_this_post)

                # Definir trayectorias posibles
                possible_paths = [
                    ["PARCIAL"],
                    ["PARCIAL", "EN_INTERCAMBIO"],
                    ["PARCIAL", "EN_INTERCAMBIO", "PENDIENTE_ENVIO"],
                    ["PARCIAL", "EN_INTERCAMBIO", "PENDIENTE_ENVIO", "EN_ENVIO"],
                    ["PARCIAL", "EN_INTERCAMBIO", "PENDIENTE_ENVIO", "EN_ENVIO", "COMPLETO"]
                ]
                path = random.choice(possible_paths)
                timestamp = datetime.strptime(selected_offer.offer_date, "%Y-%m-%d %H:%M:%S")

                for step in path:
                    timestamp += timedelta(days=1)

                    if step == "PARCIAL":
                        sql = selected_offer.change_to_parcialmente_aceptada(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                        sql = post.change_to_oferta_parcialmente_aceptada(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                    elif step == "EN_INTERCAMBIO":
                        exchange = Exchange(
                            id_exchange=len(self.exchanges) + 1,
                            id_exchange_offer=selected_offer.id_exchange_offer,
                            id_post=post.id_post,
                            id_user=post.id_user,
                            exchange_date=timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        )
                        self.exchanges.append(exchange)

                        insert_exchange_sql, insert_exchange_state = exchange.create_sql()
                        self.write(self.exchange_path, insert_exchange_sql)
                        self.write(self.state_history_path, insert_exchange_state)

                        sql = post.change_to_en_intercambio(timestamp)
                        self.write(self.state_history_path, sql)

                    elif step == "PENDIENTE_ENVIO":
                        exchange = self.exchanges[-1]
                        sql = exchange.change_to_pendiente_de_envio(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                    elif step == "EN_ENVIO":
                        exchange = self.exchanges[-1]
                        sql = exchange.change_to_en_envio(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                    elif step == "COMPLETO":
                        exchange = self.exchanges[-1]
                        sql = exchange.change_to_concretado_satisfactoriamente(timestamp.strftime("%Y-%m-%d %H:%M:%S"))
                        self.write(self.state_history_path, sql)

                        sql = post.change_to_intercambiada(timestamp)
                        self.write(self.state_history_path, sql)

                        exchange_users_sql = exchange.generate_exchage_users(post.id_user, other_post.id_user)
                        self.write(self.exchange_users_path, exchange_users_sql)

                        # Encuestas
                        survey_a = Survey(len(self.surveys) + 1, exchange.id_exchange, post.id_user, other_post.id_book, other_post.id_user)
                        survey_b = Survey(len(self.surveys) + 2, exchange.id_exchange, other_post.id_user, post.id_book, post.id_user)
                        self.surveys.extend([survey_a, survey_b])
                        self.write(self.survey_path, survey_a.create_sql())
                        self.write(self.survey_path, survey_b.create_sql())

                self.exchanges_confirmed += 1

    def check_if_post_exists(self, post):
        for p in self.posts:
            if p.id_user == post.id_user and p.id_book == post.id_book:
                return True
        return False
    
    def write(self, path, data):
        with open(path, "a", encoding="utf-8") as file:
            file.write(data + "\n")
    
    def generate_aylen_user(self):
        users_len = len(self.users) + 1
        user = User(users_len, random.randint(1, 24), random.randint(1, 100), self.valid_emails, email="jbollatti.ogma@gmail.com", name="Julian", last_name="Bollatti", genre="M")
        self.users.append(user)
        sql = user.create_sql()
        self.write(self.user_path, sql)
        return user
    
    def generate_aylen_posts(self, user):
        for i in range(15):
            post = Post(len(self.posts) + 1, user.id_user, random.randint(1, BOOKS_SIZE), "EXCHANGE", generate_random_timestamp())
            user.append_post(post)
            self.posts.append(post)
            insert_in_post, insert_in_state_history = post.create_sql()
            self.write(self.post_path, insert_in_post)
            self.write(self.state_history_path, insert_in_state_history)
    
    def get_post_by_id(self, id_post):
        return next((p for p in self.posts if p.id_post == id_post), None)
    
    def generate_aylen_exchange_offers(self, user):
        exchanges = 0
        for post in user.get_posts():
            if post.state == 1 and post.type == "EXCHANGE":
                offers_to_generate = random.randint(2, 5)
                for i in range(offers_to_generate):
                    other_post = self.find_post_not_in_user_id(post.id_user)
                    exchange_offer = ExchangeOffer(len(self.exchange_offers) + 1, other_post.id_post, post.id_post, other_post.id_user, generate_random_timestamp())
                    post.append_exchange_offer(exchange_offer)
                    self.exchange_offers.append(exchange_offer)
                    insert_in_exchange_offer, insert_in_state_history = exchange_offer.create_sql()
                    self.write(self.exchange_offer_path, insert_in_exchange_offer)
                    self.write(self.state_history_path, insert_in_state_history)

                    if post.state == 1 and random.choice([True, False]):
                        post.change_to_con_oferta(generate_random_timestamp())

                if exchanges < offers_to_generate - 1:
                    # Aceptarle una oferta de intercambio
                    # Cambiar el estado de la oferta de intercambio a PARCIALMENTE ACEPTADA
                    exchange_offer = post.get_exchange_offer(random.choice(post.get_exchange_offers()).offered_post_id)
                    other_post = self.get_post_by_id(exchange_offer.offered_post_id)
                    history_sql = exchange_offer.change_to_parcialmente_aceptada(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Cambiar el estado del post a OFERTA PARCIALMENTE ACEPTADA
                    history_sql = post.change_to_oferta_parcialmente_aceptada(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Crear intercambio
                    exchange = Exchange(len(self.exchanges) + 1, exchange_offer.id_exchange_offer, post.id_post, post.id_user, generate_random_timestamp())
                    self.exchanges.append(exchange)
                    insert_in_exchange, insert_in_state_history = exchange.create_sql()
                    self.write(self.exchange_path, insert_in_exchange)
                    self.write(self.state_history_path, insert_in_state_history)
                    # Cambiar el post a EN INTERCAMBIO
                    history_sql = post.change_to_en_intercambio(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Cambiar estado del intercambio a PENDEINTE DE ENVIO
                    history_sql = exchange.change_to_pendiente_de_envio(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Cambiar estado del intercambio a EN ENVIO
                    history_sql = exchange.change_to_en_envio(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Cambiar estado del intercambio a CONCRETADO SATISFACTORIAMENTE
                    history_sql = exchange.change_to_concretado_satisfactoriamente(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Cambiar estado del post a INTERCAMBIADA
                    history_sql = post.change_to_intercambiada(generate_random_timestamp())
                    self.write(self.state_history_path, history_sql)

                    # Generar exchange_users
                    exchange_users_sql = exchange.generate_exchage_users(post.id_user, other_post.id_user)
                    self.write(self.exchange_users_path, exchange_users_sql)

                    # Generate survey for both users
                    survey_a = Survey(len(self.surveys) + 1, exchange.id_exchange, post.id_user, other_post.id_book, other_post.id_user)
                    survey_b = Survey(len(self.surveys) + 2, exchange.id_exchange, other_post.id_user, post.id_book, post.id_user)
                    self.surveys.append(survey_a)
                    self.surveys.append(survey_b)
                    survey_a_sql = survey_a.create_sql()
                    survey_b_sql = survey_b.create_sql()
                    self.write(self.survey_path, survey_a_sql)
                    self.write(self.survey_path, survey_b_sql)

                    self.exchanges_confirmed += 1
                    exchanges += 1

    def generate_aylen_case(self):
        user = self.generate_aylen_user()
        self.generate_aylen_posts(user)
        self.generate_aylen_exchange_offers(user)

    def generate_reviews(self):
        for post in self.posts:
            if post.state == 1:
                id_book = post.id_book
                reviewed_by = []
                for review in range(random.randint(1,5)):
                    user = random.choice(self.users)
                    id_user = user.id_user
                    if id_user in reviewed_by:
                        continue
                    review = Review(random.randint(1,5), id_book, id_user)
                    sql = review.create_sql()
                    
                    self.write(self.review_path, sql)
                    reviewed_by.append(id_user)

    def generate_literary_routes(self, q):
        id = 1
        for i in range(q):
            # Generar entre 4 y 5 libros por ruta literaria
            cantidad_libros = random.randint(4, 5)
            # Generar una ruta literaria con libros aleatorios, sin repetir libros
            libros = random.sample(range(1, BOOKS_SIZE + 1), cantidad_libros)
            # Generar un nombre para la ruta literaria
            name = f"Ruta Literaria {id}"
            # Generar una descripción para la ruta literaria
            description = f"Descripción de la ruta literaria {id}"
            # Generar una fecha de creación para la ruta literaria
            created_at = generate_logical_timestamp()
            # Generar un id de ruta literaria
            id_route = id
            # Generar un id de usuario aleatorio
            user = random.choice(self.users)
            id_user = user.id_user
            # Created_at de la ruta literaria
            created_at = datetime.strptime(user.created_at, "%Y-%m-%d %H:%M:%S") + timedelta(days=random.randint(1, 5))
            # Generar una ruta literaria
            literaryRoute = LiteraryRoute(id_route, libros, id_user,created_at, name, description)
            
            # Insertar la ruta literaria en la base de datos
            insert_in_literary_route, insert_in_literary_route_book = literaryRoute.create_sql()
            self.write(self.literary_route_path, insert_in_literary_route)
            self.write(self.literary_route_book_path, insert_in_literary_route_book)
            self.literary_routes.append(literaryRoute)

            id += 1


def main():
    EXCHANGE_CONFIRMED_NEEDED = 300
    # delete all files in folder
    for file in os.listdir(FOLDER_PATH):
        os.remove(f"{FOLDER_PATH}/{file}")

    writer = Writer(USERS_PATH, POSTS_PATH, EXCHANGE_OFFERS_PATH, EXCHANGES_PATH, SURVEYS_PATH, REVIEWS_PATH, STATE_HISTORIES_PATH, EXCHANGE_USERS_PATH, EXCHANGE_CONFIRMED_NEEDED, LITERARY_ROUTES_PATH, LITERARY_ROUTES_BOOK_PATH)
    writer.generate_users(1000)
    writer.get_users()
    writer.generate_n_post_per_user(1, 2, 83)
    writer.generate_exchanges()
    writer.generate_aylen_case()
    writer.generate_reviews()
    writer.generate_literary_routes(100)

if __name__ == "__main__":
    main()