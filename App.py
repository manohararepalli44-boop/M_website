from flask import Flask, render_template_string, request, redirect, session, url_for
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "m_website_secret_key_manohar")

# తాత్కాలిక డేటాబేస్
USERS = {
    "self_style_manohar": {
        "name": "Arepalli Manohar 💖",
        "bio": "I will never abandon those who trust me 💖",
        "followers": "234",
        "following": "199",
        "posts_count": "2",
        "photos": [
            "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500",
            "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=500"
        ]
    }
}
CHATS = {}
OTP_STORE = {}

# --- కామన్ లేఅవుట్ ఫంక్షన్ ---
def render_m_page(content_html, show_nav=True):
    nav_html = ""
    is_logged_in = 'user_id' in session

    if show_nav and is_logged_in:
        nav_html = f"""
        <div class="bottom-nav">
            <a href="/profile/{session['user_id']}"><i class="fas fa-home"></i></a>
            <a href="/search"><i class="fas fa-search"></i></a>
            <a href="/chat_list"><i class="fas fa-paper-plane"></i></a>
            <a href="/logout"><i class="fas fa-sign-out-alt"></i></a>
        </div>
        """
        
    sidebar_links = ""
    if is_logged_in:
        sidebar_links = f"""
        <a href="/profile/{session['user_id']}"><i class="fas fa-home"></i> Home</a>
        <a href="/search"><i class="fas fa-search"></i> Search ID</a>
        <a href="/chat_list"><i class="fas fa-comments"></i> Messages</a>
        <a href="/logout" style="color: #ff3040;"><i class="fas fa-power-off"></i> Logout</a>
        """
    else:
        sidebar_links = """
        <a href="/"><i class="fas fa-home"></i> Home</a>
        <a href="/register"><i class="fas fa-user-plus"></i> Register</a>
        <a href="/login"><i class="fas fa-sign-in-alt"></i> Login</a>
        """

    full_layout = f"""
    <!DOCTYPE html>
    <html lang="te">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>M Website</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
        <style>
            body {{ background-color: #000; color: #fff; font-family: -apple-system, sans-serif; margin: 0; padding: 0; overflow-x: hidden; }}
            .navbar {{ background-color: #000; border-bottom: 1px solid #262626; padding: 15px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; }}
            .sidebar {{ position: fixed; top: 0; right: -250px; width: 250px; height: 100%; background-color: #121212; border-left: 1px solid #262626; z-index: 1000; transition: 0.3s; padding-top: 60px; box-sizing: border-box; }}
            .sidebar a {{ padding: 15px 25px; text-decoration: none; font-size: 18px; color: #fff; display: block; border-bottom: 1px solid #1a1a1a; }}
            .container {{ padding: 20px; max-width: 600px; margin: 0 auto; padding-bottom: 80px; }}
            .btn {{ background-color: #0095f6; color: white; border: none; padding: 12px; border-radius: 8px; font-weight: bold; cursor: pointer; width: 100%; margin-top: 10px; text-align: center; display: block; box-sizing: border-box; text-decoration: none; }}
            .input-field {{ width: 100%; padding: 12px; margin: 10px 0; border-radius: 8px; border: 1px solid #262626; background-color: #121212; color: white; box-sizing: border-box; }}
            .profile-header {{ display: flex; align-items: center; margin-bottom: 20px; }}
            .profile-pic {{ width: 85px; height: 85px; border-radius: 50%; border: 2px solid #262626; padding: 3px; object-fit: cover; }}
            .stats {{ display: flex; justify-content: space-around; flex-grow: 1; text-align: center; }}
            .stat-num {{ font-weight: bold; font-size: 18px; }}
            .stat-label {{ font-size: 13px; color: #a8a8a8; }}
            .profile-bio {{ margin-bottom: 20px; line-height: 1.4; }}
            .profile-name {{ font-weight: bold; }}
            .highlights {{ display: flex; gap: 15px; margin-bottom: 20px; overflow-x: auto; padding: 5px 0; }}
            .highlight-item {{ text-align: center; min-width: 60px; }}
            .highlight-circle {{ width: 56px; height: 56px; border-radius: 50%; border: 1px solid #262626; display: flex; align-items: center; justify-content: center; font-size: 20px; background: #121212; color: #ff3040; margin-bottom: 4px; }}
            .photo-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 3px; }}
            .grid-img {{ width: 100%; aspect-ratio: 1; object-fit: cover; background-color: #262626; }}
            .bottom-nav {{ position: fixed; bottom: 0; width: 100%; background-color: #000; border-top: 1px solid #262626; display: flex; justify-content: space-around; padding: 15px 0; }}
            .bottom-nav a {{ color: #fff; font-size: 22px; }}
            .alert {{ background-color: #262626; border-left: 4px solid #ff3040; padding: 10px; margin-bottom: 15px; color: #ffdddd; }}
        </style>
    </head>
    <body>
        <div class="navbar">
            <div style="font-weight: bold; font-size: 22px;">M WEBSITE</div>
            <button onclick="toggleSidebar()" style="background:none; border:none; color:white; font-size:24px;"><i class="fas fa-bars"></i></button>
        </div>
        <div id="mySidebar" class="sidebar">
            <button onclick="toggleSidebar()" style="position:absolute; top:15px; left:20px; background:none; border:none; color:white; font-size:24px;">×</button>
            {sidebar_links}
        </div>
        <div class="container">{content_html}</div>
        {nav_html}
        <script>
            function toggleSidebar() {{
                var s = document.getElementById("mySidebar");
                s.style.right = (s.style.right === "0px") ? "-250px" : "0px";
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(full_layout)

# --- రూట్స్ ---

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect(url_for('profile', user_id=session['user_id']))
    
    # ఇక్కడ లింకులు కరెక్ట్‌గా సెట్ చేశాను మనోహర్
    html = """
    <div style="text-align: center; margin-top: 40px;">
        <h1 style="color: #ff3040; font-size: 32px;">Welcome to M Website 💖</h1>
        <p style="color: #a8a8a8;">Created specially for love and connection</p>
        <br><br>
        <a href="/register" class="btn" style="margin-bottom: 15px; text-decoration: none; line-height: 24px;">New Register (మొబైల్ OTP ద్వారా)</a>
        <a href="/login" class="btn" style="background-color: #262626; border: 1px solid #555; text-decoration: none; line-height: 24px;">Already Registered? Login</a>
    </div>
    """
    return render_m_page(html, show_nav=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    error_html = ""
    if request.method == 'POST':
        mobile = request.form.get('mobile')
        if not mobile or len(mobile) < 10:
            error_html = '<div class="alert">సరైన మొబైల్ నంబర్ ఇవ్వండి!</div>'
        else:
            otp = random.randint(1000, 9999)
            OTP_STORE[mobile] = otp
            print(f"\n[M WEBSITE OTP] Mobile: {mobile} -> OTP Sent: {otp}\n")
            return redirect(url_for('verify_otp', mobile=mobile))
        
    html = f"""
    <h2>Create Account</h2>
    <p style="color: #a8a8a8;">నీ సిమ్‌కి మెసేజ్ ద్వారా OTP పంపబడుతుంది</p>
    {error_html}
    <form method="POST">
        <input type="text" name="mobile" placeholder="Enter Mobile Number" class="input-field" required>
        <button type="submit" class="btn">Send OTP to SIM</button>
    </form>
    """
    return render_m_page(html, show_nav=False)

@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    mobile = request.args.get('mobile')
    error_html = ""
    if request.method == 'POST':
        entered_otp = request.form.get('otp')
        user_id = request.form.get('user_id').strip().lower()
        full_name = request.form.get('full_name')
        lover_name = request.form.get('lover_name')
        
        if mobile in OTP_STORE and (int(entered_otp) == OTP_STORE[mobile] or entered_otp == "1234"):
            if user_id in USERS:
                error_html = '<div class="alert">ఈ ID పేరు ఆల్రెడీ ఉంది! వేరేది ఎంచుకోండి.</div>'
            else:
                USERS[user_id] = {
                    "name": full_name,
                    "bio": f"Obsessed with {lover_name} 💖 | Account Protected",
                    "followers": "1",
                    "following": "1",
                    "posts_count": "0",
                    "photos": []
                }
                session['user_id'] = user_id
                return redirect(url_for('profile', user_id=user_id))
        else:
            error_html = '<div class="alert">తప్పు OTP ఎంటర్ చేశారు!</div>'

    html = f"""
    <h2>Verify OTP & Setup Profile</h2>
    <div class="alert" style="border-left-color: #0095f6;">డెమో కోసమే అయితే OTP స్థానంలో '1234' ఎంటర్ చేయవచ్చు.</div>
    {error_html}
    <form method="POST">
        <input type="text" name="otp" placeholder="Enter 4-Digit OTP" class="input-field" required>
        <input type="text" name="user_id" placeholder="Create Instagram ID Name" class="input-field" required>
        <input type="text" name="full_name" placeholder="Your Full Name" class="input-field" required>
        <input type="text" name="lover_name" placeholder="Your Lover Name" class="input-field" required>
        <button type="submit" class="btn">Complete Registration 🚀</button>
    </form>
    """
    return render_m_page(html, show_nav=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_html = ""
    if request.method == 'POST':
        user_id = request.form.get('user_id').strip().lower()
        if user_id in USERS:
            session['user_id'] = user_id
            return redirect(url_for('profile', user_id=user_id))
        error_html = '<div class="alert">ఈ ఐడీ పేరుతో ఎలాంటి అకౌంట్ లేదు!</div>'
        
    html = f"""
    <h2>Login to M Website</h2>
    {error_html}
    <form method="POST">
        <input type="text" name="user_id" placeholder="Enter your Search ID Name" class="input-field" required>
        <button type="submit" class="btn">Login 🔓</button>
    </form>
    """
    return render_m_page(html, show_nav=False)

@app.route('/profile/<user_id>', methods=['GET', 'POST'])
def profile(user_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user_data = USERS.get(user_id)
    if not user_data:
        return "User not found", 404
        
    if request.method == 'POST' and session['user_id'] == user_id:
        photo_url = request.form.get('photo_url')
        if photo_url:
            user_data['photos'].append(photo_url)
            user_data['posts_count'] = str(len(user_data['photos']))
            
    p_pic = "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=500" if user_id == "self_style_manohar" else "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=500"

    grid_items = ""
    for photo in user_data['photos']:
        grid_items += f'<img src="{photo}" class="grid-img">'
    if not user_data['photos']:
        grid_items = '<div style="grid-column: span 3; text-align: center; color: #555; padding: 20px;">No Posts Yet</div>'

    action_box = ""
    if session['user_id'] == user_id:
        action_box = """
        <div style="background: #121212; padding: 10px; border-radius: 8px; margin-bottom: 20px;">
            <form method="POST" style="display: flex; gap: 10px;">
                <input type="text" name="photo_url" placeholder="Paste Image URL to post" class="input-field" style="margin:0; padding:8px;" required>
                <button type="submit" class="btn" style="margin:0; width:auto;">Post</button>
            </form>
        </div>
        """
    else:
        action_box = f'<a href="/chat/{user_id}"><button class="btn" style="background-color: #262626; border: 1px solid #363636; margin-bottom: 15px;"><i class="fab fa-instagram"></i> Message</button></a>'

    html = f"""
    <div class="profile-header">
        <img src="{p_pic}" class="profile-pic">
        <div class="stats">
            <div><div class="stat-num">{user_data['posts_count']}</div><div class="stat-label">posts</div></div>
            <div><div class="stat-num">{user_data['followers']}</div><div class="stat-label">followers</div></div>
            <div><div class="stat-num">{user_data['following']}</div><div class="stat-label">following</div></div>
        </div>
    </div>
    <div class="profile-bio">
        <div class="profile-name">{user_data['name']}</div>
        <div style="color: #a8a8a8; font-size: 14px; margin: 4px 0;">@{user_id}</div>
        <div>{user_data['bio']}</div>
    </div>
    <div class="highlights">
        <div class="highlight-item"><div class="highlight-circle">M</div><div class="stat-label">⭐</div></div>
        <div class="highlight-item"><div class="highlight-circle">a</div><div class="stat-label">🏡</div></div>
    </div>
    {action_box}
    <div class="photo-grid">{grid_items}</div>
    """
    return render_m_page(html, show_nav=True)

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user_id' not in session: return redirect(url_for('login'))
    results_html = ""
    query = ""
    if request.method == 'POST':
        query = request.form.get('query').strip().lower()
        results_list = [uid for uid in USERS if query in uid]
        if results_list:
            results_html = '<div style="background-color: #121212; border-radius: 8px; padding: 10px;">'
            for uid in results_list:
                results_html += f'<div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #262626;"><div><strong>{USERS[uid]["name"]}</strong><br>@{uid}</div><a href="/profile/{uid}" style="color: #0095f6; text-decoration: none;">Open</a></div>'
            results_html += '</div>'
        else:
            results_html = '<p style="color: #a8a8a8;">No ID found.</p>'
    html = f'<h2>Search ID</h2><form method="POST"><input type="text" name="query" class="input-field" required><button type="submit" class="btn">Search</button></form><br>{results_html}'
    return render_m_page(html, show_nav=True)

@app.route('/chat_list')
def chat_list():
    if 'user_id' not in session: return redirect(url_for('login'))
    html = '<h2>Messages</h2><div style="background:#121212; padding:10px; border-radius:8px;"><a href="/chat/self_style_manohar" style="color:white; text-decoration:none;"><strong>Arepalli Manohar (Admin)</strong></a></div>'
    return render_m_page(html, show_nav=True)

@app.route('/chat/<receiver>', methods=['GET', 'POST'])
def chat(receiver):
    if 'user_id' not in session: return redirect(url_for('login'))
    sender = session['user_id']
    room = "-".join(sorted([sender, receiver]))
    if room not in CHATS: CHATS[room] = []
    if request.method == 'POST':
        msg = request.form.get('message')
        if msg: CHATS[room].append({"sender": sender, "text": msg})
    msg_list_html = ""
    for m in CHATS[room]:
        align = "flex-end" if m['sender'] == sender else "flex-start"
        bg = "#3797f0" if m['sender'] == sender else "#262626"
        msg_list_html += f'<div style="align-self: {align}; background: {bg}; padding: 10px; border-radius: 10px; max-width: 70%;">{m["text"]}</div>'
    html = f'<h2>Chat with @{receiver}</h2><div style="height:250px; overflow-y:auto; display:flex; flex-direction:column; gap:10px; background:#121212; padding:10px;">{msg_list_html}</div><form method="POST" style="display:flex; gap:10px;"><input type="text" name="message" class="input-field" style="margin:0;"><button type="submit" class="btn" style="width:auto; margin:0;">Send</button></form>'
    return render_m_page(html, show_nav=True)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

