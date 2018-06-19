import pycurl
import time
import os
import sys
import json
import subprocess
import select
from urllib import urlencode, quote
from StringIO import StringIO    
from time import sleep

baseUrl = "http://localhost:4503"
password = "admin:admin"

def is_json(myjson):
  try:
    json.loads(myjson)
  except ValueError:
    return False
  return True

def get_formatted_time():
  return time.strftime("%Y-%m-%d %H:%M:%S")

def log(message):
  print get_formatted_time() + ": " + message

# Install packages
current_dir = os.getcwd()
log("Start installing packages")
for file_name in sorted(os.listdir(os.path.join(current_dir, "packages"))):
  if not file_name.endswith(".zip"): 
    log("File \"" + file_name + "\" is no zip-file")
    continue

  file_path = os.path.join(current_dir, "packages", file_name)
  log("Starting installation of package \"" + file_name + "\"")
  
  log("Uploading package \"" + file_name + "\"...")
  uploaded = False
  while not uploaded:
    try:
      packageUpload = StringIO()
      c = pycurl.Curl()
      c.setopt(c.WRITEFUNCTION, packageUpload.write)
      c.setopt(c.URL, baseUrl + "/crx/packmgr/service.jsp")
      c.setopt(c.POST, 1)
      c.setopt(pycurl.USERPWD, password)
      c.setopt(c.HTTPPOST, [('file', (c.FORM_FILE, file_path)), ('force', 'true'), ('install', 'true')])
      c.perform()
      c.close()
      packageUploadResponse = packageUpload.getvalue()
      packageUpload.close()
    except pycurl.error as error:
      log("Upload failed. Will retry in 10 seconds...")
      sleep(10)
      continue

    if packageUploadResponse.find('<status code="200">ok</status>') == -1:
      log("Upload failed. Will retry in 10 seconds...")
      sleep(10)
    else:
      log("Package \"" + file_name + "\" uploaded")
      uploaded = True

  log("Checking package \"" + file_name + "\" installation...")

  # Workaround for 6.2 SP1 to check installation status.
  # See https://helpx.adobe.com/experience-manager/6-2/release-notes/sp1.html
  if file_name.find('aem-service-pkg-6.2.SP1') > -1:
    log("Found 6.2 SP1 package. Monitor error.log to wait for package installation to complete...")
    match = 'from resource TaskResource(url=jcrinstall:/libs/system/aem-service-pkg-6.2.SP1/install/1/updater.aem-service-pkg-1.0.0.jar, ' \
            + 'entity=bundle:updater.aem-service-pkg, state=UNINSTALL, attributes=[Bundle-SymbolicName=updater.aem-service-pkg, Bundle-Version=1.0, ' \
            + 'org.apache.sling.installer.api.tasks.ResourceTransformer'
    f = subprocess.Popen(['tail', '-F', '/opt/aem/crx-quickstart/logs/error.log'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p = select.poll()
    p.register(f.stdout)

    while True:
      if p.poll(1):
        if f.stdout.readline().find(match) > -1:
          f.kill()
          log("Package \"" + file_name + "\" is installed")
          break
      sleep(1)
    
  else:
    installed = False
    while not installed:
      try:
        packageInstallation = StringIO()
        c = pycurl.Curl()
        c.setopt(c.WRITEFUNCTION, packageInstallation.write)
        c.setopt(c.URL, baseUrl + "/crx/packmgr/list.jsp")
        c.setopt(pycurl.USERPWD, password)
        c.perform()
        c.close()
        packageInstallationResponse = packageInstallation.getvalue()
        packageInstallation.close()
      except pycurl.error:
        log("Package not yet installed. Will retry in 10 seconds...")
        sleep(10)
        continue
    
      if not is_json(packageInstallationResponse):
        log("Package not yet installed. Will retry in 10 seconds...")
        sleep(10)
        continue
      
      # Parse packageInstallationResponse as json object and loop through results
      jsonResponse = json.loads(packageInstallationResponse)
      for result in jsonResponse["results"]:
        # TODO: build better support to strip package file name order number
        download_name = file_name[2:]
        
        # break while loop when package status is resolved (i.e. installed)
        if result["downloadName"] == download_name and result["resolved"] == True:
          log("Package \"" + file_name + "\" is installed")
          installed = True
          break

      if not installed:
        log("Package not yet installed. Will retry in 10 seconds...")
        sleep(10)

log("Finished installing packages. Now wait for 5 minutes for all background processes to complete...")
sleep(300)
