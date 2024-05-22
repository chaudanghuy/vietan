from django.test import TestCase
from .models import User
from django.http.response import HttpResponse, JsonResponse
from . import helpers
from mailjet_rest import Client
from django.conf import settings

# Create your tests here.
# Test
def create_test_user(request):
    user = User.objects.create_user(username='demo', password='123')
    
    user.first_name = 'Alice'
    user.last_name = 'Firstimer'
    user.save()
    return HttpResponse("Test user created.")

def dummy_mail(request):
    mailjet = Client(auth=(settings.MAIL_API_KEY, settings.MAIL_SECRET_KEY))
    data = {
        'FromEmail': 'admin@phapsuit.com',
        'FromName': 'Mailjet Pilot',
        'Subject': 'Your email flight plan!',
        'Text-part': 'Dear passenger, welcome to Mailjet! May the delivery force be with you!',
        'Html-part': '<h3>Dear passenger, welcome to <a href=\"https://www.mailjet.com/\">Mailjet</a>!<br />May the delivery force be with you!',
        'Recipients': [{'Email':'chaudanghuy6789@gmail.com'}]
    }
    result = mailjet.send.create(data=data)
    return JsonResponse(result.json())       

def dummy_booking(request):
    mailjet = Client(auth=(settings.MAIL_API_KEY, settings.MAIL_SECRET_KEY))
    data = {
        'FromEmail': 'admin@phapsuit.com',
        'FromName': 'Viet An Restaurant',
        'Subject': 'Your booking at Viet An Restaurant is confirmed',
        'Text-part': 'Your Reservation is confirmed',
        'Html-part': '<!DOCTYPE html><html lang="en"><head> <meta charset="UTF-8"> <meta name="viewport" content="width=device-width, initial-scale=1.0"> <title>Table Booking Confirmation</title> <!-- Include FontAwesome --> <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css"> <style> body { font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; color: #333; } .container { width: 100%; max-width: 600px; margin: 0 auto; background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); } .header { text-align: center; padding-bottom: 20px; } .header img { width: 100px; } .header h1 { margin: 0; color: #d9534f; } .content { line-height: 1.6; } .content h2 { color: #d9534f; } .content p { margin: 10px 0; } .details-table { width: 100%; border-collapse: collapse; margin-top: 20px; } .details-table th, .details-table td { border: 1px solid #ddd; padding: 8px; text-align: left; } .details-table th { background-color: #f8f8f8; color: #333; }.terms { margin-top: 20px; font-size: 0.9em; color: #555; } .terms h3 { color: #d9534f; } .footer { margin-top: 20px; text-align: center; color: #777; } .footer a { color: #d9534f; text-decoration: none; } </style></head><body> <div class="container"> <div class="header"> <img src="https://vietan.phapsuit.com/static/demo1/assets/img/logo.png" width="100px" alt="Viet An Restaurant Logo"> <h1>Viet An Restaurant</h1> </div> <div class="content"> <h2><i class="fas fa-utensils"></i> Your reservation is confirmed</h2> <p>Dear [[var:customer]],</p> <p>Thank you for your reservation at Viet An Restaurant. We are pleased to confirm your booking as follows:</p> <table class="details-table"> <tr> <th><i class="fas fa-user-friends"></i> Number of People</th> <td>[[var:total]]</td> </tr> <tr> <th><i class="fas fa-calendar-alt"></i> Date</th> <td>[[var:date]]</td> </tr> <tr> <th><i class="fas fa-clock"></i> Time</th> <td>[[var:time]]</td> </tr> <tr> <th><i class="fas fa-user"></i> Name</th> <td>[[var:customer]]</td> </tr> <tr> <th><i class="fas fa-phone"></i> Phone</th> <td>[[var:phone]]</td> </tr> <tr> <th><i class="fas fa-envelope"></i> Email</th> <td>[[var:email]]</td> </tr> </table> <p>We look forward to serving you a delightful dining experience.</p> <p>If you have any changes to your booking or need to contact us for any reason, please don\'t hesitate to reach out.</p> </div><div class="terms"> <h3>Terms and Conditions</h3> <p>Please note the following terms and conditions for your booking:</p> <ul> <li>Please arrive on time to ensure your reservation. If you are running late, kindly inform us in advance.</li> <li>Cancellations or changes to the booking should be made at least 24 hours prior to the reservation time.</li> <li>In case of any special requests or dietary requirements, please let us know in advance so we can accommodate them.</li> <li>We reserve the right to cancel or modify reservations if necessary, with prior notice.</li> </ul> </div> <div class="footer"> <p>Thank you,<br> Viet An Restaurant Team, <br>73-75 Skene Street, Aberdeen, AB10 1QD</p> <p>If there are any changes to your booking, please contact us at <a href="tel:+01224356826">+01224356826</a> or reply to this email.</p> </div> </div></body></html>',
        'Vars': {
            "customer": "Alice Firstimer",
            "total": 2,
            "date": "July 18th, 2024",
            "time": "11:00",
            "phone": "888888888",
            "email": "chaudanghuy6789@gmail.com"
        },
        'Recipients': 
        [
            {
                "Email": "chaudanghuy6789@gmail.com",
                "Name": "passenger 1"
            }
        ]
    }
    result = mailjet.send.create(data=data)
    return JsonResponse(result.json())       