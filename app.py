from flask import Flask, render_template, request, url_for, jsonify
import json

app = Flask(__name__)

# In-memory store (replace with database in production)
cards = {}

@app.route('/', methods=['GET', 'POST'])
def creator():
    if request.method == 'POST':
        card_data = {
            'id': str(len(cards) + 1),
            'name': request.form['name'],
            'language': request.form['language'],
            'password': request.form['password'],
            'message': request.form['message'],
            'button_text': 'For You!' if request.form['language'] == 'en' else 'لك!'
        }
        cards[card_data['id']] = card_data
        card_url = url_for('card', id=card_data['id'], _external=True)
        return jsonify({'url': card_url})
    return render_template('index.html')

@app.route('/card/<id>')
def card(id):
    card_data = cards.get(id)
    if not card_data:
        return "<h1 style='color: #ff99b3; text-align: center; padding: 20px;'>Card not found!</h1>"
    return render_template('card.html', card=card_data)

if __name__ == '__main__':
    app.run(debug=True)
