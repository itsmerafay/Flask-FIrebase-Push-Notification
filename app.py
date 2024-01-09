import firebase_admin
from firebase_admin import credentials, messaging
from flask import Flask, request , jsonify
import requests


app = Flask(__name__)

# cred = credentials.Certificate("C:\Users\DC\Desktop\firebase_flask\serviceAccountKey.json")
# cred = credentials.Certificate(r"C:\Users\DC\Desktop\firebase_flask\serviceAccountKey.json")
# firebase_admin.initialize_app(cred)

cred = credentials.Certificate(r"C:\Users\DC\Desktop\firebase_flask\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def send_push_notification(device_token, title , body ,dataObject=None):

    message=messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            token=device_token
    )


    server_key = "AAAAjpiSpo0:APA91bE_l9U32oLs0n41GK1vcYGcPKqcWBzF8nv4QskBf90eXXMX3khOo-l1IXnnsCKURjlAgZKQlqcdthiZntMnTEWCvfvcLvU_52S7LJfqSxQm_yx4FNdVYV2W56e5Rpb-PLg0nGY-"

    headers = {
        "Authorization": f"key={server_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "notification": {
            "title": title,
            "body": body
        },
        "to": device_token
    }

    try:
        response = requests.post("https://fcm.googleapis.com/fcm/send", headers=headers, json=payload)
        print("Message sent successfully !!", response.json())
        return True
    except Exception as e:
        print("Error in handling the error ", e)
        return False


@app.route('/send_notification', methods=['POST'])
def send_notification():
    data = request.get_json()
    device_token = data.get("device_token")
    title = data.get("title")
    body = data.get("body")

    if not all([device_token, title, body]):
        return jsonify({
            "status":False,
            "message": "Missing parameters !!"
        }), 400
    
    success = send_push_notification(device_token, title , body)

    if success:
        return jsonify({
            "status":True,
            "message": "Message sent successfully!!"
        }), 200
    else:
        return jsonify({
            "status":False,
            "message": "Failed to send notifications !!"
        }), 500


if __name__ == '__main__':
    app.run(debug=True)
