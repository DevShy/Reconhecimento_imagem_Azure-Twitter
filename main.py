import tweepy as tw
import json
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials

consumer_key = '4vJ3mcPBvCwcvH9og7nPWaYwO'
consumer_secret = 'B7yljQrDoPJtUtteOtiync4myhuDLGGpBvh3ZDQhtHxFZP9Io2'
access_token = '1305247107452997636-r04z9PH9UYDf5xHOIlLmpwnjDb3q6P'
access_token_secret = 'vOLuCMc8HqWJei61aELehCzBAbYRn4Ta4e9ZwWjayQPYI'


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth)

famosos = ['DevShy_','MTRAmazing','cauareymond','otaviano','bernardipaloma',
'IngridGuimaraes','olazaroramos','baianolol1','debranascimento','FioMattheis','moalfradique','Nandacostareal','brttOficial','revoltalol']

credenciais = CognitiveServicesCredentials('f4a87b64646b4c99986eb279cf616f31')
client = ComputerVisionClient('https://eduardoteste.cognitiveservices.azure.com/',credenciais)

famosos_id = []
for famoso in famosos:
  famoso_id = api.get_user(famoso).id_str
  famosos_id.append(famoso_id)

MyStream = None

class MyStreamListener (tw.StreamListener):
      def on_status(self,status):
    print("Nome de usuário: ",status.user.screen_name)
    print("Texto digitado: ", status.text)

    if 'media' in status.entities:
      url = status.entities['media'][0]['media_url']
      print("URL da imagem: ",url)
      descricao = client.describe_image(url,1,'en')
      texto_descricao = descricao.captions[0].text
      analise_celebridades = client.analyze_image_by_domain("celebrities",url,"en")
      print("Descrição: ",texto_descricao)
      lista_celebridades = [celebridade['name'] for celebridade in analise_celebridades.result['celebrities']]
      print(lista_celebridades)
      for tag in descricao.tags:
        print("Principais palavras chaves: \n", tag)

      resultados = {
          'usuario': status.user.screen_name,
          'texto_usuario': status.text,
          'url_imagem': url,
          'celebridades': lista_celebridades,
          'descricao': texto_descricao,
      }

      with open('tweets.txt','a') as arquivo:
        arquivo.write(json.dumps(resultados))
        arquivo.write('\n')
      


    print('----------')
    print('\n')


MyStream = tw.Stream(auth=auth, listener=MyStreamListener())
MyStream.filter(follow=famosos_id)

lista_arquivo = []
with open('tweets.txt','r') as arquivo:
  for linha in arquivo:
    lista_arquivo.append