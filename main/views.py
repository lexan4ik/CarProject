import random

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from main.forms import AddCarForm, EditCarFrom, EditImageCarForm, ImagesFormSet
from main.models import Car, ImageCar, Brand, Color, Model
from django.db.models import OuterRef, Subquery, Exists, Prefetch


# Create your views here.



def get_main_page(request):
    cars = Car.objects.prefetch_related(
        Prefetch(
            'imagecar_set',
            queryset=ImageCar.objects.filter(is_main=True),
            to_attr='main_images')).all().select_related('brand', 'model')

    context = {
        'cars': cars,
    }
    return render(request, 'main.html', context)

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

    paginator = Paginator(cars, 1)

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

def detail(request, id):
    car = Car.objects.filter(id=id).prefetch_related(
        Prefetch(
            'imagecar_set',
            queryset=ImageCar.objects.filter(is_main=True),
            to_attr='main_images')).all().select_related('brand', 'model')


    images = ImageCar.objects.filter(car__in=car, is_main=False)

    context = {
        'car': car[0],
        'images': images,
    }

    return render(request, 'detail.html', context)

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


def edit_car_new(request, id):
    car = get_object_or_404(Car, id=id)
    images = ImageCar.objects.filter(car=car)
    print(car.color.all())
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
