from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_FILE = "database.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # ప్రొఫైల్ టేబుల్ (ఐడీలు, బయో, ఫాలోవర్స్ అన్నీ శాశ్వతంగా దాచడానికి)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY,
            name TEXT, username TEXT, bio TEXT, 
            profile_pic TEXT, followers INTEGER, following INTEGER
        )
    ''')
    # పోస్ట్‌ల టేబుల్
    cursor.execute('CREATE TABLE IF NOT EXISTS posts (id INTEGER PRIMARY KEY AUTOINCREMENT, image_url TEXT)')
    # మెసేజ్‌ల టేబుల్
    cursor.execute('CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, sender TEXT, text TEXT)')
    
    # మొదటిసారి అప్లికేషన్ రన్ అయినప్పుడు డిఫాల్ట్ ప్రొఫైల్ సెట్ చేయడం కోసం
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO profile (id, name, username, bio, profile_pic, followers, following)
            VALUES (1, 'Manohar _arepalli', '@manohar', 'Obsessed with Mahee 💖 | Account Protected', 
                    'https://images.unsplash.com/photo-1534528741775-53994a69daeb', 1, 1)
        ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # డేటాబేస్ నుండి ప్రొఫైల్ వివరాలు తెచ్చుకోవడం
    cursor.execute('SELECT name, username, bio, profile_pic, followers, following FROM profile WHERE id=1')
    prof = cursor.fetchone()
    # డేటాబేస్ నుండి పోస్ట్‌లు తెచ్చుకోవడం
    cursor.execute('SELECT image_url FROM posts ORDER BY id DESC')
    posts = [row[0] for row in cursor.fetchall()]
    conn.close()
    
    return render_template('index.html', name=prof[0], username=prof[1], bio=prof[2], 
                           profile_pic=prof[3], followers=prof[4], following=prof[5], posts=posts)

@app.route('/update_profile', methods=['POST'])
def update_profile():
    profile_pic = request.form.get('profile_pic')
    followers = request.form.get('followers')
    following = request.form.get('following')
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    if profile_pic:
        cursor.execute('UPDATE profile SET profile_pic=? WHERE id=1', (profile_pic,))
    if followers:
        cursor.execute('UPDATE profile SET followers=? WHERE id=1', (followers,))
    if following:
        cursor.execute('UPDATE profile SET following=? WHERE id=1', (following,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/post', methods=['POST'])
def create_post():
    image_url = request.form.get('image_url')
    if image_url:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (image_url) VALUES (?)', (image_url,))
        conn.commit()
        conn.close()
    return redirect('/')

@app.route('/messages')
def messages_page():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT sender, text FROM messages ORDER BY id ASC')
    all_messages = cursor.fetchall()
    conn.close()
    return render_template('messages.html', messages=all_messages)

@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form.get('sender', 'Manohar')
    text = request.form.get('text')
    if text:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender, text) VALUES (?, ?)', (sender, text))
        conn.commit()
        conn.close()
    return redirect('/messages')

if __name__ == '__main__':
    app.run(debug=True)
            
