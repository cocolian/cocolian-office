#!/usr/bin/env python3
"""Local isolated candidate test. Never touches live documents or credentials."""
import os,secrets,subprocess,time,socket,shutil,json,zipfile
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[2]
build=root/'build/source-19b4efae7fb8'
data=build/'wopi-smoke-data';data.mkdir(exist_ok=True)
shutil.copy2(root/'tests/fixtures/source-build-smoke.docx',data/'collaboration.docx')
fixture=build/'ribbon-smoke-host';fixture.mkdir(exist_ok=True)
ribbon_host=fixture/'host.py'
shutil.copy2(root/'tests/integration/wopi-source-host.py',ribbon_host)
(fixture/'editor.json').write_text(json.dumps({'language':'zh-CN','ui_mode':'tabbed','use_saved_ui_state':False}))
key=secrets.token_urlsafe(32)
env=dict(os.environ,LAB_KEY=key,SOURCE_TEST_DATA=str(data),no_proxy='127.0.0.1,localhost',NO_PROXY='127.0.0.1,localhost')
log=(build/'logs/wopi-smoke.log').open('w')
host=subprocess.Popen(['python3',str(ribbon_host)],env=env,stdout=log,stderr=log)
result={}
try:
 for _ in range(50):
  try:
   with socket.create_connection(('127.0.0.1',18080),timeout=.2):break
  except OSError:time.sleep(.1)
 with sync_playwright() as p:
  browser=p.chromium.launch(channel='chrome',headless=True,chromium_sandbox=True)
  contexts=[];pages=[]
  try:
   for user in ('Alice','Bob'):
    context=browser.new_context(viewport={'width':1440,'height':1000})
    contexts.append(context)
    response=context.request.post('http://127.0.0.1:18080/login',form={'key':key})
    assert response.ok
    page=context.new_page();pages.append(page)
    page.goto('http://127.0.0.1:18080/edit?user='+user)
    frame=page.frame_locator('iframe[name=editor]')
    frame.locator('#document-canvas').wait_for(state='visible',timeout=90000)
    frame.locator('#clipboard-area').wait_for(state='attached',timeout=30000)
    try:frame.get_by_role('button',name='跳过',exact=True).click(timeout=3000)
    except Exception:pass
    result[user+'_editor_started']=True
   markers=[]
   for user,page in zip(('Alice','Bob'),pages):
    frame=page.frame_locator('iframe[name=editor]')
    frame.locator('#document-canvas').click(position={'x':300,'y':200})
    page.keyboard.press('Control+End')
    marker=user+'_SOURCE_BUILD_SAVE_'+secrets.token_hex(4);markers.append(marker)
    page.keyboard.press('Enter');page.keyboard.insert_text(marker)
    page.keyboard.press('Control+s')
    saved=False
    for _ in range(60):
     try:
      with zipfile.ZipFile(data/'collaboration.docx') as z:
       document=z.read('word/document.xml').decode()
       saved=all(m in document for m in markers)
     except (OSError,zipfile.BadZipFile):pass
     if saved:break
     time.sleep(1)
    result[user+'_wopi_saved_marker']=saved
    assert saved,'Typed markers not found in WOPI-saved DOCX'
   result['wopi_saved_marker']=saved
   result['two_independent_editor_sessions']=len(pages)==2
   for user,page in zip(('Alice','Bob'),pages):
    page.screenshot(path=str(build/'logs'/('source-editor-'+user+'.png')))
   assert saved,'Typed marker not found in WOPI-saved DOCX'
  except Exception as e:
   result['error']=str(e)
   for i,page in enumerate(pages):
    page.screenshot(path=str(build/'logs'/('source-browser-failure-'+str(i)+'.png')))
    result['page_'+str(i)+'_text']=page.locator('body').inner_text()[:2000]
    if len(page.frames)>1:result['frame_'+str(i)+'_text']=page.frames[1].locator('body').inner_text()[:2000]
   raise
  finally:
   browser.close()
finally:
 host.terminate();host.wait(timeout=10);log.close()
 (build/'baseline/ribbon-browser-smoke.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps(result,ensure_ascii=False))
