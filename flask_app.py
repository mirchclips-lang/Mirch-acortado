import json
import random
import os
import string
from flask import Flask, redirect, render_template_string, request, session, url_for, send_from_directory

app = Flask(__name__)

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

app.secret_key = 'mirch_secreto_super_seguro'
ADMIN_PASSWORD = 'mi_password123'

# Usamos una ruta absoluta basada en la carpeta actual del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ENLACES = os.path.join(BASE_DIR, 'enlaces.json')

def cargar_enlaces():
    if not os.path.exists(ARCHIVO_ENLACES):
        return {}
    try:
        with open(ARCHIVO_ENLACES, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar: {e}")
        return {}

def guardar_enlace(codigo, url):
    enlaces = cargar_enlaces()
    enlaces[codigo] = url
    try:
        with open(ARCHIVO_ENLACES, 'w', encoding='utf-8') as f:
            json.dump(enlaces, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error al guardar: {e}")

@app.route('/')
def inicio():
    return redirect('/admin')

# RUTA DEL ACORTADOR CON CONTADOR Y CLICS DE MONETAG
@app.route('/ver/<codigo>')
def ver_hub(codigo):
    enlaces = cargar_enlaces()
    destino_real = enlaces.get(codigo, 'https://google.com')
    
    html_acortador = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Continuar a tu enlace - Mirch Hub</title>
        <!-- Anuncio Push Monetag -->
        <script>(function(s){s.dataset.zone='11770371',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>
        <style>
            body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; text-align: center; padding: 50px; }}
            .card {{ background: #161b22; padding: 30px; border-radius: 10px; border: 1px solid #30363d; display: inline-block; max-width: 450px; width: 100%; box-sizing: border-box; }}
            h2 {{ color: #58a6ff; margin-top: 0; }}
            .btn {{ background: #238636; color: #fff; padding: 14px 20px; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; font-size: 16px; text-decoration: none; display: inline-block; box-sizing: border-box; margin-top: 15px; }}
            .btn:hover {{ background: #2ea043; }}
            .contador {{ font-size: 24px; font-weight: bold; color: #7ee787; margin: 20px 0; }}
            .info {{ color: #8b949e; font-size: 13px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Preparando tu enlace</h2>
            <p>Por favor, espera unos segundos para continuar...</p>
            
            <div id="contador-box">
                <div class="contador" id="timer">5</div>
            </div>

            <!-- Botón de continuar que abrirá la publicidad de Monetag -->
            <button id="btnContinuar" class="btn" style="display:none;" onclick="manejarClic()">Esperando...</button>
            
            <div class="info" id="info-clicks">Completa los pasos para desbloquear tu destino.</div>
        </div>

        <script>
            const urlPublicidad = "https://omg10.com/4/11770422";
            const enlaceDestino = "{destino_real}";
            
            let clicsRequeridos = 3; 
            let clicsActuales = 0;
            
            let segundos = 5;
            const timerElement = document.getElementById('timer');
            const contadorBox = document.getElementById('contador-box');
            const btn = document.getElementById('btnContinuar');
            const infoClicks = document.getElementById('info-clicks');

            let cuentaRegresiva = setInterval(function() {{
                segundos--;
                if (segundos > 0) {{
                    timerElement.innerText = segundos;
                }} else {{
                    clearInterval(cuentaRegresiva);
                    contadorBox.style.display = "none";
                    btn.style.display = "block";
                    btn.innerText = "Continuar (" + (clicsRequeridos - clicsActuales) + " restantes)";
                }}
            }}, 1000);

            function manejarClic() {{
                clicsActuales++;
                window.open(urlPublicidad, '_blank');

                if (clicsActuales < clicsRequeridos) {{
                    let restantes = clicsRequeridos - clicsActuales;
                    btn.innerText = "Continuar (" + restantes + " restantes)";
                    infoClicks.innerText = "Faltan " + restantes + " pasos para desbloquear.";
                }} else {{
                    btn.innerText = "¡Redirigiendo...";
                    btn.style.background = "#1f6feb";
                    infoClicks.innerText = "¡Listo! Abriendo tu destino...";
                    setTimeout(function() {{
                        window.location.href = enlaceDestino;
                    }}, 1000);
                }}
            }}
        </script>
    </body>
    </html>
    """
    return render_template_string(html_acortador)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['autenticado'] = True
            return redirect('/admin')
        else:
            error = "Contraseña incorrecta"

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login - Mirch Hub</title>
        <script>(function(s){s.dataset.zone='11770371',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>
        <style>
            body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; text-align: center; padding: 60px; }}
            .card {{ background: #161b22; padding: 30px; border-radius: 10px; display: inline-block; border: 1px solid #30363d; max-width: 400px; width: 100%; box-sizing: border-box; }}
            input[type="password"] {{ width: 100%; padding: 12px; margin: 15px 0; background: #0d1117; border: 1px solid #484f58; color: #fff; border-radius: 5px; box-sizing: border-box; }}
            button {{ background: #58a6ff; color: #0d1117; padding: 12px 20px; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; }}
            button:hover {{ background: #79b8ff; }}
            .error {{ color: #f85149; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Acceso Restringido</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Contraseña de Administrador" required>
                <button type="submit">Entrar al Panel</button>
            </form>
            <div class="error">{error}</div>
        </div>
    </body>
    </html>
    """

@app.route('/admin', methods=['GET', 'POST'])
def panel_admin():
    if not session.get('autenticado'):
        return redirect('/login')

    mensaje = ""
    enlace_generado = ""

    if request.method == 'POST':
        url_acortada = request.form.get('url')
        if url_acortada:
            codigo_nuevo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            guardar_enlace(codigo_nuevo, url_acortada)
            enlace_generado = f"https://mirchservice.xyz/ver/{codigo_nuevo}"
            mensaje = "¡Enlace registrado con éxito!"

    enlaces = cargar_enlaces()

    filas_tabla = ""
    for codigo, url in list(enlaces.items()):
        link_completo = f"https://mirchservice.xyz/ver/{codigo}"
        filas_tabla += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #30363d; font-family: monospace; color: #7ee787;">/ver/{codigo}</td>
            <td style="padding: 10px; border-bottom: 1px solid #30363d; word-break: break-all; color: #8b949e;"><a href="{url}" target="_blank" style="color: #58a6ff; text-decoration: none;">{url}</a></td>
            <td style="padding: 10px; border-bottom: 1px solid #30363d;"><input type="text" value="{link_completo}" readonly style="background: #0d1117; color: #c9d1d9; border: 1px solid #30363d; padding: 5px; border-radius: 3px; font-size: 11px; width: 180px;" onclick="this.select();"></td>
        </tr>
        """

    if not filas_tabla:
        filas_tabla = '<tr><td colspan="3" style="padding: 15px; text-align: center; color: #8b949e;">Aún no hay enlaces creados.</td></tr>'

    html_resultado = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Panel Admin - Mirch Hub</title>
        <script>(function(s){s.dataset.zone='11770371',s.src='https://nap5k.com/tag.min.js'})([document.documentElement, document.body].filter(Boolean).pop().appendChild(document.createElement('script')))</script>
        <style>
            body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; text-align: center; padding: 20px; }}
            .container {{ max-width: 700px; margin: 0 auto; }}
            .card {{ background: #161b22; padding: 20px; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 20px; text-align: left; box-sizing: border-box; }}
            input[type="text"] {{ width: 100%; padding: 12px; margin: 10px 0; background: #0d1117; border: 1px solid #484f58; color: #fff; border-radius: 5px; box-sizing: border-box; }}
            button {{ background: #58a6ff; color: #0d1117; padding: 12px 20px; border: none; font-weight: bold; border-radius: 5px; cursor: pointer; width: 100%; }}
            button:hover {{ background: #79b8ff; }}
            .result {{ background: #21262d; padding: 15px; margin-top: 15px; border-radius: 5px; color: #58a6ff; }}
            .link-box {{ background: #0d1117; color: #7ee787; padding: 10px; border-radius: 5px; word-break: break-all; font-family: monospace; font-size: 14px; user-select: all; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 13px; }}
            th {{ background: #21262d; padding: 10px; text-align: left; border-bottom: 1px solid #30363d; color: #c9d1d9; }}
            .logout {{ float: right; color: #f85149; text-decoration: none; font-size: 13px; font-weight: bold; }}
            .logout:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="card">
                <a href="/login" class="logout">Cerrar Sesión</a>
                <h2 style="margin-top: 0;">Panel Admin - Mirch Hub</h2>
                <form method="POST">
                    <label style="font-size: 13px; color: #8b949e;">Pega tu link acortador:</label>
                    <input type="text" name="url" placeholder="Ej: https://ouo.io/..." required>
                    <button type="submit">Generar Enlace para Compartir</button>
                </form>
    """

    if mensaje:
        html_resultado += f"""
                <div class="result">
                    <strong>{mensaje}</strong><br><br>
                    Copia este enlace para tus videos/Telegram:<br>
                    <div class="link-box">{enlace_generado}</div>
                </div>
        """

    html_resultado += f"""
            </div>

            <div class="card">
                <h3 style="margin-top: 0;">Historial de Enlaces Creados</h3>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>Código</th>
                                <th>Destino (Acortador)</th>
                                <th>Link para Compartir</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filas_tabla}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_resultado

if __name__ == '__main__':
    app.run(debug=True)
