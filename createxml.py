'''
This is a practice
'''
import xml.etree.ElementTree as ET

def __indent(elem,level=0):
    i="\n" + level*"\t"
    if len(elem):
        if not elem.text or elem.text.strip():
            elem.text=i+"\t"
        if not elem.tail or elem.tail.strip():
                elem.tail=i
        for elem in elem:
            __indent(elem,level+1)
        if not elem.tail or elem.tail.strip():
            emel.tail=i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail=i

root=ET.Element('objectSet')
tree=ET.ElementTree(root)
root.set('ExportMode',"Standard")
root.set('Note',"TypesFirst")
root.set('Version',"2.0.3.45")
metaInformation=ET.Element('MetaInformation')
root.append(metaInformation)
exportmode=ET.Element('ExportMode')
exportmode.set('Value',"Standard")
metaInformation.append(exportmode)
runtimeversion=ET.Element('RuntimeVersion')
runtimeversion.set('Value',"2.0.3.45")
metaInformation.append(runtimeversion)
sourceversion=ET.Element('SourceVersion')
sourceversion.set('Value',"2.0.3.45")
metaInformation.append(sourceversion)
serverfullpath=ET.Element('ServerFullPath')
serverfullpath.set('Value',"/Server 1")
metaInformation.append(serverfullpath)
exportedobjects=ET.Element('ExportedObjects')
root.append(exportedobjects)
Oi=ET.Element('OI')
Oi.set('NAME',"modbus Interface001")
Oi.set('TYPE',"modbus.network.SlaveDevice")
exportedobjects.append(Oi)
Pi=ET.Element('PI')
Pi.set('Name',"Timeout")
Pi.set('Value',"1200")
Oi.append(Pi)
for i in range(2000):
    name="AnalogValue" + str(i+1)
    registnumber=100+i+1
    oi=ET.Element('OI')
    oi.set('NAME',name)
    oi.set('TYPE',"modbus.point.AnalogValue")
    pi=ET.Element('PI')
    pi.set('Name',"RegisterNumber")
    pi.set('Value', str(registnumber))
    pi1=ET.Element('PI')
    pi1.set('Name', "RegisterType")
    pi1.set('Value', "2")
    pi2 = ET.Element('PI')
    pi2.set('Name', "Value")
    pi2.set('RefNull', "1")
    pi2.set('Value', "2")
    oi.append(pi)
    oi.append(pi1)
    oi.append(pi2)
    Oi.append(oi)

#for i in range(5):
#    element=ET.Element('name')
#    element.set('age',str(i))
#    element.text='default'
#    root.append(element)

__indent(root)
tree.write('default.xml',encoding='utf-8',xml_declaration=True)
