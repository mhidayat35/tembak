# app.py
# Server ini bertugas untuk menerima permintaan dari website,
# menjalankan script main.py, dan mengirimkan hasilnya kembali.
from flask import Flask, jsonify
from flask_cors import CORS
import subprocess

# Inisialisasi aplikasi Flask
app = Flask(__name__)
# Mengizinkan permintaan dari sumber lain (penting agar HTML bisa berkomunikasi)
CORS(app)

@app.route('/run', methods=['GET'])
def run_script():
    """
    Endpoint API yang akan diakses oleh website.
    Saat diakses, ia akan menjalankan `main.py` sebagai proses terpisah.
    """
    try:
        # Menjalankan script main.py menggunakan subprocess
        # Ini adalah cara yang aman untuk menjalankan script eksternal.
        # 'python' bisa diganti dengan 'python3' tergantung sistem Anda.
        result = subprocess.run(
            ['python', 'main.py'],
            capture_output=True,
            text=True,
            check=True,  # Akan error jika script gagal
            encoding='utf-8' # Memastikan encoding yang benar
        )
        
        # Mengambil output dari standar output script
        # Kita memotong bagian "OUTPUT UNTUK WEBSITE" yang kita buat di main.py
        output_text = result.stdout.split("--- OUTPUT UNTUK WEBSITE ---")[-1].strip()
        
        # Mengirim output kembali ke browser dalam format JSON
        return jsonify({'output': output_text})

    except subprocess.CalledProcessError as e:
        # Jika terjadi error saat menjalankan script
        error_message = f"Error saat menjalankan script:\n{e.stderr}"
        return jsonify({'error': error_message}), 500
    except FileNotFoundError:
        # Jika command 'python' tidak ditemukan
        return jsonify({'error': "Perintah 'python' tidak ditemukan. Pastikan Python terinstall dan ada di PATH."}), 500
    except Exception as e:
        # Menangani error lainnya
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Menjalankan server di http://127.0.0.1:5000
    # debug=True agar server otomatis restart jika ada perubahan kode
    app.run(debug=True, port=5000)

