from flask import Flask, request, jsonify
from supabase import create_client, Client
import os

app = Flask(__name__)

# ===============================
# Configuración de Supabase
# ===============================
# 👇 Reemplaza con tu URL y KEY de Supabase
SUPABASE_URL = "https://TU_URL.supabase.co"
SUPABASE_KEY = "TU_API_KEY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ===============================
# Rutas de prueba
# ===============================

@app.route("/")
def home():
    return "✅ API Flask con Supabase funcionando!"

@app.route("/insert", methods=["POST"])
def insert():
    try:
        data = request.json  # espera un JSON
        response = supabase.table("test").insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get", methods=["GET"])
def get_data():
    try:
        response = supabase.table("test").select("*").execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ===============================
# Run Flask
# ===============================
if __name__ == "__main__":
    app.run(debug=True)

