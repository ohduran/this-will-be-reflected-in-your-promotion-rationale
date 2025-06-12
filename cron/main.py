import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from celery import Celery
from celery.schedules import crontab
import subprocess

# Configure Celery to use Redis as the broker and result backend
app = Celery(
    'cron',
    broker='redis://redis:6379/0',  # Use redis service name from docker-compose
    backend='redis://redis:6379/0'
)

# Explicitly set the broker transport
app.conf.broker_transport = 'redis'

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'main.test',  # Changed from 'tasks.add' to 'main.add'
        'schedule': 30.0,
        'args': ("arg", )
    },
}
app.conf.timezone = 'UTC'

@app.task(name='main.test')
def test(arg):
    print(f"Task 'test' executed with argument: {arg}")

    # Run the MCP client as a separate process
    result = subprocess.run(
        ["python", "mcp_client.py", "../postgres_mcp/main.py"],
        capture_output=True,
        text=True
    )
    print("MCP client output:", result.stdout)
    if result.stderr:
        print("MCP client error output:", result.stderr)

    return f"Task completed: {arg}"
