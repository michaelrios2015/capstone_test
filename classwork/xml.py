#in theory I would get a bunch of XML data and look for accidentsAndIncidents and then get location
# description... it's a way of sending information JSON is more popular now 

# so they always start with event so I guess you just look for event then start getting the information an d

# so in python i just know how to read things a line at a time... how would that work
# 
# oh well there is a library so that works https://docs.python.org/3/library/xml.etree.elementtree.html

#511ny.org

import xml.etree.ElementTree as ET
tree = ET.parse('classwork/test.xml')
root = tree.getroot()

print(root.tag)

for child in root:
    print(child.tag, child.attrib)

print(root[0][1].text)

for location in root.iter('Location'):
    print(location.text)

# something like that but you then check some other stuff