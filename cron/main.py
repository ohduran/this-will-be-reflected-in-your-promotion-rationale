from celery import Celery
from celery.schedules import crontab
import redis  # Explicitly import redis

# Configure Celery to use Redis as the broker and result backend
app = Celery(
    'cron',
    broker='redis://redis:6379/0',  # Use redis service name from docker-compose
    backend='redis://redis:6379/0'
)

# Explicitly set the broker transport
app.conf.broker_transport = 'redis'

@app.on_after_configure.connect
def setup_periodic_tasks(sender: Celery, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    sender.add_periodic_task(30.0, test.s('world'), expires=10)

@app.task
def test(arg):
    print(arg)

@app.task
def add(x, y):
    z = x + y
    print(z)
