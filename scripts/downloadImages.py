from rdflib import Graph, URIRef
from bs4 import BeautifulSoup
import requests, time, os.path


g = Graph()
g.parse("names.nt", format="nt")


urlPatern = 'http://cdm16313.contentdm.oclc.org/utils/getdownloaditem/collection/p16313coll33/id/{imageid}/type/singleitem/filename/file.jpg/width/{width}/height/{height}/mapsto/image/filesize/0/title/0/size/medium'


for subject,predicate,obj in g:

	if predicate == URIRef("http://xmlns.com/foaf/0.1/depiction"):

		#print (obj)
		id = obj.split('/id/')[1]

		#check if we have the file, if it errored out half way and needed to restart
		if os.path.isfile('imgs/' + id + '.jpg') == False:

			print("Downloading",obj)

			r = requests.get(obj)

			if r.status_code == 200:	
				soup= BeautifulSoup(r.text)		


				cdm_item_width = soup.find("input", {"id": "cdm_item_width"}).attrs['value']
				cdm_item_height = soup.find("input", {"id": "cdm_item_width"}).attrs['value']

				downloadUrl = urlPatern.replace('{imageid}',id).replace('{width}',cdm_item_width).replace('{height}',cdm_item_height)
				print (downloadUrl)


				with open('imgs/' + id + '.jpg', 'wb') as handle:

					response = requests.get(downloadUrl, stream=True)

					if not response.ok:
						# Something went wrong
						print("Error downloading",id)

					for block in response.iter_content(1024):

						if not block:
							break

						handle.write(block)


				
			else:
				print ("There was an error with", obj)
				


			time.sleep(0.5)

		else:

			print("Skipping",id)