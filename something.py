import re
import requests
import nest_asyncio


import pyromod.listen

from requests_html import HTMLSession
from pyrogram import Client, filters, idle




pbot = Client(
    'mu_mai_lele_bc', 
    api_id = 19500615,
    api_hash = '7ee1d55d072add75a01e617fc0cef635',
    bot_token = '5832903711:AAEc3OWGarirPSDurWqv-xfNc6wun1oXMxU'
)
ACCESS = [5649200762, 5022574807]

def access(f):
    async def wrapper(bot, m):
        if m.from_user.id not in ACCESS:
            return await m.reply("**You don't have access to use this bot\n\nMessage @BotsExpert or @Xotic69 to grant you access\n\n||@ViolenceChitChat , @TEACH_TEAMOP|| **")
        return await f(bot, m)
    return wrapper

def getHTML(url):
    session = HTMLSession()
    response = session.get(url)

    #thanks to stackoverflow, helped in fixing a rare error.
    #await response.html.arender(timeout=30)


    html = response.html.html
    if "Something went wrong" in html or "You might be having a network connection problem, the link might be expired, or the payment provider cannot be reached at the moment." in html:
        return None
    else:
        return html

def getPK(html):
    regex="pk_live_[0-9a-zA-Z]{99}|pk_live_[0-9a-zA-Z]{34}|pk_live_[0-9a-zA-Z]{24}"
    try:
        return re.findall(regex, html)[0]
    except Exception as e:
        return "Not Found"

def getCS(data):
    regex="cs_live_[0-9a-zA-Z]{58}"
    try:
        return re.findall(regex, data)[0]
    except:
        return "Not Found"

def getRawData(pk, cs):
    h={
    "Host": "api.stripe.com",
    "sec-ch-ua": "\"Chromium\";v\u003d\"112\", \"Google Chrome\";v\u003d\"112\", \"Not:A-Brand\";v\u003d\"99\"",
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "dnt": "1",
    "sec-ch-ua-mobile": "?1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": "\"Android\"",
    "origin": "https://checkout.stripe.com",
    "sec-fetch-site": "same-site",
    "sec-fetch-mode": "cors",
    "sec-fetch-dest": "empty",
    "referer": "https://checkout.stripe.com/",
    "accept-language": "en-IN,en-GB;q\u003d0.9,en-US;q\u003d0.8,en;q\u003d0.7,hi;q\u003d0.6"
    }
    data=f"key={pk}&eid=NA&browser_locale=en-IN&redirect_type=url"
    url=f"https://api.stripe.com/v1/payment_pages/{cs}/init"
    req=requests.post(url, data=data, headers=h)
    if req.status_code==200:
        return req.json()
    return None

def getEmail(raw):
    email=raw.get("customer_email", "Not Found")
    return str(email)

def getAmt(raw):
    try:
        amt=raw.get("line_item_group", {}).get("line_items", [{}])[0].get("total", "Not Found")
        return str(amt)
    except:
        return "Not Found"

def getCurrency(raw):
    try:
        
        
        c=raw.get("line_item_group", {}).get("currency", "Not Found")
        return c
    except:
        return "Not Found"


@pbot.on_message(filters.command('start'))
@access
async def stc(bot, m):
    await m.reply('**This is a Simple Checkout grabber bot**\n\n★ No fully Completed yet so u can see some errors report it at @ViolenceChitChat , @TEACH_TEAMOP .')

@pbot.on_message(filters.command('grab'))
@access
async def main_func(bot, m):
    url = await m.chat.ask('Send Your checkout link: ')
    html = getHTML(url.text)
    if html == None:
        await m.reply("Session Expire hogya vai abb tu rr krle but yaha nahi kahi or jaake kr rr...")
        return
    pk = getPK(html)
    cs = getCS(url)
    raw = getRawData(pk, cs)
    await m.reply(f"Lele details tu b kya yaad rakhega:\n\nPK: {pk}\nCS: {cs}\n\nAMT: {getAmt(raw)}\nCurrency: {getCurrency(raw)}")


async def main():
    await pbot.start()
    print('\033[33mBot start hogya vai\033[0m')
    await idle()
    await pbot.stop()
    print('\033[32mAlvida vai\033[0m')

pbot.run(main())