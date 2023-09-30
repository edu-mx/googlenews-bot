import logging

class Logger:
    def __init__(self):
        # Configuração básica do logger
        logging.basicConfig(filename='logs.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s: %(message)s')

    def error(self, message):
        # Registra uma mensagem de erro no log
        logging.error(message)

    def critical(self, message):
        # Registra uma mensagem crítica no log
        logging.critical(message)
