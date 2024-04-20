import datetime
import hashlib
import hmac
import json
import traceback

import requests
import stripe
from flask import Flask, Response, jsonify, request

from utils.supabase_auth import SupabaseClient

endpoint_secret = "whsec_9oDunt9S7M9Vd8TwLlOx5I5xrwapNwRg"
stripe.api_key = "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"
SELLER_KEY = "f6386c16787e0eb51b24d168205267e6"
endpoint_secret = ""
tiers = {
    "plink_1NUTSTHSUSFhHVtR6TH6AGUS": "tier1",
    "plink_1OYTBEHSUSFhHVtRtxVu5EGL": "tier2",
    "plink_1OYTJMHSUSFhHVtRTQ9TLgxH": "tier3",
    "plink_1OYTKHHSUSFhHVtRvaq7l78T": "tier4",
    "64f503ef5cb73": "tier1",
    "65a3dc5232bac": "tier2",
    "65a3dc548727a": "tier3",
    "65a3dc5913f70": "tier4",
}


application = Flask(__name__)


@application.route("/webhook", methods=["POST"])
def webhook():
    try:
        s = SupabaseClient()
    except Exception as e:
        return Response(response=str(e), status=500, mimetype='application/json')
    event = None
    payload = request.data
    try:
        event = json.loads(payload)
        print(event)
    except Exception as e:
        print("⚠️  Webhook error while parsing basic request." + str(e))
        return Response(response="Webhook error while parsing basic request." + str(e), status=400, mimetype='application/json')
    if endpoint_secret:
        sig_header = request.headers.get("stripe-signature")
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
        except stripe.error.SignatureVerificationError as e:
            print("⚠️  Webhook signature verification failed." + str(e))
            return Response(response="Webhook signature verification failed." + str(e), status=400, mimetype='application/json')

    # Handle the event
    if event and event["type"] == "checkout.session.completed":
        try:
            payment_intent = event["data"]["object"]
            email = payment_intent["customer_details"]["email"]
            tier = tiers[payment_intent["payment_link"]]

            data, count = s.client.table("users").select("*").eq("email", email).execute()
            if len(data[1]) == 0:
                password = payment_intent["custom_fields"][0]["text"]["value"]

                s.client.auth.sign_up(
                    {
                        "email": email,
                        "password": password,
                    }
                )
                data, count = s.client.table("users").select("*").eq("email", email).execute()

            user = data[1][0]

            s.client.rpc("create_subscription", {"user_id": user["user_id"], "tier": tier, "days": 30}).execute()

        except Exception as e:
            return Response(response=str(e), status=400, mimetype='application/json')
    else:
        return Response(response="Wrong event", status=400, mimetype='application/json')
    return Response(response="Success", status=200, mimetype='application/json')


@application.route("/webhook/sellix", methods=["POST"])
def sellix_webhook():
    s = SupabaseClient()
    try:
        payload = request.data
        secret = b"aBUy0rbb9PZlmZHxRE9x7Dtux1lPxYkI"  # Replace with your webhook secret

        header_signature = request.headers["X-Sellix-Signature"]  # get our signature header
        # depending on your server configuration, you might need to use the X-Sellix-Unescaped-Signature header instead

        signature = hmac.new(secret, payload, hashlib.sha512).hexdigest()

        if not hmac.compare_digest(signature, header_signature):
            # Invalid webhook
            return Response(response="Webhook signature verification failed.", status=400, mimetype='application/json')

        # Parse the JSON payload
        webhook_data = json.loads(payload)

        if not (webhook_data["event"] == "order:paid"):
            return Response(response="Wrong event", status=400, mimetype='application/json')

        data = webhook_data.get("data", {})
        # Extract custom fields from the webhook data
        custom_fields = data.get("custom_fields", {})

        email = data.get("customer_email")
        password = custom_fields.get("password", None)
        tier = tiers[data.get("product_id")]

        data, count = s.client.table("users").select("*").eq("email", email).execute()

        if len(data[1]) == 0:
            s.client.auth.sign_up(
                {
                    "email": email,
                    "password": password,
                }
            )
            data, count = s.client.table("users").select("*").eq("email", email).execute()

        user = data[1][0]

        s.client.rpc("create_subscription", {"user_id": user["user_id"], "tier": tier, "days": 30}).execute()
    except Exception as e:
        return Response(response=str(e), status=400, mimetype='application/json')
    return Response(response="Success", status=200, mimetype='application/json')

@application.route("/")
def home():
    return f"Hello world ! {datetime.datetime.now()}"


if __name__ == "__main__":
    application.run(port=5001)
