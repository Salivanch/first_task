from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
import random
import string
from django.core.exceptions import ValidationError


def CheckObject(self):
    """ Проверка на то, чтобы объект класса BlockInfo не использовался """
    if HeaderBlock.objects.filter(info__name=self.info.name).exists():
        if not HeaderBlock.objects.filter(info__name=self.info.name, pk=self.pk).exists():
            raise ValidationError("Вы не можете использовать эту информацию об блоке. Пожалуйста, создайте новую запись.")
    elif HaveQuestionsBlock.objects.filter(info__name=self.info.name).exists():
        if not HaveQuestionsBlock.objects.filter(info__name=self.info.name, pk=self.pk).exists():
            raise ValidationError("Вы не можете использовать эту информацию об блоке. Пожалуйста, создайте новую запись.")
    elif SendQuestionBlock.objects.filter(info__name=self.info.name).exists():
        if not SendQuestionBlock.objects.filter(info__name=self.info.name, pk=self.pk).exists():
            raise ValidationError("Вы не можете использовать эту информацию об блоке. Пожалуйста, создайте новую запись.")


class BlockInfo(models.Model):
    """ Информация об блоке """
    name=models.CharField("Название блока на английском",max_length=50,unique=True)
    title=models.CharField("Название блока на русском",max_length=20)
    description=models.TextField("Описание блока",max_length=100,blank=True)
    date_create=models.DateTimeField(auto_now_add=True)
    date_uppdate=models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.name} был создан {self.date_create}"

    class Meta:
        verbose_name="Информация об блоке"
        verbose_name_plural="Информация об блоках"


class KAMAZ(models.Model):
    """ Описание камаза """
    name=models.CharField("Название камаза",max_length=40)
    img=models.ImageField("Фото камаза",upload_to='kamaz')
    description=models.TextField("Описание камаза", max_length=100)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Камаз"
        verbose_name_plural="Камазы"


class HeaderBlock(models.Model):
    """ Шапка сайта """
    info=models.ForeignKey(BlockInfo,verbose_name="Информация об блоке", on_delete=models.CASCADE)
    logo=models.CharField("Лого", max_length=8)
    number=models.DecimalField("Номер телефrона(без +)", max_digits=11,decimal_places=0)
    kamaz=models.ForeignKey(KAMAZ, verbose_name="Пример камаза",on_delete=models.CASCADE)
    link_to_teleport=models.CharField("Название блока(англ) на который будет ссылаться",max_length=50)

    def __str__(self):
        return f"{self.info.name} последний раз был обновлен {self.info.date_uppdate}"

    def clean(self):
        super(HeaderBlock, self).clean()
        CheckObject(self)

    class Meta:
        verbose_name="Блок - шапка сайта"
        verbose_name_plural="Блоки - шапка сайта"


class HaveQuestionsBlock(models.Model):
    """ Блок с переходом на форму """
    info=models.ForeignKey(BlockInfo,verbose_name="Информация об блоке", on_delete=models.CASCADE)
    heading=models.CharField("Заголовок", max_length=25)
    content=models.CharField("Сообщение", max_length=300)
    kamaz=models.ForeignKey(KAMAZ, verbose_name="Пример камаза",on_delete=models.CASCADE)
    link_to_teleport=models.CharField("Название блока(англ) на который будет ссылаться",max_length=50)

    def __str__(self):
        return f"{self.info.name} последний раз был обновлен {self.info.date_uppdate}"

    def clean(self):
        super(HaveQuestionsBlock, self).clean()
        CheckObject(self)

    class Meta:
        verbose_name="Блок - 'Остались вопросы?'"
        verbose_name_plural="Блоки - 'Остались вопросы?'"


class SendQuestionBlock(models.Model):
    """ Блок с отпрвкой вопроса """
    info=models.ForeignKey(BlockInfo,verbose_name="Информация об блоке", on_delete=models.CASCADE)
    heading=models.CharField("Заголовок", max_length=25)
    email=models.EmailField("Почта")
    number=models.DecimalField("Номер телефrона(без +)", max_digits=11,decimal_places=0)
    working=models.CharField("График работы",max_length=30)
    insta=models.CharField("Ссылка на инсту",max_length=100)
    telega=models.CharField("Ссылка на телегу",max_length=100)
    kamaz=models.ForeignKey(KAMAZ, verbose_name="Пример камаза",on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.info.name} последний раз был обновлен {self.info.date_uppdate}"

    def clean(self):
        super(SendQuestionBlock, self).clean()
        CheckObject(self)

    class Meta:
        verbose_name="Блок - 'Отправить вопросы'"
        verbose_name_plural="Блоки - 'Отправить вопросы'"


class Question(models.Model):
    name=models.CharField("Имя",max_length=50)
    phone=models.CharField("Телефон",max_length=20)
    email=models.EmailField("E-mail",max_length=50)
    date=models.DateField("Дата создания",auto_now=True)

    def __str__(self):
        return f"{self.date} был задан вопрос от {self.name}"

    class Meta:
        verbose_name="Вопрос клиента"
        verbose_name_plural="Вопросы клиентов"


class RegistrationBlock(models.Model):
    """ Список возможных блоков для выбора """
    header=models.ForeignKey(HeaderBlock,verbose_name="Шапка",on_delete=models.CASCADE,blank=True,null=True)
    have_questions=models.ForeignKey(HaveQuestionsBlock,verbose_name="Остались вопросы?",on_delete=models.CASCADE,blank=True,null=True)
    send_question=models.ForeignKey(SendQuestionBlock,verbose_name="Отправить вопрос",on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return f"Набор блоков - {self.pk}"

    class Meta:
        verbose_name="Зарегистрировать блок"
        verbose_name_plural="Регистрация блоков"


class SiteContent(models.Model):
    """ Содержимое сайта """
    content=models.ManyToManyField(RegistrationBlock,verbose_name="Блоки")
    name=models.CharField("Название сборки блоков",max_length=50)
    description=models.TextField("Описание сборки",max_length=500,blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name="Контент"
        verbose_name_plural="Контент сайта"


class Profile(models.Model):
    """ Профиль пользователя """
    user=models.OneToOneField(User,verbose_name="Пользователь",on_delete=models.CASCADE)
    confirmed=models.BooleanField("Почта подтверждена",default=False)
    token=models.CharField("Токен для подтверждени почты",max_length=30)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if not self.token:
            self.token=''.join(random.choice(string.ascii_lowercase) for _ in range(20))

    @receiver(post_save, sender=User)
    def update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return f"{self.user.username}"