import mysql.connector
from pathlib import Path
from configparser import ConfigParser

# Read configuration file
current_directory = Path.cwd()
CONFIG_FILE = f"{current_directory}/config.ini"
config = ConfigParser()
config.read(CONFIG_FILE)


class MySql:

    def __init__(self):
        self.config = {"host": config["mysql"]["host"],
                       "port": config["mysql"]["port"],
                       "user": config["mysql"]["user"],
                       "password": config["mysql"]["password"],
                       "database": config["mysql"]["database"]}

        self.__create_database = """CREATE DATABASE IF NOT EXISTS hgvs_variant_db"""

        self.__create_table = """CREATE TABLE IF NOT EXISTS hgvs_variants (
                                 id INT AUTO_INCREMENT PRIMARY KEY,
                                 variant_id VARCHAR(255) NOT NULL,
                                 g_hgvs_description VARCHAR(255) NOT NULL,
                                 c_hgvs_description VARCHAR(255) NOT NULL,
                                 p_hgvs_description VARCHAR(255) NOT NULL,
                                 mane VARCHAR(255) NOT NULL,
                                 gene_symbol VARCHAR(255) NOT NULL,
                                 hgnc_id VARCHAR(255) NOT NULL,
                                 metadata JSON NOT NULL
                                 )"""

        self.__drop_table = """DROP TABLE hgvs_variants"""

    def get_conn(self):
        # Connect to MySQL database
        conn = mysql.connector.connect(host=self.config["host"],
                                       user=self.config["user"],
                                       password=self.config["password"],
                                       database=self.config["database"])
        return conn

    def get_cursor(self, conn):
        cursor = conn.cursor()
        return cursor

    def create_database(self):
        conn = mysql.connector.connect(host=self.config["host"],
                                       user=self.config["user"],
                                       password=self.config["password"])
        cursor = self.get_cursor(conn)
        cursor.execute(self.__create_database)
        conn.commit()
        cursor.close()
        conn.close()

    def create_table(self):
        conn = self.get_conn()
        cursor = self.get_cursor(conn)
        cursor.execute(self.__create_table)
        conn.commit()
        cursor.close()
        conn.close()

    def drop_table(self):
        conn = self.get_conn()
        cursor = self.get_cursor(conn)
        cursor.execute(self.__drop_table)
        conn.commit()
        cursor.close()
        conn.close()
