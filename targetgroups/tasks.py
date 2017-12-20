from __future__ import absolute_import, unicode_literals
import requests
from celery import shared_task
from itertools import islice

from vk_test.settings import IMPORT_CONTACTS


@shared_task
def handle_uploaded_file(file, account_id, target_group_id, access_token):
    lines = islice(file.split('\r\n'), 1000)
    for contact in lines:
        data = {
            'account_id': account_id,
            'target_group_id': target_group_id,
            'access_token': access_token,
            'contacts': contact
        }
        response = requests.get(IMPORT_CONTACTS, params=data)
