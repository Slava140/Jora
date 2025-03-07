import time

from app import dramatiq

broker = dramatiq.broker


@dramatiq.actor()
def test_actor():
    print('Долгий процесс начался')
    time.sleep(30)
    print('Долгий процесс завершился')
