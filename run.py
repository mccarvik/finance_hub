#!flask/bin/python
import os
import sys
# Need this to set up modules
sys.path.append("/home/ubuntu/workspace/finance")
sys.path.append("/usr/local/lib/python2.7/dist-packages")
from app import app


# Need this to reset DB
os.system('sudo /etc/init.d/mysql restart')

# app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=False)