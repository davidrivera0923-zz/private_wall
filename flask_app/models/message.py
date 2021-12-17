from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math


class Message:
    db_name = 'private_wall'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.content = db_data['posts']
        self.sender_id = db_data['send_id']
        self.receiver_id = db_data['receiver_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
    
    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        elif delta.total_seconds() >= 1:
            return f"{math.floor(delta.total_seconds)} seconds ago"
        else:
            return f"Just Now"

    @classmethod
    def get_user_messages(cls,data):
        query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users JOIN messages ON users.id = messages.send_id JOIN users as users2 ON users2.id = messages.receiver_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        if len(results) < 1:
            return []
        messages = []
        print(results)
        for message in results:
            message_data = {
                "id": message['id'],
                "posts": message['posts']
            
            }
            messages.append( cls(message) )
        return messages

    @classmethod
    def save(cls,data):
        query = "INSERT INTO messages (posts,send_id,receiver_id) VALUES (%(posts)s,%(send_id)s,%(receiver_id)s);"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM messages WHERE messages.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)