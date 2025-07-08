import qrcode

bot_username = "pulsar.watch"
link = f"https://t.me/pulsar42_bot"

qr = qrcode.make(link)
qr.save("telegram_bot_qr.png")
