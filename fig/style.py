#!/usr/bin/env python3

import matplotlib.pyplot as plt
import pyutils.latexify as lt

lt.update_width('r4-single')
plt.rc('font', size=9)
plt.rc('axes', labelsize=9)

c1 = 'tab:orange'
c2 = 'tab:red'
c3 = 'tab:blue'
colors = [c2, c1, c3]


### Make sure this is reloaded by IPython ###
# exit_register runs at the end of ipython %run or the end of the python interpreter
from IPython import get_ipython
ip = get_ipython()
if (ip == None):
    from atexit import register as exit_register
else:
    def exit_register(fun, *args, **kwargs):
        """ Decorator that registers at post_execute. After its execution it
        unregisters itself for subsequent runs. """
        def callback():
            fun()
            ip.events.unregister('post_execute', callback)
        ip.events.register('post_execute', callback)
@exit_register
def reset_rcparams():
    # Ensure IPython reloads the module
    import sys
    del sys.modules['style']
