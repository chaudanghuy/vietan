from django.db import models
from django.conf import settings
from google.oauth2 import service_account
import googleapiclient.discovery
from datetime import datetime as dt, timedelta
import datetime
from mailjet_rest import Client

CALENDAR_ID = settings.CALENDAR_ID
CALENDAR_ORDER_ID = settings.CALENDAR_ORDER_ID
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "./google-credentials.json"


def book_calender_api(booking, booking_date, booking_time, duration, customer_name, customer_phone, total_people, restaurant_address, special_request):
    print("RUNNING CALENDER")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

    start_datetime_str = f"{booking_date}T{booking_time}:00"
    start_datetime = dt.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")

    # Calculate end datetime (start datetime plus 30 minutes)
    end_datetime = start_datetime + timedelta(minutes=duration)

    new_event = {
        "summary": f'Booking: {customer_phone} - {customer_name}',
        "location": f'{restaurant_address}',
        "description": f'Phone: {customer_phone} - {total_people} People - Time: {booking_time} - {special_request}',
        "start": {
            "dateTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        },
        "end": {
            "dateTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        },
        'colorId': '9',
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    print(new_event)
    event = service.events().insert(calendarId=CALENDAR_ID, body=new_event).execute()

    if event:
        booking.booking_event_id = event['id']
        booking.save()
    print(event)
    print("Event created")

def delete_calender_api(event_id):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)
        eventDeleted = service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        print(eventDeleted)
        print('Event deleted')
    except Exception as e:
        print(e)

def update_calendar_api(booking, booking_date, booking_time, duration, customer_name, customer_phone, total_people, restaurant_address, special_request):
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

        start_datetime_str = f"{booking_date}T{booking_time}:00"
        start_datetime = dt.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")

        # Calculate end datetime (start datetime plus 30 minutes)
        end_datetime = start_datetime + timedelta(minutes=duration)

        event = service.events().get(calendarId=CALENDAR_ID, eventId=booking.booking_event_id).execute()

        event['summary'] = f'Booking: {customer_phone} - {customer_name}'
        event['description'] = f'Phone: {customer_phone} - {total_people} People - Time: {booking_time} - {special_request}'
        event['start'] = {
            "dateTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        }
        event['end'] = {
            "dateTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        }
        updated_event = service.events().update(calendarId=CALENDAR_ID, eventId=booking.booking_event_id, body=event).execute()
    except:
        print("Something went wrong")


def order_calender_api(booking_date, booking_time, duration, customer_name, customer_phone, total_people, restaurant_address, detail_request, total_price_html, special_requests):
    print("RUNNING CALENDER")
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = googleapiclient.discovery.build("calendar", "v3", credentials=credentials)

    start_datetime_str = f"{booking_date}T{booking_time}:00"
    start_datetime = dt.strptime(start_datetime_str, "%Y-%m-%dT%H:%M:%S")

    # Calculate end datetime (start datetime plus 30 minutes)
    end_datetime = start_datetime + timedelta(minutes=duration)

    new_event = {
        "summary": f'Order: {customer_phone} - {customer_name}',
        "location": f'{restaurant_address}',
        "description": f'<hr>Phone: {customer_phone} - {customer_name} <hr> {detail_request} <br> {total_price_html} <hr> {special_requests}',
        "start": {
            "dateTime": start_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        },
        "end": {
            "dateTime": end_datetime.strftime("%Y-%m-%dT%H:%M:%S+01:00"),
            "timeZone": "Europe/London",
        },
        'colorId': '9',
        "reminders": {
            "useDefault": False,
            "overrides": [
                {"method": "email", "minutes": 24 * 60},
                {"method": "popup", "minutes": 10},
            ],
        },
    }

    print(new_event)
    service.events().insert(calendarId=CALENDAR_ORDER_ID, body=new_event).execute()
    print("Event created")

def send_email(cust_name, cust_total, book_date, book_time, cus_phone, cus_email):
    mailjet = Client(auth=(settings.MAIL_API_KEY, settings.MAIL_SECRET_KEY))
    data = {
        'FromEmail': settings.FROM_EMAIL,
        'FromName': 'Viet An Restaurant',
        'Subject': 'Your booking at Viet An Restaurant is confirmed',
        'Text-part': 'Your Reservation is confirmed',
        'Html-part': '<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Table Booking Confirmation</title> <!-- Include FontAwesome --> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"> <style> body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; } .container { width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); } .header { text-align: center; padding-bottom: 20px; } .header img { width: 100px; } .header h1 { margin: 0; color: #d9534f; } .content { line-height: 1.6; } .content h2 { color: #d9534f; } .content p { margin: 10px 0; } .details-table { width: 100%; border-collapse: collapse; margin-top: 20px; } .details-table th, .details-table td { border: 1px solid #ddd; padding: 8px; text-align: left; } .details-table th { background-color: #f8f8f8; color: #333; }.terms { margin-top: 20px; font-size: 0.9em; color: #555; } .terms h3 { color: #d9534f; } .footer { margin-top: 20px; text-align: center; color: #777; } .footer a { color: #d9534f; text-decoration: none; } </style></head><body> <div class="container"> <div class="header"> <img src="https://vietan.phapsuit.com/static/demo1/assets/img/logo.png" width="100px" alt="Viet An Restaurant Logo"> <h1>Viet An Restaurant</h1> </div> <div class="content"> <h2><i class="fas fa-utensils"></i> Your reservation is confirmed</h2> <p>Dear [[var:customer]],</p> <p>Thank you for your reservation at Viet An Restaurant. We are pleased to confirm your booking as follows:</p> <table class="details-table"> <tr> <th><i class="fas fa-user-friends"></i> Number of People</th> <td>[[var:total]]</td> </tr> <tr> <th><i class="fas fa-calendar-alt"></i> Date</th> <td>[[var:date]]</td> </tr> <tr> <th><i class="fas fa-clock"></i> Time</th> <td>[[var:time]]</td> </tr> <tr> <th><i class="fas fa-user"></i> Name</th> <td>[[var:customer]]</td> </tr> <tr> <th><i class="fas fa-phone"></i> Phone</th> <td>[[var:phone]]</td> </tr> <tr> <th><i class="fas fa-envelope"></i> Email</th> <td>[[var:email]]</td> </tr> </table> <p>We look forward to serving you a delightful dining experience.</p> <p>If you have any changes to your booking or need to contact us for any reason, please don\'t hesitate to reach out.</p> </div><div class="terms"> <h3>Terms and Conditions</h3> <p>Please note the following terms and conditions for your booking:</p> <ul> <li>Please arrive on time to ensure your reservation. If you are running late, kindly inform us in advance.</li> <li>Cancellations or changes to the booking should be made at least 24 hours prior to the reservation time.</li> <li>In case of any special requests or dietary requirements, please let us know in advance so we can accommodate them.</li> <li>We reserve the right to cancel or modify reservations if necessary, with prior notice.</li> </ul> </div> <div class="footer"> <p>Thank you,<br> Viet An Restaurant Team, <br>73-75 Skene Street, Aberdeen, AB10 1QD</p> <p>If there are any changes to your booking, please contact us at <a href="tel:+01224356826">+01224356826</a> or reply to this email.</p> </div> </div></body></html>',
        'Vars': {
            "customer": cust_name,
            "total": cust_total,
            "date": book_date,
            "time": book_time,
            "phone": cus_phone,
            "email": cus_email
        },
        'Recipients': 
        [
            {
                "Email": cus_email,
                "Name": cust_name
            },
            {
                "Email": settings.CC_EMAIL,
                "Name": "Viet An Restaurant"
            }
        ]
    }
    result = mailjet.send.create(data=data)    

def get_day_suffix(day):
    if 11 <= day <= 13:
        return 'th'
    if day % 10 == 1:
        return 'st'
    if day % 10 == 2:
        return 'nd'
    if day % 10 == 3:
        return 'rd'
    return 'th'    