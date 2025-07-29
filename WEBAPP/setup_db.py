import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def setup_database():
    """Setup database webapp_db"""
    print("Memulai setup database...")
    
    try:
        # Koneksi ke PostgreSQL (tanpa database spesifik)
        conn = psycopg2.connect(
            host='localhost',
            user='postgres',
            password='password_anda',  # Ganti dengan password PostgreSQL Anda
            port='5432'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        # Cek apakah database sudah ada
        cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'webapp_db'")
        exists = cur.fetchone()

        if not exists:
            cur.execute('CREATE DATABASE webapp_db')
            print("Database 'webapp_db' berhasil dibuat!")
        else:
            print("ℹDatabase 'webapp_db' sudah ada.")

        cur.close()
        conn.close()
        return True

    except Exception as e:
        print(f"Error: {e}")
        print("Pastikan:")
        print(" - PostgreSQL sudah berjalan")
        print(" - Password sudah benar")
        print(" - Port 5432 terbuka")
        return False

if __name__ == '__main__':
    print("=" * 40)
    print(" SETUP DATABASE UNTUK WEB APP FLASK")
    print("=" * 40)
    
    if setup_database():
        print("\nSetup selesai!")
        print("Sekarang jalankan: python app.py")
    else:
        print("\nSetup gagal")
    
    input("\nTekan Enter untuk keluar...")