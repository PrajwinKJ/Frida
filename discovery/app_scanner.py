from pathlib import Path as path
import configparser
import json
import logging
import os

def scan_apps():
    project_root=path(__file__).resolve().parent.parent
    apps={}
    app_path=path('/usr/share/applications')
    log_path=path(project_root/"logs")
    os.makedirs(name=log_path,exist_ok=True)

    logging.basicConfig(filename=log_path/"apps.log",level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s")

    try:
        logging.info('Scanning Installed Applications...')

        for file in app_path.glob("*.desktop"):
            parser=configparser.ConfigParser(interpolation=None)
            parser.read(file)
            name=parser['Desktop Entry'].get('Name')
            exec_cmd=parser['Desktop Entry'].get('Exec')
            no_disp=parser['Desktop Entry'].get('NoDisplay')
            kill_name=''
            if name.lower()=='google chrome':
                 kill_name='chrome'
            if name and exec_cmd and not no_disp=='true':
                    exec_cmd=exec_cmd.split()[0]
                    apps[name.lower()]={"Exec":exec_cmd}
                    if kill_name:
                         apps[name.lower()]['Name']=kill_name                          #Hardcoded killname chrome for killing chrome processes

        config=path(project_root/'config')
        os.makedirs(name=config,exist_ok=True)
        json_path=config/'apps.json'
        with open(json_path,'w') as file:
            json.dump(apps,file,indent=4)
        logging.info(f'Scanned {len(apps)}  Applications')
    except:
        logging.exception('Scanning Failed')

if __name__=="__main__":
     scan_apps()