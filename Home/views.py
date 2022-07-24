from itertools import product
from multiprocessing import context
from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from .models import Product, Blogs
from django.contrib.auth.hashers import make_password
from django.contrib.auth import   get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import  View
from django.contrib.auth.decorators import login_required
from .forms import *
import json
from django.contrib.auth.models import User

from .models import *
from django.http import JsonResponse


# For reset password
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def home(request):

    return render(request,'home/home.html',)

@login_required(login_url="login")
def profile(request):
    email = request.POST.get('email')
    customer = Customer.get_customer_by_email(email)


    return render(request,'Account/profile.html',{'customer': customer})


class Signup(View):
    def get(self, request):
        return render(request, 'Account/signuplogin.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('productpage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'Account/signuplogin.html', data)

    def validateCustomer(self, customer):
        error_message = None;
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message


class Login(View):
    return_url = None
    def get(self , request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'Account/signuplogin.html')

    def post(self , request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('/store')
            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request,'Account/signuplogin.html',{'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')


def categorie(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories

    print('you are : ', request.session.get('email'))
    return render(request, 'productpage/categorie.html', data)  

def SearchView(request):
    query = request.GET['query']
    products = Product.objects.filter(name__icontains =query)
    context ={ 'products':products}
    return render(request,'productpage/search.html',context)    

def searchresult(request):
    query = request.GET['query']
    products = Product.objects.filter(name__icontains =query)
    context ={ 'products':products}
    return render(request,'productpage/search.html',context)  

def productpage(request):
    if(request.method == 'POST'):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('/store')
    else:
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

    
def store(request):
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        products = None
        categories = Category.get_all_categories()
        customer = Customer.objects.all()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();

        data = {}
        data['products'] = products
        data['categories'] = categories
        

        print('you are : ', request.session.get('email'))
        return render(request, 'productpage/productpage.html', data)

class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'productpage/cart.html' , {'products' : products} )

def edit(request, id):
    numbers = Product.objects.get(id=id)
    products = Product.objects.all()
    context  = {
        'products': products,'numbers' : numbers
      }
    print(request)
    if(request.method == "POST"):
        try:
            review = ReviewForm(request.POST,request.FILES)
            if review.is_valid():
                review.save()
                return redirect("/")

        except:
            print(request)
    if request.method =='POST':
        form = orderform(request.POST)
        if form.is_valid(): 
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"your order has been placed " + user)
                print(form)
        else:
            print(form)
            messages.success(request,"your order could not be placed " )
        return redirect('/')     
                

    return render(request,'productpage/edit.html',context)




def contact(request):

    if request.method =='POST':

        form = contact(request.POST  or None)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,"your enquiry has been submitted " + user)
            print(form)
            return render(request, 'contact/contactus.html')


    return render(request, 'contact/contact.html')     



class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):


    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request , 'productpage/orders.html'  , {'orders' : orders})

def delete_cart(request,id):
    cart = Cart(request)
    cart.delete(id)
    messages.error(request,"item has removed")
    context = {
            'cart':cart
          }
    return render(request,'store/cart.html',context)

def showblog(request):
    user = get_user_model()
    blogs=Blogs.objects.all()

    return render (request,"blog/blogpage.html",{'blogs':blogs,})

def blog_detail(request, id):
    single_blog = get_object_or_404(Blogs, pk=id)
    if(request.method == "POST"):
        try:
            comment = CommentForm(request.POST,request.FILES)
            if comment.is_valid():
                comment.save()
                return redirect("/blog/")

        except:
            print(request)

    # usercount = User.objects.all().filter(is_superuser=False).count()
    # productcount = Products.objects.all().count()
    # productcount = Khana.objects.all().count()

    data = {
        'single_blog': single_blog,
    #     'single_blog': single_blog,
    #     'product':productcount,
       
    #     'usercount':usercount,
    #     # 'bookingcount':bookingcount,
    #     'productcount':productcount,
    }

    return render(request, 'blog/blog_detail.html', data)

def view_comment(request):
    user = get_user_model()
    comment=Comment.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    
    data = {
        'comment': comment,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
    }

    return render (request,"admin/view_comment.html", data)

def view_review(request):
    user = get_user_model()
    review=Review.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    
    data = {
        'review': review,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
    }

    return render (request,"admin/view_review.html", data)

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "Account/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'sthronesh11@gmail.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="Account/password_reset_form.html", context={"password_reset_form":password_reset_form})


def admin_dashboard_view(request):
    user = get_user_model()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    #bookingcount = Booking.objects.all().count()
    
    order = Product.objects.all()
    data = {
        'order': order,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
    }
    return render(request, 'admin/admindashboard.html',data)

def view_customer(request):
    User = get_user_model()
    user_data = Customer.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    #bookingcount = Booking.objects.all().count()
    data = {
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
        'Customer':user_data
        
    }
    return render(request,'admin/view_customer.html',data)

def delete_customer(request, p_id):
    customer = Customer.objects.get(id=p_id)
    customer.delete()
    return redirect('/view-customer')

def view_blog(request):
    user = get_user_model()
    single_blog=Blogs.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    #bookingcount = Booking.objects.all().count()
    data = {
        'single_blog':single_blog,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
        
    }
    return render(request,'admin/view_blog.html',data)

def edit_blog(request,p_id):

    try:

       blog=Blogs.objects.get(blog_id=p_id)

       return render(request, "admin/blog_edit.html", {'single_blog':blog})

    except:

       print("No Data Found")

    return redirect("/view-blog")

def update_blog(request,p_id):

    blog=Blogs.objects.get(blog_id=p_id)
    form=BlogForm(request.POST,request.FILES, instance=blog)
    form.save()

    return redirect ("/view-blog")

def delete_blog(request, p_id):
    blog = Blogs.objects.get(blog_id=p_id)
    blog.delete()
    return redirect('/view-blog')


def blogform(request):

    print(request.FILES)
    usercount = Customer.objects.all().count()
    #bookingcount = Booking.objects.all().count()
    productcount = Product.objects.all().count()

    data={
            'usercount':usercount,
            #'bookingcount':bookingcount,
            'productcount':productcount,     
        }


 

    if request.method=="POST":

        blogs=BlogForm(request.POST,request.FILES)
       

        blogs.save()
        return redirect ("blog")

    else:

        blogs=BlogForm()

     

    return render (request,"admin/blog_form.html",data)

def view_product(request):
    user = get_user_model()
    product=Product.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()
    #bookingcount = Booking.objects.all().count()
    data = {
        'product':product,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
        
    }
    return render(request,'admin/view_product.html',data)

def productform(request):
    product=Product.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()

    print(request.POST,request.FILES)
    data = {
        'product':product,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
        
    }

    if request.method=="POST":

        product=ProductsForm(request.POST,request.FILES)
        print(" has been readt")
        if product.is_valid():
            print(" has been saved")
            product.save()
            return redirect ("/view-product")

    else:
        print(" has ")
        product=ProductsForm()

     

    return render (request,"admin/product_form.html",{'product':product})

def edit_product(request,p_id):

    try:

       product=Product.objects.get(id=p_id)

       return render(request, "admin/product_edit.html", {'product':product})

    except:

       print("No Data Found")

    return redirect("/view-product")

def update_product(request,p_id):

    product=Product.objects.get(id=p_id)

    form=ProductsForm(request.POST, instance=product)

    form.save()

    return redirect ("/view-product")

def delete_product(request, p_id):
    product = Product.objects.get(id=p_id)
    product.delete()
    return redirect('/view-product')

#changes made by sarthak for khalti
def verify_payment(request):
   data = request.POST
   product_id = data['product_identity']
   token = data['token']
   amount = data['amount']

   url = "https://khalti.com/api/v2/payment/verify/"
   payload = {
   "token": token,
   "amount": amount
   }
   headers = {
   "Authorization": "Key test_secret_key_c406db1d5d0e425a991d6de296d329e3"
   }
   

   response = request.post(url, payload, headers = headers)
   
   response_data = json.loads(response.text)
   status_code = str(response.status_code)

   if status_code == '400':
      response = JsonResponse({'status':'false','message':response_data['detail']}, status=500)
      return response

   import pprint 
   pp = pprint.PrettyPrinter(indent=4)
   pp.pprint(response_data)
   
   return JsonResponse(f"Payment Done !! With IDX. {response_data['user']['idx']}",safe=False)

def creator(request):
    print(request)
    if request.method == 'POST':
        form = Creator(request.POST or None)
        if form.is_valid():
            # if Customer.objects.filter(first_name=request.POST['first_name']).exists():
            #     messages.error(request,"username already exists")
            #     return render(request, 'account/signupascreator.html')
            # else:
            form.save()
            user = form.cleaned_data.get('firstname')
            messages.success(request, "you can now login " + user)
            print(form)
            
        return redirect('/logincreator')
    
    return render(request,'Account/signupascreator.html',)

def logincreator(request):
    if request.method=='POST':
        print(request)
        username=request.POST["username"]
        password=request.POST["password"]
     
        customers=signupasseller.objects.get(username=username,password=password)
        request.session['username']=request.POST['username']
        request.session['id']=customers.id
        return redirect ('/creatordashboard')
    else:
        form= signupasseller()
        print("invalid")
    return render(request,'Account/creatorlogin.html',)

def creatordashboard(request):
    product=Product.objects.all()
    usercount = Customer.objects.all().count()
    productcount = Product.objects.all().count()

    print(request.POST,request.FILES)
    data = {
        'product':product,
        'usercount':usercount,
        #'bookingcount':bookingcount,
        'productcount':productcount,
        
    }

    if request.method=="POST":

        product=ProductsForm(request.POST,request.FILES)
        print(" has been readt")
        if product.is_valid():
            print(" has been saved")
            product.save()
            return render(request,'Account/creatordashboard.html',data)

    else:
        print(" has ")
        product=ProductsForm()

   
    return render(request,'Account/creatordashboard.html',data)


def logoutcreator(request):
    request.session.clear()
    return redirect('/logincreator')


def creatorprofile(request):
    customers = signupasseller.objects.get(username=request.session['username'])
    context  = {
            'customers': customers
            
            }
    return render(request,'Account/creatorprofile.html',context)




def adminlogin(request):
    if request.method=='POST':
        print(request)
        username=request.POST["Username"]
        password=request.POST["Password"]
   
        customers=adminaccount.objects.get(username=username,password=password)
        request.session['username']=request.POST['Username']
        request.session['id']=customers.id
        return redirect ('/admindashboard')
        
                
    return render(request, 'admin/adminlogin.html')