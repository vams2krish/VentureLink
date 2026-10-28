"""Local-only integration checks. Requires a migrated development D1 database."""
import json, urllib.request, urllib.error
BASE='http://127.0.0.1:5173'
checks=[]
def request(payload=None,auth=True,origin=BASE,path='/api/platform'):
    headers={'Origin':origin}
    if auth: headers['Cookie']='__sites_local_auth=1'
    body=None
    if payload is not None:
        headers['Content-Type']='application/json'; body=json.dumps(payload).encode()
    r=urllib.request.Request(BASE+path,data=body,headers=headers)
    try:
        with urllib.request.urlopen(r,timeout=90) as res:return res.status,json.load(res)
    except urllib.error.HTTPError as e:
        raw=e.read()
        try: value=json.loads(raw)
        except: value={'error':raw.decode(errors='replace')}
        return e.code,value
def check(name,condition):
    assert condition,name
    checks.append(name);print('PASS',name,flush=True)
status,d=request(auth=False);check('Anonymous accounts expose no members or messages',status==200 and not d['profiles'] and not d['messages'])
status,d=request({'action':'profile'},auth=False);check('Anonymous writes require sign-in',status==401)
status,d=request({'action':'profile'},origin='https://other.example');check('Cross-origin writes are rejected',status==403)
status,d=request({'action':'profile','role':'admin'});check('Invalid registration fields rejected',status==400)
status,d=request({'action':'profile','role':'business','name':'Local QA Business','sector':'Technology','country':'United States','amount':500000,'stage':'Seed','bio':'Local synthetic test profile.','cadence':'month'});check('Business profile saved',status==200)
status,d=request();check('New profile cannot self-approve or self-verify',d['me']['paid']==0 and d['me']['verified']==0 and d['me']['status']=='pending')
status,d=request({'action':'checkout'});check('Unconfigured Stripe fails clearly without granting access',status==503)
status,d=request({'action':'moderate','id':'local_seedy','status':'approved','verify':True});check('Non-admin cannot approve profiles',status==403)
status,d=request({'action':'connect','target':'someone','body':'Hello'});check('Unpaid member cannot initiate connections',status==403)
status,d=request(path='/api/platform?file=missing');check('Unowned file is inaccessible',status==403)
# Upload content signature validation and private ownership.
def upload(content,mime='application/pdf',kind='verification'):
    boundary='VentureLinkLocalBoundary'
    body=(f'--{boundary}\r\nContent-Disposition: form-data; name="kind"\r\n\r\n{kind}\r\n--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="qa.pdf"\r\nContent-Type: {mime}\r\n\r\n').encode()+content+f'\r\n--{boundary}--\r\n'.encode()
    r=urllib.request.Request(BASE+'/api/platform',data=body,headers={'Origin':BASE,'Cookie':'__sites_local_auth=1','Content-Type':'multipart/form-data; boundary='+boundary})
    try:
        with urllib.request.urlopen(r,timeout=90) as res:return res.status,json.load(res)
    except urllib.error.HTTPError as e:
        raw=e.read()
        try: value=json.loads(raw)
        except: value={'error':raw.decode(errors='replace')}
        return e.code,value
status,d=upload(b'not really a pdf');check('Forged PDF rejected',status==400)
status,d=upload(b'%PDF-1.4\n% local test document\n%%EOF');check('Verification file stored',status==200)
status,d=request();check('Uploading a document does not grant verification',d['me']['verified']==0 and len(d['files'])>0)
print(json.dumps({'passed':len(checks),'checks':checks},indent=2))
