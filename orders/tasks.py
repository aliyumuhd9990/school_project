from celery import shared_task
from time import sleep

@shared_task
def order_created(order_id):
    """Simulate order processing"""
    sleep(5)  # Simulate delay
    return f"Order {order_id} processed successfully!"
