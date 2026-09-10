import json
import random
import string
from flask import Flask, redirect, render_template, request, session, url_for, send_from_directory

app = Flask(__name__)

@app.route('/sw.js')
def serve_sw():
    return send_from_directory('.', 'sw.js')

# Clave secreta necesaria para manejar sesiones seguras en Flask
app.secret_key = 'mirch_secreto_super_seguro'

# CONTRASEÑA DE TU PANEL (Puedes cambiar 'mi_password123' por la clave que tú quieras)
ADMIN_PASSWORD = 'mi_password123'

ARCHIVO_ENLACES = '/home/mirchhub/mysite/enlaces.json'

def cargar_enlaces():
    try:
        with open(ARCHIVO_ENLACES, 'r') as f:
            return json.load(f)
    except:
        return {}

def guardar_enlace(codigo, url):
    enlaces = cargar_enlaces()
    enlaces[codigo] = url
    with open(ARCHIVO_ENLACES, 'w') as f:
        json.dump(enlaces, f, indent=4)

@app.route('/')
def inicio():
    return redirect('/admin')

@app.route('/ver/<codigo>')
def ver_hub(codigo):
    enlaces = cargar_enlaces()
    destino_real = enlaces.get(codigo, 'https://google.com')
    return render_template('mirch_acortador.html', enlace_destino=destino_real)

# PANTALLA DE LOGIN PARA EL ADMIN
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
            <div class="error">{{error}}</div>
        </div>
    </body>
    </html>
    """

# PANEL DE CONTROL CON HISTORIAL Y SEGURIDAD
@app.route('/admin', methods=['GET', 'POST'])
def panel_admin():
    # Si no ha iniciado sesión, lo mandamos al login
    if not session.get('autenticado'):
        return redirect('/login')

    mensaje = ""
    enlace_generado = ""

    if request.method == 'POST':
        url_acortada = request.form.get('url')
        if url_acortada:
            codigo_nuevo = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            guardar_enlace(codigo_nuevo, url_acortada)
            enlace_generado = f"https://mirchhub.pythonanywhere.com/ver/{{codigo_nuevo}}"
            mensaje = "¡Enlace registrado con éxito!"

    enlaces = cargar_enlaces()

    # Construimos la tabla con el historial de enlaces
    filas_tabla = ""
    for codigo, url in list(enlaces.items()):
        link_completo = f"https://mirchhub.pythonanywhere.com/ver/{{codigo}}"
        filas_tabla += f"""
        <tr>
            <td style="padding: 10px; border-bottom: 1px solid #30363d; font-family: monospace; color: #7ee787;">/ver/{{codigo}}</td>
            <td style="padding: 10px; border-bottom: 1px solid #30363d; word-break: break-all; color: #8b949e;"><a href="{{url}}" target="_blank" style="color: #58a6ff; text-decoration: none;">{{url}}</a></td>
            <td style="padding: 10px; border-bottom: 1px solid #30363d;"><input type="text" value="{{link_completo}}" readonly style="background: #0d1117; color: #c9d1d9; border: 1px solid #30363d; padding: 5px; border-radius: 3px; font-size: 11px; width: 180px;" onclick="this.select();"></td>
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
                    <strong>{{mensaje}}</strong><br><br>
                    Copia este enlace para tus videos/Telegram:<br>
                    <div class="link-box">{{enlace_generado}}</div>
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
          
