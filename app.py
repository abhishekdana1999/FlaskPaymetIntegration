import os

from flask import Flask, render_template, jsonify , request
import stripe

import json
import razorpay
client = razorpay.Client(auth=("rzp_test_mXt5GN9PYG3INt", "lMFDCTUWoO0HcRaUUKN5Nr1i"))

stripePubKey="pk_test_51IBXvrHFlaZskmdtXXHAzgxBDTxDLe6Xzshtnwu7LB6GdFgsDsT34RW7tatGdm5QXb6Pflfw7k3QKlokcor9cg2500RewOpC4q"
stripeSecKey="sk_test_51IBXvrHFlaZskmdtwtBXMvDFA95iY2fPaQiHmPPSAqDS4FkcvKrM5yt3BWLf0qQSImFNHKcvT9yMdC1aADNjKqhs00JKAkXA5W"


app = Flask(__name__)

stripe_keys = {
  'secret_key': stripeSecKey,
  'publishable_key': stripePubKey
}

stripe.api_key = stripe_keys['secret_key']


@app.route('/')
def index():
    return render_template('index.html',key=stripe_keys['publishable_key'] , razorPayKey="rzp_test_mXt5GN9PYG3INt")

@app.route('/checkout', methods=['POST'])
def checkout():

    amount = 500

    customer = stripe.Customer.create(
        email='sample@customer.com',
        source=request.form['stripeToken']
    )

    stripe.Charge.create(
        customer=customer.id,
        amount=amount,
        currency='usd',
        description='Flask Charge'
    )

    return render_template('checkout.html', amount=amount)

@app.route('/razorpay', methods=['POST'])
def app_charge():
    amount = 5100
    payment_id = request.form['razorpay_payment_id']
    client.payment.capture(payment_id, amount)
    return json.dumps(client.payment.fetch(payment_id))


if __name__ == '__main__':
    app.run(debug=True)