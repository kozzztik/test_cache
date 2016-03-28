from rest_framework.views import APIView
from django.http import Http404
from .models import BankClient, ClientAction
from rest_framework.response import Response
from rest_framework import permissions
from django.contrib.auth import login, logout
from django.db import transaction


class BankClientDetailView(APIView):
    """
    Get info is bank client card is active
    """
    def get(self, request, pk):
        try:
            client = BankClient.objects.get(pk=pk)
        except BankClient.DoesNotExist:
            raise Http404
        return Response({'active': client.is_active})


class BankClientAuthView(APIView):
    """
    API for login & logout
    """
    def get(self, request):
        """
        Logout
        """
        logout(request)
        return Response({'success': True})

    @transaction.atomic
    def post(self, request):
        """
        Login
        """
        try:
            if request.data:
                card_number = request.data['card_number']
                pin = request.data['pin']
            else:
                card_number = request.query_params['card_number']
                pin = request.query_params['pin']
        except KeyError:
            return Response(status=400)
        if not card_number:
            raise Http404()
        user = BankClient.objects.select_for_update().get(pk=card_number)
        if not (user and user.is_active):
            raise Http404()
        success = user.check_password(pin)
        if not success:
            user.login_fail_count += 1
            if user.login_fail_count > BankClient.MAX_LOGIN_FAIL_COUNT:
                user.is_active = False
            user.save()
        else:
            user.login_fail_count = 0
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
        user_name = user.full_name if user and success else ''
        return Response({'success': success, 'card_locked': not user.is_active, 'user_name': user_name})


class UserActionException(Exception):
    pass


class BaseClientAction(APIView):
    action_code = None
    permission_classes = (permissions.IsAuthenticated,)

    def user_action(self, user, **kwargs):
        """
        Process custom user action
        :param BankClient user: user, doing action
        :param dict kwargs: action params
        :return: (return_result, action_value): data for return to client and to put in actions log
        """
        raise NotImplementedError()

    @transaction.atomic
    def post(self, request):
        kwargs = {key: request.data[key] for key in request.data.keys()}
        try:
            return_result, action_value = self.user_action(request.user, **kwargs)
        except UserActionException, e:
            return Response({'success': False, 'reason': str(e.message)})
        action = ClientAction(bank_client=request.user, code=self.action_code, value=action_value)
        action.save()
        return Response({'success': True, 'result': return_result, 'account': request.user.pk,
                         'date': action.time.date().isoformat(), 'time': action.time.isoformat()})


class CheckBalanceView(BaseClientAction):
    action_code = ClientAction.ACTION_CHECK_BALANCE

    def user_action(self, user, **kwargs):
        return user.balance, user.balance


class GetMoneyView(BaseClientAction):
    action_code = ClientAction.ACTION_GET_MONEY

    def user_action(self, user, value=None, **kwargs):
        user = BankClient.objects.select_for_update().get(pk=user.pk)
        value = int(value)
        if value > user.balance:
            raise UserActionException('Not enought money')
        user.balance -= value
        user.save()
        return user.balance, value
