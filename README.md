# vulnerable_telegram_bot
A telegram bot that speaks out loud the text you say to it. It is vulnerable to code injection, used in a challenge for BjornCTF 2020

---

There is a really easy command injection in the `/say` command. However, reading the flag is not so easy, as the bot only replies with vocal messages of the output of your command generated with `espeak`, and the flag contains some non-pronounceable characters :)
