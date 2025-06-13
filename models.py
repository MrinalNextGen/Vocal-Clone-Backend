from database import db
from datetime import datetime

class Blog(db.Model):
    __tablename__ = 'blogs'
    
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text)  # Changed from VARCHAR(500) to TEXT
    heading = db.Column(db.String(200), nullable=False)
    subHeading = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)  # Changed to TEXT
    author = db.Column(db.String(100), default="Current User")
    authorImage = db.Column(db.Text)  # Changed from VARCHAR(500) to TEXT
    isFavorite = db.Column(db.Boolean, default=False)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, **kwargs):
        super(Blog, self).__init__(**kwargs)
        if not self.authorImage:
            self.authorImage = "https://via.placeholder.com/40x40/cccccc/666666?text=User"

    def to_dict(self):
        """Convert blog object to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'image': self.image,
            'heading': self.heading,
            'subHeading': self.subHeading,
            'description': self.description,
            'author': self.author,
            'authorImage': self.authorImage,
            'isFavorite': self.isFavorite,
            'createdAt': self.createdAt.isoformat() if self.createdAt else None,
            'updatedAt': self.updatedAt.isoformat() if self.updatedAt else None
        }

    def validate(self):
        """Validate blog data and return list of errors"""
        errors = []
        
        if not self.heading or not self.heading.strip():
            errors.append("Heading is required")
        
        if not self.description or not self.description.strip():
            errors.append("Description is required")
        
        if self.description and len(self.description.strip()) < 10:
            errors.append("Description must be at least 10 characters")
        
        return errors

    def __repr__(self):
        return f'<Blog {self.id}: {self.heading}>'
