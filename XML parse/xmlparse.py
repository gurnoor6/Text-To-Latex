import xml.etree.ElementTree as ET

def getRectLocation(filename="locations.xml"):
	name =[]
	x=[]
	y=[]
	w=[]
	h=[]

	tree = ET.parse(filename)
	root = tree.getroot()
	image = root.findall('image')
	for img in image:
		image_name =img.find('imageName').text
		tagged_rects = img.find('taggedRectangles').findall('taggedRectangle')
		for rect in tagged_rects:
			name.append(image_name)
			x.append(int(rect.attrib['x'].split(".")[0]))
			y.append(int(rect.attrib['y'].split(".")[0]))
			w.append(int(rect.attrib['x'].split(".")[0])+int(rect.attrib['width'].split(".")[0]))
			h.append(int(rect.attrib['y'].split(".")[0])+int(rect.attrib['height'].split(".")[0]))

	zipped = list(zip(name,x,y,w,h))
	return zipped

if __name__=='__main__':
	print(getRectLocation())