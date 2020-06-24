import xml.etree.ElementTree as ET
with open('locations.xml','r') as file:
	contents = file.read()

tree = ET.fromstring(contents)	#tree represents the root node of the xml file which is tagset
tags = tree.findall(".//taggedRectangle")
attribs = ['x','y','width','height']
x = []
y = []
width = []
height = []
imageName = []

# for tag in tags:
# 	x.append(tag.get('x'))
# 	y.append(tag.get('y'))
# 	width.append(tag.get('width'))
# 	height.append(tag.get('height'))
# 	print(type(tag))
# 	print(tag.tag)
# 	print(type(temp))
# 	break

tag = tags[0]
tag = tree.find('./image/imageName')
print(tag)
parent = tag.find("./..imageName")
print(parent)