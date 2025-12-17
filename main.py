import flask
import sqlite3
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = flask.Flask(
    __name__,
    static_folder="static",
    static_url_path="/"
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["20 per day"],
    storage_uri="memory://",
)

conn = sqlite3.connect('gifts.db') 
cursor = conn.cursor()  
cursor.execute('''
    CREATE TABLE IF NOT EXISTS gifts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        gift TEXT NOT NULL,
        complete INTEGER NOT NULL DEFAULT 0
    )
''')
conn.commit()  
conn.close()

@app.get("/")
def index():
    return flask.send_from_directory("static", "index.html")

@app.post("/gifts/complete/<int:gift_id>")
def complete_gift(gift_id):
    """
    Marks a gift as complete (sets 'complete' to 1) based on its ID.
    """
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()

    try:
        cursor.execute(
            'UPDATE gifts SET complete = 1 WHERE id = ?', 
            (gift_id,)
        )
        conn.commit()
        
        if cursor.rowcount == 0:
            conn.close()
            return 'Gift ID not found', 404
        
        conn.close()
        return '', 204
        
    except sqlite3.Error as e:
        conn.close()
        print(f"Database error during update: {e}")
        return 'Internal Server Error', 500

@app.post("/gifts")
def create_gift():
    data = flask.request.get_json()
    name = data.get('name')
    gift = data.get('gift')
    
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO gifts (name, gift) VALUES (?, ?)', (name, gift))
    conn.commit()
    conn.close()

    return '', 201
    
@app.get("/gifts")
def get_gifts():
    conn = sqlite3.connect('gifts.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, gift, complete FROM gifts')
    rows = cursor.fetchall()
    conn.close()
    
    gifts = [{'id': row[0], 'name': row[1], 'gift': row[2], 'complete': row[3]} for row in rows]
    return flask.jsonify(gifts)

if __name__ == "__main__":
    app.run()