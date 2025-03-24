from django import forms
from django.core.exceptions import ValidationError

from main.models import Brand, ImageCar, Color, Model
from django.forms import formset_factory, BaseFormSet


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class CustomFormSet(BaseFormSet):
    def add_fields(self, form, index):
        super().add_fields(form, index)
        # Меняем label для поля DELETE
        if self.can_delete:
            form.fields["DELETE"].label = "Удалить фото"  # Ваш текст



class EditCarFrom(forms.Form):
    name = forms.CharField(max_length=100, label='Введите название')
    model = forms.ModelChoiceField(Model.objects.all(),label='Введите модель')
    price = forms.DecimalField(label='Введите цену')
    brand = forms.ModelChoiceField(Brand.objects.all(), label='Выберите бренд')
    description = forms.CharField(widget=forms.Textarea, label='Введите описание')
    color = forms.ModelMultipleChoiceField(widget=forms.CheckboxSelectMultiple, queryset=Color.objects.all())

class EditImageCarForm(forms.Form):

    image = forms.ImageField(label='Отправьте фото')
    is_main = forms.BooleanField(label='Сделать главной',required=False)
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)


class AddCarForm(EditCarFrom):
    is_main_image = forms.ImageField(label='Главное изображение')
    image = MultipleFileField(label='Отправьте вторичные фото')


ImagesFormSet = formset_factory(EditImageCarForm, formset=CustomFormSet, can_delete=True)




