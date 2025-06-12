from celery import Celery
from celery.schedules import crontab

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

    import mcp_client
    import asyncio
    asyncio.run(mcp_client.main())
    
    return f"Task completed: {arg}"
