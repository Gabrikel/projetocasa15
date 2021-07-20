from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.decorators.csrf import csrf_exempt


from .forms import RegistrationForm, AccountDetailsForm
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
            user.user_name = registerForm.cleaned_data['user_name']
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password']) 
            user.is_active = False
            user.save()
            return redirect('account:details')

    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})

@csrf_exempt
def account_details(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        detailForm = AccountDetailsForm(request.POST)
        if detailForm.is_valid():
            user = detailForm.save(commit=False)
            user.cpf = detailForm.cleaned_data['cpf']
            user.phone_number = detailForm.cleaned_data['number_phone']
            user.cep = detailForm.cleaned_data['cep']
            user.address_line_1 = detailForm.cleaned_data['address_line_1'] 
            user.address_line_2 = detailForm.cleaned_data['address_line_2']
            user.city = detailForm.cleaned_data['city']
            user.district = detailForm.cleaned_data['district']
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
            return HttpResponse('registered succesfully and activation sent')
    else:
        detailForm = AccountDetailsForm()
    return render(request, 'account/registration/account_details.html', {'form': detailForm})



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
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')