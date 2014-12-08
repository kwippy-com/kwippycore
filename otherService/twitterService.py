from django.conf import settings
import twitter
import simplejson
import urllib
import urllib2
import binascii
from Crypto.Hash import MD5
from Crypto.Cipher import DES

def rfill(data):
    if len(data)%8 == 0:
        return data
    mul = len(data)/8;
    deficit = ((mul+1)*8) - len(data)
    return data+(' '*deficit)

def post_call(url,vars):
    data = urllib.urlencode(vars)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    page = response.read()
    return page

def getFollowers(username,password):
    vkey = settings.VAKEY
    vskey = settings.VSKEY
    m = MD5.new()
    m.update(username+vskey)
    hash = m.hexdigest()
    url = settings.VURL + '/contact/twitter'
    enc = DES.new(vskey[:8])
    epassword = binascii.hexlify(enc.encrypt(rfill(password)))
    vars = {'ak':vkey,'hash':hash,'username':username,'password':epassword,'vendor':'twitter'}
    data = simplejson.loads(post_call(url,vars))
    if data.has_key('error'):
        return (-1,[])
    txn = data['txn']
    total = data['data']
    return (txn,total)

def sendDM(username,txnID,message,sendList):
    vkey = settings.VAKEY 
    vskey = settings.VSKEY
    m = MD5.new()
    m.update(username+vskey)
    hash = m.hexdigest()
    url = settings.VURL + '/message/twitter'
    vars = {'ak':vkey,'hash':hash,'username':username,'txn':txnID,'message':message,'list':simplejson.dumps(sendList)}
    data = simplejson.loads(post_call(url,vars))
    return data[0]
