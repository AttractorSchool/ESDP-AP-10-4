from datetime import datetime, timedelta

import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from choices import BookingChoice


def hold_payment_now(booking):
    scheduler = BackgroundScheduler()
    response = httpx.post(
        'https://api.cloudpayments.ru/payments/tokens/auth',
        auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
        json={
            'Amount': booking.hold_sum(),
            'Currency': 'KZT',
            'AccountId': booking.user,
            'Token':  booking.user.encrypted_card_token,
        },
    )
    print(response)
    response_data = response.json()
    if response_data['Model'] == "true":
        booking.booking_status = BookingChoice.HOLD
        booking.transaction_id = response_data['Model']['TransactionId']
    else:
        scheduler.add_job(repeat_hold_payment(booking), 'date', run_date=datetime.now() + timedelta(days=1))


def repeat_hold_payment(booking):
    response = httpx.post(
        'https://api.cloudpayments.ru/payments/tokens/auth',
        auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
        json={
            'Amount': booking.hold_sum(),
            'Currency': 'KZT',
            'AccountId': booking.user,
            'Token': booking.user.encrypted_card_token,
        },
    )
    response_data = response.json()
    if response_data['Model'] == "true":
        booking.booking_status = BookingChoice.HOLD
        booking.transaction_id = response_data['Model']['TransactionId']
    else:
        booking.booking_status = BookingChoice.CANCELED


def schedule_payment(booking_with_hold):
    for booking in booking_with_hold:
        response = httpx.post(
            'https://api.cloudpayments.ru/payments/tokens/confirm',
            auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
            json={
                'Amount': booking.confirm_payment_sum(),
                'Currency': 'KZT',
                'AccountId': booking.user,
                'Token': booking.user.encrypted_card_token,
                'TransactionId': booking.transaction_id,
            },
        )
        response_data = response.json()
        if response_data['Model'] == "true":
            booking.booking_status = BookingChoice.PAYED
        else:
            booking.booking_status = BookingChoice.CANCELED


def is_enough_tourist(tour):
    tourists = 0
    booking_with_hold = tour.users.filter(booking_status=BookingChoice.HOLD)
    for booking in booking_with_hold:
        tourists += booking.passengers.count()
    if tourists >= tour.min_number_of_tourists:
        return schedule_payment(booking_with_hold)
