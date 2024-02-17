import logging
from django.db.models.signals import post_save, m2m_changed, post_delete
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from django.contrib.auth import get_user_model


user_logger = logging.getLogger("user")


@receiver(user_logged_in)
def log_user_login(sender, user, **kwargs):
    """ log user login to user log """
    user_logger.info('%s login successful', user)

# -------------------------------------------------------------------

@receiver(user_login_failed)
def log_user_login_failed(sender, user=None, **kwargs):
    """ log user login to user log """
    if user:
        user_logger.info('%s login failed', user)
    else:
        user_logger.error('login failed; unknown user')

# -------------------------------------------------------------------

@receiver(user_logged_out)
def log_user_logout(sender, user, **kwargs):
    """ log user logout to user log """
    user_logger.info('%s log out successful', user)

# -------------------------------------------------------------------
