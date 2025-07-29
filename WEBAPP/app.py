from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = 'secret123'

# Konfigurasi Database - GANTI PASSWORD ANDA DI SINI!
DB_CONFIG = {
    'host': 'localhost',
    'database': 'webapp_db',
    'user': 'postgres',
    'password': 'zaramyst',
    'port': '5432'
}

def get_db_connection():
    """Membuat koneksi ke database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

def create_tables():
    """Membuat tabel jika belum ada"""
    conn = get_db_connection()
    if conn:
        try:
            cur = conn.cursor()
            
            # Buat tabel users
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Buat tabel posts
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT NOT NULL,
                    author VARCHAR(100) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            print("Tabel berhasil dibuat!")
        except Exception as e:
            print(f"Error creating tables: {e}")
        finally:
            cur.close()
            conn.close()

@app.route('/')
def home():
    """Halaman Home"""
    conn = get_db_connection()
    posts = []
    
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT 5")
            posts = cur.fetchall()
        except Exception as e:
            print(f"Error fetching posts: {e}")
        finally:
            cur.close()
            conn.close()
    
    return render_template('home.html', posts=posts)

@app.route('/users', methods=['GET', 'POST'])
def users():
    """Halaman Users"""
    conn = get_db_connection()
    users_list = []
    
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        
        if name and email and conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s)",
                    (name, email)
                )
                conn.commit()
                flash('User berhasil ditambahkan!', 'success')
            except psycopg2.IntegrityError:
                flash('Email sudah ada!', 'error')
            except Exception as e:
                flash(f'Terjadi error: {e}', 'error')
            finally:
                cur.close()
    
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM users ORDER BY created_at DESC")
            users_list = cur.fetchall()
        except Exception as e:
            print(f"Error fetching users: {e}")
        finally:
            cur.close()
            conn.close()
    
    return render_template('users.html', users=users_list)

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    """Halaman Posts"""
    conn = get_db_connection()
    posts_list = []
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')
        
        if title and content and author and conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    """INSERT INTO posts (title, content, author)
                    VALUES (%s, %s, %s)""",
                    (title, content, author)
                )
                conn.commit()
                flash('Post berhasil ditambahkan!', 'success')
            except Exception as e:
                flash(f'Terjadi error: {e}', 'error')
            finally:
                cur.close()
    
    if conn:
        try:
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("SELECT * FROM posts ORDER BY created_at DESC")
            posts_list = cur.fetchall()
        except Exception as e:
            print(f"Error fetching posts: {e}")
        finally:
            cur.close()
            conn.close()
    
    return render_template('posts.html', posts=posts_list)

if __name__ == '__main__':
    create_tables()
    print("Server berjalan di http://localhost:5000")
    app.run(debug=True)
