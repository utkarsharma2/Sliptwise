from django.db import models

class User(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)
    def __str__(self):
        return self.name

    def getShares(self, event, contribs):
        total = [c.amount for c in contribs]
        totalSpentAmount = sum(total)
        noOfParticipants = len(total)

        share = []
        if event.type == Event.Equal:
            for contrib in contribs:
                value = totalSpentAmount/noOfParticipants
                share.append(value)

        elif event.type == Event.Percent:
            for contrib in contribs:
                value = (totalSpentAmount / 100) * contrib.percent
                share.append(value)

        elif event.type == Event.Fixed:
            for contrib in contribs:
                share.append(contrib.fixed)

        return share


    def UpdateLedger(self, event, contribs, share=None, revert=False):
        # contribs = Contributions.objects.filter(event=event)
        
        sign = 1
        if revert:
            sign = -1

        if share is None:
            share = self.getShares(event, contribs)

        positives = []
        negatives = []
        for index, contrib in enumerate(contribs):
            contrib.amount = contrib.amount - share[index]
            if contrib.amount > 0:
                positives.append(contrib)
            elif contrib.amount < 0:
                negatives.append(contrib)

        #ledger update section
        for pos in positives:
            amount = pos.amount
            for neg in negatives:
                
                if neg.amount >= 0:
                    continue

                owedAmount = (neg.amount) * -1
                ledger = Ledger.objects.get(
                    lender=pos.user,
                    borrower=neg.user,
                    group=self
                )
                if amount <= owedAmount:
                    neg.amount = (owedAmount - amount) * -1
                    # update ledger
                    ledger.amount = ledger.amount + (amount * sign)
                    ledger.save()
                    break
                else:
                    amount = amount - owedAmount
                    # update ledger
                    ledger.amount = ledger.amount + (owedAmount * sign)
                    ledger.save()
                    neg.amount = 0
                    if amount <= 0:
                        break
                

class Event(models.Model):
    Fixed = 'fixed'
    Percent = 'percent'
    Equal = 'Equal'
    Types = [
        (Fixed, Fixed),
        (Percent, Percent),
        (Equal, Equal)
    ]
    
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=50,
        choices=Types,
        default=Equal,
    )
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class Contributions(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    # To do - add validartion: 1 : 100
    percent = models.IntegerField()
    fixed = models.IntegerField()
    amount = models.IntegerField(default=0)
    share = models.IntegerField(default=0)
    def __str__(self):
        return str(self.user) + ' amount: ' + str(self.amount) + ' percent: ' + str(self.percent) + ' fixed: ' + str(self.fixed)

class Ledger(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    lender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='lender')
    borrower = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)

    def __str__(self):
        return "lender : " + str(self.lender) + " borrower : " + str(self.borrower) + " amount : " + str(self.amount)