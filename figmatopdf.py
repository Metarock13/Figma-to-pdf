# -*- coding: utf- 8 -*-
import json
import sys, os
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import requests

token = "< T O K E N >"

def getfileid(url):
    d = url.split('/')
    if len(d) > 3:
        if d[2] == 'www.figma.com' and d[3] == 'file':
            return d[4]
        if d[0] == 'www.figma.com' and d[1] == 'file':
            return d[2]
    return ''


def load(token, fileid):
    site = "https://api.figma.com/v1/files/" + fileid
    header = {'X-FIGMA-TOKEN': token}
    r = requests.get(site, headers=header)
    r.encoding = 'utf-8'
    if r.status_code == 200:
        return r.text
    return ''


def imagejson(token, fileid, id):
    site = "https://api.figma.com/v1/images/" + fileid + "?ids=" + id + "&format=png"
    header = {'X-FIGMA-TOKEN': token}
    r = requests.get(site, headers=header)
    r.encoding = 'utf-8'
    if r.status_code == 200:
        return r.text


def imagefile(token, fileid, id):
    data = imagejson(token, fileid, id)
    jsn = json.loads(data)
    img = jsn["images"][id]
    if img != None:
        return img
    else:
        return False
    return True


site = sys.argv[1]
fileid = getfileid(site)
pathname = os.path.dirname(sys.argv[0])

if fileid:
    rez = load(token, fileid)
    print("START")
    arr = []
    jsn = json.loads(rez)
    t = jsn["document"]["children"]
    for t1 in t:
        t2 = t1["children"]
        for t3 in t2:
            if t3["type"] == "FRAME":
                rr = imagefile(token, fileid, t3["id"])
                if rr != False:
                    arr.append(rr)
    if len(arr) > 0:
        canv = canvas.Canvas(fileid + ".pdf")
        for t1 in arr:
            logo = ImageReader(t1)
            image_width, image_height = logo.getSize()
            canv.drawImage(image=logo, x=0, y=0, width=image_width, height=image_height)
            canv.setPageSize((image_width, image_height))
            canv.showPage()
        canv.save()
        print("Save to "+fileid + ".pdf")
print("FINISH ")
