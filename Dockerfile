FROM ubuntu
RUN apt update; apt install python-pip espeak vorbis-tools -y; \
	useradd -m bot -u 1000 -s /bin/bash
COPY telegram_bot.py puns.txt flag.txt /home/bot/
RUN pip install python-telegram-bot; \
	chmod 777 /home/bot; chmod +t /home/bot; \
	chown -R root:root /home/bot; \
	chmod 704 /home/bot/*; 
WORKDIR /home/bot
CMD ["python", "telegram_bot.py"]
