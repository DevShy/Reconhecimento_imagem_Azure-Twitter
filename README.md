## Introdução

Neste artigo, será mostrado como você leitor, pode pegar uma imagem de algum famoso ou qualquer pessoa no twitter automaticamente e analisar quem está nessa imagem e os principais elementos que a compõe. Para isso, será preciso apenas de três coisas:

1. Uma conta de desenvolvedor no twitter;
2. Uma conta na azure da microsoft; 
3. Muita vontade de aprender. 

Três requisitos fáceis e gratuitos, assim fica fácil. E então, prontos para adquirir mais um conhecimento? 
Vamos lá!!!


## Twitter 

Como já mencionado, neste artigo precisaremos de uma developer account pois precisaremos minerar o twitter, isto é, recolher informações específicas dele, como por exemplo: 

1. Userid do usuário que desejamos obter a imagem; 
2. Descrição do post utilizado por ele; 
3. A imagem que ele postou e entre outras coisas. 

para o artigo não ficar muito grande, basta clickar [aqui](https://developer.twitter.com/en/docs) e você será direcionado para a documentação, basta seguir o tutorial para obter a conta de desenvolvedor. Caso não consigam, ou tenham alguma dúvida, podem deixar nos comentários e posteriormente eu crio um artigo somente para explicar isto. 

O que precisaremos do twitter são as chaves para usarmos a API deles. Após a criação da conta, basta acessar o campo dashboard e você irá de deparar com uma página parecida com esta: 

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p4yef0xhgvz6uszie1y4.png)

Feito isso, o primeiro passo está feito, vamos para o próximo! 

## Utilizando a API
Para nos auxiliar na nossa tarefa, utilizaremos uma *biblioteca* 
do python criada especificamente para utilizarmos a API do twitter, chamamos ela de [tweepy](https://docs.tweepy.org/en/stable/). Vamos fazer então a importação desta *lib* 

```python
import tweepy as tw
```
Agora precisamos definir nossa autenticação para podermos acessar a API do twitter, para isso, irei criar algumas variáveis obrigatórias neste processo: 

```python
consumer_key = xxx
consumer_secret = xxx
access_token = xxx
access_token_secret = xxx


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth)
```
Como cada chave é secreta, neste artigo não passarei a string das minhas. Para o código de vocês, basta substituir o x por sua própria chave. 

Após declarar as 4 chaves necessários, é preciso criar a variável auth, com ela, atribuiremos o método *OAuthHandler*, e passaremos como parâmetro a consumer_key e a consumer_secret. Logo em seguida, precisamos liberar o nosso acesso com o token de acesso, para isso, chamo a variável auth, e passo o método *set_acess_token* 

Para finalizar esta parte, crio uma variável api, e atribuo a ela o método *API* passando a variável auth como parâmetro. 

Pronto, inicializamos nossas variáveis principais para que possamos ter acesso a todos os dados postados no twitter! 

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gpqtrzdmrmhqn0gfbxiy.png) 

## Azure 
Já criamos nossa conta no twitter, e agora tudo que falta para irmos pro nosso código é nossa conta na Azure. Apesar de ser um serviço pago, a microsoft libera um acesso a todas as ferramentas de graça por 7 dias! Neste artigo, utilizaremos isto para obtermos acesso! 

Assim como feito como a developer account do twitter, para não ficar extenso, deixarei aqui um [tutorial](https://docs.microsoft.com/en-us/) que levará a vocês a documentação da própria microsoft, resumindo, é  necessário a criação de uma conta microsoft, acesso ao dashboard da plataforma e precisaremos assim como no twitter, pegar nossa chave gratuita de 7 dias que nos dará acesso a API da azure. 

Após essa etapa, vamos continuar nosso código! Agora é preciso importar a biblioteca da azure, para isso, faremos o seguinte: 
```python
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
```
E logo em seguida, criaremos outra variáveis de acesso e uma variável que será nosso client. 
```python
credenciais = CognitiveServicesCredentials('xxx')
client = ComputerVisionClient('https://eduardoteste.cognitiveservices.azure.com/',credenciais) 
```
Agora, com todas as contas criadas e chaves de acesso liberadas, podemos partir finalmente para nosso código. E ai, bora lá? 

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fpd18q3892clajho6c6h.png)
 
## Vamo codar! 
Aqui daremos início a todo lógica por trás do nosso programa. Tudo será feito em python e é necessário conhecimento básico prévio da linguagem de programação para que vocês entendam 100% do que será feito aqui. 

Bom, vamos pensar primeiro no que será feito aqui. O nosso código se resume em acessarmos o twitter, passar alguns usernamers para ele, e ele nos retornará a url da imagem que usaremos para fazer a análise. Após receber esta url, enviaremos ela para a azure, e lá será feito todo o processamento e obtenção das informações que está imagem contêm.  

Tudo explicado, então vamos lá! Primeiro irei criar uma lista com alguns usernames de famosos aleatórios. 

```python 
famosos = ['cauareymond','otaviano','bernardipaloma',
'IngridGuimaraes','olazaroramos','baianolol1','debranascimento','FioMattheis','moalfradique','Nandacostareal','brttOficial','revoltalol']
```
Isto é completamente editável, se quiser passar o seu perfil aqui, ou o de um amigo, pode modificar sem problema. 
Após isso, irei criar uma lista vazia chamada famosos_id, esta lista irá armazenar todos os ids da nossa lista de famosos. Após criarmos esta variável, farei um for para acessarmos todos os usernames contidos na lista famosos, e farei um append na lista famosos_id buscando apenas o ID de cada username. 
```python
famosos_id = []
for famoso in famosos:
  famoso_id = api.get_user(famoso).id_str
  famosos_id.append(famoso_id)
```
Se printarmos o que contêm a lista famosos_id agora, isso será mostrado: 
```python
['246591347', '24209365', '75082334', '59932653', '219112689',
 '2567508709', '163972875', '163601846', '68839460', '764565242', '292013793', '2334322310']
```

Agora, para que nosso código seja completamente automático, irei criar uma *Streaming*. Esta Streaming será responsável por buscar as nossas informações desejadas em tempo real, ou seja, se qualquer famoso daquela lista postar algum tweet 5 segundos, 10, 15, ou até mesmo 5 dias depois que o meu código estar rodando, conseguiremos ainda sim obter acesso as informações. 
 
Assim sendo, criarei então uma classe que será responsável por rodar nossa Streaming, a ela darei o nome de MyStreamListener, e passei como parâmetro o método StreamListener da biblioteca tweepy. 

Agora, criei o método *on_status*, passando como parâmetro (self, status). 

Vamos preencher nossa classe agora, primeiro, sempre que o meu bot achar as informações que eu quero, vou pedir pra ele mostrar o nome do usuário e o texto digitado no post, para isso, usarei os métodos *user.screen_name* e o *text* da biblioteca tweepy. 
```python
print("Nome de usuário: ",status.user.screen_name)
print("Texto digitado: ", status.text)
```
Agora, vou verificar se no post foi postado alguma imagem além apenas do texto. Para isso, utilizaremos o if buscando a chave "media" do json retornado através do parâmetro status. A media fica localizada no atributo entities, então passarei ele como local de busca. 
```python
if 'media' in status.entities:
      url = status.entities['media'][0]['media_url']
      print("URL da imagem: ",url)
```
Dentro do if, crio uma variável url para receber justamente a url desta imagem, e mando printar na tela logo em seguida. 

**Ainda dentro do if**, agora vamos acessar a variável client para enviarmos nossa url para a Azure. Para isto, chamaremos o método *describe_imagem*, e como parâmetro passaremos nossa url, a quantidade de elementos que queremos que volte e a linguagem. Como a linguagem padrão desta lib é o inglês, passei o inglês como linguagem mesmo. 
```python
descricao = client.describe_image(url,1,'en')
texto_descricao = descricao.captions[0].text
print("Descrição: ",texto_descricao)
```
Depois de chamar o método *describe_imagem*, criei uma variável chamada texto_descrição que ficará responsável por armazenar a  descrição que será retornada da azure. Pois para isso precisamos acessar o atributo *captions* e passar posteriormente o atribulo *text*. 

Uma coisa muito interessante contida nas análises da Azure, é que ela através das análises, nos diz o suposto nome do famoso que estamos analisando, como isto é muito interessante, traremos para nosso código também. 
Para isto, chamarei o método *analyze_image_by_domain* contido na nossa variável Client, e passarei como parâmetro o que pode estar contigo naquela imagem que iremos passar, que no nosso caso, são celebridades/famosos, a url da imagem e novamente a linguagem desejada. 

```python
analise_celebridades = client.analyze_image_by_domain("celebrities",url,"en")
lista_celebridades = [celebridade['name'] for celebridade in analise_celebridades.result['celebrities']]
print(lista_celebridades)
```
Como o que nos é retornado são vários valores e não exclusivamente 1, utilizei o for para armazenar todos os valores em uma lista. 

Estamos no finalzinho do nosso código, e um outro recurso dos serviços da azure, é que ele nos retornas tags que se assemelham com a imagem que estamos analisando. Vamos por essas tags no nosso código? 

Para isso, é muito fácil, basta eu acessar o atributo *tag*, dentro da nossa variável descrição e fazer um for printando todos os valores contidos nesta variável. 
```python 
for tag in descricao.tags:
        print("Principais palavras chaves: \n", tag)
```

E com isso finalizamos nossa classe, se você quiser armazenar os resultados obtidos em documento de texto, basta criar um json no final da classe e você obterá acesso a tudo. 
Pode ser feito assim
```python
resultados = {
          'usuario': status.user.screen_name,
          'texto_usuario': status.text,
          'url_imagem': url,
          'celebridades': lista_celebridades,
          'descricao': texto_descricao,
      }
with open('tweets.txt','a') as arquivo:
     arquivo.write(json.dumps(re sultados))
     arquivo.write('\n')
```
Utilizamos o with open para criarmos nosso arquivo txt e armazenar nosso documento de texto contigo no json resultados. 

Agora, para executar a classe, vamos criar uma variável chamada MyStream, atribuindo a ela o método Stream e passando como  parâmetro a variável auth, criada no começo do artigo, e nossa classe. Feito isso, aplicaremos o método *filter* a variável 
MyStream, e passaremos como parâmetro nossa lista famosos_id, contendo todos os ids dos famosos que iremos atualizar. E fim!!!

```python 
MyStream = tw.Stream(auth=auth, listener=MyStreamListener())
MyStream.filter(follow=famosos_id)
``` 
 
## Bot rodando

![Alt Text](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xdoy87348rdtdun47ess.gif)
