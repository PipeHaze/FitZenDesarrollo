from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        """
        user es el usuario al que se le va enviar el token
        timestamp retorna la fecha y hora al usuario se le envio el token
        
        la funcion retorna los parametros ingresados en la funcion convertidos a texto
        con text_type
        """
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )
    
account_activation_token = AccountActivationTokenGenerator()