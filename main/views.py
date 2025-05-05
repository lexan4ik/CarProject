import random
from pprint import pprint

from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.cache import cache
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from cart.forms import CartAddProductForm
from main.forms import AddCarForm, EditCarFrom, EditImageCarForm, ImagesFormSet
from main.models import Car, ImageCar, Brand, Color, Model
from django.db.models import OuterRef, Subquery, Exists, Prefetch
from django.views.decorators.cache import cache_page


# Create your views here.

#Страница всех результатов поиска
def search_page(request):
    print('get', request.GET)
    cars = Car.objects.filter(description__icontains=request.GET.get('brand'))

    paginator = Paginator(cars, 3)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    page_obj.elided_page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    context = {
        'cars': page_obj,
        'search': request.GET.get('brand'),

    }

    return render(request, 'search_page.html', context)

# Тема (меняли фон на пустой странице)
def themes(request):


    return render(request, 'themes.html')

# Смена темы посредством Django, смена светлой и темной темы
def current_theme(request):
    print('Смена темы')

    current_themes = request.session.get('theme')
    print('theme', current_themes)
    if current_themes == 'light':
        new_theme = 'dark'
    else:
        new_theme = 'light'
    request.session['theme'] = new_theme
    print(request.META['HTTP_REFERER'])
    return redirect(request.META['HTTP_REFERER'])

# Логика главной страницы, вывод машин на страницу
#@cache_page(60 * 10, key_prefix='main_page')
def get_main_page(request):
    main_page_cache = cache.get('main_page')
    if main_page_cache is None:
        cars = Car.objects.prefetch_related(
            Prefetch(
                'imagecar_set',
                queryset=ImageCar.objects.filter(is_main=True),
                to_attr='main_images')).all().select_related('brand', 'model').order_by('-id')
        cache.set('main_page', cars)
        print('кэш', cache.get('main_page'))
    print(request.session.get('theme'))
    context = {
        'cars': main_page_cache,
    }
    return render(request, 'main.html', context)

def admin_check(user):
    return user.is_authenticated and user.is_superuser

# Логика страницы каталога, вывод машин в каталог и фильтрация их
@user_passes_test(admin_check)
def catalog(request):
    cars = Car.objects.prefetch_related(
        Prefetch(
            'imagecar_set',
            queryset=ImageCar.objects.filter(is_main=True),
            to_attr='main_images')).all().select_related('brand', 'model')


    brands = Brand.objects.all()
    colors = Color.objects.all()
    # Фильтрация
    filters = {
        'price_min': request.GET.get('price_min'),
        'price_max': request.GET.get('price_max'),
        'model': request.GET.get('model'),
        'brand': request.GET.get('brand'),
        'colors': request.GET.getlist('color'),
    }

    print(filters.get('brand'))

    if filters['price_min']:
        cars = cars.filter(price__gte=filters['price_min'])
    if filters['price_max']:
        cars = cars.filter(price__lte=filters['price_max'])
    if filters['brand']:
        cars = cars.filter(brand_id=filters['brand'])
    if filters['model'] and filters['brand']:
        cars = cars.filter(model_id=filters['model'])
    if not filters['colors']:
        pass
    else:
        cars = cars.filter(color__in=filters['colors']).distinct()

    paginator = Paginator(cars, 6)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    page_obj.elided_page_range = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)

    context = {
        'cars': page_obj,
        'brands': brands,
        'colors': colors,
        'selected': filters,
    }

    if filters['brand']:
        models = Model.objects.filter(brand=filters.get('brand'))
        context['models'] = models


    return render(request, 'catalog.html', context)

# Логика страницы Брендов, вывод брендов на страницу
def brands(request):
    brands = Brand.objects.all()
    print(request)
    context = {
        'brands': brands
    }

    return render(request, 'brands.html', context)

# Логика страницы с добавлением машин, обработка форм и добавление
def add_car(request):
    form = AddCarForm()
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES)
        if form.is_valid():
            new_car = Car(model=form.cleaned_data['model'], price=form.cleaned_data['price'],brand=form.cleaned_data['brand'], description=form.cleaned_data['description'])
            new_car.save()
            img_obj = [ImageCar(image=form.cleaned_data['is_main_image'], is_main=True, car=new_car)]
            for img in form.cleaned_data['image']:
                img_obj.append(ImageCar(image=img, car=new_car))

            ImageCar.objects.bulk_create(img_obj)

            return redirect('add_car')

    context = {
        'form': form,
    }
    return render(request, 'add_car.html', context)

# Логика для страниц машин по кнопке подробнее
def detail(request, id):
    car = Car.objects.filter(id=id).prefetch_related(
        Prefetch(
            'imagecar_set',
            queryset=ImageCar.objects.filter(is_main=True),
            to_attr='main_images')).all().select_related('brand', 'model')

    images = ImageCar.objects.filter(car__in=car, is_main=False)

    cart_product_form = CartAddProductForm()

    context = {
        'car': car[0],
        'images': images,
        'cart_product_form': cart_product_form,
    }

    return render(request, 'detail.html', context)

# Логика изменения данных машин (стар.)
def edit_car(request, id):
    car = get_object_or_404(Car, id=id)
    images = ImageCar.objects.filter(car=car, is_main=False)
    main_image = car.main_image
    initial_dict = {
        'name': car.name,
        'model': car.model,
        'price': car.price,
        'brand': car.brand,
        'description': car.description,
    }
    print(len(images))
    form = AddCarForm(initial=initial_dict)
    check_is_main_image(car, form, images)
    context = {
        'form': form,
        'images': images,
        'image': main_image
    }
    print(request.GET)
    if request.method == 'POST':
        form = AddCarForm(request.POST, request.FILES)
        check_is_main_image(car, form, images)
        if request.POST.get('delete_images'):
            ImageCar.objects.filter(id=request.POST.get('delete_images')).delete()
        if form.is_valid():
            print('Валид')
            Car.objects.filter(id=id).update(model=form.cleaned_data['model'], price=form.cleaned_data['price'],brand=form.cleaned_data['brand'], description=form.cleaned_data['description'])
            if form.cleaned_data.get('is_main_image'):
                if not ImageCar.objects.filter(is_main=True, car=car):
                    ImageCar.objects.create(image=form.cleaned_data['is_main_image'], is_main=True, car=car)
            if form.cleaned_data.get('image'):
                for img in form.cleaned_data['image']:
                    ImageCar.objects.update_or_create(image=img, car=car)

            return redirect('edit_car', car.id)


    return render(request, 'edit_car.html', context)

#Функция для изменения машин (стар.)
def check_is_main_image(car, form, images):
    if car.main_image:
        form.fields['is_main_image'].required = False
        form.fields['image'].required = False
    elif not car.main_image:
        form.fields['is_main_image'].required = True
        form.fields['image'].required = False
    else:
        form.fields['is_main_image'].required = True
        form.fields['image'].required = False

# Логика изменения данных машин (нов.)
def edit_car_new(request, id):
    car = get_object_or_404(Car, id=id)
    images = ImageCar.objects.filter(car=car)
    initial_dict = {
        'name': car.name,
        'model': car.model,
        'price': car.price,
        'brand': car.brand,
        'description': car.description,
        'color': car.color.all(),


    }
    initial_image = [{'image': i.image, 'is_main': i.is_main, 'id': i.id} for i in images]
    form = EditCarFrom(initial=initial_dict)
    formset = ImagesFormSet(initial= initial_image)
    if request.method == 'POST' :
        form = EditCarFrom(request.POST, request.FILES, initial=initial_dict)
        formset = ImagesFormSet(request.POST, request.FILES, initial=initial_image)
        if form.is_valid():
            print(form.cleaned_data)
            if form.has_changed():
                for key, value in form.cleaned_data.items():
                    if value is not None and value != getattr(car, key):
                        if key == 'color':
                            car.color.set(value)
                        else:
                            setattr(car, key, value)
                car.save()
            if formset.is_valid():
                count = 0
                for form_img in formset:
                    if form_img.cleaned_data.get('is_main') is True:
                        count += 1
                        print('Кол-во галочек', count)
                        if count >= 2:
                            formset.non_form_errors = 'Невозможно выбрать 2 фото как главные!'
                            return render(request, 'edit_car_new.html', {'form': form, 'formset': formset})

                for form_img in formset:
                    if form_img.has_changed():
                        if form_img.cleaned_data.get('id') in [i.id for i in images] and not formset.deleted_forms:
                            instance = images.get(id=form_img.cleaned_data.get('id'))
                            instance.image = form_img.cleaned_data.get('image')
                            instance.is_main = form_img.cleaned_data.get('is_main')
                            instance.save()
                        elif not formset.deleted_forms:
                            new_image = ImageCar(image=form_img.cleaned_data.get('image') , is_main=form_img.cleaned_data.get('is_main') , car=car)
                            new_image.save()

                if len(formset) - 1 > len(formset.deleted_forms):
                    ImageCar.objects.filter(id__in=[form_delete.cleaned_data.get('id') for form_delete in formset.deleted_forms]).delete()

                images = ImageCar.objects.filter(car=car)

                for img in images:
                    if len(images) == 1:
                        img.is_main = True
                        img.save()
                        break
                    elif len(image_is_main(car, False)) == len(images):
                        img = images[random.randrange(0, len(images))]
                        img.is_main = True
                        img.save()
                        break
                    elif len(image_is_main(car, True)) >= 2:
                        img = images[random.randrange(0, len(image_is_main(car, True)))]
                        img.is_main = False
                        img.save()
                        break

            return redirect('edit_car_new', car.id)

    context = {
        'form': form,
        'formset': formset,
    }

    return render(request, 'edit_car_new.html', context)


def image_is_main(car, is_main: bool):
    image_is_main = ImageCar.objects.filter(car=car, is_main=is_main)
    return image_is_main


def add_car_api(request):
    form = AddCarForm()

    context = {
        'form': form,
    }

    return render(request, 'add_car_api.html', context)