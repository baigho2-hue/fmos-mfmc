from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

# Page d'accueil / index
def index(request):
    return render(request, 'index.html')


# Inscription
def inscription(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Compte créé avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de la création du compte.")
    else:
        form = UserCreationForm()
    return render(request, 'inscription.html', {'form': form})


# Connexion
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        username = None
        password = None
        try:
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                
                # Nettoyer immédiatement les identifiants de la mémoire
                if 'password' in form.cleaned_data:
                    del form.cleaned_data['password']
                if 'username' in form.cleaned_data:
                    del form.cleaned_data['username']
                
                # Nettoyer les variables locales
                username = None
                password = None
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Bienvenue {user.username} !")
                    return redirect('index')
                else:
                    messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            else:
                # Nettoyer les données sensibles même en cas d'erreur
                if hasattr(form, 'cleaned_data'):
                    if 'password' in form.cleaned_data:
                        del form.cleaned_data['password']
                    if 'username' in form.cleaned_data:
                        del form.cleaned_data['username']
                messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
        finally:
            # Garantir le nettoyage même en cas d'exception
            username = None
            password = None
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Déconnexion
def logout_view(request):
    logout(request)
    messages.success(request, "Vous êtes déconnecté.")
    return redirect('index')
