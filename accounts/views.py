from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import auth


def login(request):
    if request.user.is_authenticated:
        pass
        # return render(request, 'app/home/login.html')
        return redirect('scheduleapp:dashboard')
    else:
        if request.method == 'POST':
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                # print("hello")
                # t1.start()
                # t1.join()
                # return render(request, 'app/home/login.html', {'segment': 'index'})
                return redirect('scheduleapp:dashboard')

            else:
                # return render(request, 'scheduleapp/accounts/page-403.html', {'error': 'invalid username or password'})
                return render(request, 'scheduleapp/accounts/page-403.html')
        else:
            return render(request, 'scheduleapp/accounts/login.html')
        # return render(request, 'app/accounts/login.html')

def register(request):
    return render(request, 'scheduleapp/accounts/register.html')


def logout(request):
    auth.logout(request)
    return redirect('accounts:login')




