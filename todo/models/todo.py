import datetime
from . import db

class Todo(db.Model):
    __tablename__ = 'todos'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)   
    # Mandatory column of 80 characters
    title = db.Column(db.String(80), nullable=False)
    # Optional column of 120 characters
    description = db.Column(db.String(120), nullable=True)
    # Column with default value of False
    completed = db.Column(db.Boolean, default=False, nullable=False)
    deadline_at = db.Column(db.DateTime, nullable=True)
    # Column with default value is a function call
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    # Updates on update
    updated_at = db.Column(db.DateTime, nullable=False,
                            default=datetime.datetime.now,
                            onupdate=datetime.datetime.now)
    
    # Helper method to convert the model to a dictionary
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'deadline_at': self.deadline_at.isoformat() if self.deadline_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Todo {self.id} {self.title}>'