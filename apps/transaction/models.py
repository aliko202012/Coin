from django.conf import settings
from django.db import models, transaction
from django.core.exceptions import ValidationError


class Transactions_coin(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='transactions_from',
        on_delete=models.CASCADE
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='transactions_to',
        on_delete=models.CASCADE
    )
    amount = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):

        if self.is_completed:
            raise ValidationError("Transaction is already completed.")


        if self.from_user == self.to_user:
            raise ValidationError("Нельзя отправить себе.")

        with transaction.atomic():

            if self.from_user.balance < self.amount:
                raise ValidationError("Insufficient funds for the transaction.")


            self.from_user.balance -= self.amount
            self.to_user.wallet += self.amount

            self.from_user.save()
            self.to_user.save()


            self.is_completed = True


            super(Transactions_coin, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'

