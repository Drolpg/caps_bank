from django.core.exceptions import ValidationError
from validate_docbr import CPF
import re
from account.models import Account  

def validate_cpf(cpf):

    cpf_validator = CPF()
    if len(cpf) > 11:
        raise ValidationError("CPF tem mais de 11 digitos.")

    if not cpf_validator.validate(cpf):
        raise ValidationError("CPF inválido.")

    if Account.objects.filter(cpf=cpf).exists():
        raise ValidationError('Já existe uma conta com este CPF.')


def validate_username(username):

    if not re.match(r'^[A-Za-záàãâéêíóôúç\'\- ]+$', username):
        raise ValidationError('O nome só pode conter letras, espaços, apóstrofos e hífens.')
    
    formatted_username = ' '.join(word.capitalize() for word in username.split())
    return formatted_username


def validate_email(email):

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_regex, email):
        raise ValidationError('Endereço de e-mail inválido.')

    if Account.objects.filter(email=email).exists():
        raise ValidationError('Já existe uma conta com este E-mail.')
    
    
def validate_password(password, confirm_password):
    if password != confirm_password:
        raise ValidationError('As senhas não coincidem.')
