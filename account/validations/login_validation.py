from account.models import Account

def validate_login(email, password):
    try:
        user = Account.objects.get(email=email)

        if user.check_password(password):
            return user, None
        else:
            return None, "Senha inválida."
    except Account.DoesNotExist:
        return None, "Usuário não encontrado."
