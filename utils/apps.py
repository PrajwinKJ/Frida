import subprocess
import json
import logging
from pathlib import Path as path
from discovery.app_scanner import scan_apps
import psutil
from core.schema import tool

log_file=path(__file__).resolve().parent.parent/"logs/apps.log"
logging.basicConfig(filename=log_file,level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s")
pdir=path(__file__).resolve().parent.parent
app_path=pdir/"config/apps.json"

@tool("Open an installed application by providing the app name")
def open_app(app_name: str):
    logging.info(f'Opening application: {app_name}')
    print(app_name)
    try:
        if not app_path.exists():
            scan_apps()
        with open(app_path,'r') as file:
            apps=json.load(file)
        for i in apps.keys():
            if app_name.lower()==i:
                subprocess.Popen([apps[i]['Exec']],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)
                logging.info(f'Successfully Launched {app_name}')
                return f"Successfully opened {app_name}"
    except:
        logging.exception(f'Failed to open {app_name}')
    
@tool("Close an existing session of an application by providing the app name")
def close_app(app_name: str):
    print("closing")
    if not app_path.exists():
        scan_apps()
    with open(app_path,'r') as file:
        apps=json.load(file)
    for i in apps.keys():
        if app_name.lower()==i:
            try :
                app_name=apps[i]['Name']
            except:
                pass

    for process in psutil.process_iter(['pid','name']):
        if app_name in process.info['name']:
            logging.info(f"Closing {app_name}")
            process.terminate()
            try:
                process.wait(timeout=5)
                logging.info(f"Closed {app_name}")

            except psutil.TimeoutExpired:
                process.kill()
                process.wait()
                logging.warning("Forced Closed {app_name}")
            return f"Successfully closed {app_name}"