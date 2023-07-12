from datetime import datetime, timedelta

import httpx
from apscheduler.schedulers.background import BackgroundScheduler
from choices import BookingChoice, StatusChoice

hold_scheduler = BackgroundScheduler()
hold_scheduler.start()


def repeat_hold_payment(booking):
    response = httpx.post(
        'https://api.cloudpayments.ru/payments/tokens/auth',
        auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
        json={
            'Amount': booking.hold_sum(),
            'Currency': 'KZT',
            'AccountId': booking.user.id,
            'Token': booking.user.encrypted_card_token,
        },
    )
    response_data = response.json()
    if response_data['Success']:
        booking.booking_status = BookingChoice.HOLD
        booking.transaction_id = response_data['Model']['TransactionId']
    else:
        booking.booking_status = BookingChoice.CANCELED


def hold_payment_now(booking):
    print("начинаю холдирование")
    response = httpx.post(
        'https://api.cloudpayments.ru/payments/tokens/auth',
        auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
        json={
            'Amount': booking.hold_sum(),
            'Currency': 'KZT',
            'AccountId': booking.user.id,
            'Token':  booking.user.encrypted_card_token,
        },
    )
    print(response.json())
    response_data = response.json()
    if response_data['Success']:
        print("success true")
        booking.booking_status = BookingChoice.HOLD
        booking.transaction_id = response_data['Model']['TransactionId']
        booking.save()
    else:
        print("success false")
        hold_scheduler.add_job(
            repeat_hold_payment,
            'date',
            run_date=datetime.now() + timedelta(days=1),
            args=(booking,),
            id=f'{booking.id}'
        ) #при отмене брони юзером нужно у hold_scheduler убирать джоб на холд или на повторную заморозку
        hold_scheduler.print_jobs()


def schedule_payment(booking_with_hold):
    for booking in booking_with_hold:
        response = httpx.post(
            'https://api.cloudpayments.ru/payments/tokens/confirm',
            auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
            json={
                'Amount': booking.confirm_payment_sum(),
                'Currency': 'KZT',
                'AccountId': booking.user.id,
                'Token': booking.user.encrypted_card_token,
                'TransactionId': booking.transaction_id,
            },
        )
        response_data = response.json()
        if response_data['Success']:
            booking.booking_status = BookingChoice.PAYED
            booking.save()
        else:
            booking.booking_status = BookingChoice.CANCELED
            booking.save()


def cancel_tour(tour, booking_with_hold):
    tour.moderation_status = StatusChoice.CANCELED
    for booking in booking_with_hold:
        response = httpx.post(
            'https://api.cloudpayments.ru/payments/void',
            auth=('pk_aad02fa59dec0bacabf00955821fd', '9b431e1c5d36c6c36d01b7635751af5f'),
            json={
                'TransactionId': booking.transaction_id,
            },
        )
        booking.booking_status = BookingChoice.CANCELED
        booking.save()


def is_enough_tourist(tour):
    tourists = 0
    booking_with_hold = tour.users.filter(booking_status=BookingChoice.HOLD)
    for booking in booking_with_hold:
        tourists += booking.passengers.count()
    if tourists >= tour.min_number_of_tourists:
        return schedule_payment(booking_with_hold)
    else:
        return cancel_tour(tour, booking_with_hold)
