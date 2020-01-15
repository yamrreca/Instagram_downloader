from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from urllib.request import urlopen
from bs4 import BeautifulSoup
from os.path import join as pathjoin
from sys import argv
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

def downloadIG(argv):
	

	def downloadIGFile(numArchivo):
		vids = bsObj.find('video')
		if vids is not None: #Ve si hay un tag de video
			html = urlopen(vids['src'])
			with open(pathjoin(argv[2], argv[3] + str(numArchivo) + '.mp4'),'wb') as video:
				video.write(html.read())
		else: #Si no lo hay significa que es imagen
			imgs = bsObj.findAll('img',{'class':'FFVAD'})
			html = urlopen(imgs[-1]['src']) #Hay un montón de tags img. El bueno es el último
			with open(pathjoin(argv[2], argv[3] + str(numArchivo) + '.jpg'),'wb') as imagen:
				imagen.write(html.read())
		print('Se ha guardado la imagen/video %d'%(numArchivo))
		numArchivo += 1
		return numArchivo


	def saveAlbumFile(numBrincos, numArchivo,primeraVez = False):
	
		"""Obtiene las imágenes de un álbum dependiendo de la posición del driver. Regresa el número actual de imágenes que se han guardado más uno, esto para que se puedan nombrar correctamente los archivos.
		
		Los álbumes de Instagram no son tan sencillos como los archivos por sí solos. Básicamente, mientras que en los archivos se podía determinar si era imagen o video buscando el tag video, aquí este puede aparecer
		aun en imágenes ya que para cada archivo aparecen los tags no solamente de ese archivo, sino también de los dos adyacentes. El método para obtener los archivos es entonces el posicionarse en un archivo y obtener
		tres archivos: en el que se está (el 'presente'), el pasado y el subsecuente en el álbum. Una vez que se obtienen los tres archivos, para los siguientes tres se debe mover el driver tres posiciones a la derecha.
		En el siguiente diagrama se observa un esquema de las tres imágenes en el orden que aprecerían en el álbum.
		
		
		---------------           ---------------           ---------------
		-             -           -             -           -             -
		- antecedente -           -   presente  -           - subsecuente -
		-             -           -             -           -             -
		---------------           ---------------           ---------------
		
		
		La gran cantidad de if-else's que hay en esta función se debe a que la cantidad exacta y la calidad (i.e. si es imagen o video) de archivos depende de si se está al 
		final del álbum o no y en cuántos pasos se llegó ahí desde el último presente"""
		
		logging.info('Se está en la función saveAlbumFile')
		bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
		vids = bsObj.findAll('video')  #Ve si hay algún video para que la función que descarga las tres imágenes sepa qué acción tomar
		for vid in vids:
			logging.info('links a los videos: %s'%(vid['src']))
		if bsObj.find('div',{'class':'coreSpriteRightChevron'}) is not None: #Si no está al final del álbum
			logging.info('No se está al final del álbum')
			if len(vids) == 0:
				logging.info('longitud de vids: None')
				imgs = bsObj.findAll('img',{'class':'FFVAD'})
				lastimgs = imgs[-3:]
				logging.info('longitud de lastimgs: %d'%(len(lastimgs)))
				for i, imgTag in enumerate(lastimgs):
					html = urlopen(imgTag['src'])
					with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
						imagen.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))
			elif len(vids) == 1:
				logging.info('longitud de vids: %d'%(len(vids)))
				imgs = bsObj.findAll('img',{'class':'FFVAD'})
				lastimgs = imgs[-2:]
				logging.info('longitud de lastimgs: %d'%(len(lastimgs)))
				for i, imgTag in enumerate(lastimgs):
					html = urlopen(imgTag['src'])
					with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
						imagen.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))
				for i, vidTag in enumerate(vids):
					html = urlopen(vidTag['src'])
					with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
						video.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))

			elif len(vids) == 2:
				logging.info('longitud de vids: %d'%(len(vids)))
				imgs = bsObj.findAll('img',{'class':'FFVAD'})
				lastimgs = imgs[-1:]
				logging.info('longitud de lastimgs: %d'%(len(lastimgs)))
				for i, imgTag in enumerate(lastimgs):
					html = urlopen(imgTag['src'])
					with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
						imagen.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))
				for i, vidTag in enumerate(vids):
					html = urlopen(vidTag['src'])
					with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
						video.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))
			else:
				logging.info('longitud de vids: %d'%(len(vids)))
				logging.info('longitud de lastimgs: None')
				for i, vidTag in enumerate(vids):
					html = urlopen(vidTag['src'])
					with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
						video.write(html.read())
					numArchivo += 1
					logging.info('numArchivo: %d'%(numArchivo))

		else: #Cuando está al final del álbum
			logging.info('Se está al final del álbum')
			if numBrincos == 3:
				logging.info('numBrincos = %d'%(numBrincos))
				if len(vids) == None:
					logging.info('longitud de vids: None')
					imgs = bsObj.findAll('img',{'class':'FFVAD'})
					lastimgs = imgs[-2:]
					logging.info('longitud de imgs: %d'%(len(lastimgs)))
					for i, imgTag in enumerate(lastimgs):
						html = urlopen(imgTag['src'])
						with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
							imagen.write(html.read())            
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
						
				elif len(vids) == 1:
					logging.info('longitud de vids: %d'%(len(vids)))
					imgs = bsObj.findAll('img',{'class':'FFVAD'})
					lastimgs = imgs[-1:]
					logging.info('longitud de imgs: %d'%(len(lastimgs)))
					
					for image in imgs:
						logging.info('clases de las imágenes: %s'%(image['class']))
						
					for i, imgTag in enumerate(lastimgs):
						html = urlopen(imgTag['src'])
						with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
							imagen.write(html.read())
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
					for i, vidTag in enumerate(vids):
						html = urlopen(vidTag['src'])
						with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
							video.write(html.read())
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
				else:
					logging.info('longitud de vids: %d'%(len(vids)))
					for i, vidTag in enumerate(vids):
						html = urlopen(vidTag['src'])
						with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
							video.write(html.read())
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
			elif numBrincos == 2:
				logging.info('numBrincos = %d'%(numBrincos))
				if len(vids) == 0:
					logging.info('longitud de vids: 0')
					imgs = bsObj.findAll('img',{'class':'FFVAD'})
					lastimgs = imgs[-1:]
					logging.info(lastimgs)
					logging.info('longitud de imgs: %d'%(len(imgs)))
					for i, imgTag in enumerate(lastimgs):
						print(i,imgTag)
						html = urlopen(imgTag['src'])
						with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
							imagen.write(html.read())
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
				else:
					logging.info('longitud de vids: %d'%(len(vids)))
					for i, vidTag in enumerate(vids):
						html = urlopen(vidTag['src'])
						with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
							video.write(html.read())
						numArchivo += 1
						logging.info('numArchivo: %d'%(numArchivo))
			else:
				if primeraVez == False:
					logging.info('numBrincos = %d'%(numBrincos))
					pass
				else:
					logging.info('Es la primera parte del álbum')
					logging.info('numBrincos = %d'%(numBrincos))
					if len(vids) == 0:
						logging.info('longitud de vids: 0')
						imgs = bsObj.findAll('img',{'class':'FFVAD'})
						lastimgs = imgs[-2:]
						logging.info('longitud de lastimgs: %d'%(len(lastimgs)))
						for i, imgTag in enumerate(lastimgs):
							print(i,imgTag['src'])
							html = urlopen(imgTag['src'])
							with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
								imagen.write(html.read())
							numArchivo += 1
							logging.info('numArchivo: %d'%(numArchivo))
					else:
						logging.info('longitud de vids: %d'%(len(vids)))
						for i, vidTag in enumerate(vids):
							html = urlopen(vidTag['src'])
							with open(argv[2] + str(numArchivo) + '.mp4','wb') as video:
								video.write(html.read())
							numArchivo += 1
							logging.info('numArchivo: %d'%(numArchivo))
						imgs = bsObj.findAll('img',{'class':'FFVAD'})
						lastimgs = imgs[-1]
						logging.info(lastimgs)
						logging.info('longitud de lastimgs: %d'%(len(lastimgs)))
						for i, imgTag in enumerate(lastimgs):
							print(i,imgTag)
							html = urlopen(imgTag['src'])
							with open(argv[2] + str(numArchivo) + '.jpg','wb') as imagen:
								imagen.write(html.read())
							numArchivo += 1
							logging.info('numArchivo: %d'%(numArchivo))


		logging.info('numArchivo: %d'%(numArchivo))
		return numArchivo
		


	def downloadIGAlbum(numArchivo):
		logging.info('Se está en la función downloadIGAlbum')
		logging.info('numArchivo antes de dar el primer click: %d'%(numArchivo))
		smallRightArrowElem = driver.find_element_by_class_name('coreSpriteRightChevron')
		smallRightArrowElem.click()
		sleep(1.5)
		bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
		if bsObj.find('div',{'class':'coreSpriteRightChevron'}) is not None: #Si hay flecha:
			numArchivo = saveAlbumFile(3,numArchivo) #Guarda los tres archivos
			saltar = False
		else:
			numArchivo = saveAlbumFile(1,numArchivo,primeraVez = True)
			saltar = True
			
		logging.info('numArchivo después de dar el primer click: %d'%(numArchivo))
		
		bandera = True
		while bandera:
			numBrincos = 0
			bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
			
			if bsObj.find('div',{'class':'coreSpriteRightChevron'}) is not None: #Si no se ha llegado al final
				for i in range(3): #Se avanza tres entradas del álbum
					logging.info('Iteración %d en el loop que se mueve en el álbum'%(i))
					bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
					if bsObj.find('div',{'class':'coreSpriteRightChevron'}) is not None: #Si no se ha llegado al final
						smallRightArrowElem = driver.find_element_by_class_name('coreSpriteRightChevron')
						smallRightArrowElem.click()
						sleep(1.5)
						bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
						numBrincos += 1
					else: #Si se llegó al final
						bandera = False
						break
					sleep(1.5)
				sleep(1.5)
			elif saltar == False: #Si ya se llegó al final afuera del for
				numBrincos = 3
				numArchivo = saveAlbumFile(numBrincos,numArchivo) #Se corre aquí porque la otra llamada está dentro del while
				logging.info('numArchivo después de saveAlbumFile: %d'%(numArchivo))
				break
			else:
				break
		
			"""numArchivo = saveAlbumFile(numBrincos,numArchivo)
			logging.info('numArchivo después de saveAlbumFile: %d'%(numArchivo))
			"""
		return numArchivo

	if len(argv) < 3:
		print('Se debe escribir el nombre de usuario, el camino al directorio donde se van a guardar las imágenes y el nombre base de las imágenes, en ese orden')
		exit()
	#Primero se abre la página deseada
	driver = webdriver.Firefox()
	driver.get('https://www.instagram.com/' + argv[1] + '/')

	#Se checa que la página se haya cargado completamente

	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,'_9AhH0')))

	#Se abre la primera imagen

	imgLink = driver.find_element_by_class_name('_9AhH0')
	imgLink.click()
	WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'img')))
	numArchivo = 1 #Contador para saber en qué imagen se está
	while True: #Irá de imagen en imagen usando las flechas de siguiente hasta llegar a la última imagen
		bsObj = BeautifulSoup(driver.page_source, features = 'html.parser')
		dots = bsObj.find('div', {'class':'JSZAJ'})
		try:
			if dots is None:
				numArchivo = downloadIGFile(numArchivo)
				logging.info('numArchivo despues de downloadIGFile: %d'%(numArchivo))
			else:
				numArchivo = downloadIGAlbum(numArchivo)
				logging.info('numArchivo despues de downloadIGAlbum: %d'%(numArchivo))
		except Exception:
			print(Exception)
			pass
		if bsObj.find('a', {'class':'coreSpriteRightPaginationArrow'}) == None: #Se sale del while si está en la última imagen
			break
		arrowElem = driver.find_element_by_class_name('coreSpriteRightPaginationArrow') #Se va a la siguiente imagen
		arrowElem.click()
		sleep(1.5)
	print('Se han decargado todos los archivos')
	driver.close()




downloadIG(argv)