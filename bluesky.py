import tweepy
import twitter
import requests
import os
import telebot
import urllib.parse
import time
import threading
import schedule
import subprocess
import datetime
from collections import defaultdict, deque
from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random
from atproto import Client, models
import io
import re

client = Client()
client.login('xxxxxxx.bsky.social','xxxx-xxxx-xxxx-xxxx')

# Twitter API keys
api_key = "xxxxxxxxxxxxxx"
api_secrets = "xxxxxxxxxxxxxxx"
access_token = "xxxxxxxxxxxxxxxx"
access_secret = "xxxxxxxxxxxxxxxxx"
bearer_token = "xxxxxxxxxxxxxxxxxxxxxxxx"

 # Authenticate to Twitter API V2.0
tweety = tweepy.Client(
     consumer_key="xxxxxxxxxxxxx",
     consumer_secret="xxxxxxxxxxxxxxxxx",
     access_token="xxxxxxxxxxxxxxxxxxxxx",
     access_token_secret="xxxxxxxxxxxxxxxxxxxxxxxx"
)

 # Authenticate to Twitter API V1.1
auth = tweepy.OAuth1UserHandler(api_key,api_secrets,access_token,access_secret)
api = tweepy.API(auth)

bot = telebot.TeleBot('xxxxxxxxxxxxxxxxxxxxxx') # Telegram Bot şifresi


def skeet(ddi,txt,image):
    with open(image, 'rb') as f:
        img = f.read()
    upload = client.com.atproto.repo.upload_blob(img)
    images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
    facets = [models.AppBskyRichtextFacet.Main(features=[models.AppBskyRichtextFacet.Mention(did=ddi)],index=models.AppBskyRichtextFacet.ByteSlice(byteStart=0, byteEnd=len(ddi.encode('UTF-8'))),)]
    client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=txt, facets=facets,embed=embed),))


def extract_url(text, *, aggressive: bool, encoding='UTF-8'):
    """
    If aggressive is False, only links beginning http or https will be detected
    """
    encoded_text = text.encode(encoding)

    if aggressive:
        pattern = rb'(?:[\w+]+\:\/\/)?(?:[\w\d-]+\.)*[\w-]+[\.\:]\w+\/?(?:[\/\?\=\&\#\.]?[\w-]+)+\/?'
    else:
        pattern = rb'https?\:\/\/(?:[\w\d-]+\.)*[\w-]+[\.\:]\w+\/?(?:[\/\?\=\&\#\.]?[\w-]+)+\/?'

    matches = re.finditer(pattern, encoded_text)
    url_byte_positions = []
    for match in matches:
        url_bytes = match.group(0)
        url = url_bytes.decode(encoding)
        url_byte_positions.append((url, match.start(), match.end()))

    return url_byte_positions


def foto(futu):
    file = 'temp.jpg'
    request = requests.get(futu, stream=True)
    if request.status_code == 200:
        with open(file, 'wb') as image:
            for chunk in request:
                image.write(chunk)
    return file


def bskyfot(file):
    with open(file, 'rb') as f:
        img = f.read()
    return img


def resize_image(image_file, max_size_kb=976.56, max_iterations=10):
    with Image.open(image_file) as img:
        img_format = 'JPEG'
        for _ in range(max_iterations):
            img_data = io.BytesIO()
            img.save(img_data, img_format)
            size_kb = len(img_data.getvalue()) / 1024
            if size_kb <= max_size_kb:
                return img_data.getvalue()
            quality = int(max((1 - (size_kb - max_size_kb) / size_kb) * 100, 0))
            img.save(img_data, img_format, quality=quality)
        raise ValueError(f"Could not reduce image size below {max_size_kb}KB")


def search():
    dosya = 'handles.txt'
    with open(dosya, 'r') as file:
        content = file.readlines()
        return content


def selam():
    hour = datetime.datetime.now().hour
    slm = "İyi geceler" if 0<=hour<5 else "Günaydın" if hour<=10 else "İyi günler" if hour<=16 else "İyi akşamlar" if hour<=21 else "İyi geceler"
    return slm


@bot.message_handler(commands=['start','help'])
def welcome(message):
    gif = "https://i.ibb.co/cbdwMC7/IMG-20220725-021219.jpg"
    bot.send_photo(message.chat.id, gif)
    vid = "https://github.com/TA2KVC/DuckBot/raw/main/OTA/duckvid.mp4"
    bot.send_video(message.chat.id, vid)


@bot.message_handler(commands=['vak','vakvak'])
@bot.message_handler(regexp="Ördek")
@bot.message_handler(regexp="Vak")
@bot.message_handler(regexp="Vakvak")
def duckbot(message):
    try:
        ordeek=twitter.otaduck()
        ordek = foto(ordeek)
        slm = selam()
        tip = "Sevgili Ördeksever Dostlarım. \U0001F986"
        yt,tt=twitter.otatube()
        stat = slm+" "+tip+"\n\n"+tt+"\n"+yt+"\n\n\U0001F986\U0001F916 Vakvak\U00002122"
        resize_image(ordek)
        with open(ordek, 'rb') as f:
            img = f.read()
        upload = client.com.atproto.repo.upload_blob(img)
        images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
        embed = models.AppBskyEmbedImages.Main(images=images)
        url_positions = extract_url(stat, aggressive=True)
        facets = []
        for link in url_positions:
            uri = link[0] if link[0].startswith('http') else f'https://{link[0]}'
            facets.append(
                models.AppBskyRichtextFacet.Main(
                    features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                    index=models.AppBskyRichtextFacet.ByteSlice(byteStart=link[1], byteEnd=link[2]),
                 )
            )
        client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, facets=facets,embed=embed),))
        media = api.media_upload(ordek)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
        print("skeet gönderildi")
        bot.send_photo(message.chat.id, ordeek, 'Vakvak created by Volkan TA2KVC\nClick /vakvak')
    except:
        print("kod başarısız")
        bot.send_message(message.chat.id, 'Hata: Kod başarısız.')



@bot.message_handler(commands=['miyav'])
def catbot(message):
    caat=twitter.otacat()
    cat = foto(caat)
    slm = selam()
    tipc = "Sevgili Kedisever Dostlarım. \U0001F986"
    yt,tt=twitter.otatube()
    stat = slm+" "+tipc+"\n\n"+tt+"\n"+yt+"\n\n\U0001F986\U0001F916 Vakvak\U00002122"
    resize_image(cat)
    with open(cat, 'rb') as f:
        img = f.read()
    upload = client.com.atproto.repo.upload_blob(img)
    images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
    url_positions = extract_url(stat, aggressive=True)
    facets = []
    for link in url_positions:
        uri = link[0] if link[0].startswith('http') else f'https://{link[0]}'
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                index=models.AppBskyRichtextFacet.ByteSlice(byteStart=link[1], byteEnd=link[2]),
            )
        )
    client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, facets=facets,embed=embed),))
    media = api.media_upload(cat)
    tweety.create_tweet(text=stat, media_ids=[media.media_id])
    print("skeet gönderildi")
    bot.send_photo(message.chat.id, caat, 'Miiv created by Volkan TA2KVC\nClick /miyav')



@bot.message_handler(commands=['hav'])
def dogbot(message):
    doog=twitter.otadog()
    dog = foto(doog)
    slm = selam()
    tipd = "Sevgili Patisever Dostlarım. \U0001F986"
    yt,tt=twitter.otatube()
    stat = slm+" "+tipd+"\n\n"+tt+"\n"+yt+"\n\n\U0001F986\U0001F916 Vakvak\U00002122"
    resize_image(dog)
    with open(dog, 'rb') as f:
        img = f.read()
    upload = client.com.atproto.repo.upload_blob(img)
    images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
    url_positions = extract_url(stat, aggressive=True)
    facets = []
    for link in url_positions:
        uri = link[0] if link[0].startswith('http') else f'https://{link[0]}'
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                index=models.AppBskyRichtextFacet.ByteSlice(byteStart=link[1], byteEnd=link[2]),
            )
        )
    client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, facets=facets,embed=embed),))
    media = api.media_upload(dog)
    tweety.create_tweet(text=stat, media_ids=[media.media_id])
    print("skeet gönderildi")
    bot.send_photo(message.chat.id, doog, 'Puppy created by Volkan TA2KVC\nClick /hav')



@bot.message_handler(commands=['mix'])
def cutebot(message):
    miix=twitter.otamix()
    mix = foto(miix)
    slm = selam()
    tipx = "Sevgili Hayvansever Dostlarım. \U0001F986"
    yt,tt=twitter.otatube()
    stat = slm+" "+tipx+"\n\n"+tt+"\n"+yt+"\n\n\U0001F986\U0001F916 Vakvak\U00002122"
    resize_image(mix)
    with open(mix, 'rb') as f:
        img = f.read()
    upload = client.com.atproto.repo.upload_blob(img)
    images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
    url_positions = extract_url(stat, aggressive=True)
    facets = []
    for link in url_positions:
        uri = link[0] if link[0].startswith('http') else f'https://{link[0]}'
        facets.append(
            models.AppBskyRichtextFacet.Main(
                features=[models.AppBskyRichtextFacet.Link(uri=uri)],
                index=models.AppBskyRichtextFacet.ByteSlice(byteStart=link[1], byteEnd=link[2]),
            )
        )
    client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, facets=facets,embed=embed),))
    media = api.media_upload(mix)
    tweety.create_tweet(text=stat, media_ids=[media.media_id])
    print("skeet gönderildi")
    bot.send_photo(message.chat.id, miix, 'Mixx created by Volkan TA2KVC\nClick /mix')



def botlisten():
    bot.infinity_polling(interval=0, timeout=20)


def system_call_with_response(command):
    with subprocess.Popen(command, shell=True, stdout=subprocess.PIPE) as task:
        output = task.stdout.read()
        task.wait()
        return output.decode("utf-8").strip()


def datey():
    cmnd = "date "+"\"+%d.%m.%Y  %H:%M\""
    deyt = system_call_with_response(cmnd)
    return deyt



def botstop():
    botstop = system_call_with_response("sudo systemctl stop bluebot")
    return botstop


def vakbotstatus():
    botstatus = system_call_with_response("systemctl status bluebot")
    return botstatus


@bot.message_handler(commands=['botstop'])
def botstp(message):
    bot.send_message(message.chat.id, "VolPi4 bot durduruldu.")
    botstop()


@bot.message_handler(commands=['botstatus'])
def botstatus(message):
    status = vakbotstatus()
    bot.send_message(message.chat.id, status)


@bot.message_handler(commands=['ata'])
def atato(message):
    ata()
    bot.send_message(message.chat.id, "Mustafa Kemal ATATÜRK...")


def ata():
    try:
        ata1,ata2,ata3 = twitter.atam()
        atam = "Ebedi Başkomutan, Ölümsüz Türk... \n"
        atamm = "\" " +ata3+ " \""
        atamm += "\n\n"
        atamm += ata2
        ataa1 = foto(ata1)
        stat = atam+"\n"+atamm+"\n"
        resize_image(ataa1)
        with open(ataa1, 'rb') as f:
            img = f.read()
        upload = client.com.atproto.repo.upload_blob(img)
        images = [models.AppBskyEmbedImages.Image(alt='Mustafa Kemal ATATÜRK', image=upload.blob)]
        embed = models.AppBskyEmbedImages.Main(images=images)
        client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, embed=embed),))
        media = api.media_upload(ataa1)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Ata modülü başarısız")



@bot.message_handler(commands=['havaa'])
def havauto(message):
    accuhava()
    bot.send_message(message.chat.id, "Hava durumu bilgileri tweetlenecek...")


def accuhava():
    try:
        info,scak,nem,rzghz,rzgyn = twitter.accu()
        otoo,tipo=twitter.otofunc()
        slm = selam()
        oto = foto(otoo)
        hvd = slm +" "
        hvd += "Sevgili " + tipo + "\n"
        hvdu = "Başkentimiz Ankara'nın hava durumu: \n"
        hvdu += "Gökyüzü : " +info + "\n"
        hvdu += "Sıcaklık : " +scak + " °C\n"
        hvdu += "Nem : %" +nem + "\n"
        hvdu += "Rüzgar : " +rzghz+ " km/s hızla " +rzgyn+ " yönünde\n"
        stat = hvd+"\n"+hvdu+"\n \U0001F986\U0001F916 Vakvak\U00002122"
        resize_image(oto)
        with open(oto, 'rb') as f:
            img = f.read()
        upload = client.com.atproto.repo.upload_blob(img)
        images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
        embed = models.AppBskyEmbedImages.Main(images=images)
        client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, embed=embed),))
        media = api.media_upload(oto)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Hava durumu modülü başarısız")


@bot.message_handler(commands=['film'])
def filmoto(message):
    film()
    bot.send_message(message.chat.id, "Film bilgileri tweetlenecek...")


def film():
    try:
        title,poster,gen = twitter.yts()
        otoo,tipo=twitter.otofunc()
        slm = selam()
        oto = foto(poster)
        flm = slm +" "
        flm += "Sevgili " + tipo + "\n"
        flmu = "Sizin için seçtiğim film: \n"
        flmu += "\" " +title+ " \"\n"
        flmu += "Tür: " +gen+ " \n"
        stat = flm+"\n"+flmu+"\n \U0001F986\U0001F916 Vakvak\U00002122"
        resize_image(oto)
        with open(oto, 'rb') as f:
            img = f.read()
        upload = client.com.atproto.repo.upload_blob(img)
        images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
        embed = models.AppBskyEmbedImages.Main(images=images)
        client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, embed=embed),))
        media = api.media_upload(oto)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Film modülü başarısız")


@bot.message_handler(commands=['hava'])
@bot.message_handler(regexp="Hava")
@bot.message_handler(regexp="hava")
def havadurumu(message):
    nam = message.chat.first_name
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "Hatalı işlem yaptınız.. Kullanımı: hava sehirismi")
        return
    citya = args[1]
    city = citya.title()
    info,scak,nem,rzghz,rzgyn = twitter.accukod(city)
    hvvi = 'Sevgili ' + nam + '; \n'
    hvvi += "" +city + ' şehrinin hava durumu bilgisi \n'
    hvvi += 'birazdan twitlenecek..!'
    bot.send_message(message.chat.id, hvvi)
    otoo,tipo=twitter.otofunc()
    oto = foto(otoo)
    slm = selam()
    hvvd = slm
    hvvd += " Sevgili " + nam +"; \n"
    hvvdu = "Hava durumunu öğrenmek istediğin " +city+ " şehrinin bilgileri: \n"
    hvvdu += "Gökyüzü : " +info + "\n"
    hvvdu += "Sıcaklık : " +scak + " °C\n"
    hvvdu += "Nem : %" +nem + "\n"
    hvvdu += "Rüzgar : " +rzghz+ " km/s hızla " +rzgyn+ " yönünde\n"
    stat = hvvd+"\n"+hvvdu+"\n \U0001F986\U0001F916 Vakvak\U00002122"
    resize_image(oto)
    with open(oto, 'rb') as f:
        img = f.read()
    upload = client.com.atproto.repo.upload_blob(img)
    images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
    embed = models.AppBskyEmbedImages.Main(images=images)
    client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, embed=embed),))
    media = api.media_upload(oto)
    tweety.create_tweet(text=stat, media_ids=[media.media_id])
    print('skeeet gönderildi')
    bot.reply_to(message, hvvdu)


@bot.message_handler(commands=['ppfav'])
def ppfav(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Hatalı işlem yaptınız.. Kullanımı: ppfav Bluesky_handle limit")
        return
    hand = args[1]
    handle = hand + '.bsky.social'
    lmt = int(args[2])
    a = 1
    print(f'\n{handle} Profilinin skeetleri:\n\n')
    profile_feed = client.bsky.feed.get_author_feed({'actor': handle})
    for feed_view in profile_feed.feed:
         rpl= feed_view.post.record.reply
         if rpl == None:
             print('-', feed_view.post.record.text)
             client.like(feed_view.post)
             print('Skeet beğenildi...  ', a)
           # time.sleep(1)
             a = a + 1
             if a == lmt :
                 break
         else:
             pass


@bot.message_handler(commands=['allfav'])
def followsfav(message):
    allfav()


def allfav():
    name = search()
    for line in name:
        hand = line.splitlines()
        handle = ''.join(hand)
        fav(handle,11)


def fav(handle,limit):
    a = 1
    #b = 1
    pfav =(f'{handle} Profilinin skeetleri Auto-Fav:\n')
    bot.send_message("xxxxxxxx: Telegram kullanıcı-ID ", pfav)
    #b = b + 1
    profile_feed = client.bsky.feed.get_author_feed({'actor': handle})
    for feed_view in profile_feed.feed:
        rpl= feed_view.post.record.reply
        if rpl == None:
            print('-', feed_view.post.record.text)
            client.like(feed_view.post)
            a = a + 1
            if a == limit :
                break
        else:
            pass


@bot.message_handler(commands=['otofav'])
def autofav(message):
    try:
        xl= client.bsky.graph.get_followers({'actor':'vakvak.bsky.social', 'limit':100})
        for nane in xl.followers:
            hd = nane.handle
            li = hd.splitlines()
            for line in li:
                print(line)
                inputt=line
                fav(inputt,6)
    except:
        print('Hata...')
        time.sleep(3)


@bot.message_handler(commands=['piyasa'])
def piyssa(message):
    piysa()
    bot.send_message(message.chat.id, "Piyasa bilgileri birazdan tweetlenecek...")


def piysa():
    try:
        usa,uss,eua,eus,aua,aus,aga,ags = twitter.piyasa()
        borsa = twitter.borsa()
        tarh = datey()
        ordeek=twitter.otaduck()
        ordek = foto(ordeek)
        pyss = "Piyasalar: \n"
        pyss += "\U0001F986 Amerikan Ördeği :  " +usa+ "  -  " +uss+ "\n"
        pyss += "\U0001F986 Avrupa Ördeği :  " +eua + "  -  " +eus+ "\n"
        pyss += "\U0001F986 Altın Ördek :  " +aua + "  -  " +aus+ "\n"
        pyss += "\U0001F986 Gümüş Ördek :  " +aga + "  -  " +ags+ "\n"
        pyss += "\U0001F986 B-Ördek100 :  " +borsa+ "\n\n"
        pyss += tarh
        stat = pyss+"\n\U0001F986\U0001F916 VakvakBot\U00002122"
        with open(ordek, 'rb') as f:
            imgd = f.read()
        client.send_image(text=stat, image=imgd, image_alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC')
        media = api.media_upload(ordek)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Piyasa modülü başarısız")


def isimi():
    try:
        ordeek = twitter.otaduck()
        ordek = foto(ordeek)
        ff = twitter.kizisimci()
        mm = twitter.erkisimci()
        hvdu = "Bugün yumurtadan çıkan ördekler için isim önerileri: \n\n"
        hvdu += "Kız Ördek: " +ff+ "\n"
        hvdu += "Erkek Ördek : " +mm+ "\n"
        stat = hvdu+"\n \U0001F986\U0001F916 Vakvak\U00002122"
        with open(ordek, 'rb') as f:
            imgd = f.read()
        client.send_image(text=stat, image=imgd, image_alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC')
        media = api.media_upload(ordek)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("İsim modülü başarısız")


@bot.message_handler(commands=['isim'])
def isimlik(message):
    isimi()
    bot.send_message(message.chat.id, "isimler birazdan tweetlenecek...")


@bot.message_handler(commands=['isimci'])
def isimci(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Hata! Kullanım: /isimci [kız ismi] [erkek ismi]")
        return
    kiz = args[1]
    ff = kiz.title()
    erkek = args[2]
    mm = erkek.title()
    ordeek = twitter.otaduck()
    ordek = foto(ordeek)
    nam = "Bugün yumurtadan çıkan ördekler için isim önerileri: \n\n"
    nam += "Kız Ördek: " +ff+ "\n"
    nam += "Erkek Ördek : " +mm+ "\n"
    stat = nam+"\n \U0001F986\U0001F916 Vakvak\U00002122"
    with open(ordek, 'rb') as f:
        imgd = f.read()
    client.send_image(text=stat, image=imgd, image_alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC')
    media = api.media_upload(ordek)
    tweety.create_tweet(text=stat, media_ids=[media.media_id])
    print('Skeet gönderildi...')
    bot.send_message(message.chat.id, "isimler birazdan twitlenecek...")


@bot.message_handler(commands=['places'])
def placeoto(message):
    places()
    bot.send_message(message.chat.id, "Manzaralar twitleniyor...")


def places():
    try:
        plink,pdat = twitter.place()
        plll = "Dünya Ördeklerinin yaşadığı en güzel yerler: \n\n"
        plll+= "\" " +pdat+ " \"\n"
        flink = foto(plink)
        stat = plll + "\n \U0001F986\U0001F916 Vakvak\U00002122"
        with open(flink, 'rb') as f:
            imgd = f.read()
        client.send_image(text=stat, image=imgd, image_alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC')
        media = api.media_upload(flink)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Şehirler modülü başarısız")


@bot.message_handler(commands=['yemek'])
def pisiroto(message):
    pisir()
    bot.send_message(message.chat.id, "Yemekler twitleniyor...")


def pisir():
    try:
        crb=twitter.corba()
        ymk=twitter.yemek()
        ymk2=twitter.yemek()
        slt=twitter.salata()
        ick=twitter.icki()
        tat=twitter.tatli()
        ymkft="https://i.ibb.co/tm4Cs7H/yemek2.gif"
        neymk = "\U0001F986 \U0001F372  Akşam Ne Pişireceğiz?  \U0001F372 \U0001F986\n\n"
        neymk += "\U0001F963 " +crb + "\n"
        neymk += "\U0001F372 " +ymk + " veya " +ymk2 + "\n"
        neymk += "\U0001F957 " +slt + "\n"
        neymk += "\U0001F36E " +tat + "\n"
        neymk += "\U0001F379 " +ick + "\n\n"
        ymfot = foto(ymkft)
        stat = neymk + "\n \U0001F986\U0001F916 Vakvak\U00002122"
        with open(ymfot, 'rb') as f:
            imgd = f.read()
        client.send_image(text=stat, image=imgd, image_alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC')
        media = api.media_upload(ymfot)
        tweety.create_tweet(text=stat, media_ids=[media.media_id])
    except:
        print("Yemek modülü başarısız")


@bot.message_handler(commands=['follow'])
def follow(message):
    follower()
    bot.send_message(message.chat.id, "Bluesky yeni takipçi dinleniyor...")



def follower():
    last_seen_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    response = client.bsky.notification.list_notifications({'limit':1})
    for notification in response.notifications:
        if not notification.isRead:
            if notification.reason == 'follow':
                pp=notification.author.avatar
                name=notification.author.displayName
                hand=notification.author.handle
                didi = notification.author.did
                print(didi)
                foto(pp)
                bg = Image.open('bckgrnd2.jpg')
                lgo = Image.open('logo.jpg')
                lgo = lgo.resize((500, 500), Image.Resampling.LANCZOS)
                mask = Image.new("L", lgo.size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0, 495, 495), fill=255)
                mask = mask.filter(ImageFilter.GaussianBlur(3))
                mask.save('mask.jpg', quality=95)
                bg.paste(lgo,(520,270), mask)
                d1 = ImageDraw.Draw(bg)
                myFont = ImageFont.truetype('Mont.otf', 60)
                d1.text((80, 800), "Hoş geldin Ördeksever:\n"+name+"\n@"+hand, font=myFont, fill =(255, 255, 255))
                bg.save('tw.jpg')
                oto = 'tw.jpg'
                with open(oto, 'rb') as f:
                    img = f.read()
                upload = client.com.atproto.repo.upload_blob(img)
                images = [models.AppBskyEmbedImages.Image(alt='Vakvak\U00002122 created by Volkan\U00002122 TA2KVC', image=upload.blob)]
                embed = models.AppBskyEmbedImages.Main(images=images)
                facets = [models.AppBskyRichtextFacet.Main(features=[models.AppBskyRichtextFacet.Mention(did=didi)],
                    index=models.AppBskyRichtextFacet.ByteSlice(byteStart=24, byteEnd=len(didi.encode('UTF-8'))), )]
                stat = "Hoş geldin Ördeksever " + name + " !"
                client.com.atproto.repo.create_record(models.ComAtprotoRepoCreateRecord.Data(repo=client.me.did,collection=models.ids.AppBskyFeedPost,record=models.AppBskyFeedPost.Main(createdAt=datetime.datetime.now().isoformat(), text=stat, facets=facets, embed=embed),))
                print(f' {notification.author.handle} {notification.author.displayName} takip etti.')
    client.bsky.notification.update_seen({'seenAt': last_seen_at})
    print('Successfully process notification. Last seen at:', last_seen_at)
    time.sleep(15)



@bot.message_handler(commands=['homefav'])
def homefav(message):
    homfav()
    bot.send_message(message.chat.id, "Bluesky Auto-fav Timeline...")


def homfav():
    #mesj= 'Auto-Fav: ON \n\U0001F986\U0001F916 Vakvak\U00002122'
    #client.send_post(text = mesj)
    a=1
    timeline = client.bsky.feed.get_timeline({'algorithm': 'reverse-chronological','limit':100})
    for feed_view in timeline.feed:
        rpl= feed_view.post.record.reply
        if rpl == None:
            post = feed_view.post.record
            author = feed_view.post.author
            client.like(feed_view.post)
            #time.sleep(3)
            a=a+1
        else:
            #print('\n ###',rpl,'\n ###')
            pass
    #mesaj= 'Blueline\'dan '+ str(a-1) + ' skeetinizi favladım.\n\U0001F986\U0001F916 Vakvak\U00002122'
    #client.send_post(text = mesaj)


t1=threading.Thread(target=botlisten)
schedule.every().day.at("19:38").do(ata)
schedule.every().day.at("20:00").do(film)
schedule.every().day.at("09:30").do(places)
schedule.every().day.at("09:31").do(isimi)
schedule.every().day.at("09:32").do(piysa)
schedule.every().day.at("09:33").do(accuhava)
schedule.every().day.at("12:00").do(pisir)
schedule.every(4).hours.do(homfav)
#schedule.every(180).minutes.do(auto)
t1.start()


while True:
    schedule.run_pending()
#    follower()
    time.sleep(30)

