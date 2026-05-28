from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# డేటాబేస్ మరియు టేబుల్స్ క్రియేట్ చేసే ఫంక్షన్
def init_db():
    # 🌟 పాత తప్పుడు డేటాబేస్ ఫైల్‌ను ఆటోమేటిక్‌గా రీసెట్ చేయడానికి ఈ 3 లైన్ల ట్రిక్ కలిపాను
    import os
    if os.path.exists('database.db'):
        os.remove('database.db')
        
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # 1. ప్రొఫైల్ కౌంట్స్ (Followers, Following, Posts) టేబుల్
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            posts_count TEXT,
            followers_count TEXT,
            following_count TEXT
        )
    ''')
    
    # 2. మెసెంజర్ చాట్ మెసేజ్ల టేబుల్
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message_text TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 3. పోస్ట్‌ల టేబుల్ (ఇమేజ్ లింక్స్ కోసం)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_url TEXT
        )
    ''')
    
    # ప్రొఫైల్ టేబుల్‌లో మొదట్లో డీఫాల్ట్ వాల్యూస్ ఉంచడానికి
    cursor.execute('SELECT COUNT(*) FROM profile')
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO profile (posts_count, followers_count, following_count) VALUES ('0', '150', '180')")
        
    conn.commit()
    conn.close()

# యాప్ స్టార్ట్ అయ్యేటప్పుడు డేటాబేస్ రన్ అవుతుంది
init_db()

# 1. హోమ్ పేజీ (ఇన్‌స్టాగ్రామ్ ఫీడ్ మరియు ప్రొఫైల్ డేటా)
@app.route('/')
def home():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # ప్రొఫైల్ డేటా తెచ్చుకోవడం
    cursor.execute('SELECT posts_count, followers_count, following_count FROM profile WHERE id = 1')
    profile_data = cursor.fetchone()
    
    # అన్ని పోస్ట్‌లను తెచ్చుకోవడం
    cursor.execute('SELECT image_url FROM posts ORDER BY id DESC')
    all_posts = cursor.fetchall()
    
    conn.close()
    
    return render_template('index.html', profile=profile_data, posts=all_posts)

# 2. ప్రొఫైల్ కౌంట్స్ అప్‌డేట్ చేసే రూట్
@app.route('/update_profile', methods=['POST'])
def update_profile():
    posts = request.form.get('posts')
    followers = request.form.get('followers')
    following = request.form.get('following')
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE profile 
        SET posts_count = ?, followers_count = ?, following_count = ? 
        WHERE id = 1
    ''', (posts, followers, following))
    conn.commit()
    conn.close()
    
    return redirect('/')

# 3. కొత్త పోస్ట్ యాడ్ చేసే రూట్ (+ సింబల్ కోసం)
@app.route('/add_post', methods=['POST'])
def add_post():
    image_url = request.form.get('image_url')
    if image_url:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO posts (image_url) VALUES (?)', (image_url,))
        
        # పోస్ట్‌ల కౌంట్‌ను ఆటోమేటిక్‌గా 1 పెంచడానికి
        cursor.execute('SELECT posts_count FROM profile WHERE id = 1')
        current_count = int(cursor.fetchone()[0])
        new_count = str(current_count + 1)
        cursor.execute('UPDATE profile SET posts_count = ? WHERE id = 1', (new_count,))
        
        conn.commit()
        conn.close()
        
    return redirect('/')

# 4. ఇన్‌స్టాగ్రామ్ డీఎమ్ (Messenger) చాట్ పేజీ రూట్
@app.route('/messenger')
def messenger():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    # అన్ని మెసేజ్లను పాత వాటి నుండి కొత్త వాటి ఆర్డర్‌లో తెచ్చుకుంటుంది
    cursor.execute('SELECT sender, message_text FROM messages ORDER BY timestamp ASC')
    chat_messages = cursor.fetchall()
    conn.close()
    
    return render_template('messenger.html', messages=chat_messages)

# 5. కొత్త చాట్ మెసేజ్ పంపే రూట్
@app.route('/send_message', methods=['POST'])
def send_message():
    sender = request.form.get('sender', 'Me') # డీఫాల్ట్‌గా 'Me' అని వస్తుంది
    message_text = request.form.get('message_text')
    
    if message_text:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO messages (sender, message_text) VALUES (?, ?)', (sender, message_text))
        conn.commit()
        conn.close()
        
    return redirect('/messenger')

if __name__ == '__main__':
    app.run(debug=True)
    
