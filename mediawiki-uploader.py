import wikitools
import poster
import pyexiv2
import os
import shutil

wiki_url = "MediaWiki API url here"

#Example: http://commons.wikimedia.org/w/api.php

wiki_username = "USER NAME HERE"
wiki_password = "PASSWORD HERE"

category = "TamilWiki Media Contest"

try:
	wiki = wikitools.wiki.Wiki(wiki_url)
except:
	print "Can not connect with wiki. Check the URL"


try:
	wiki.login(username=wiki_username,password=wiki_password)

except:
	print "Invalid Username or Password"

path = './'

listing = os.listdir(path)

def filetype(file):
	return file.split(".")[-1]

def filename(file):
	return file.split(".")[-2]


def get_file_details(image):
	try:
		metadata = pyexiv2.ImageMetadata(image)
		metadata.read()
		file_name=metadata['Iptc.Application2.Headline'].raw_value[0].strip()
		caption=metadata['Iptc.Application2.Caption'].raw_value[0].strip()
		file_meta = {'name':file_name,'caption':caption}
		return file_meta
	except:
		print "No tag is set for the image " + image	
		exit	

	
def move_photo(image):
	source = image
	destination = "./uploaded/"+image

	if os.path.isdir("uploaded"):
		shutil.move(source,destination)
	else:
		os.mkdir("uploaded")
		shutil.move(source,destination)		
	print "Moving the Photo " + image + " to the folder 'uploaded' "

def uploadphoto(image):
	meta = get_file_details(image)	
	
	if meta:
		file_name = meta['name']
		caption = meta['caption']
		
		image_object=open(image,"r")
		picture=wikitools.wikifile.File(wiki=wiki, title=file_name)
        	picture.upload(fileobj=image_object,comment=caption, ignorewarnings=True)
		print "Uploaded the Image " + file_name

		page_name = file_name.replace(" ","_")

		page = wikitools.Page(wiki, "File:" + page_name + ".jpeg", followRedir=True)
		wikidata = "=={{int:filedesc}}=={{Information|description={{en|1= " + caption + "}}{{TamilWiki Media Contest}}|source={{own}}|author=[[User:" + wiki_username + "|" + wiki_username + "]]}}=={{int:license-header}}=={{self|cc-by-sa-3.0}}[[Category:" + category + "]] [[Category:Uploaded with MediawikiUploader]]"

		page.edit(text=wikidata)

		move_photo(image)
		
for photo in listing:
	if filetype(photo) in ['JPG','jpg','GIF','gif','png','PNG']:
		uploadphoto(photo)
		



