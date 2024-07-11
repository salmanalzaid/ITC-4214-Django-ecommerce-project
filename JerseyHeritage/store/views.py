from django.shortcuts import render, redirect
from .models import Product, Category
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm
from django import forms
# Create your views here.

def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products':products})

def about(request):
    return render(request, 'about.html', {})

def category(request, look):
    look=  look.replace('-', ' ')
    
    try:
        category = Category.objects.get(name=look)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products,'category':category})
    except:
        messages.success(request, ("The category doesn't exist"))

        return redirect('home')
        
#logging in account 

def login_user(request):
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("You successfully Logged in! "))
            return redirect('home')
        
        else:
            messages.success(request, ("The Username or Password is incorrect Please try again "))
            return redirect('login')
    else:
        
        return render(request, 'login.html', {})

# logging out 
def logout_user(request):
    logout(request)
    messages.success(request, ("you successfully loged out !"))
    return redirect('home')

#registering a new user
def register_user(request):
    
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You are part of the family now, Welcome to the JerseyHeritage !"))
            return redirect('home')
        
        else:
            messages.success(request, ("OOPS!! something went wrong, try again :)"))
            return redirect('register')

                
    return render(request, 'register.html', {'form':form} )

def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product':product})


# update the profile 

def update_user(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		user_form = UpdateUserForm(request.POST or None, instance=current_user)

		if user_form.is_valid():
			user_form.save()

			login(request, current_user)
			messages.success(request, "User Has Been Updated!!")
			return redirect('home')
		return render(request, "update_user.html", {'user_form':user_form})
	else:
		messages.success(request, "You Must Be Logged In To Access That Page!!")
		return redirect('home')

#update password 
def update_password(request):
	if request.user.is_authenticated:
		current_user = request.user
		# Did they fill out the form
		if request.method  == 'POST':
			form = ChangePasswordForm(current_user, request.POST)
			# Is the form valid
			if form.is_valid():
				form.save()
				messages.success(request, "Your Password Has Been Updated Successfully ")
				login(request, current_user)
				return redirect('update_user')
			else:
				for error in list(form.errors.values()):
					messages.error(request, error)
					return redirect('update_password')
		else:
			form = ChangePasswordForm(current_user)
			return render(request, "update_password.html", {'form':form})
	else:
		messages.success(request, "You Must Be Logged In To View That Page...")
		return redirect('home')

#search for products

def search(request):
    
	if request.method == "POST":
     
		searched = request.POST['searched']
		#searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
  
		if not searched:
			messages.success(request, "That Product Does Not Exist...Please try Again.")
			return render(request, "search.html", {})

		else:
			return render(request, "search.html", {'searched':searched})

	else:
		return render(request, "search.html", {})