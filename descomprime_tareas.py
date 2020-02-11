import os
import io
import shutil
from zipfile import ZipFile

def descomprimir():

	path = os.getcwd()

	for archivo_zip in os.listdir(path):
		if archivo_zip.endswith(".zip"):
			dir = archivo_zip.split(".")[0]
			
			try:
				os.mkdir(dir)
			except FileExistsError:
				shutil.rmtree((path + "/" + dir))

			# En python3 se debería usar shutil pero si lo hago así no me sale la "flechita" para abrir la carpeta en el navegador en modo
			# vista de lista --> Pequeñísimo detalle pero por mi comodidad así lo prefiero
			#shutil.unpack_archive(archivo_zip, dir)

			with ZipFile(archivo_zip, 'r') as zipObj:
		   		zipObj.extractall(dir)
		else:
		 	pass
		
	items = os.listdir(dir)

	for item in items:		

		object = os.path.join(path, dir, item)

		if os.path.isdir(object):
			directorio = os.listdir(object)
			fichero = object + "/" + str(directorio[0])
			unzip(fichero, object)
		elif os.path.isfile(object):
			pass

				
def unzip(fichero, object):
		try:
			shutil.unpack_archive(fichero, object)
		except:
			pass

if __name__ == '__main__':
	descomprimir()