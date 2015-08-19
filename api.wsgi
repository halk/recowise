# Activate virtualenv
import os
activate_env=os.path.expanduser('~/.virtualenvs/framework/bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))

# Make sure current path is in the PATH environment
import sys
sys.path.append(os.path.dirname(__file__))

# Detect file changes and reload WSGI application
import monitor
monitor.start(interval=1.0)
monitor.track(os.path.dirname(__file__))

# Load application
from api import app as application
