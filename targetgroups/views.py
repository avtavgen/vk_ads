from itertools import islice

import requests
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from .tasks import handle_uploaded_file

from .forms import NewTargetGroupForm

from vk_test.settings import CLIENT_ID, CLIENT_REDIRECT_URL, CLIENT_LOGIN_URL, CLIENT_KEY, CLIENT_ACCESS_URL, \
    CREATE_TARGET_GROUP, GET_TARGET_GROUPS, IMPORT_CONTACTS


def start(request):
    return render(request, 'targetgroups/index.html')


def auth(request):
    auth_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': CLIENT_REDIRECT_URL,
        'display': 'page',
        'response_type': 'code',
        'scope': 'ads'
    }
    response = requests.get(CLIENT_LOGIN_URL, params=auth_params)
    return redirect(response.url)


def get_token(request):
    auth_params = {
        'client_id': CLIENT_ID,
        'redirect_uri': CLIENT_REDIRECT_URL,
        'client_secret': CLIENT_KEY,
        'code': request.GET.get('code')
    }
    response = requests.get(CLIENT_ACCESS_URL, params=auth_params)
    data = json.loads(response.text)
    request.session['access_token'] = data['access_token']
    return redirect('targetgroups:new_group')


def new_group(request):
    if request.method == 'POST':
        form = NewTargetGroupForm(request.POST, request.FILES)
        request.session['account_id'] = request.POST['account_id']
        if form.is_valid():
            cd = form.cleaned_data
            request.session['account_id'] = cd['account_id']
            data = {
                'account_id': cd['account_id'],
                'name': cd['name'],
                'lifetime': 100,
                'access_token': request.session.get('access_token')
            }
            response = requests.get(CREATE_TARGET_GROUP, params=data)
            j = json.loads(response.text)
            group_id = j['response']['id']
            data_file = request.FILES['file']
            for chunk in data_file.chunks():
                handle_uploaded_file.delay(str(chunk,'utf-8'),
                                     request.session.get('account_id'),
                                     group_id,
                                     request.session.get('access_token'))
            return HttpResponseRedirect('targetgroups:group_list')
    else:
        form = NewTargetGroupForm()
    return render(request, 'targetgroups/groups.html', {'form': form})


def group_list(request):
    data = {
        'account_id': request.session.get('account_id'),
        'access_token': request.session.get('access_token')
    }
    response = requests.get(GET_TARGET_GROUPS, params=data)
    j = json.loads(response.text)
    group_list = j['response']
    return render(request, 'targetgroups/grop_list.html', {'group_list': group_list})

