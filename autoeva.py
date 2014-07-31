
import urllib.request
import urllib.parse
import socket
import http.cookiejar
import random

timeout = 10
socket.setdefaulttimeout(timeout)
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'
ac = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
headers = {'User-Agent' : user_agent,'Accept': ac, 'Content-Type': 'application/x-www-form-urlencoded'}

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
urllib.request.install_opener(opener)
url = 'http://cms.rdfz.cn/'
req = urllib.request.Request(url,None,headers)

try:
    response = urllib.request.urlopen(req)
except urllib.error as e:
    if hasattr(e, 'reason'):
        print('Failed to reach a server.')
        print('Reason: ', e.reason)
    elif hasattr(e, 'code'):
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
else:
    print('Reached Server. ',response.code)

response = urllib.request.urlopen(req)
def chopFile(front,back,f):
    c2 = front
    [c1,c2,pre] = f.partition(c2)
    c2 = back
    [pre,c2,c1] = pre.partition(c2)
    return pre
def getViewstate(f):
#    c2 = 'id="__VIEWSTATE" value="'
#    [c1,c2,viewstate] = response.read().decode('utf-8').partition(c2)
#    c2 = '"'
#    [viewstate,c2,c1] = viewstate.partition(c2)
    return chopFile('id="__VIEWSTATE" value="','"',f)

def mkr(rawdata, addr):
    data = urllib.parse.urlencode(rawdata)
    data = data.encode('utf-8')
    req = urllib.request.Request(addr,data,headers)
    res = urllib.request.urlopen(req)
    return res

# login
usn = input('Your username: ')
psw = input('And your password: ')
vst = getViewstate(response.read().decode('utf-8'))
loginfo = {'__VIEWSTATE': vst, '__EVENTTARGET': '', '__EVENTARGUMENT': '','TxtUserName': usn, 'TxtPassword': psw, 'ImgbtnLogin.x': '86', 'ImgbtnLogin.y': '13'}
response = mkr(loginfo,response.geturl())
if vst == getViewstate(response.read().decode('utf-8')):
    raise NameError('There is a problem with logging in.')
else:
    vst = getViewstate(response.read().decode('utf-8'))
    print('Login successful.')

# change page to ass
response = mkr({},'http://cms.rdfz.cn/TeacherAppraise/AppraiseInput/AppraiseStuInput.aspx')

#read rules
rulesf = open('rules','r')
infteas = ['a']
inftgrades = ['a']
for l in rulesf:
    [te,sp,gr] = l.rpartition(' ')
    infteas.append(te)
    inftgrades.append(gr[0])
infteas.pop(0)
inftgrades.pop(0)
rulesf.close()
rules = dict(zip(infteas,inftgrades))
if 'Default' in rules:
    grade = rules['Default']
else:
    grade = 'A'
page = response.read().decode('utf-8')
random.seed()

# kick ass
while True:
    fpt = page.rfind('<table')
    fpt += page[fpt:].find('<input')
    currtea = chopFile('">','<',page[fpt:])
    
    if not currtea: break
    print('Processing', chopFile('(',')',currtea))
    for i in rules.keys():
        if currtea.find(i):
            grade = rules[i]
            del rules[i]
            break
    selected = chopFile('<option selected="selected" value="','">',page)
    teaid = chopFile('value="','"',page[fpt:])
    rfcf = [chopFile('<select name="','"',page),chopFile('name="','"',page[fpt:])]
    rfcb = [selected,teaid]
    dataf = ['__EVENTTARGET', '__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE']
    datab = [chopFile('__doPostBack(\\&#39;','\\&#39;',page[fpt:]), '', '', getViewstate(page)]
    dataf+=(rfcf)
    datab+=(rfcb)
    data = dict(zip(dataf,datab))

    response = mkr(data,response.geturl())
    page = response.read().decode('utf-8')
    datab = ['','','',getViewstate(page)]
    datab+=(rfcb)

    for i in range(10):
        fpt = page.rfind('{}、'.format(i+1))
        page = page[fpt:]

        dataf.append(chopFile('name="','"',page))
        datab.append(chopFile('value="','"',page))
        fpt = page.find('ul')
        page = page[fpt:]
        choices = ['A','B','C','D']
        if grade.upper() in choices:
            fpt = page.find('{}、'.format(grade.upper()))
        else:
            fpt = page.find('{}、'.format(choices[random.randrange(4)]))
        fpt = page.rfind('<input',0,fpt)
        page = page[fpt:]
        dataf.append(chopFile('name="','"',page))
        datab.append(chopFile('value="','"',page))

    fpt = page.find('<ul')
    page = page[fpt:]
    dataf.append(chopFile('name="','"',page))
    datab.append(chopFile('value="','"',page))
    fpt = page.find('<textarea')
    page = page[fpt:]
    dataf.append(chopFile('name="','"',page))
    datab.append('')
    fpt = page.find('<input')
    page = page[fpt:]
    dataf.append(chopFile('name="','"',page))
    datab.append(chopFile('value="','"',page))
    data = dict(zip(dataf,datab))
    
    response = mkr(data,response.geturl())
    page = response.read().decode('utf-8')
# rp = open('res.html','w')
# rp.write(response.read().decode('utf-8'))
# rp.close()
# print(response.geturl())
print('Execution complete. Goodbye.')
