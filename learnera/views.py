from django.shortcuts import render
from django.http import HttpResponse
from .models import allcourse,profile,Orders,contribution,Contact
from math import ceil
from django.dispatch import receiver
from allauth.account.signals import user_logged_in,user_signed_up
from Elearning import settings
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


import razorpay
razorpay_client = razorpay.Client(auth=(settings.razorpay_id,settings.razorpay_account_id))

# Create your views here.

def index(request):
    return render(request, 'learnera/index.html')

#def signup(request):
#    return render(request,'learnera/signup.html')

def contact(request):
    contactthank = False
    if request.method == "POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        contactthank = True
    return render(request, 'learnera/contact.html', {'contactthank': contactthank})

def about(request):
    return render(request, 'learnera/about.html')


@csrf_exempt
def handlerequest(request,id):
    print("hello world")
    id = int(id)
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        result = razorpay_client.utility.verify_payment_signature(params_dict)
        Order = Orders.objects.get(order_id=id)
        if result == None:
            amount = (Order.amount) * 100
            try:
                razorpay_client.payment.capture(payment_id, amount)
                Order.payment_status = 1
                Order.save()

                '''## For generating Invoice PDF
                template = get_template('firstapp/payment/invoice.html')
                data = {
                    'order_id': order_db.order_id,
                    'transaction_id': order_db.razorpay_payment_id,
                    'user_email': order_db.user.email,
                    'date': str(order_db.datetime_of_payment),
                    'name': order_db.user.name,
                    'order': order_db,
                    'amount': order_db.total_amount,
                }
                html = template.render(data)
                result = BytesIO()
                pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)  # , link_callback=fetch_resources)
                pdf = result.getvalue()
                filename = 'Invoice_' + data['order_id'] + '.pdf'

                mail_subject = 'Recent Order Details'
                # message = render_to_string('firstapp/payment/emailinvoice.html', {
                #     'user': order_db.user,
                #     'order': order_db
                # })
                context_dict = {
                    'user': order_db.user,
                    'order': order_db
                }
                template = get_template('firstapp/payment/emailinvoice.html')
                message = template.render(context_dict)
                to_email = order_db.user.email
                # email = EmailMessage(
                #     mail_subject,
                #     message, 
                #     settings.EMAIL_HOST_USER,
                #     [to_email]
                # )

                # for including css(only inline css works) in mail and remove autoescape off
                email = EmailMultiAlternatives(
                    mail_subject,
                    "hello",  # necessary to pass some message here
                    settings.EMAIL_HOST_USER,
                    [to_email]
                )
                email.attach_alternative(message, "text/html")
                email.attach(filename, pdf, 'application/pdf')
                email.send(fail_silently=False)'''

                thank = True
                return render(request, 'learnera/paymentsuccesful.html', {'thank': thank})
            except:
                Order.payment_status = 2
                Order.save()
                return render(request, 'learnera/paymentfailed.html')
        else:
            Order.payment_status = 2
            Order.save()
            return render(request, 'learnera/paymentfailed.html')

def checkout(request):
    if request.user.is_anonymous:
        messages.warning(request, 'Login Required For Checkout !')
        return render(request, 'learnera/index.html')

    if request.method=='POST':
        items_json = request.POST.get('itemsJson','')
        amount = request.POST.get('amount','')
        name = request.POST.get('firstName','')+" "+request.POST.get('lastName','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        country = request.POST.get('country','')
        state = request.POST.get('state','')

        order = Orders(items_json=items_json,payment_status=2,amount=amount,name=name,email=email,phone=phone,country=country,state=state)
        order.save()
        thank = True

        order_currency = 'INR'

        amount=int(amount)

        callback_url = 'https://learnerra.herokuapp.com'+"/learnera/handlerequest/"+str(order.order_id)
        print(callback_url)

        razorpay_order=razorpay_client.order.create(dict(amount=amount*100,currency=order_currency,receipt=str(order.order_id),payment_capture='0'))
        return render(request, 'learnera/paymentsummaryrazorpay.html', {'order':order, 'order_id': razorpay_order['id'], 'orderId':order.order_id, 'final_price':amount, 'razorpay_merchant_id':settings.razorpay_id, 'callback_url':callback_url})

    return render(request, 'learnera/checkout.html')

def allcourses(request):
    courses = []
    course = allcourse.objects.values('category', 'id')
    cours = {item['category'] for item in course}
    for cs in cours:
        cst = allcourse.objects.filter(category=cs)
        n = len(cst)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        courses.append([cst, range(1, nSlides), nSlides])
    params = {'courses': courses}
    return render(request, 'learnera/allcourses.html', params)

@receiver(user_logged_in)
def populate_profile(request,sociallogin , user, **kwargs):
    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        print(user_data)
        picture_url = user_data['picture']
        email = user_data['email']
        name = user_data['name']
        u_id = user_data['id']
        Profile = profile(name=name,email=email,picture_url=picture_url,u_id=u_id)
        Profile.save()

@receiver(user_signed_up)
def populate_profile(request,sociallogin , user, **kwargs):
    if sociallogin.account.provider == 'google':
        user_data = user.socialaccount_set.filter(provider='google')[0].extra_data
        print(user_data)
        picture_url = user_data['picture']
        email = user_data['email']
        name = user_data['name']
        u_id = user_data['id']
        Profile = profile(name=name,email=email,picture_url=picture_url,u_id=u_id)
        Profile.save()


def coursedetail(request, id):
    course = allcourse.objects.filter(id=id)
    return render(request, 'learnera/CourseDetail.html', {'course': course[0]})


@csrf_protect
def dashboard(request,id):
    if request.method=='POST':
        social_id = request.POST.get('social_id','')
        socia_email = request.POST.get('social_email','')
        content_url = request.POST.get('contenturl','')
        coursename = request.POST.get('coursename', '')
        cost = request.POST.get('cost', '')
        shortdesc = request.POST.get('shortdesc', '')
        fulldesc = request.POST.get('fulldesc', '')
        Contribution = contribution(social_id=social_id,email=socia_email,content_url=content_url,course_name=coursename,cost=cost,
                                    short_desc=shortdesc,full_desc=fulldesc)

        Contribution.save()
    course = contribution.objects.filter(social_id=id)
    Profile = profile.objects.filter(u_id=id)
    order = Orders.objects.filter(email=Profile[0]).exclude(payment_status=2)
    return render(request,'learnera/dashboard.html',{'course':course,'order':order})
