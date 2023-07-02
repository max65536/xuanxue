class Fu(db.Model):
    __tablename__ = 'your_table'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    question = db.Column(db.String(255))
    answer = db.Column(db.String(255))
