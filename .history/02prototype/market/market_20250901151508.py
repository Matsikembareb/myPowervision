from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)

    def __repr__(self):
        return f'Item {self.name}'


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html', items=items)

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if Item.query.count() == 0:
            # Add sample data
            item1 = Item(name="Phone", price=500, barcode="123456789012", description="A smartphone")
            item2 = Item(name="Laptop", price=1000, barcode="123456789013", description="A gaming laptop")
            item3 = Item(name="Keyboard", price=150, barcode="123456789014", description="Mechanical keyboard")
            
            db.session.add(item1)
            db.session.add(item2)
            db.session.add(item3)
            db.session.commit()
            print("Sample data added!")
        
    app.run(debug=True)