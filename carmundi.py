import requests 
from bs4 import BeautifulSoup
import json
import csv

finallist = []

def crawl(l):
	if l=="http://en.carmudi.ae//2009-bmw-3-series-325i-113945-43.html":
		return
	print l
	f = requests.get(l)
	data = f.text
	soup = BeautifulSoup(data,"html.parser")
	imglist = []
	newitem = dict()
	newitem["url"] = ""
	newitem["userid"] = ""
	newitem["address"] = ""
	newitem["model"] = ""
	newitem["year"] = ""
	newitem["brand"] = ""
	newitem["imgurl"] = ""
	newitem["carcondition"] = ""
	newitem["transmissiontype"] = ""
	newitem["fueltype"] = ""
	newitem["cc"] = ""
	newitem["price"] = ""
	newitem["desc"] = ""

	#LOCATION
	try:
		address = soup.find("div",{"id":"addressBlock"})
		addressinside = address.find("address").text.strip()
		newitem["address"] = addressinside
	except:
		pass
	#print addressinside

	#USER
	try:
		username = soup.find("p",{"class":"left dealer-name"}).find("strong").text
		newitem["userid"] = username
	except:
		pass
	#print username

	#PRICE
	try:
		price = soup.find("div",{"class":"left small-6 medium-8 price"}).find("div",{"class":"type-xl"}).text.encode("utf-8").strip()
		newitem["price"] = price
	except:
		pass
	#print price

	#BRAND,MDOEL AND YEAR
	try:
		breadcrumbs = soup.find("ol",{"class":"breadcrumbs"})
		breadcrumbsli = breadcrumbs.find_all("li")
		model = breadcrumbsli[3].find("span").text
		brand = breadcrumbsli[2].find("span").text
		year = breadcrumbsli[4].find("span").text.replace(model,"").replace(brand,"")
		newitem["model"] = model
		newitem["year"] = year
		newitem["brand"] = brand
	except:
		pass
	#print brand,model,year

	#IMAGES
	try:
		images = soup.find("div",{"class":"listing-images"})
		for img in images.find_all("img",{"class":"lazy"}):
			link =  img["data-original"]
			imglist.append(link)
		newitem["imgurl"] = imglist
	except:
		pass

	#ROM DETAILS
	try:
		techbar = soup.find("div",{"class":"tech-bar clearfix"})
		techbarcols = techbar.find_all("div",{"class":"column attribute"})
		try:
			carcondition = techbarcols[0].find("b").text
		except:
			carcondition = techbarcols[0].find("span").text
		cartransmission = techbarcols[1].find("span").text
		cartype = techbarcols[2].find("span").text
		carcc = techbarcols[3].find("span").text
		newitem["carcondition"] = carcondition
		newitem["transmissiontype"] = cartransmission
		newitem["fueltype"] = cartype
		newitem["cc"] = carcc
	except:
		pass
	
	#print cartype,carcc

	#REST OF THE SPECIFICATION
	try:
		clearfix = soup.find("div",{"class":"accordions clearfix"})
		clearfixcols = clearfix.find_all("div",{"class":"dropclick selected"})
		detaildiv = clearfixcols[0]
		twodivleft = detaildiv.find("div",{"class":"small-12 medium-6 left"})
		twodivright = detaildiv.find("div",{"class":"small-12 medium-6 right"})
		carcolorspan = twodivleft.find("li").find("span").text.strip()
		carcolor = twodivleft.find("li").text.replace(carcolorspan,"").strip()
		
		careditionspan = twodivright.find("li").find("span").text.strip()
		caredition = twodivright.find("li").text.replace(careditionspan,"").strip()
		newitem["color"] = carcolor
		newitem["edition"] = caredition
	except:
		pass

	#DESCRIPTION
	try:
		desc = soup.find("div",{"class":"description clearfix"}).find("p").text
		newitem["desc"] = desc
	except:
		pass
	#print desc
	newitem["url"] = l.replace("http://en.carmudi.ae//","")
	
	
	
	
	
	

	with open('catalog_config_selective_data.csv', 'r') as f:
	     reader = csv.reader(f, delimiter=',') # good point by @paco
	     for row in reader:
	     	if row[2] == newitem["url"]:
	     		newitem["id"] = row[0]
	print newitem
	finallist.append(newitem)


def mainlinks(l,num):
	f = requests.get(l+str(num))
	data = f.text
	soup = BeautifulSoup(data,"html.parser")
	i=num+1
	maincontent = soup.find_all("div",{"class":"gallery-image"})
	for x in maincontent:
		link =  x.find("a")['href']
		newlink = "http://en.carmudi.ae/"+link
		crawl(newlink)
	with open('carmundi.json', 'w') as f:
			json.dump(finallist, f)	
	if soup.find("div",{"class":"next-page"}):
			mainlinks(l,i)

mainlinks("http://en.carmudi.ae/all/?sort=newest&page=",643)
