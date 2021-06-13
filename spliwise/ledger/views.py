# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets

from . import models, serializer
from rest_framework.response import Response
from rest_framework import status
from . import constants, util

class UserViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializer.UserSerializer

class GroupViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = models.Group.objects.all()
        resp = serializer.GroupSerializer(queryset, many=True)
        return Response(resp.data)

    def create(self, request):
        reqParams = constants.Group[constants.Create]
        missingParams = util.checkRequired(reqParams, request.data)
        if len(missingParams) > 0:
            return Response({
                'error' : 'missing params',
                'params' : missingParams}, 
            status.HTTP_400_BAD_REQUEST)


        group = models.Group(name=request.data['name'])
        group.save()

        ledgerEntry = []
        users = models.User.objects.all()
        for lender in users:
            for borrower in users:
                if lender != borrower:
                    ledgerEntry.append(models.Ledger(
                        group=group,
                        lender=lender,
                        borrower=borrower,
                        amount=0
                    ))
        models.Ledger.objects.bulk_create(ledgerEntry)
        return Response(status.HTTP_200_OK)

class EventViewSet(viewsets.ViewSet):
    
    def list(self, request):
        queryset = models.Event.objects.all()
        resp = serializer.EventSerializer(queryset, many=True)
        return Response(resp.data)

    def create(self, request):
        group = models.Group.objects.get(id=request.data['group'])
        event = models.Event(
            name=request.data['name'],
            type=request.data['type'],
            group=group
        )
        event.save()

        contribs = []
        for user in request.data['user']:
            userObj = models.User.objects.get(id=user.get['id'])

            contribs.append(
                models.Contributions(
                    event=event,
                    user=userObj,
                    amount=user['amount'],
                    percent= user[models.Event.Percent] if models.Event.Percent in user else 0,
                    fixed=user[models.Event.Fixed] if models.Event.Fixed in user else 0
                )
            )

        # get Shares
        shares = group.getShares(event, contribs)
        for index, contrib in enumerate(contribs):
            contrib.share = shares[index]

        models.Contributions.objects.bulk_create(contribs)
        group.UpdateLedger(event, contribs, shares)

        return Response(status.HTTP_200_OK)


    def destroy(self, request, pk=None):
        
        event = models.Event.objects.get(id=pk)
        contribs = models.Contributions.objects.filter(event=event)
        event.group.UpdateLedger(event, contribs, revert=True)
        event.delete()
        return Response(status.HTTP_200_OK)

class TransactionsViewSet(viewsets.ViewSet):
    
    def list(self, request):
        user = models.User.objects.get(id=request.query_params['user'])
        data = models.Contributions.objects.filter(user=user)
        resp = serializer.ContributionsSerializer(data, many=True)
        return Response(resp.data)

class SettleViewSet(viewsets.ViewSet):
    
    def list(self, request):
        
        ledger = models.Ledger.objects.filter(
                    lender=request.query_params['lender'],
                    borrower=request.query_params['borrower'],
                    group=request.query_params['group']
                ).first()
        ledger.amount = ledger.amount - int(request.query_params['amount'])
        ledger.save()
        return Response(status.HTTP_200_OK)
    
class SummaryViewSet(viewsets.ViewSet):
    
    def list(self, request):
        data = models.Ledger.objects.filter(group=request.query_params['group'])
        resp = serializer.LedgerSerializer(data, many=True)
        return Response(resp.data)

class AddUserViewSet(viewsets.ViewSet):
    
    def list(self, request):
        import ipdb; ipdb.set_trace()
        group = models.Group.objects.filter(id=request.query_params['group']).first()
        user = models.User.objects.filter(id=request.query_params['user']).first()
        
        group.users.add(user)

        return Response(status.HTTP_200_OK)