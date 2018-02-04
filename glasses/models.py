from django.core.exceptions import ValidationError
from django.db import models
from django.contrib import messages

from django import forms


class Glasses(models.Model):
    GLASS_TYPE = (
        ('dpt', 'з діоптріями'),
        ('frame', 'оправи'),
        ('sunglass', 'сонцезахисні'),
        ('computer', 'з комп. захистом'),
        ('drive', 'антифари'),
        ('others', 'інші')
        )
    kod = models.CharField(max_length=15, verbose_name='Код')
    name = models.CharField(max_length=20, blank=True, null=True, verbose_name="Ім'я")
    price_opt = models.FloatField(verbose_name='Оптова ціна', help_text='грн')
    price_roz = models.IntegerField(verbose_name='Роздрібна ціна', help_text='грн')
    dpt = models.FloatField(verbose_name='Діоптрії', blank=True, null=True)
    pcs = models.PositiveIntegerField(verbose_name='Кількість', help_text='шт.')
    glass_type = models.CharField(max_length=20, verbose_name='Тип', choices=GLASS_TYPE, default='dpt')
    comment = models.TextField(blank=True, null=True, verbose_name='Примітка')

    # class Meta:
    #     unique_together

    def clean(self):
        data_list = [k/100 for k in range(-2000, 2000, 25)]
        if self.dpt not in data_list and self.glass_type == 'dpt':
            if not self.dpt:
                raise ValidationError("Якщо окуляри з діоптріями то поле 'Діоптрії' не може бути пустим")
            raise ValidationError("Значення діоптрій не коректне (введіть значення від -20 до 20, наприклад '2,75', '-3.5')")

    # def increment_and_save(self, kod, dpt):
    #     try:
    #         if self.glass_type == 'dpt':
    #             glass = Glasses.objects.get(kod=kod, dpt=dpt)
    #         else:
    #             glass = Glasses.objects.get(kod=kod, glass_type=self.glass_type)
    #         glass.pcs += self.pcs
    #         glass.price_roz = self.price_roz
    #         glass.price_opt = self.price_opt
    #         glass.save()
    #     except Glasses.DoesNotExist:
    #         return self.save()

    def save(self, *args, **kwargs):
        try:
            if self.glass_type == 'dpt':
                glass = Glasses.objects.get(kod=self.kod, dpt=self.dpt)
            else:
                glass = Glasses.objects.get(kod=self.kod, glass_type=self.glass_type)
            glass.pcs += self.pcs
            glass.price_roz = self.price_roz
            glass.price_opt = self.price_opt
            super(Glasses, glass).save(*args, **kwargs)
        except Glasses.DoesNotExist:
            return super(Glasses, self).save(*args, **kwargs)

    def decrement_or_delete(self, glass):
        if self.pcs - glass.pcs == 0:
            self.delete()
        elif self.pcs-glass.pcs < 0:
            raise ValidationError('')
        else:
            self.pcs -= glass.pcs
            self.save()

    def messages_text(self, kod, dpt):
        try:
            if self.glass_type == 'dpt':
                glass = Glasses.objects.get(kod=kod, dpt=dpt)
            else:
                glass = Glasses.objects.get(kod=kod, glass_type=self.glass_type)
            messages_dict = {'message': 'Окуляри %s змінені' % glass, 'second_message': 'ціни не змінилися'}
            if self.price_opt != glass.price_opt or self.price_roz != glass.price_roz:
                messages_dict['second_message'] = 'Роздрібна ціна: стара %d грн, нова %d грн;' \
                                                  ' оптова ціна стара %d грн, нова %d грн;' % (
                                                  glass.price_roz, self.price_roz,
                                                  glass.price_opt, self.price_opt)
        except Glasses.DoesNotExist:
            messages_dict = {
                'message': 'Окуляри %s добавлені' % self,
                'second_message': 'Роздрібна ціна - %d грн,'
                ' оптова ціна - %d грн' % (
                    self.price_roz,
                    self.price_opt
                )
            }
        return messages_dict

    def __str__(self):
        return '%s %s' % (self.name, self.kod)
