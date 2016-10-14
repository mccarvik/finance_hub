#!flask/bin/python
import os
import sys
from app import app
sys.path.append("/home/ubuntu/workspace/finance")

# app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=True)
app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)), debug=False)