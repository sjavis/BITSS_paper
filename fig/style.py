#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import pyutils.latexify as lt

lt.dpi = 500
lt.update_width('natcomm-single')

# Font size
plt.rc('font', size=9)
plt.rc('axes', labelsize=9)

# Helvetica font
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['font.sans-serif'] = ['Helvetica']
mpl.rcParams['text.latex.preamble'] = "\n".join([mpl.rcParams['text.latex.preamble'],
                                                 r"\usepackage{helvet}",
                                                 r"\usepackage{sansmath}",
                                                 r"\sansmath"])

# Colours
plt.rc('font', size=9)
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
