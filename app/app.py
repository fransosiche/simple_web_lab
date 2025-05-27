from flask import Flask, render_template, request, jsonify, make_response
import subprocess
import os
import threading
import json

# Créer les deux applications Flask avec le bon chemin de templates
app = Flask(__name__, 
    template_folder='../templates'
)
fake_app = Flask(__name__)

# Middleware pour ajouter des en-têtes révélateurs
@app.after_request
def add_headers(response):
    response.headers['Server'] = 'Werkzeug/2.0.1 Python/3.9.0'
    response.headers['X-Powered-By'] = 'Flask'
    return response

# Routes pour l'application vulnérable (port 45678)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        return "Message envoyé ! (Simulation)"
    return render_template('contact.html')

# Routes pour le dossier devtools
@app.route('/devtools')
def devtools():
    response = make_response("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>418 - I'm a teapot</title>
        <style>
            body {
                font-family: monospace;
                background: #000;
                color: #0f0;
                margin: 40px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
            .matrix {
                font-size: 12px;
                line-height: 1;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="matrix">
                ERROR: SYSTEM COMPROMISED
                WARNING: UNAUTHORIZED ACCESS
                ALERT: SECURITY BREACH DETECTED
                INITIATING SELF-DESTRUCT SEQUENCE
                ABORT? (Y/N)
            </div>
        </div>
    </body>
    </html>
    """)
    response.status_code = 418
    return response

@app.route('/devtools/logs')
def devtools_logs():
    return "Logs système (accès restreint)"

@app.route('/devtools/stats')
def devtools_stats():
    return "Statistiques système (accès restreint)"

@app.route('/devtools/config')
def devtools_config():
    return "Configuration système (accès restreint)"

# internal backdoor – debug only
@app.route('/devtools/debug', methods=['GET', 'POST'])
def debug_api():
    if request.method == 'GET':
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Debug Interface</title>
            <style>
                body { font-family: monospace; margin: 40px; }
                .container { max-width: 800px; margin: 0 auto; }
                .error { color: red; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Debug Interface</h1>
                <p class="error">Cette interface est réservée aux administrateurs.</p>
                <p>Veuillez vous connecter pour continuer.</p>
            </div>
        </body>
        </html>
        """
    
    cmd = request.form.get('cmd', '')
    if not cmd:
        return "Debug API Ready. Plz provide cmd command"
    
    # Nettoyer la commande des retours à la ligne et espaces
    cmd = cmd.strip()
    
    # Vérifier si la commande est dans la liste blanche
    allowed_commands = ['ping', 'traceroute', 'netstat', 'ps']
    if any(cmd.startswith(c) for c in allowed_commands):
        try:
            result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
            return result.decode('utf-8')
        except Exception as e:
            error_msg = str(e)
            if "No such file or directory" in error_msg:
                return f"Erreur: Commande non trouvée. Il faut utiliser ping ou traceroute ou ps ou netstat: {error_msg}"
            return f"Erreur d'exécution: {error_msg}"
    else:
        return "Commande non autorisée. Vérifiez la liste des commandes autorisées dans le code source."

# Routes pour le faux site (port 80)
@fake_app.route('/')
def fake_home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bienvenue</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                line-height: 1.6;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Bienvenue sur notre site</h1>
            <p>Ce site est en maintenance. Veuillez revenir plus tard.</p>
        </div>
    </body>
    </html>
    """

def run_fake_app():
    fake_app.run(host='0.0.0.0', port=80, debug=False, use_reloader=False)

def run_main_app():
    app.run(host='0.0.0.0', port=45678, debug=False, use_reloader=False)

if __name__ == '__main__':
    # Démarrer le faux site sur le port 80 dans un thread séparé
    fake_thread = threading.Thread(target=run_fake_app, daemon=True)
    fake_thread.start()
    
    # Démarrer l'application vulnérable sur le port 45678
    run_main_app() 