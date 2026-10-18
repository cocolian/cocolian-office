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
  for mode,width in [('compact',1440),('tabbed',1800),('tabbed',1440),('tabbed',1024)]:
   (fixture/'editor.json').write_text(json.dumps({'language':'zh-CN','ui_mode':mode,'use_saved_ui_state':False}))
   log=(out/(mode+'-host.log')).open('w');host=subprocess.Popen(['python3',str(fixture/'host.py')],env=env,stdout=log,stderr=log)
   try:
    for _ in range(60):
     try:
      if op.open('http://127.0.0.1:18080/health',timeout=1).status==200:break
     except Exception:pass
     time.sleep(.2)
    c=browser.new_context(viewport={'width':width,'height':1100})
    assert c.request.post('http://127.0.0.1:18080/login',form={'key':key}).ok
    page=c.new_page();page.goto('http://127.0.0.1:18080/edit?user=Alice')
    f=page.frame_locator('iframe[name=editor]');f.locator('#document-canvas').wait_for(state='visible',timeout=90000)
    try:f.get_by_role('button',name='跳过',exact=True).click(timeout=3000)
    except Exception:pass
    frame=page.frames[1];results=[]
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
    metrics=frame.evaluate("""() => {
     const el=s=>document.querySelector(s), css=s=>getComputedStyle(el(s));
     const r=s=>el(s)?.getBoundingClientRect();
     return {tabFont:el('.ui-tab.notebookbar')?css('.ui-tab.notebookbar').fontSize:null,
       iconWidth:r('.unoBold img')?.width,toolbarHeight:r('#toolbar-row')?.height,
       styleTitle:el('#stylesview .ui-iconview-entry-title')?css('#stylesview .ui-iconview-entry-title').display:null,
       styleWidths:[...document.querySelectorAll('#stylesview .ui-iconview-entry')].map(e=>e.getBoundingClientRect().width),
       styleCount:document.querySelectorAll('#stylesview .ui-iconview-entry').length};
    }""")
    result[mode+'_'+str(width)+'_metrics']=metrics
    if mode=='tabbed':
     assert metrics['tabFont']=='14px',metrics
     assert metrics['iconWidth']==20 or (width<1280 and metrics['iconWidth']==0),metrics
     assert metrics['styleTitle']=='block',metrics
     assert all(w==96 for w in metrics['styleWidths']),metrics
     if metrics['iconWidth']==0:
      frame.locator("[id^=overflow-button-home-font] .arrowbackground:visible").first.click()
      frame.locator(".unoBold button:visible").first.wait_for(state='visible')
      result['narrow_font_overflow_accessible']=True
      page.keyboard.press('Escape')
    else:assert metrics['styleTitle'] is None,metrics

    page.screenshot(path=str(out/(mode+'-'+str(width)+'.png')))
    page.screenshot(path=str(out/(mode+'-'+str(width)+'-toolbar.png')),clip={'x':0,'y':0,'width':width,'height':125})
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
 for mode,width in [('compact',1440),('tabbed',1800),('tabbed',1440),('tabbed',1024)]:
  for tab in result.get(mode,[]):
   for item in tab['buttons']:
    for field in ['text','tooltip','aria']:
     value=item.get(field) or '';clean=re.sub(r'\([^)]*\)','',value)
     words=re.findall(r'[A-Za-z][A-Za-z -]{2,}',clean)
     if words:suspicious.append({'mode':mode,'tab':tab['tab'],'id':item['id'],'field':field,'value':value})
 (out/'latin-labels.json').write_text(json.dumps(suspicious,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'success':result['success'],'error':result.get('error'),'latin_labels':suspicious},ensure_ascii=False))
if not result.get('success') or suspicious:raise SystemExit(1)
