# add local package to import path
# not needed if package is installed
from sys import path, exit, argv
from os.path import dirname
import logging
path.insert(0, dirname(__file__) + '/../src/mentat')

# add all modules
from inspect import getmembers, signature, getdoc
from textwrap import indent
from mentat import Module
from modules import engine
import modules
engine.add_module(modules.openstagecontrol)
for name, mod in getmembers(modules):
    if name[0] != '_' and isinstance(mod, Module) and name not in ['raysession', 'openstagecontrol']:
        engine.add_module(mod)
engine.add_module(modules.raysession)


# add routes
import routes
from mentat import Route
for name, mod in getmembers(routes):
    if name[0] != '_' and isinstance(mod, Route):
        engine.add_route(mod)

# set default route
engine.set_route('Chapitre1')

#################################################################
#################################################################
# UGLY DOCS GENERATION
_docs = ''
_types = []
def print_params(mod, depth=0):
    global _docs

    t = type(mod).__name__
    # if t in _types:
    #     return
    _types.append(t)

    _docs += '\n\n' + '    ' * depth
    # if depth != 0:
    #     _docs += t + ': ' + ', '.join([mod.name] + [x.name for x in mod.parent_module.submodules.values() if type(x) == type(mod) and x != mod])
    # else:
    _docs += t + ': ' + mod.name

    params = [p for p in mod.parameters.values() if type(p).__name__ == 'Parameter']
    mparams = [p for p in mod.parameters.values() if type(p).__name__ == 'MetaParameter']

    for pbank in [params, mparams]:
        if pbank:
            _docs += '\n\n' + '    ' * (depth + 1)
            _docs += type(pbank[0]).__name__ + 's:\n\n'
            for param in pbank:
                _docs += '    ' * (depth + 1)
                _docs += '%s (%s %s)' % (param.name, param.address, param.types) + '\n'

    methods = [x for n,x in getmembers(mod) if callable(x) and not hasattr(Module,n)]
    if methods:
        _docs += '\n\n' + '    ' * (depth + 1)
        _docs += 'Methods:\n\n'
        for m in methods:
            _docs += '    ' * (depth + 1)
            _docs += '%s%s' % (m.__name__, str(signature(m))) + '\n'

    for name in mod.submodules:
        print_params(mod.submodules[name], depth + 1)

def print_routes():
    global _docs

    for name, route in engine.routes.items():
        if getdoc(route):
            print(getdoc(route))
        else:
            print(route.name)
        print()
        methods = [x for n,x in getmembers(route) if callable(x) and (hasattr(x, 'mk2_buttons') or hasattr(x, 'pedalboard_buttons'))]
        methods = sorted(methods, key=lambda m: m.index)
        for part in methods:
            # if hasattr(part, 'mk2_buttons'): #### ORL -> normalement inutile
            #     print('  Mk2 button: %s' % ', '.join([str(x) for x in part.mk2_buttons.keys()]))
            if hasattr(part, 'pedalboard_buttons'):
                print('  Pedalboard button: %s' % ', '.join([str(x) for x in part.pedalboard_buttons.keys()]))
            if getdoc(part):
                print(indent(getdoc(part), '    '), '\n')
            else:
                print(indent(part.__name__, '    '), '\n')


def docs():
    engine.root_module.wait(2,'s')
    print_params(engine.root_module, 0)
    f = open('docs.txt', 'w')
    f.write(_docs)
    f.close()

if '--docs' in argv:
    engine.root_module.start_scene('docs', docs)
    engine.stop_scene('*')
    exit(0)

if '--routes-docs' in argv:
    logging.getLogger().setLevel(logging.CRITICAL)
    print_routes()
    engine.stop_scene('*')
    exit(0)


#################################################################
#################################################################

# enable autorestart upon file modification
engine.autorestart()

# start main loop
engine.start()
