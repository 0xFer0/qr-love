from flask import Flask, render_template, request, url_for, jsonify
import psycopg2
import psycopg2.extras
import random
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Database connection using Render's External Database URL
def get_db_connection():
    database_url = os.getenv('DATABASE_URL', 'postgresql://qr_love_user:JpLt6qxiagIxegNhAT0e4VJrAP5kmaBo@dpg-cvhndchopnds73flgp80-a.oregon-postgres.render.com/qr_love')
    result = urlparse(database_url)
    conn = psycopg2.connect(
        database=result.path[1:],  # 'qr_love'
        user=result.username,      # 'qr_love_user'
        password=result.password,  # 'JpLt6qxiagIxegNhAT0e4VJrAP5kmaBo'
        host=result.hostname,      # 'dpg-cvhndchopnds73flgp80-a.oregon-postgres.render.com'
        port=result.port           # 5432
    )
    return conn

def init_db():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            password TEXT,
            message TEXT NOT NULL,
            button_text TEXT NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

# Initialize database on startup
try:
    init_db()
except Exception as e:
    print(f"Error initializing database: {e}")
MESSAGES = {
    'en': [
        "You are the calm in my storm, the peace in my chaos, and the love in my life.",
        "Every day spent with you is a blessing, every moment with you feels like home.",
        "I never knew what true happiness was until I met you. You complete me in ways I can’t explain.",
        "You're not just my love, you're my best friend, my safe place, my constant.",
        "When I think of the future, I see nothing but you by my side, today and always.",
        "With every breath I take, I love you more, and I will continue to love you beyond forever.",
        "You are my heart's desire, my reason for everything good that happens in my life.",
        "My love for you grows stronger every day, like a beautiful story that has no end.",
        "You make my world brighter, my heart lighter, and my life worth living.",
        "You're not just someone I love, you're my whole world, and I want to spend every moment with you.",
        "I never imagined life could be so perfect until I met you. You are everything I ever wanted.",
        "You are the best part of me, and I thank the universe every day for bringing us together.",
        "With you, life is not just a journey; it's an adventure full of love, laughter, and endless memories.",
        "I am the luckiest person alive because I get to love you and be loved by you.",
        "You are the reason I wake up smiling every day. My life is brighter because of you.",
        "In your eyes, I find my home. In your heart, I find my peace.",
        "You make everything better – my days, my nights, my world. You are my everything.",
        "I’ve never felt more alive than when I’m with you. You’re the beat of my heart and the rhythm of my soul.",
        "Your love is the greatest gift I could ever receive, and I will cherish it for the rest of my life.",
        "I want to grow old with you, create memories with you, and love you for the rest of my days.",
        "You are my forever, my always, my everything.",
        "Every time I think of you, my heart skips a beat. You are the love I’ve always dreamed of.",
        "No matter where life takes us, I’ll always be by your side, loving you every step of the way.",
        "I thank God every day for bringing you into my life. You are my answer to every prayer.",
        "You are the reason I believe in destiny. We were meant to be, now and forever.",
        "Being with you feels like I’m living in a dream, and I never want to wake up.",
        "You make everything brighter. Your smile, your laughter, your love – they make my world complete.",
        "I love you in ways that words can’t explain, and I will continue to love you with all my heart.",
        "In this life and the next, I’ll choose you every single time.",
        "My heart belongs to you, today, tomorrow, and forever.",
        "With you, every moment is a beautiful memory I want to keep forever.",
        "I will love you until the stars fall from the sky, and even then, my love will remain.",
        "I’m so grateful for your love. It makes everything worth it.",
        "I never knew love could be so beautiful until I met you. You are my everything.",
        "You complete me in ways I never thought possible. I’m so lucky to have you.",
        "If I had a choice, I would choose you over and over again, without hesitation.",
        "The world may change, but my love for you will remain constant and unshakable.",
        "I would give up everything just to see your smile for the rest of my life.",
        "With every kiss, with every hug, you make me feel like the luckiest person in the world.",
        "I could search a thousand lifetimes and still never find someone as special as you.",
        "You are the best decision I’ve ever made. I’m so glad I chose you.",
        "You are my dream come true. Thank you for making my life so beautiful.",
        "I will love you in every lifetime, in every world, in every universe.",
        "There is no greater joy in life than knowing you’re with me, always.",
        "You are my strength, my light, my reason for living.",
        "Together, we can conquer the world. With you, there’s nothing I can’t do.",
        "I’d rather spend one lifetime with you than face all the ages of this world alone.",
        "You are my destiny, my forever, and the love of my life.",
        "In your arms, I find peace. In your eyes, I see forever.",
        "I want to be with you in every way possible, now and always.",
        "You are the one I’ve been waiting for all my life.",
        "No distance can ever separate us. My heart is always with you.",
        "I’d choose you, even if I had a thousand lives to live.",
        "You are my home, my heart, and my forever."
    ],
    'ar': [
        "أنت الهدوء في حياتي، السكينة في فوضاي، والحب في قلبي.",
        "كل لحظة معك هي نعمة، وكل يوم معك يشعرني كأني في بيتي.",
        "ما كنت أعرف معنى السعادة الحقيقية إلا بعد ما قابلتك. أنت تكملني بطرق ما أقدر أشرحها.",
        "أنت مو بس حبيبي، أنت أعز صديق لي، مكان أمان في حياتي، وسندي دايمًا.",
        "لما أفكر في المستقبل، ما أقدر أتخيل حياتي من دونك. أنت اليوم، وكل يوم، ودائمًا.",
        "مع كل نفس آخذته، حبي ليك يزيد، وبحبك أكثر من أي وقت مضى، وأعدك أنني سأظل أحبك إلى ما بعد الأبد.",
        "أنت رغبة قلبي، سبب كل شيء حلو في حياتي، وكل شيء حلو يصير لي بسببك.",
        "حبي ليك يزيد كل يوم، كأننا قصة جميلة ما لها نهاية.",
        "أنت تجعل عالمي أكثر إشراقًا، وقلبي أخف، وحياتي تستحق العيش بوجودك.",
        "أنت مو بس شخص أحبك، أنت عالمي كله، وأبغى أعيش معك كل لحظة.",
        "ما كنت أتخيل الحياة ممكن تكون بهذا الجمال إلا بعد ما قابلتك. أنت كل شيء كنت أتمناه.",
        "أنت أجمل جزء في حياتي، وأشكر الله كل يوم على أنك دخلت حياتي.",
        "معك، الحياة مو مجرد رحلة، هي مغامرة مليانة بالحب، والضحك، والذكريات اللي ما تنسى.",
        "أنا أسعد إنسان في الدنيا لأني أحبك وأنت تحبني.",
        "أنت السبب في أنني أستيقظ مبتسم كل يوم، حياتي أصبحت أفضل بوجودك.",
        "في عيونك، لقيت بيتي. في قلبك، لقيت سكينتي.",
        "أنت تجعل كل شيء أفضل – أيامي، ليالي، عالمي. أنت كل شيء بالنسبة لي.",
        "ما حسيت بالحياة الحقيقية إلا معك. أنت نبض قلبي وإيقاع روحي.",
        "حبك هو أعظم هدية في حياتي، وأعدك أنني سأحتفظ به إلى الأبد.",
        "أبغى أكبر معك، وأصنع معك ذكريات، وأحبك لبقية أيام عمري.",
        "أنت إلى الأبد، وأنت دائمًا، وأنت كل شيء.",
        "كلما فكرت فيك، ينبض قلبي بسرعة. أنت الحب الذي حلمت به دائمًا.",
        "ما يهم وين الحياة تأخذنا، أنا دائمًا معك، أحبك في كل خطوة.",
        "أشكر الله كل يوم لأنه جابك في حياتي. أنت جواب كل دعاء.",
        "أنت السبب اللي خلاني أؤمن بالقضاء والقدر. كنا مكتوبين لبعض، اليوم ودائمًا.",
        "كوني معك، شعور يشبه الحلم، وما أبغى أصحى منه أبدًا.",
        "أنت تضيء كل شيء. ابتسامتك، ضحكتك، حبك – هم اللي يكملون عالمي.",
        "أحبك بطرق ما تقدر الكلمات تشرحها، وسأظل أحبك بكل قلبي.",
        "في هذه الحياة والمستقبل، راح أختارك كل مرة.",
        "قلبي ملكك، اليوم، بكرة، ودائمًا.",
        "معك، كل لحظة هي ذكرى جميلة أريد الاحتفاظ بها للأبد.",
        "راح أحبك حتى لو سقطت النجوم من السماء، وحتى بعدين، حبك راح يظل.",
        "أنا ممتن لحبك. هو اللي بيخلي كل شيء يستحق.",
        "ما كنت أعرف الحب ممكن يكون جميل كذا إلا بعد ما قابلتك. أنت كل شيء في حياتي.",
        "أنت تكملني بطرق ما كنت أتخيلها. أنا محظوظ جدًا فيك.",
        "لو عندي اختيار، كنت راح أختارك مرة ثانية، من غير تردد.",
        "العالم قد يتغير، لكن حبي لك راح يظل ثابت وما يتغير.",
        "كنت مستعد أضحي بكل شيء بس عشان أشوف ابتسامتك طول حياتي.",
        "مع كل قبلة، مع كل عناق، تحسسني إني أكثر شخص محظوظ في الدنيا.",
        "أقدر أبحث في ألف حياة، ولا ألقى شخص مثلك.",
        "أنت أفضل قرار اتخذته في حياتي. أنا سعيد جدًا إني اخترتك.",
        "أنت حلمي اللي تحقق. شكرًا لأنك جعلت حياتي أجمل.",
        "راح أحبك في كل حياة، في كل عالم، في كل كون.",
        "ما في سعادة أكبر في حياتي من إني أكون معك، دايمًا.",
        "أنت قوتي، ضوءي، وسبب حياتي.",
        "معك، نقدر نغزو العالم. معك، مافي شيء مستحيل.",
        "أفضل أعيش معك حياة واحدة عن إني أعيش كل العصور وأنا لوحدي.",
        "أنت قدري، أنت الأبد، وأنت حب حياتي.",
        "في ذراعيك، لقيت سكينتي. في عيونك، شفت الأبد.",
        "أبغى أكون معك بكل الطرق الممكنة، اليوم ودائمًا.",
        "أنت الشخص اللي كنت أستناه طوال حياتي.",
        "ما في مسافة ممكن تفرقنا. قلبي دايمًا معك.",
        "كنت راح أختارك، حتى لو عندي ألف حياة أعيشها.",
        "أنت بيتي، قلبي، وأبديتي."
    ]
}
@app.route('/', methods=['GET', 'POST'])
def creator():
    language = request.args.get('lang', 'en')
    if request.method == 'POST':
        try:
            card_data = {
                'name': request.form['name'],
                'language': request.form['language'],
                'password': request.form.get('password', None),
                'message': request.form['message'],
                'button_text': 'For You!' if request.form['language'] == 'en' else 'لك!'
            }
            
            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("""
                INSERT INTO cards (name, language, password, message, button_text)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (card_data['name'], card_data['language'], card_data['password'], 
                  card_data['message'], card_data['button_text']))
            card_id = cur.fetchone()['id']
            conn.commit()
            cur.close()
            conn.close()

            card_url = url_for('card', id=card_id, _external=True)
            return jsonify({'url': card_url, 'success': True})
        except Exception as e:
            return jsonify({'error': str(e), 'success': False}), 500
    
    return render_template('index.html', messages=MESSAGES, language=language)
import uuid
import random
import string

# Function to generate a unique ID (e.g., 4hf5#4)
def generate_unique_id():
    # Example format: 4 characters + # + 1 character
    letters = string.ascii_lowercase + string.digits
    part1 = ''.join(random.choice(letters) for _ in range(4))
    part2 = random.choice(letters)
    return f"{part1}#{part2}"

# Modified route to accept string IDs instead of integers
@app.route('/card/<string:id>')
def card(id):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute('SELECT * FROM cards WHERE id = %s', (id,))
        card = cur.fetchone()
        cur.close()
        conn.close()
        
        if not card:
            return "<h1 style='color: #ff99b3; text-align: center; padding: 20px;'>Card not found!</h1>"
        
        return render_template('card.html', card=dict(card))
    except Exception as e:
        return f"<h1 style='color: #ff99b3; text-align: center; padding: 20px;'>Error: {str(e)}</h1>"

@app.route('/random_message/<lang>')
def random_message(lang):
    message = random.choice(MESSAGES.get(lang, MESSAGES['en']))
    return jsonify({'message': message})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
