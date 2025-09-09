from django.test import TestCase
from django.utils import timezone
from group.models import Group
from account.models import Account, AccountType
import os
from django.conf import settings



class GroupModelTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(
            username="user1", 
            email="user1@example.com", 
            cpf="11500634670", 
            type=AccountType.FREE.value
        )
        self.account2 = Account.objects.create(
            username="user2", 
            email="user2@example.com", 
            cpf="02055626639", 
            type=AccountType.FREE.value
        )
        icon_path = os.path.join(settings.MEDIA_ROOT, 'icons', 'icon.png')
        
        self.group = Group.objects.create(
            name="Test Group",
            icon=icon_path,
            begin=timezone.now().date(),
            end=timezone.now().date(),
        )

    def test_string_representation(self):
        
        self.assertEqual(str(self.group), f"#{self.group.id} | Test Group")

def test_group_accounts(self):

    self.assertEqual(self.group.accounts.count(), 0)

    self.group.accounts.add(self.account1)
    self.account1.refresh_from_db()
    self.assertEqual(self.group.accounts.count(), 1)
    self.assertEqual(self.account1.type, AccountType.PREMIUM.value)

    self.group.accounts.add(self.account2)
    self.account2.refresh_from_db()
    self.assertEqual(self.group.accounts.count(), 2)
    self.assertEqual(self.account2.type, AccountType.PREMIUM.value)

    self.group.accounts.remove(self.account1)
    self.account1.refresh_from_db()
    self.assertEqual(self.group.accounts.count(), 1)
    self.assertEqual(self.account1.type, AccountType.FREE.value)

    self.group.accounts.remove(self.account2)
    self.account2.refresh_from_db()
    self.assertEqual(self.group.accounts.count(), 0)
    self.assertEqual(self.account2.type, AccountType.FREE.value)
