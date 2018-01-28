import discord
import random
import asyncio 
import requests 
import io
import safygiphy
import shelve
import json
import re
from discord import Game
client = discord.Client()
legal = safygiphy.Giphy()
minutos = 0
hora = 0

@client.event
async def on_ready():
	print(' BOT INICIADO ')
	print(client.user.name)
	print(client.user.id)
	print('==============')
	await client.change_presence(game=Game(name="Utilize ?help para saber meus comandos!"))

@client.event
async def on_message(message):
	#CRIACAO DO MENU DE HELP
	if message.content.lower().startswith('?help'):
		embed=discord.Embed(
			title='Minha lista de comandos 📄',
			color=0xed2d2d,
			description=#'**> ?tempo**        Exibe quanto tempo você está conectado ao servidor\n\n'
'**> ?bot**              Mensagem do BOT\n\n'
'**> ?fome**          Você é alimentado\n\n'
'**> ?cpf**              Gera um CPF aleatorio\n\n'
'**> ?gif**               Este comando gera um gif aleatorio. Exemplo `?gif naruto` \n\n'
'**> ?coins**          Ganha uma quantidade de coins aleatoria\n\n'
'**> ?carteira**     Exibe a carteira com toda quantidade de coins acumuladas\n\n'
'**> ?give**            Doa a quantidade de coins passada para um membro\n\n'
'**> ?ola**               Interação com o BOT\n\n'
'**> ?avatar**         Exibe seu avatar ou de alguém mencionado\n\n'
'**> ?xp**                 Exibe sua quantidade de XP acumulado com as mensagens\n\n'
'**> ?rank**             Exibe o Rank de XP do servidor.\n\n'
'**> ?soma**            BOT realiza a soma de dois numeros passados é importante usar o sinal de atribuição `+`\n\n'
'**> ?diminuir**       BOT realiza a subtração de dois numeros passados é importante usar o sinal de atribuição `-`\n\n'
'**> ?divi**                BOT realiza uma divisão é preciso utilizar dois numeros e o sinal de atribuição `/`\n\n'
'**> ?multi**             BOT realiza a multiplicação de dois valores é importante utilizar o sinal de atribuição `*`\n\n'
'**> ?servidor**        Exibe as informações do servidor\n\n'
'**> ?user**               Exibe informações do usuário.\n\n'
'**> ?add**                 Comando para o Dono do servidor adicionar cargos para usarem clear chat\n\n'
'**> ?remove**          Dono do servidor remove cargos do add\n\n'
'**> ?clear**              Apaga mensagem do chat caso for autorizado\n\n'


			)
		
		embed.set_author(
				name='Robot how to create',
				icon_url='http://www.primapaginaonline.it/wp-content/uploads/2017/07/mr_robot_icon_by_gonkasth-dac0sk9.png'
			)
		
		embed.set_footer(
				text='Criado por ROBOT',
				icon_url='http://www.primapaginaonline.it/wp-content/uploads/2017/07/mr_robot_icon_by_gonkasth-dac0sk9.png'
			)
		
		await client.send_message(message.channel,embed = embed)

	#ENVIO DE MENSAGEM SE ALGUEM ENVIAR UMA MENSAGEM DE ?OLA NO CHAT E AS MENSAGEM SAO REMOVIDAS EM UM DELAY DE 1 SEGUNDO
	if message.content.lower().startswith('?ola'):

		hello = await client.send_message(message.channel,'Olá amigo')
		await asyncio.sleep(1)
		await client.delete_message(message)

		await asyncio.sleep(1)
		await client.delete_message(hello)

	#MENSAGEM DO BOT
	if message.content.lower().startswith('?bot'):
		
		embed=discord.Embed(title='Madara BOT',description='Oi eu sou o Madara BOT você pode saber mais sobre mim utilizando ?help')
		await client.send_message(message.channel,embed=embed)

	#BOT ADICIONA UM REACTION AO AUTOR DA MENSAGEM E ENVIA UMA MENSAGEM LEGAL :P
	if message.content.lower().startswith('?fome'):
		
		await client.add_reaction(message,'🍩')
		
		embed=discord.Embed(title='Fome 🍩', description="<@"+message.author.id+">"+" Você foi alimentado 🍴", color=0x4571f0)
		await client.send_message(message.channel,embed = embed)

	#GERA UM NUMERO FICTIO DE CPF ALEATORIO DE ADICIONA UMA REAÇÃO A MENSAGEM DO AUTOR
	if message.content.lower().startswith('?cpf'):
		
		await client.add_reaction(message,'🕵')
		
		cpf1 = random.randint(100,500)
		cpf2 = random.randint(100,500)
		cpf3 = random.randint(100,500)
		cpf4 = random.randint(10,99)
		
		embed = discord.Embed(title='CPF 🕵',description=str(cpf1)+'.'+str(cpf2)+'.'+str(cpf3)+'-'+str(cpf4),color=0x2dbced)
		await client.send_message(message.channel,embed = embed)

	#GERA UMA QUANTIDADE DE COINS ALEATORIO ADICIONA UMA REAÇÃO A MENSAGEM CRIADA PELO AUTOR E SEGUIDA SALVA NA DB
	if message.content.lower().startswith('?coins'):
		
		await client.add_reaction(message,'💰')
		coin = random.randint(1,100)

		with shelve.open('coins.db') as grava_coins:
			#VERIFICA SE O ID DO AUTOR DA MENSAGEM ESTA CONTIDO NO DB
			if not message.author.id in grava_coins:
				grava_coins[message.author.id] = coin
			else:
				grava_coins[message.author.id] += coin

		embed=discord.Embed(title='Coins',description='<@'+message.author.id+'>'+' Você recebeu '+str(coin)+' 💰',color=0xeddb2d)
		await client.send_message(message.channel,embed=embed)

	#PROCURA PELO ID DO AUTOR DA MENSAGEM NO DB E EM SEGUIDA ENVIA UMA MENSAGEM CONTENDO SEU NUMERO DE COINS
	if message.content.lower().startswith('?carteira'):
		
		with shelve.open('coins.db') as visualiza_coins:
			#VERIFICA SE AUTOR DA MENSAGEM NAO MENCIONOU NINGUEM E EM SEGUIDA EXIBE SUA CARTEIRA
			if message.author.id in visualiza_coins and not message.mentions:
				
				embed = discord.Embed(title='Carteira',description='<@'+message.author.id+'> Sua carteira tem um total de '+str(visualiza_coins[message.author.id])+' 💰.',color=0xdded2d)
				await client.send_message(message.channel,embed = embed)

			#VERIFICA SE HOUVE UMA MENÇÃO NA MENSAGEM E PROCURA PELO ID DE QM FOI MENCIONADO
			
			###INICIO###
			elif len(message.content) > 11:
				try:
					perfil = message.mentions[0].id
				except Exception:	
					pass

			#VERIFICA SE A VARIAVEL PERFIL Q FOI ARMAZENADA COM A MENÇÃO ESTA CONTIDA NA DB E EM SEGUIDA ENVIA UM AWAIT
				if perfil in visualiza_coins:
					
					embed = discord.Embed(title='Carteira',description='<@'+perfil+'> Possui '+str(visualiza_coins[perfil])+' 💰 em sua carteira.',color=0xeddb2d)
					await client.send_message(message.channel,embed=embed)
				
				else:
					#CASO CONTRARIO ELE IMPRIME UMA MENSAGEM AMIGAVEL
					embed = discord.Embed(title='Carteira',description='<@'+perfil+'> `Não possui carteira.`',color=0xeddb2d)
					await client.send_message(message.channel,embed=embed)
			###FIM###
			
			else:
				#CASO NENHUMA DAS EXEÇOES RETORNE TRUE O BOT ENVIA UMA MENSAGEM DIZENDO Q A CARTEIRA ESTA ZERADA 
				embed = discord.Embed(title='Carteira',description='<@'+message.author.id+'> Sua carteira esta 0 💰 digite ?coins para ganhar coins',color=0xdded2d)
				await client.send_message(message.channel,embed=embed)

	if  message.content.lower().startswith('?give'):
		try:
			ganha = message.mentions[0].id
			doa = ''
			position = 0
			for i in range(len(message.content)):
				if message.content[i] == '>':
					position = i
			for i in message.content[position:len(message.content)]:
				if i.isnumeric():
					doa += i
			recebe = int(doa)
			with shelve.open('coins.db') as doar:
				if message.author.id in doar:
					if message.author.id == ganha:
						embed = discord.Embed(title='Ops ! ❌',description='Você não pode doar um valor para você mesmo',color=0xff0000)
						await client.send_message(message.channel,embed=embed) 
					elif recebe > doar[message.author.id]:
						embed = discord.Embed(title='Ops ! ❌',description='Você não possui essa quantidade de coins para saber o valor da sua carteira digite \n**?carteira**',color=0xff0000)
						await client.send_message(message.channel,embed=embed)
					else:
						doar[message.author.id] -= recebe
						doar[ganha]	+= recebe
						embed = discord.Embed(title='Doa ❤',description='Você acabou de doar '+str(recebe)+' 💰 para <@'+ganha+'>',color=0xe2ff00)
						await client.send_message(message.channel,embed=embed)
		except:
			pass

	#GERA UMA EXEÇÃO TOTAL DA MENSAGEM PARA NAO BUGAR O BOT CASO VALORES INCORRETOS SEJAM FORNECIDOS
	try:	
		
		if message.content.lower().startswith('?soma'):
			#RECEBE A MENSAGEM DO AUTOR
			recebe = message.content
			#VERFICA A POSIÇÃO DO ELEMENTO + PARA PROCURAR POR NUMEROS 
			for i in range(len(recebe)):
				
				if '+' == recebe[i]:
					posicao = i
			#VARIAVEL PARA ARMAZENAR O 1 NUMERO PASSADO
			somaUm = ''
			#PERCORRE A MENSAGEM INDO DA ESQUERDA PARA DIREITA 
			for i in range(len(recebe[:posicao])):
				#VERIFICA SE O ELEMENTO PERCORRIDO E UM NUMERO SE ISSO ACONTECER ELE ARMAZENA NA VARIAVEL
				if recebe[i].isnumeric():
					somaUm += recebe[i]
			#VARIVEL CRIADA PARA ARMAZENAR O 2 VALOR 
			somaDois = ''
			#VARIVEL PARA RECEBER O TAMANHO DA STRING
			novo = len(recebe)
			#PERCORRE A MENSAGEM NA DIREÇÃO DIREITA DEPOIS DO SINAL DE ATRIBUIÇÃO
			for i in recebe[posicao:novo]:
				#SE O ELEMENTO PASSADO FOR UM NUMERO ELE ADICIONA NA VARIAVEL DE SOMA 2
				if i.isnumeric():
					somaDois += i
			#REALIZA A SOMA DOS NUMEROS ENCONTRADOS
			soma_definida = int(somaUm) + int(somaDois)
			
			embed = discord.Embed(title='Soma',description='Resultado : `'+str(soma_definida)+'`')
			await client.send_message(message.channel,embed=embed)
	
	except Exception:
		#CASO CONTRARIO OS VALORES PASSADOS SAO INCORRETOS E BOT GERA UMA MENSAGEM AMIGAVEL
		await client.send_message(message.channel,'`Eu não sou capaz de somar esses valores.`')

	#MESMO PROCEDIMENTO GERANDO UMA EXEÇÃO TOTAL
	try:	
		#TODOS OS COMENTARIOS DA SOMA VALEM PARA ESSA PARTE
		if message.content.lower().startswith('?diminuir'):
			
			recebe = message.content
			
			for i in range(len(recebe)):
				
				if '+' == recebe[i]:
					posicao = i
			
			menosUm = ''
			
			for i in range(len(recebe[:posicao])):
				
				if recebe[i].isnumeric():
					menosUm += recebe[i]
			
			menosDois = ''
			novo = len(recebe)
			
			for i in recebe[posicao:novo]:
				
				if i.isnumeric():
					menosDois += i
			
			soma_definida = int(menosUm) - int(menosDois)
			
			embed = discord.Embed(title='Soma',description='Resultado : `'+str(menos_definida)+'`')
			await client.send_message(message.channel,embed=embed)
	
	except Exception:
		
		await client.send_message(message.channel,'`Eu não sou capaz de diminuir esses valores.`')
	###FIM###
	

	if message.content.lower().startswith('?multi'):
	#TODOS OS COMENTARIOS DA SOMA VALEM PARA ESSE TRECHO DO PROGRAMA	
		try:
			
			recebe = message.content
			
			for i in range(len(recebe)):
				
				if '*' == recebe[i]:
					posicao = i
			
			multiUm = ''
			
			for i in range(len(recebe[:posicao])):
				
				if recebe[i].isnumeric():
					multiUm += recebe[i]
			
			multiDois = ''
			novo = len(recebe)
			
			for i in recebe[posicao:novo]:
				
				if i.isnumeric():
					multiDois += i
			
			multi_definida = int(multiUm) * int(multiDois)
			
			embed = discord.Embed(title='Multiplicação',description='Resultado : `'+str(multi_definida)+'`')
			await client.send_message(message.channel,embed=embed)
		
		except Exception:
			
			await client.send_message(message.channel,'`Eu não sou capaz de multiplicar esses valores.`')
		##FIM###

	if message.content.lower().startswith('?divi'):
		#TODOS OS COMENTARIOS DA SOMA VALEM PARA ESTA PARTE
		try:
			
			recebe = message.content
			
			for i in range(len(recebe)):
				
				if '/' == recebe[i]:
					posicao = i
			
			diviUm = ''
			
			for i in range(len(recebe[:posicao])):
				
				if recebe[i].isnumeric():
					diviUm += recebe[i]
			
			diviDois = ''
			agora_vai = len(recebe)
			
			for i in recebe[posicao:agora_vai]:
				
				if i.isnumeric():
					diviDois += i
			
			divi_definida = int(diviUm) / int(diviDois)
			
			embed = discord.Embed(title='Divissão',description='Resultado : `'+str(divi_definida)+'`')
			await client.send_message(message.channel,embed=embed)
		
		except Exception:
			
			await client.send_message(message.channel,'`Eu não sou capaz de dividir esses valores`')
		###FIM####

	#MENSAGEM LEGAL DE POSITIVO DO NARUTO
	if message.content.startswith('?positivo'):
		
		response = requests.get("http://138.68.18.62/wp-content/uploads/2017/04/4625957a-0afb-4bdc-9035-8d4ac902fd14.png", stream=True)
		await client.send_file(message.channel, io.BytesIO(response.raw.read()), filename='positivo.png', content='`Positivo chefe.`')
	
	#MENSAGEM LEGAL OBSERVANDO DO MADARA
	if message.content.startswith('?observando'):
		
		response = requests.get('https://kanto.legiaodosherois.com.br/w750-h1200/wp-content/uploads/2017/11/legiao_ZALP7wFQuh0k4DqTeIc8z3tYbaGvWxKJHigN6oBSVX.jpg',stream=True)
		await client.send_file(message.channel,io.BytesIO(response.raw.read()),filename='observando.png',content='`To de olho 🕵`')		

	#GERA UM GIF ALEATORIO DO NOME PASSADO
	if message.content.lower().startswith('?gif'):
		#RECEBE A PARTE DA MENSAGEM COM O NOME DO GIF
		gif_tag = message.content[5:]
		gera = legal.random(tag=str(gif_tag))

		#BAIXA O GIF
		image = requests.get(str(gera.get('data',{}).get('image_original_url')),stream=True)
		
		await client.send_file(message.channel, io.BytesIO(image.raw.read()),filename='image.gif')

	#IMPRIME MENSAGEM DE INFORMAÇÃO DA CONTA DO USUARIO
	if message.content.lower().startswith('?user'):
		#TODOS OS METODOS USADOS AQUI SAO SIMPLES E ESTAO NA DOC DO DISCORD
		try:
			
			try: 
				
				userinfo = message.mentions[0]
			
			except Exception:
				
				userinfo = message.author
			
			avatar = str(userinfo.avatar_url)
			data = str(userinfo.joined_at).split('.',1)[0]
			criada = str(userinfo.created_at).split('.',1)[0]
			#GERANDO UM EMBED COM AS INFORMAÇÕES DO USER
			userembed = discord.Embed(title='Nick : ',description=userinfo.name,color=0xb61eca)
			userembed.set_author(name='Informação do User')
			userembed.set_thumbnail(url=avatar)
			userembed.add_field(name='Entrou no servidor : ',value=data,inline=True)
			userembed.add_field(name='Conta criada : ',value=criada)
			userembed.add_field(name='Info :  ',value=userinfo.discriminator)
			userembed.add_field(name='ID : ',value=userinfo.id,inline=False)
			userembed.add_field(name='Status :',value=userinfo.status,inline=True)
			userembed.add_field(name='Playing',value=userinfo.game)

			teste = [str(i).strip('@') for i in userinfo.roles]
			cargos = ','.join(teste)
			
			userembed.add_field(name='Cargos : ',value=cargos,inline=False)
			userembed.add_field(name='Tempo : ',value=str(hora)+' Horas e '+str(minutos)+' minutos online no servidor')
			userembed.set_author(name = userinfo.name,icon_url=avatar)
			
			await client.send_message(message.channel,embed=userembed)
		
		except Exception:
			
			await client.send_message(message.channel,'`Ops! Utilize ?user ou ?user **menção**`')
	#FIM

	#VISUALIZAÇÃO DO AVATAR
	if message.content.lower().startswith('?avatar'):
		
		try:
			
			userinfo = message.mentions[0]
		
		except Exception:
			
			userinfo = message.author
		
		avatar = str(userinfo.avatar_url)
		
		userembed = discord.Embed(title='Avatar',description=userinfo.name,color=0xca811e)
		userembed.set_image(url=avatar)
		await client.send_message(message.channel,embed=userembed)

	#GERA XP BASEADO NO TAMANHO DA MENSAGEM DIGITADA E GUARDA NO DB
	if message.content:
		
		with shelve.open('xp.pck') as rank:
			
			if not message.author.id in rank:
				
				rank[message.author.id] = len(message.content)
			
			else:
				
				rank[message.author.id] += len(message.content)
	
	#PROCURA NO DB PELO ID DO AUTHOR DA MENSAGEM E EXIBE SUA QUANTIDADE XP
	if message.content.lower().startswith('?xp'):
		
		with shelve.open('xp.pck') as rank:
			
			if message.author.id in rank:
				
				embed = discord.Embed(title='XP',description='<@'+message.author.id+'> Sua quantidade total de XP '+str(rank[message.author.id]),color=0x6bf7e0)
				await client.send_message(message.channel,embed=embed)
			
			else:
				
				embed = discord.Embed(title='XP',description='<@'+message.author.id+'> Voce ainda não possui XP')
				await client.send_message(message.channel,embed=embed)
	
	#EXIBE O RANK DOS TOP EM XP
	if message.content.startswith('?rank'):
		
		membros = message.author.server.members
		ident = [i.id for i in membros]
		
		rank = discord.Embed(title='Rank',description='Jogadores no rank de xp',color=0x9bf76b)
		
		with shelve.open('xp.pck') as xp:
			lista = []
			#RECEBE O NOME E O ID DOS USERS
			for i in ident:		
				if i in xp:			
					lista.append([xp[i],'<@'+str(i)+'>'])
		#ORDENA OS USERS
		rank = sorted(lista,reverse=True)
		#TITLE DO RANK
		list_rank = discord.Embed(title='Top Rank : ',description='Rank baseado na contabilizade de xp',color=0x9bf76b)
		cont = 1
		#PERCORRE TODOS OS USERS E ENVIA UM EMBED
		for orde in rank:
			list_rank.add_field(name='Rank '+str(cont),value=orde[1]+'  Total de xp : '+str(orde[0]),inline=False)
			cont += 1	
		
		await client.send_message(message.channel,embed=list_rank)
	
	#EXIBE TODAS AS INFORMAÇÕES DO SERVIDOR
	if message.content.lower().startswith('?servidor'):
		#RECEBE A QUANTIDADE DE MEMBROS E O AVATAR DO SERVIDOR
		membros = message.author.server.member_count
		avatar_serve = message.author.server.icon_url
		#RECEBE TODOS OS CARGOS DO SERVIDOR
		servidor_cargos = [str(i).strip('@') for i in message.author.server.roles]
		#SEPARA TODOS OS CARGOS DO SERVIDOR PARA SEREM IMPRIMIDOS
		cargo_pronto = ' ,'.join(servidor_cargos) 
		#RECEBE A DATA DE CRIAÇÃO DO SERVIDOR
		criado_server = str(message.author.server.created_at).split('.',1)[0]
		
		servidor = discord.Embed(title='Servidor',description='Informação do servidor',color=0x9dee56)
		servidor.set_thumbnail(url=avatar_serve)
		servidor.add_field(name='Membros : ',value='    '+str(membros))
		servidor.set_author(name=message.author.server.name,icon_url=avatar_serve)
		servidor.add_field(name='Servidor criado : ',value=criado_server)
		servidor.add_field(name='Canal Default: ',value=message.author.server.default_channel,inline=True)
		servidor.add_field(name='Cargo Default:',value=message.author.server.default_role)
		servidor.add_field(name='Cargos:',value=cargo_pronto,inline=False)
		servidor.add_field(name='Região:',value=message.author.server.region,inline=True)
		servidor.add_field(name='ID:',value=message.author.server.id)
		await client.send_message(message.channel,embed=servidor)

	#OWNER DO SERVER ADICIONA CARGOS PARA PODEREM USAR ?CLEAR
	if message.content.lower().startswith('?add') and message.author.id == message.author.server.owner.id:
		#RECEBE O CARGO MENCIONADO
		mencion = message.content[5:]
		#SEPARA TODOS OS ATRIBUTOS PARA PEGAR O ID
		novo = mencion.strip('<@').strip('&').rstrip('>')
		#RECEBE TODOS OS CARGOS DO SERVIDOR
		cargos = [i.id for i in message.author.server.roles]
		#VERIFICA SE O CARGO PASSADO ESTA NOS CARGOS DO SERVIDOR
		if novo in cargos:
			with shelve.open('permissao.pck') as permissao:
				#VERIFICA SE O CARGO N ESTA CONTIDO NA DB
				if not novo in permissao:
					#CASO N ESTEJA O CARGO PASSADO RECEBE PERMISSAO
					permissao[novo] = True
					embed = discord.Embed(title='☑',description='O cargo foi adiconado e pode utilizar comandos especiais do BOT.',color=0x19b7de)
					await client.send_message(message.channel,embed=embed)
				else:
					#SE O CARGO JA ESTIVER NA DB ELE ENVIA UMA MENSAGEM AMIGAVEL
					embed = discord.Embed(title='✖',description='Cargo já foi adicionado.',color=0xde191f)
					await client.send_message(message.channel,embed=embed)
		else:
			#CASO ELE PASSE UM CARGO INVALIDO GERAMOS UMA EXECAO
			embed = discord.Embed(title='✖',description='Cargo não pode ser adicionado',color=0xde191f)
			await client.send_message(message.channel,embed=embed)
	#OWNER REMOVE UM CARGO E TIRA SUA PERMISSAO DE USAR ?CLEAR
	if message.content.lower().startswith('?remove') and message.author.id == message.author.server.owner.id:
		#RECEBE O CARGO
		mencao = message.content[8:]
		#SEPARA TODOS OS ELEMENTOS DESNECESSAARIOS
		novo = mencao.strip('<@').strip('&').strip('>')
		with shelve.open('permissao.pck') as permissao:
			#VERIFICA SE O CARGO ESTA NO DB
			if novo in permissao:
				#CASO ESTEJA O BOT REMOVE O CARGO
				del permissao[novo]
				embed = discord.Embed(title='☑',description='Cargo removido .',color=0x19b7de)
				await client.send_message(message.channel,embed=embed)
			else:
				#CASO PASSE UM CARGO INVALIDO BOT GERA UMA MENSAGEM AMIGAVEL
				embed = discord.Embed(title='✖',description='Cargo nao adiconado impossivel remover.',color=0xde191f)
				await client.send_message(message.channel,embed=embed)
	#REMOVE UMA QUANTIDADE DE MENSAGEM DO SERVIDOR 
	if message.content.startswith("?clear"):
		#RECEBE O ID DO DONO DO SERVIDOR
		permite = message.author.server.owner.id
		adiconado = [str(i.id) for i in message.author.roles]
		#VERIFICA SE QUEM DIGITOU O CLEAR ESTA NAS PERMISSOES DE APAGAR A MENSAGEM
		verifica = Verficia(adiconado)
		if message.author.id == permite or verifica == True:
			#CASO ESTIVER ELE APAGA AS MENSAGENS
			try:
				mensagem = message.content.split()
				if not (re.findall('[0-9]',mensagem[1])):
					return
				if(int(mensagem[1]) > 100):
					mensagem[1] = 100
				print("\033[91mApagando", mensagem[1], "\033[39m")
				list_msg = []
				async for x in client.logs_from(message.channel, limit = int(mensagem[1])):
					list_msg.append(x)
				await client.delete_messages(list_msg)
			except Exception:
				pass

def Verficia(recebe):
	with shelve.open('permissao.pck') as limpa:
		verifica = False
		for i in recebe:
			if i in limpa:
				verifica = True
	return verifica
@client.event
async def on_member_join(member):
	try:
		serverchannel = member.server.default_channel
		print(serverchannel)
		embed = discord.Embed(title='Bem Vindo',description=member.mention+' Acabou de apararecer no '+member.server.name,color=0xeddb2d)
		await client.send_message(serverchannel,embed=embed)
	except:
		pass

@client.event
async def on_member_remove(member):
	serverchannel = member.server.default_channel
	embed = discord.Embed(title='Bye bye',description=member.mention+' Acabou de ser sair do Servidor.',color=0xfc4141)
	await client.send_message(serverchannel,embed=embed)

async def uptime():
	await client.wait_until_ready()
	global minutos
	minutos = 0
	global hora
	hora = 0
	while not client.is_closed:
		await asyncio.sleep(60)
		minutos += 1
		if minutos == 60:
			minutos = 0
			hora += 1
client.loop.create_task(uptime())
client.run('NDA1Nzc4ODg4ODEyMjY1NDky.DUsWrg.IN7zRFGHunVjwKVzSsT7TzUZFAQ')