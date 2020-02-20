from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST

from mypage.forms import ProfileForm, PetForm, DiaryForm
from mypage.models import Profile, Pet, Diary
from django.contrib.auth.models import User


@login_required
@transaction.atomic
def update_profile(request):
    diary1 = Diary.objects.filter(author=request.user.profile).order_by('-created_at')[0]
    diary2 = Diary.objects.filter(author=request.user.profile).order_by('-created_at')[1]
    diary3 = Diary.objects.filter(author=request.user.profile).order_by('-created_at')[2]
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('mypage:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        ctx = {
            'diary1': diary1,
            'diary2': diary2,
            'diary3': diary3,
            'form': profile_form,
        }
    return render(request, 'mypage/profile.html', ctx)


def name_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_name = request.POST['name_update']
        user.profile.name = new_name
        user.save()
        return redirect('mypage:profile')


def email_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_email = request.POST['email_update']
        user.profile.email = new_email
        user.save()
        return redirect('mypage:profile')


def tel_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_tel = request.POST['tel_update']
        user.profile.tel = new_tel
        user.save()
        return redirect('mypage:profile')


# pet#pet
# pet
# pet

def pet_brief(request):
    pet1 = Pet.objects.filter(owner=request.user.profile).order_by('-created_at')[0]
    pet2 = Pet.objects.filter(owner=request.user.profile).order_by('-created_at')[1]
    pet3 = Pet.objects.filter(owner=request.user.profile).order_by('-created_at')[2]
    ctx = {
        'pet1': pet1,
        'pet2': pet2,
        'pet3': pet3,
    }
    return render(request, 'mypage/pet_brief.html',ctx)

def pet_list(request):
    pets = Pet.objects.filter(owner=request.user.profile).order_by('-created_at')[0:3]
    ctx = {
        'pets': pets
    }
    return render(request, 'mypage/pet_list.html', ctx)


@login_required
@transaction.atomic
def create_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            pet.owner = request.user.profile
            pet.save()
            messages.success(request, 'Your pet info was successfully updated!')
            return redirect(reverse('mypage:pet_detail', kwargs={'pk': pet.pk}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PetForm()
    return render(request, 'mypage/create_pet.html', {'form': form})


def pet_detail(request, pk):
    pet = Pet.objects.get(pk=pk)
    ctx = {
        'pet': pet,
        'pk': pk,
    }
    return render(request, 'mypage/pet_detail.html', ctx)


def pet_update(request, pk):
    pet = Pet.objects.get(pk=pk)
    form = PetForm(request.POST, request.FILES, instance=pet)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your pet was successfully updated!')
            return redirect(reverse('mypage:pet_detail', kwargs={'pk': pk}))
    else:
        form = PetForm(instance=pet)
    return render(request, 'mypage/pet_edit.html', {
        'pk': pk,
        'form': form,
    })


def pet_delete(request, pk):
    pet = Pet.objects.get(pk=pk)
    if request.user.profile == pet.owner:
        pet.delete()
        messages.success(request, '성공적으로 삭제되었습니다.')
    return redirect(reverse('mypage:pet'))


# diary
# diary
# diary


@login_required
def diary_list(request):
    return render(request, 'mypage/diary_list.html')


@login_required
@transaction.atomic
def create_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save()
            diary.author = request.user.profile
            diary.save()
            messages.success(request, 'Your pet was successfully created!')
            return redirect(reverse('mypage:detail_diary', kwargs={'pk': diary.pk}))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = DiaryForm()
    return render(request, 'mypage/diary_create.html', {
        'form': form,
    })


def detail_diary(request, pk):
    diary = Diary.objects.get(pk=pk)
    data = {
        'diary': diary,
        'pk': pk,
    }
    return render(request, 'mypage/diary_detail.html', data)


def update_diary(request, pk):
    diary = Diary.objects.get(pk=pk)
    form = DiaryForm(request.POST, request.FILES, instance=diary)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Your pet was successfully created!')
            return redirect(reverse('mypage:detail_diary', kwargs={'pk': pk}))
    else:
        form = DiaryForm(instance=diary)
    return render(request, 'mypage/diary_edit.html', {
        'pk': pk,
        'form': form,
    })


def delete_diary(request, pk):
    diary = Diary.objects.get(pk=pk)
    if request.user.profile == diary.author:
        diary.delete()
        messages.success(request, '성공적으로 삭제되었습니다.')
    return redirect(reverse('mypage:diary'))


# favorites
# favorites
# favorites


def favorites(request):
    return render(request, 'mypage/favorites.html')
