import telegram
from PIL import Image
from io import BytesIO

#chatid hoangnt bot 717351343
#chatid group meditech bot -333227761 
class Bot(object):
	token = '755096508:AAF-y3VoupvctXgF-byJjgBaIt7gRFUBDX0'
	chat_id = 717351343
	def __init__(self):
		self.bot = telegram.Bot(token=self.token)
	
	def send(self, l):
		image = Image.fromarray(l[1])
		bio = BytesIO()
		bio.name = 'image.jpeg'
		image.save(bio, 'JPEG')
		bio.seek(0)
		self.bot.sendMessage(chat_id=self.chat_id, text=l[0])
		self.bot.send_photo(chat_id=self.chat_id, photo=bio)
		self.bot.sendLocation(chat_id=self.chat_id, latitude=21.0415752, longitude=105.7868537)



