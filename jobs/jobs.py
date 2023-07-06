from datetime import datetime, timedelta
import time
from apscheduler.schedulers.background import BackgroundScheduler
from django.contrib.auth import get_user_model
from tours.models.tour import Tour
from booking.models import Booking
import httpx
from choices import StatusChoice, BookingChoice


def confirmed_payment():
    pass
    # tour = Tour.objects.all()
    # if tour.min_number_of_tourist >
    # response = httpx.post(
    #     'https://api.cloudpayments.ru/payments/void',
    #     auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
    #     json={
    #         'amount': tour.max_seat_hold_price() * 'count passengers', # отдельный метод с проверкой
    #         'currency': 'KZT',
    #         'account_id': 'request.user.id',
    #         'token': 'token s bazy',
    #     },
    # )


def hold_payment(request):
    print(request.user)
    # scheduler = BackgroundScheduler()
    # scheduler.add_job(confirmed_payment(1, 2), 'date', run_date=datetime(2023, 7, 5, 23, 18, 0))
    # scheduler.start()
    # tour = Tour.objects.all()
    # booking = Booking.objects.all()
    # if booking.booking_status == BookingChoice.RESERVED:
    #     response = httpx.post(
    #         'https://api.cloudpayments.ru/payments/void',
    #         auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
    #         json={
    #             'amount': booking.hold_sum(),
    #             'currency': 'KZT',
    #             'account_id': get_user_model(),
    #             'token': 'token s bazy',
    #         },
    #     )
    #     if response.success:
    #         booking.booking_status = BookingChoice.HOLD
    #         booking.transaction_id = response['Model']['TransactionId']
            # scheduler.add_job(confirmed_payment, 'date', run_date=tour.start_date - timedelta(days=1))
