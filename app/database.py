import mysql.connector
from mysql.connector import Error
from app.config import Config
import json

class Database:
    def __init__(self):
        self.config = {
            'host': Config.MYSQL_HOST,
            'user': Config.MYSQL_USER,
            'password': Config.MYSQL_PASSWORD,
            'database': Config.MYSQL_DATABASE
        }
        
    def connect(self):
        try:
            conn = mysql.connector.connect(**self.config)
            return conn
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return None
            
    def initialize_db(self):
        """创建必要的数据库表"""
        conn = self.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            
            # 用户表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(80) NOT NULL UNIQUE,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    password_hash VARCHAR(128) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 问卷表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS surveys (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(200) NOT NULL,
                    json_data JSON,
                    author_id INT,
                    is_public BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (author_id) REFERENCES users(id)
                )
            ''')
            
            # 答案表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS results (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    survey_id INT NOT NULL,
                    user_id INT,
                    json_data JSON NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (survey_id) REFERENCES surveys(id),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            conn.commit()
            return True
        except Error as e:
            print(f"Error creating tables: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
            
    def execute_query(self, query, params=None, fetch=True):
        """执行SQL查询并返回结果"""
        conn = self.connect()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch:
                result = cursor.fetchall()
            else:
                conn.commit()
                result = cursor.lastrowid
                
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
            
    def execute_many(self, query, params_list):
        """批量执行SQL查询"""
        conn = self.connect()
        if not conn:
            return False
            
        try:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            conn.commit()
            return True
        except Error as e:
            print(f"Error executing batch query: {e}")
            return False
        finally:
            cursor.close()
            conn.close()