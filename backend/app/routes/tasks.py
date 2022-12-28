from random import choice, randint
from fastapi import APIRouter

from app.worker import my_delay_task


router = APIRouter()


@router.get("/")
async def go_task():
    """ Test Celery task
    """
    count = randint(1, 10)
    heroes = ['Spyder-Man', 'Superman',
              'Dr.Strange', 'Moon Knight', 'Wanda', 'Loki']
    for i in range(count):
        my_delay_task.delay(choice(heroes), i)
    return {'task_count': count}
