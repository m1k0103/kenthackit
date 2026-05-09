import os
import sys

base_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(base_dir, "server")

sys.path.insert(0, server_dir)
os.chdir(server_dir)

from main import app

print("server starting on http://localhost:5000")

app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT", 5000)),
    debug=os.environ.get("FLASK_DEBUG", "0") == "1"
)