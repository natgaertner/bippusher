import imp
table_functions = imp.load_module('reformat', *imp.find_module('reformat', ['data']))
DATABASE_CONFIG = {
        'user':'postgres',
        'db':'bip_dump',
        'pw':'|-|3lp3rb34r'
        }
ERSATZPG_CONFIG = {
        'debug':True
        }
ERSATZPG_CONFIG.update(DATABASE_CONFIG)

