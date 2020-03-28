# NAid Bot
Neighbor Aid (NAid) Telegram Bot ist ein Projekt in der Entwicklungsphase. Dieser Bot soll lokale Initiativen (Nachbarschaftshilfen) bei der Koordinierung von Aufgaben unterschtuetzen.

## Updates
- **23.03.2020**:
Kick off, fruehe Entwicklungsphase
- **25.03.2020:**:
Erste funktionale Demoversion verfuegbar.
- **28.03.2020:**:
Umstellung auf `python_telegram_bot`

## Idee
Für eine lokale Initiative wird eine Gruppe auf Telegram erstellt und der Bor der Gruppe hinzugefuegt. Über die Gruppe kann man den Bot mit Aufgaben füttern. Der Bot postet eine Vorschau in die Gruppe und wartet darauf, dass jemand die Aufgabe annimmt. Sobald das passiert, informiert er die beide Parteien und wartet auf die beiderseitige Bestätigung. Erst dann werden persönliche Daten in einem privaten Chat herausgegeben. Zusätzlich gibt der Bot den Freiwilligen Tips zum Ablauf und zur Hygiene über den Chat.


## Developer
### ToDo
- Texten/Uebersetzen der Bot Nachrichten, Hinweistexte fuer den Ablauf bei z.B. beim Einkaufen
- Installation vereinfachen, evt. Docker
- Blacklist bei spam/scam
- [Hosting](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Where-to-host-Telegram-Bots)

### Install
```bash
pip install pyTelegramBotAPI

git clone git@github.com:andrejberg/naid_bot.git
cd naid_bot
cp bot_credentials.py bot_credentials_private.py
```

In `bot_credentials_private.py` eintragen:
- Telegram API Token
- Chat ID Gruppe
- Chat ID Channel

### Run
```bash
python naid_bot.py
```


## Credits
- [python_telegram_bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Logo based on [font awesome helping hands icon](https://fontawesome.com/icons/hands-helping).
