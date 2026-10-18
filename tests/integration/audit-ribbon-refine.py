#!/usr/bin/env python3
"""Audit localized toolbar captions with local fixture documents, in both UI modes."""
import json,os,secrets,shutil,subprocess,time,urllib.request,re
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path.home()/'projects/cocolian-office';out=root/'artifacts/ribbon-refine-20261017';out.mkdir(exist_ok=True)
fixture=out/'fixture';fixture.mkdir(exist_ok=True)
shutil.copy2(root/'tests/integration/wopi-source-host.py',fixture/'host.py')
shutil.copy2(root/'tests/fixtures/source-build-smoke.docx',fixture/'collaboration.docx')
key=secrets.token_urlsafe(32)
env=dict(os.environ,LAB_KEY=key,SOURCE_TEST_DATA=str(fixture),NO_PROXY='localhost,127.0.0.1',no_proxy='localhost,127.0.0.1')
result={};op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True,chromium_sandbox=True)
  for mode in ['tabbed']:
   (fixture/'editor.json').write_text(json.dumps({'language':'zh-CN','ui_mode':mode,'use_saved_ui_state':False}))
   log=(out/(mode+'-host.log')).open('w');host=subprocess.Popen(['python3',str(fixture/'host.py')],env=env,stdout=log,stderr=log)
   try:
    for _ in range(60):
     try:
      if op.open('http://127.0.0.1:18080/health',timeout=1).status==200:break
     except Exception:pass
     time.sleep(.2)
    c=browser.new_context(bypass_csp=True,viewport={'width':1800,'height':1100})
    assert c.request.post('http://127.0.0.1:18080/login',form={'key':key}).ok
    page=c.new_page();page.goto('http://127.0.0.1:18080/edit?user=Alice')
    f=page.frame_locator('iframe[name=editor]');f.locator('#document-canvas').wait_for(state='visible',timeout=90000)
    try:f.get_by_role('button',name='跳过',exact=True).click(timeout=3000)
    except Exception:pass
    frame=page.frames[1];results=[]
    page.screenshot(path=str(out/'before.png'))
    frame.add_style_tag(content=Path('/tmp/ribbon-refine.css').read_text())
    page.wait_for_timeout(1500)
    def collect(name):
     rows=frame.evaluate('''() => [...document.querySelectorAll('.unotoolbutton, #toolbar-up button, .ui-pushbutton.notebookbar')].filter(e=>e.getBoundingClientRect().width && e.querySelector('img,.w2ui-icon')).map(e=>({id:e.id,text:e.innerText.trim(),tooltip:e.getAttribute('data-cooltip'),aria:e.getAttribute('aria-label')||e.querySelector('button')?.getAttribute('aria-label')}))''')
     results.append({'tab':name,'buttons':rows})
    if mode=='tabbed':
     tabs=frame.locator('.ui-tab.notebookbar')
     for i in range(tabs.count()):
      t=tabs.nth(i)
      if not t.is_visible():continue
      name=t.inner_text();t.click();page.wait_for_timeout(300);collect(name)
     frame.locator('#Home-tab-label').click()
    else:collect('compact')
    result[mode]=results
    result['metrics']=frame.evaluate("() => Object.fromEntries([\"#toolbar-row\",\"#NotebookBar\",\".notebookbar-scroll-wrapper\",\"#stylesview\"].map(s=>{let e=document.querySelector(s);return [s,{height:e?.getBoundingClientRect().height,classes:e?.className,parent:e?.parentElement.className}]}))")
    result['dom']=frame.locator('#stylesview').evaluate('e=>e.outerHTML')
    result['inputs']=frame.locator('#toolbar-row input').evaluate_all('es=>es.map(e=>e.outerHTML)')
    page.screenshot(path=str(out/(mode+'.png')))
    result[mode+'_frame_text']=frame.locator('body').inner_text()[:7000]
    for label in ['Hanging Indent','Above:','Below:','Line Spacing:','Before:','After:','First:']:
     assert label not in result[mode+'_frame_text'], 'Untranslated sidebar label: '+label
    c.close()
   finally:host.terminate();host.wait(timeout=10);log.close()
  browser.close()
 result['success']=True
except Exception as e:result['error']=str(e).replace(key,'[redacted]')[:2000];result['success']=False
finally:
 (out/'toolbar-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 suspicious=[]
 for mode in ['tabbed']:
  for tab in result.get(mode,[]):
   for item in tab['buttons']:
    for field in ['text','tooltip','aria']:
     value=item.get(field) or '';clean=re.sub(r'\([^)]*\)','',value)
     words=re.findall(r'[A-Za-z][A-Za-z -]{2,}',clean)
     if words:suspicious.append({'mode':mode,'tab':tab['tab'],'id':item['id'],'field':field,'value':value})
 (out/'latin-labels.json').write_text(json.dumps(suspicious,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'success':result['success'],'error':result.get('error'),'latin_labels':suspicious},ensure_ascii=False))
if not result.get('success') or suspicious:raise SystemExit(1)
