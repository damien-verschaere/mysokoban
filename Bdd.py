import mysql.connector

class MySQLConnector:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connexion à la base de données MySQL réussie.")
        except mysql.connector.Error as error:
            print("Impossible de se connecter à la base de données : {}".format(error))

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Déconnexion de la base de données MySQL réussie.")
        else:
            print("Aucune connexion active à la base de données MySQL.")

    def execute_query(self, query, params=None):
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            print("Requête exécutée avec succès.")
        except mysql.connector.Error as error:
            print("Impossible d'exécuter la requête : {}".format(error))
        return cursor

