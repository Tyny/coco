import requests


def send_email(text, mail):

    url = "https://api.sendinblue.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Correntosa Mutual",
            "email": "lacorrentosa@gmail.com"
        },
        "to": [
            {
                "email": mail
            }
        ],
        "textContent" : text,
        "subject": "Compras Comunitarias"
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": "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"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)


def check_sended_mails():
    url = "https://api.sendinblue.com/v3/smtp/statistics/aggregatedReport?days=1"

    headers = {
        "accept": "application/json",
        "api-key": "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"
    }

    response = requests.get(url, headers=headers)

    return response.json()


def send_email_template(text, mail, month):
    url = "https://api.sendinblue.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "La Correntosa",
            "email": "lacorrentosa@gmail.com"
        },
        "to": [
            {
                "email": mail,
                "name": "José"
            }
        ],
        "params": {"DETALLECOMPRA": text},
        "templateId": 7,
        "subject": "🌊 Confirmación Compra Comunitaria " + month + " 🌊"
    } 
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": "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"
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
