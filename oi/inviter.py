from subprocess import *
import string,random,os
from kwippyproject.console_app.views import *

def getvendors():
    pwd = os.getcwd()
    ret_hash = {}
    output = Popen(["php",pwd + "/oi/OpenInviter/getvendors.php"], stdout=PIPE).communicate()[0]
    arr = string.split(output,"\n")
    sel_string = ""
    for a in arr:
        new_arr = string.split(a,"|||")
        if len(new_arr)==3:
            ret_hash[new_arr[1]]=(new_arr[0],new_arr[2])
            sel_string = '%s<option value="%s">%s</option>' % (sel_string,new_arr[1],new_arr[0],)
    return ret_hash

def getcontacts(service,username,password):
    ret_hash1 = {}
    ret_hash = []
    pwd = "/home/staging/kwippyproject"
    output = Popen(["php",pwd + "/oi/OpenInviter/getcontacts.php",service,username,password], stdout=PIPE).communicate()[0]
    arr = string.split(output,"\n")
    for a in arr:
        new_arr = string.split(a,"|||")
        if len(new_arr)==2:
            ret_hash.append({"email":new_arr[1],"name":new_arr[0]})
        if len(new_arr)==1:
            if new_arr[0]!="":
                ret_hash1["sessionid"]=new_arr[0]
    ret_hash1["contacts"]=ret_hash
    return ret_hash1

def sendmessage(request,service,sessionid,contacts):
    STATIC_SERVICE = {'tagged': ('Tagged', 'social'), 'doramail': ('Doramail', 'email'), 'meinvz': ('Meinvz', 'social'), 'netaddress': ('Netaddress', 'email'), 'indiatimes': ('IndiaTimes', 'email'), 'zapak': ('Zapakmail', 'email'), 'web_de': ('Web.de', 'email'), 'multiply': ('Multiply', 'social'), 'inbox': ('Inbox.com', 'email'), 'rambler': ('Rambler', 'email'), 'badoo': ('Badoo', 'social'), 'interia': ('Interia', 'email'), 'facebook': ('Facebook', 'social'), 'xing': ('Xing', 'social'), 'friendster': ('Friendster', 'social'), 'gawab': ('Gawab', 'email'), 'xuqa': ('Xuqa', 'social'), 'hi5': ('Hi5', 'social'), 'myspace': ('MySpace', 'social'), 'bigstring': ('Bigstring', 'email'), 'perfspot': ('Perfspot', 'social'), 'flingr': ('Flingr', 'social'), 'abv': ('Abv', 'email'), 'gmx_net': ('GMX.net', 'email'), 'lastfm': ('Last.fm', 'social'), 'azet': ('Azet', 'email'), 'gmail': ('GMail', 'email'), 'famiva': ('Famiva', 'social'), 'eons': ('Eons', 'social'), 'walla': ('Walla', 'email'), 'flixster': ('Flixster', 'social'), 'kincafe': ('Kincafe', 'social'), 'hotmail': ('Live/Hotmail', 'email'), 'konnects': ('Konnects', 'social'), 'terra': ('Terra', 'email'), 'fastmail': ('FastMail', 'email'), 'aol': ('AOL', 'email'), 'xanga': ('Xanga', 'social'), 'yahoo': ('Yahoo!', 'email'), 'lycos': ('Lycos', 'email'), 'wpl': ('Wp.pt', 'email'), 'lovento': ('Lovento', 'social'), 'sapo': ('Sapo.pt', 'email'), 'rediff': ('Rediff', 'email'), 'linkedin': ('LinkedIn', 'social'), 'mevio': ('Mevio', 'social'), 'operamail': ('OperaMail', 'email'), 'motortopia': ('Motortopia', 'social'), 'mail_com': ('Mail.com', 'email'), 'mynet': ('Mynet.com', 'email'), 'clevergo': ('Clevergo', 'email'), 'fdcareer': ('Fdcareer', 'social'), 'brazencareerist': ('Brazencareerist', 'social'), 'flickr': ('Flickr', 'social'), 'care2': ('Care2', 'email'), 'apropo': ('Apropo', 'email'), 'katamail': ('KataMail', 'email'), 'vimeo': ('Vimeo', 'social'), 'bebo': ('Bebo', 'social'), 'fm5': ('5Fm', 'email'), 'mail_ru': ('Mail.ru', 'email'), 'libero': ('Libero', 'email'), 'cyworld': ('Cyworld', 'social'), 'plazes': ('Plazes', 'social'), 'livejournal': ('Livejournal', 'social'), 'skyrock': ('Skyrock', 'social'), 'friendfeed': ('Friendfeed', 'social'), 'faces': ('Faces', 'social'), 'orkut': ('Orkut', 'email'), 'hushmail': ('Hushmail', 'email'), 'plaxo': ('Plaxo', 'social'), 'plurk': ('Plurk', 'social'), 'yandex': ('Yandex', 'email')}
    if(STATIC_SERVICE[service][1]=='social'):
        new_file = str(random.random())
        f = open("temp/"+new_file,"w")
        for key in contacts.keys():
            f.write("%s|||%s" % (contacts[key],key,))
        f.close()
        pwd = "/home/staging/kwippyproject"
        output = Popen(["php",pwd+"/oi/OpenInviter/sendmessage.php","temp/"+new_file,service,sessionid], stdout=PIPE).communicate()[0]
    else:
        for key in contacts.keys():
            invite_hash = generate_invite_code(str(key),"support@kwippy.com")
            store_invite_in_db(request,invite_hash,'friend')
    return True    

#getvendors()
#print getcontacts("gmail","dipankarsarkar@gmail.com","")
#sendmessage("linkedin","1235238279.5994",{"dipankarsarkar@gmail.com":"Dipankar"})
