import xml.etree.ElementTree as ET
tree = ET.parse('hbsDrawing.svg')
root = tree.getroot()


#%%





#%%


f = open("hbsDrawing.svg",'r')
text = f.read()
f.close()
ids = ["path3061-0-4"]

tag = ids[0]
regex = f"({tag})([^/]*)(/>)"
p = re.compile(regex)
result = p.search(text)
backslash_idx = result.span()[1]-2
anim = '\n<animate attributeName="stroke-opacity" values="0.5;0.5;1;0.5;0.5" dur="5s" repeatCount="indefinite" />'
ender = '\n</path>'

#%% find layer, make mask with id

layer = "layer4"
position = text.find(f'id="{layer}"')
group_openers = text.("<g")
group_closers = text.find("/g>")

distances = [openpos - position for openpos in group_openers if openpos - position > 0]


#%%

newtext = text[:backslash_idx] + " >" + anim + ender + text[backslash_idx+2:]
f = open("hbsAnim.svg","w")
f.write(newtext)
f.close()

#%%

from xml.dom import minidom

doc = minidom.parse("hbsDrawing.svg")  # parseString also exists
path_strings = [path.getAttribute('id') for path
                in doc.getElementsByTagName('g')]
doc.unlink()

