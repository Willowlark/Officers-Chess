from glob import glob
import json
import os
# import pandas as pd
from shutil import copy
from os.path import join
import fire
import datetime
from hashlib import blake2b
import string
import pandas as pd
from random import choice
from copy import deepcopy

secrets = json.load(open('secrets.json'))

class Foundry(object):
    
    def _token_source(self, classname, color='Blue', weapon='NoWeapon'):
        if classname == "Dancer": 
            return "Officer_Chess/Engage/Unique/Seadas/Dancer/Dancer-NoWeapon.png"
        root = '/Users/bill/Library/Application Support/FoundryVTT/Data/Officer_Chess/Engage/'
        relroot = 'Officer_Chess/Engage/'
        tokens = []
        fname = f'{color}/Soldier/{classname}/Female-{classname}-{weapon}.png'
        mname = f'{color}/Soldier/{classname}/Male-{classname}-{weapon}.png'
        if os.path.exists(root+fname): tokens.append(relroot+fname)
        if os.path.exists(root+mname): tokens.append(relroot+mname)
        if tokens: 
            return choice(tokens) 
        else: 
            print("No Token found for " + classname)
            return ''
    
    def __init__(self, version=None):
        self.version = version if version else secrets['game_version']
        self.path_setup(self.version)

    def path_setup(self, version):
        
        self.data_path = f'{version}'
        self.template_path = f'foundry_templates/'
        if not os.path.exists(self.data_path): raise Exception(f"ERROR: Path not found!", self.data_path)
            
        self.data_output = f"{secrets['FoundryDataDir']}/data/"
        self.packs_output = f"{secrets['FoundryDataDir']}/packs/"
        if not os.path.exists(self.data_output): raise Exception(f"ERROR: Path not found!")
            
        return 0
    
    def _classes(self):
        
        data = pd.read_csv(join(self.data_path, 'classes_engage.csv')).fillna('')
        
        db = []
        db_foe = []
        db_npc = []
        for i, x in data.iterrows():
            img = self._token_source(x.Class)

            foundry = json.loads(open(self.template_path+'class.json').read())
            foundry['name'] = x.Class
            foundry['_id'] = blake2b(bytes(x.Class+x.Proficencies+'Blue', 'utf-8'), digest_size=16).hexdigest()
            foundry['img'] = img
            foundry['system']['props']['health'] = int(x.HP)
            foundry['system']['props']['maxhplabel'] = str(x.HP)
            # foundry['system']['body']['contents'][6]['contents'][0]['contents'][2]['value'] = str(x.HP)
            foundry['system']['props']['class'] = x.Class
            foundry['system']['props']['totalcost'] = 0
            foundry['system']['props']['maxhp'] = (x.HP)
            foundry['system']['props']['str'] = str((x.Str))
            foundry['system']['props']['mag'] = str((x.Mag))
            foundry['system']['props']['dex'] = str((x.Dex))
            foundry['system']['props']['spd'] = str((x.Spd))
            foundry['system']['props']['def'] = str((x.Def))
            foundry['system']['props']['res'] = str((x.Res))
            foundry['system']['props']['profs'] = x.Proficencies
            foundry['system']['props']['classcost'] = str(int('0'))
            foundry['system']['props']['tags'] = x.Tags if x.Tags else ''
            foundry['system']['props']['invweight'] = "0"
            foundry['system']['props']['tier'] = 'Promoted' if x.Promoted == 'Yes' else 'Base'
            foundry['system']['props']['gameversion'] = self.version
            foundry['prototypeToken']['name'] = x.Class
            foundry['prototypeToken']['texture']['src'] = img
            foundry['_stats']['modifiedTime'] = datetime.datetime.now().timestamp()
            # foundry['folder'] = FOLDER_ID[self.version]
            foundry['_stats']['lastModifiedBy'] = "uq5xdVlxrWSzTiGc"
            db.append(foundry)
            
            npc = deepcopy(foundry)
            npc['_id'] = blake2b(bytes(x.Class+x.Proficencies+'Green', 'utf-8'), digest_size=16).hexdigest()
            img = self._token_source(x.Class, 'Green')
            npc['img'] = img
            npc['prototypeToken']['texture']['src'] = img
            db_npc.append(npc)
            
            foe = deepcopy(foundry)
            foe['_id'] = blake2b(bytes(x.Class+x.Proficencies+'Red', 'utf-8'), digest_size=16).hexdigest()
            img = self._token_source(x.Class, 'Red')
            foe['img'] = img
            foe['prototypeToken']['texture']['src'] = img
            db_foe.append(foe)
        
        with open(self.packs_output+"classes-engage.db",'w') as f:
                for x in db:
                    f.write(json.dumps(x)+'\n')
        with open(self.packs_output+"npc-classes-engage.db",'w') as f:
                for x in db_npc:
                    f.write(json.dumps(x)+'\n')
        with open(self.packs_output+"foe-classes-engage.db",'w') as f:
                for x in db_foe:
                    f.write(json.dumps(x)+'\n')
        return db
    
    def _weapons(self):
        
        data = pd.read_csv(join(self.data_path, 'weapons_engage.csv')).fillna('')
        
        db = []
        for i, x in data.iterrows():
            foundry = json.loads(open(self.template_path+'weapons.json').read())
            foundry['name'] = x.Name
            foundry['_id'] = blake2b(bytes(x.Name, 'utf-8'), digest_size=16).hexdigest()
            foundry['system']['props']['dmgtype'] = 'Martial' if x.DmgType == 'Phys' else 'Magic'
            foundry['system']['props']['type'] = x.Type
            foundry['system']['props']['cost'] = str(int(x.Price))
            foundry['system']['props']['might'] = str(int(x.Mt))
            foundry['system']['props']['wt'] = str(int(x.Wt))
            foundry['system']['props']['hit'] = str(int(x.Hit))
            foundry['system']['props']['wprange'] = x.Rng
            foundry['system']['props']['lvl'] = x.Lvl
            foundry['system']['props']['tags'] = x.Tags if x.Tags else ''
            foundry['system']['props']['gameversion'] = self.version
            foundry['system']['props']['wpname'] = x.Name
            foundry['_stats']['modifiedTime'] = datetime.datetime.now().timestamp()
            # foundry['folder'] = FOLDER_ID[self.version]
            foundry['_stats']['lastModifiedBy'] = "uq5xdVlxrWSzTiGc"
            db.append(foundry)
        
        new = []
        # with open(self.data_output+f"items.db",'r') as f:
        #     for l in f.readlines():
        #         if FOLDER_ID[self.version] not in l:
        #             new.append(l)
        # with open(self.data_output+f"items.db",'w') as f:
        #     f.writelines(new)
        # with open(self.data_output+f"items.db",'a') as f:
        #     for x in db:
        #         f.write(json.dumps(x)+'\n')
        with open(self.packs_output+"weapons-engage.db",'w') as f:
                for x in db:
                    f.write(json.dumps(x)+'\n')
        return db
        
    def _accessories(self):
        
        FOLDER_ID = {
                    'v0.6' : "djtkX6e16wC1RZJT"
                    }
        
        data = pd.read_csv(join(self.data_path, 'accessories.csv')).fillna('')
        
        db = []
        for i, x in data.iterrows():
            foundry = json.loads(open(self.template_path+'accessory.json').read())
            foundry['name'] = x.Name
            foundry['_id'] = blake2b(bytes(entry['name'], 'utf-8'), digest_size=16).hexdigest()
            foundry['system']['props']['cost'] = str(int('0'))
            foundry['system']['props']['defbonus'] = str(int(x.Def))
            foundry['system']['props']['weight'] = str(int(x.Wt))
            foundry['system']['props']['wptags'] = x.Tags if x.Tags else ''
            foundry['system']['props']['gameversion'] = self.version
            foundry['system']['props']['wpname'] = x.Name
            foundry['_stats']['modifiedTime'] = datetime.datetime.now().timestamp()
            foundry['folder'] = FOLDER_ID[self.version]
            foundry['_stats']['lastModifiedBy'] = "uq5xdVlxrWSzTiGc"
            db.append(foundry)
        
        new = []
        with open(self.data_output+f"items.db",'r') as f:
            for l in f.readlines():
                if FOLDER_ID[self.version] not in l:
                    new.append(l)
        with open(self.data_output+f"items.db",'w') as f:
            f.writelines(new)
        with open(self.data_output+f"items.db",'a') as f:
            for x in db:
                f.write(json.dumps(x)+'\n')
        return db
        
    def _consumables(self):
        
        FOLDER_ID = {
                    'v0.6' : "U6M9ohgt1pOYJtLn"
                    }
        
        data = pd.read_csv(join(self.data_path, 'consumables.csv')).fillna('')
        
        db = []
        for i, x in data.iterrows():
            foundry = json.loads(open(self.template_path+'consumables.json').read())
            foundry['name'] = x.Name
            foundry['_id'] = blake2b(bytes(entry['name'], 'utf-8'), digest_size=16).hexdigest()
            foundry['system']['props']['cost'] = str(int('0'))
            foundry['system']['props']['wptags'] = x.Tags if x.Tags else ''
            foundry['system']['props']['gameversion'] = self.version
            foundry['system']['props']['wpname'] = x.Name
            foundry['_stats']['modifiedTime'] = datetime.datetime.now().timestamp()
            foundry['folder'] = FOLDER_ID[self.version]
            foundry['_stats']['lastModifiedBy'] = "uq5xdVlxrWSzTiGc"
            db.append(foundry)
        
        new = []
        with open(self.data_output+f"items.db",'r') as f:
            for l in f.readlines():
                if FOLDER_ID[self.version] not in l:
                    new.append(l)
        with open(self.data_output+f"items.db",'w') as f:
            f.writelines(new)
        with open(self.data_output+f"items.db",'a') as f:
            for x in db:
                f.write(json.dumps(x)+'\n')
        return db
        
def update( *argv, 
            batch=False, 
            version=None, 
            confirm=False,
            sheet_images='book',
            token_images='book'):
        
    foundry = Foundry(version)
    
    targets = {
        "classes":   foundry._classes,
        "weapons": foundry._weapons,
        "accessories": foundry._accessories,
        "consumables":     foundry._consumables
    }
    
    updates = list(targets.keys()) if batch else []
    for t in argv:
        if t.lower() in targets:
            updates.append(t.lower())
        else:
            print(f"WARN: Target {t.lower()} not configuRed, Skipping...")
    updates = set(updates)
    if not confirm: 
        conf = input(f'INFO: {updates}\nQUERY: Update these folders in Foundry? [Y/Yes]: ')
        if conf.lower() not in ['y', 'yes']:
            return "WARN: Did not confirm update, cancelling..."
    else: print(f'INFO: {updates}\nQUERY: Updating these folders in the Foundry...')
    
    for t in updates:
        func = targets[t]
        func()
        print(f'INFO: Folder {t} updated!')
        
    print('INFO: Foundry Update Complete.')
        
def help():
    print("""
    Python Script to update the Obsidian Foundry with the latest Data. 
    
    update: 
        update [collection names], [--batch] [--version Version] [--confirm] [--sheet_images src] [--token_images src]
            collection names     : one or more of the folders in Foundry. Optional when using --batch.
            batch                : Optional. Updates all Foundry folderss
            version              : Optional. Changes the Version folder to be used in paths.
            confirm              : Optional. Skips confirmation step. 
    """)

if __name__ == '__main__':
    fire.Fire()
    