from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt


from .forms import RegistrationForm, AccountDetailsForm, AccountAddressForm
from .models import UserBase
from .tokens import account_activation_token

@csrf_exempt
def account_register(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password']) 
            user.is_active = False
            user.save()

            #Setup email
            current_site = get_current_site(request)
            subject = 'Ativar sua conta'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return HttpResponse('Cheque seu email registrado e clique no link para ativação da sua conta!')

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

@csrf_exempt
def account_details(request):
    if request.method == 'POST':
        detailForm = AccountDetailsForm(request.POST)
        if detailForm.is_valid():
            user = request.user
            user.user_name = detailForm.cleaned_data['user_name']
            user.cpf = detailForm.cleaned_data['cpf']
            user.phone_number = detailForm.cleaned_data['phone_number']
            user.save()
            return redirect('account:address')
    else:
        detailForm = AccountDetailsForm()
    return render(request, 'account/registration/account_details.html', {'form': detailForm})


def account_address(request):
    if request.method == 'POST':
        addressForm = AccountAddressForm(request.POST)
        if addressForm.is_valid():
            user = request.user
            user.cep = addressForm.cleaned_data['cep']
            user.address_line_1 = addressForm.cleaned_data['address_line_1'] 
            user.address_line_2 = addressForm.cleaned_data['address_line_2']
            user.city = addressForm.cleaned_data['city']
            user.district = addressForm.cleaned_data['district']
            user.save()
            return redirect('home:home')
    else:
        addressForm = AccountAddressForm()
    return render(request, 'account/registration/account_address.html', {'form': addressForm})

def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserBase.objects.get(pk=uid)
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:details')
    else:
        return render(request, 'home.html')