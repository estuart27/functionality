import os
import sqlite3
from datetime import datetime
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from groq import Groq

class RestaurantDatabase:
    def __init__(self):
        self.menu_conn = sqlite3.connect('restaurant_menu.db')
        self.customer_conn = sqlite3.connect('customer_interactions.db')
        self.create_tables()
    
    def create_tables(self):
        # Tabela de Menu
        menu_cursor = self.menu_conn.cursor()
        menu_cursor.execute('''
        CREATE TABLE IF NOT EXISTS dishes (
            dish_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            price REAL,
            is_available BOOLEAN DEFAULT 1
        )
        ''')
        
        # Tabela de Clientes
        customer_cursor = self.customer_conn.cursor()
        customer_cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            address TEXT,
            phone TEXT,
            first_visit TEXT
        )
        ''')
        
        # Tabela de Pedidos
        customer_cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            order_date TEXT,
            items TEXT,
            total_amount REAL,
            status TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        ''')
        
        # Nova tabela para histórico de conversas
        customer_cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            timestamp TEXT,
            customer_message TEXT,
            bot_response TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        ''')
        
        # Nova tabela para preferências do cliente
        customer_cursor.execute('''
        CREATE TABLE IF NOT EXISTS customer_preferences (
            preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            preference_type TEXT,
            preference_value TEXT,
            last_updated TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
        )
        ''')
        
        self.menu_conn.commit()
        self.customer_conn.commit()
    
    def add_customer(self, name, address, phone):
        cursor = self.customer_conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO customers (name, address, phone, first_visit)
        VALUES (?, ?, ?, ?)
        ''', (name, address, phone, current_date))
        self.customer_conn.commit()
        return cursor.lastrowid
    
    def get_customer(self, phone):
        cursor = self.customer_conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE phone = ?', (phone,))
        return cursor.fetchone()
    
    def add_conversation(self, customer_id, customer_message, bot_response):
        cursor = self.customer_conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute('''
        INSERT INTO conversations (customer_id, timestamp, customer_message, bot_response)
        VALUES (?, ?, ?, ?)
        ''', (customer_id, current_date, customer_message, bot_response))
        self.customer_conn.commit()
    
    def get_customer_history(self, customer_id):
        cursor = self.customer_conn.cursor()
        
        # Obter últimos 5 pedidos
        cursor.execute('''
        SELECT order_date, items, total_amount 
        FROM orders 
        WHERE customer_id = ? 
        ORDER BY order_date DESC LIMIT 5
        ''', (customer_id,))
        recent_orders = cursor.fetchall()
        
        # Obter últimas 5 conversas
        cursor.execute('''
        SELECT timestamp, customer_message, bot_response 
        FROM conversations 
        WHERE customer_id = ? 
        ORDER BY timestamp DESC LIMIT 5
        ''', (customer_id,))
        recent_conversations = cursor.fetchall()
        
        # Obter preferências do cliente
        cursor.execute('''
        SELECT preference_type, preference_value 
        FROM customer_preferences 
        WHERE customer_id = ?
        ''', (customer_id,))
        preferences = cursor.fetchall()
        
        return {
            'orders': recent_orders,
            'conversations': recent_conversations,
            'preferences': preferences
        }
    
    def update_preferences(self, customer_id, message):
        # Análise básica de preferências baseada nas mensagens
        keywords = {
            'comida_preferida': ['favorito', 'adoro', 'gosto muito', 'prefiro'],
            'restricao': ['não como', 'alergia', 'não gosto', 'vegetariano', 'vegano'],
            'horario_preferido': ['almoço', 'jantar', 'hora do almoço', 'noite']
        }
        
        cursor = self.customer_conn.cursor()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for pref_type, words in keywords.items():
            for word in words:
                if word.lower() in message.lower():
                    # Extrair contexto (palavras próximas ao keyword)
                    words = message.lower().split()
                    word_index = words.index(word.lower())
                    context = ' '.join(words[max(0, word_index-2):min(len(words), word_index+3)])
                    
                    cursor.execute('''
                    INSERT OR REPLACE INTO customer_preferences 
                    (customer_id, preference_type, preference_value, last_updated)
                    VALUES (?, ?, ?, ?)
                    ''', (customer_id, pref_type, context, current_date))
        
        self.customer_conn.commit()

class RestaurantBot:
    def __init__(self, api_key):
        os.environ['GROQ_API_KEY'] = api_key
        self.chat = ChatGroq(model='gemma2-9b-it')
        self.db = RestaurantDatabase()
        
    def process_response(self, customer_id, query):
        # Atualizar preferências baseado na mensagem do cliente
        self.db.update_preferences(customer_id, query)
        
        # Obter histórico completo do cliente
        history = self.db.get_customer_history(customer_id)
        
        system_message = f"""
        Você é um atendente de restaurante inteligente e atencioso.
        
        Informações do cliente:
        - Últimos pedidos: {history['orders']}
        - Histórico de conversas recentes: {history['conversations']}
        - Preferências conhecidas: {history['preferences']}
        
        Use essas informações para:
        1. Personalizar suas respostas
        2. Fazer recomendações baseadas no histórico
        3. Evitar sugerir itens que o cliente não gosta
        4. Lembrar de preferências e restrições anteriores
        5. Manter consistência com conversas anteriores
        6. Seja Objetivo , direta e curta nas respostas

        
        Seja sempre cordial e profissional.
        """
        
        mensagens = [
            ('system', system_message),
            ('user', query)
        ]
        
        template = ChatPromptTemplate.from_messages(mensagens)
        chain = template | self.chat
        response = chain.invoke({}).content
        
        # Salvar a conversa
        self.db.add_conversation(customer_id, query, response)
        
        return response

def main():
    api_key = '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'
    bot = RestaurantBot(api_key)
    
    print('Bem-vindo ao Restaurante!')
    
    # Coleta inicial de informações
    name = input('Por favor, digite seu nome: ')
    address = input('Por favor, digite seu endereço: ')
    phone = input('Por favor, digite seu número de telefone: ')
    
    # Verificar se cliente já existe
    customer = bot.db.get_customer(phone)
    if customer:
        customer_id = customer[0]
        print(f'Bem-vindo de volta, {name}!')
        
        # Mostrar algumas preferências conhecidas
        history = bot.db.get_customer_history(customer_id)
        if history['preferences']:
            print('\nBaseado em suas visitas anteriores, notei que você:')
            for pref_type, pref_value in history['preferences']:
                print(f'- {pref_value}')
    else:
        customer_id = bot.db.add_customer(name, address, phone)
        print('Cadastro realizado com sucesso!')
    
    print('\nComo posso ajudar você hoje?')
    
    while True:
        query = input('Cliente: ')
        if query.lower() == 'sair':
            break
            
        response = bot.process_response(customer_id, query)
        print(f'Atendente: {response}')
    
    print('Obrigado pela preferência! Volte sempre!')

if __name__ == "__main__":
    main()