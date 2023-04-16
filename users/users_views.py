from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from users.models import CustomUser
from users.forms import (CustomUserForm, SignupForm, LoginForm, GroupForm,
                         PermissionsForm, UserPermissionsForm, EditUserForm)
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, Permission
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.contrib.contenttypes.models import ContentType

from django.core.paginator import Paginator

from django.core.mail import send_mail
from django.conf import settings
from users.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponseRedirect


@login_required(login_url='finlab:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password Update Successfully')
            return redirect('/password/')
        else:
            messages.warning(request, 'Form is not valid')

    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'finlab/modules/change-password.html', {'form': form, "page_title": "Change Password"})


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def users(request):
    user_list = CustomUser.objects.filter(is_superuser=False).order_by('groups__name')
    paginator = Paginator(user_list, 7)  # Show 7 Users per page.
    context = {
        "user_list": paginator.get_page(request.GET.get('page')),
        "page_title": "Users"
    }
    return render(request, "finlab/modules/users.html", context)


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser'}, raise_exception=True)
def user_details(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    context = {
        "user_obj": user_obj,
        "user_group_perms": user_obj.get_group_permissions(),
        "user_perms": user_obj.get_user_permissions(),
        "page_title": "User Details"
    }

    return render(request, "finlab/modules/user-details.html", context)


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_user(request, id):
    usr = CustomUser.objects.get(id=id)
    if usr:
        usr.delete()
        messages.success(request, "User deleted successfully")
    else:
        messages.warning(request, "User does not exist")

    return redirect('finlab:users')


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser', 'users.delete_customuser'}, raise_exception=True)
def delete_multiple_user(request):
    id_list = request.POST.getlist('id[]')
    id_list = [i for i in id_list if i != '']
    for id in id_list:
        user_obj = CustomUser.objects.get(pk=id)
        if user_obj:
            user_obj.delete()
            response = JsonResponse({"success": 'user deleted successfully'})
        else:
            response = JsonResponse({"warning": 'User does not exist'})

    response.status_code = 200
    return response


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser', 'users.add_customuser'}, raise_exception=True)
def add_user(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data.get('groups'):
                user_obj.groups.add(i)
            messages.success(request, f'le compte de {user_obj.first_name} {user_obj.last_name} a bien été créé')
            return redirect('finlab:users')
    else:
        form = CustomUserForm()
    return render(request, 'finlab/modules/add-user.html', {'form': form, "page_title": "Add User"})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user_obj = form.save(commit=False)
            user_obj.is_active = False
            user_obj.save()
            # Default Group assign Start -------------------------------------------------------
            if Group.objects.filter(name='Customer'):
                user_obj.groups.add(Group.objects.filter(name='Customer')[0])

            else:
                Customer_group, created = Group.objects.get_or_create(name="Customer")
                # content_type = ContentType.objects.get_for_model(CustomUser)
                # CustomUser_permission = Permission.objects.filter(content_type=content_type)
                # for perm in CustomUser_permission:
                # 	if perm.codename == "view_customuser":
                # 		Customer_group.permissions.add(perm)
                user_obj.groups.add(Customer_group)
            # Default Group assign End-----------------------------------------------------------
            current_site = get_current_site(request)
            subject = 'Activate Your finlab Account'
            message = render_to_string('finlab/modules/account_activation/account_activation_email.html', {
                'user': user_obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_obj.pk)),
                'token': account_activation_token.make_token(user_obj),
            })
            email = form.cleaned_data.get('email')
            name = form.cleaned_data.get('first_name')
            ReceiversList = [email]
            EmailSender = settings.EMAIL_HOST_USER
            try:
                send_mail(subject, message, EmailSender, ReceiversList, fail_silently=False)
                if user_obj.is_active == False:
                    message = f'''
                    We emailed a confirmation link to <span class="text-primary">{email}</span>.
                    Check your email for a link to activate you account.
                    '''
                    return render(request, 'finlab/modules/signup.html', {'message': message})
            except:
                messages.warning(request, 'Email Not valid')
                user_obj.delete()

        else:
            messages.warning(request, 'Form is not valid')
    else:
        if request.user.is_authenticated:
            return redirect('finlab:index')
        form = SignupForm()
    return render(request, 'finlab/modules/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('finlab:index')
    else:
        # return render(request, 'finlab/modules/account_activation/account_activation_invalid.html')
        return HttpResponse('Invalid')


@login_required(login_url='finlab:login')
@permission_required({'users.view_customuser', 'users.change_customuser'}, raise_exception=True)
def edit_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        form = EditUserForm(request.POST, request.FILES, instance=user_obj)
        if form.is_valid():
            user_obj = form.save()
            user_obj.groups.clear()
            for i in form.cleaned_data['groups']:
                user_obj.groups.add(i)
            return redirect('finlab:users')
    else:
        form = EditUserForm(instance=user_obj)
    return render(request, 'finlab/modules/add-user.html', {'form': form, "page_title": "Edit User"})


def login_user(request):
    message = ''
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.login(request)
            if user is not None and user.is_active:
                login(request, user)
                usergroup = ','.join(request.user.groups.values_list('name', flat=True))
                messages.success(request, f'Welcome To {usergroup} Dashborad')
                next_url = request.GET.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                else:
                    return redirect('finlab:index')
            else:
                messages.warning(request, "Votre compte est désactivé")

        else:
            messages.warning(request, 'SVP vérifiez votre Email et Password')
            return render(request, 'finlab/modules/login.html', context={'form': form})
    else:
        if request.user.is_authenticated:
            return redirect('finlab:index')
        form = LoginForm()
    return render(request, 'finlab/modules/login.html', context={'form': form})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return redirect('finlab:login')


@login_required(login_url='finlab:login')
@permission_required({'auth.view_group'}, raise_exception=True)
def groups_list(request):
    context = {
        "groups": Group.objects.annotate(user_count=Count('customuser', distinct=True)).annotate(
            perms_count=Count('permissions', distinct=True)),
        "colors": {'primary': 'primary', 'success': 'success', 'dark': 'dark'},
        "page_title": "Groups"
    }

    return render(request, 'finlab/modules/group-list.html', context)


@login_required(login_url='finlab:login')
@permission_required({'auth.view_group', 'auth.change_group'}, raise_exception=True)
def group_edit(request, id):
    group_obj = get_object_or_404(Group, id=id)

    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        try:
            group_obj.name = data['name'][0]
            group_obj.save()
        except:
            response = JsonResponse({"error": "Group Name already exist"})
            response.status_code = 403
            return response

        if 'permissions[]' in data:
            group_obj.permissions.clear()
            group_obj.permissions.set(data['permissions[]'])
        else:
            group_obj.permissions.clear()

        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = GroupForm(instance=group_obj)

    return render(request, 'finlab/modules/group-edit.html', {'form': form, "page_title": "Edit Group"})


@login_required(login_url='finlab:login')
@permission_required({'auth.view_group', 'auth.delete_group'}, raise_exception=True)
def group_delete(request, id):
    g = get_object_or_404(Group, id=id)
    g.delete()
    messages.success(request, 'Group Deleted Sucessfully')
    return redirect('finlab:groups')


@login_required(login_url='finlab:login')
@permission_required({'auth.view_group', 'auth.add_group'}, raise_exception=True)
def group_add(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Group Created Successfully')
            return redirect('finlab:groups')
        else:
            messages.warning(request, 'Name Already Exist')
            return render(request, 'finlab/modules/group-add.html', {'form': form, 'page_title': 'Add Group'})
    else:
        form = GroupForm()
        return render(request, 'finlab/modules/group-add.html', {'form': form, "page_title": "Add Group"})


@login_required(login_url='finlab:login')
@permission_required({'auth.view_permission'}, raise_exception=True)
def permissions(request):
    permission_list = Permission.objects.all()
    paginator = Paginator(permission_list, 5)  # Show 5 permission per page.
    context = {
        "permissions_obj": paginator.get_page(request.GET.get('page')),
        "page_title": "Permissions"
    }

    return render(request, 'finlab/modules/permissions.html', context)


@login_required(login_url='finlab:login')
@permission_required({'auth.view_permission', 'auth.change_permission'}, raise_exception=True)
def edit_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    if request.method == 'POST':
        form = PermissionsForm(request.POST, instance=perm_obj)
        if form.is_valid():
            form.save()
            return redirect('finlab:permissions')
    else:
        form = PermissionsForm(instance=perm_obj)
        return render(request, 'finlab/modules/edit-permissions.html', {'form': form, "page_title": "Edit Permissions"})


@login_required(login_url='finlab:login')
@permission_required({'auth.view_permission', 'auth.delete_permission'}, raise_exception=True)
def delete_permissions(request, id):
    perm_obj = get_object_or_404(Permission, id=id)
    perm_obj.delete()
    messages.success(request, 'Permission Delete Successfully')
    return redirect('finlab:permissions')


@login_required(login_url='finlab:login')
@permission_required({'auth.view_permission', 'auth.add_permission', 'auth.change_permission'}, raise_exception=True)
def assign_permissions_to_user(request, id):
    user_obj = get_object_or_404(CustomUser, id=id)
    if request.method == 'POST':
        queryDict = request.POST
        data = dict(queryDict)

        if 'user_permissions[]' in data:
            user_obj.user_permissions.clear()
            user_obj.user_permissions.set(data['user_permissions[]'])
        else:
            user_obj.user_permissions.clear()
        response = JsonResponse({"success": "Save Successfully"})
        response.status_code = 200
        return response

    else:
        form = UserPermissionsForm(instance=user_obj)
    return render(request, 'finlab/modules/assign_permissions_to_user.html',
                  {'form': form, "page_title": "Assign Permissions"})


def views_404(request, exception):
    return render(request, '404.html')


def views_403(request, exception):
    return render(request, '403.html')
