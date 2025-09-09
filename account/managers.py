from django.contrib.auth.models import BaseUserManager


class AccountManager(BaseUserManager):
    def create_user(self, username, email, cpf, password, save=False, **extra_fields):
        if not username:
            raise ValueError("O nome de usuário é obrigatório")
        if not email:
            raise ValueError("O email é obrigatório")
        if not cpf:
            raise ValueError("O CPF é obrigatório")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, cpf=cpf, **extra_fields)
        user.set_password(password)
        if save:
            user.save(using=self._db)
        return user

    def create_superuser(self, username, email, cpf, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("type", "admin")

        return self.create_user(
            username, email, cpf, password, save=True, **extra_fields
        )
