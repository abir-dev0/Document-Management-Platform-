from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required




from .models import Document, Categorie
from .forms import DocumentForm, SearchDocForm, CustomUserCreationForm, UserEditForm


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm() #Un objet form est créé à partir du formulaire personnalisé CustomUserCreationForm
        return render(request, 'register.html', {'form': form})#Cette ligne affiche la page register.html et y passe le formulaire (form) pour qu'il soit rendu dans le template HTML

    def post(self, request):
        form = CustomUserCreationForm(request.POST)#Le formulaire est rempli avec les données envoyées par l'utilisateur
        if form.is_valid():#Vérifie si les données du formulaire sont valides
            form.save()#Si les données sont valides, le formulaire est sauvegardé, ce qui crée un nouvel utilisateur dans la base de données
            messages.success(request, "Compte créé avec succès. Connectez-vous.")
            return redirect('login')
        return render(request, 'register.html', {'form': form})


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:#Si l'utilisateur est déjà connecté (utilisateur classique), il est redirigé vers la page principale des documents
            if request.user.is_superuser:#Si l'utilisateur est un administrateur (superuser), il est redirigé vers le tableau de bord admin
                return redirect('admin_dashboard')
            return redirect('documents')
        return render(request, 'login.html')#Si l'utilisateur n'est pas connecté, on lui affiche le formulaire de connexion (login.html)

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")#Récupération du nom d'utilisateur et du mot de passe à partir des données envoyées par le formulaire
        user = authenticate(request, username=username, password=password)#Django essaie d'authentifier l'utilisateur avec les informations fournies
        if user is not None:
            login(request, user)#L'utilisateur est connecté (une session est créée)
            if user.is_superuser:
                return redirect('admin_dashboard')#Si c'est un administrateur, on le redirige vers le tableau de bord admin
            return redirect('documents')#Sinon, vers la page documents (utilisateur standard)
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")#Si l'authentification échoue, on ajoute un message d'erreur à afficher dans le template
            return redirect('login')


class Documents(View):
    def get(self, request):
        # Récupération du terme de recherche
        search_query = request.GET.get('search', '')#On récupère le texte saisi dans le champ de recherche (dans l'URL sous forme ?search=mot) avec request.GET.get. Si aucun mot n'est saisi, search_query sera une chaîne vide ('')
        
        # Filtrage des documents si un terme de recherche est présent
        if search_query:
            docs = Document.objects.filter(titre__icontains=search_query)#Si un terme est présent, on filtre les documents dont le titre contient le mot, sans tenir compte de la casse (icontains = insensitive contains)
        else:
            docs = Document.objects.all()#Si aucun terme n'est fourni, on affiche tous les documents
            
        return render(request, "index.html", {
            "docs": docs,
            "search_query": search_query,
            'messages': messages.get_messages(request)
        })

    def post(self, request):#La méthode post() permet de faire une recherche via un formulaire (SearchDocForm)
        form = SearchDocForm(request.POST)
        if form.is_valid():
            titre = form.cleaned_data.get('titre')
            docs = Document.objects.filter(titre__icontains=titre)
        else:
            docs = Document.objects.all()
        return render(request, 'index.html', {'form': form, 'docs': docs})


@method_decorator(login_required, name='dispatch')
class AddDoc(View):
    def get(self, request):
        form = DocumentForm()#Création d'un formulaire vide basé sur DocumentForm
        return render(request, "ajouter_document.html", {'form': form})#Affiche la page ajouter_document.html, avec le formulaire à remplir 

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)#Remplit le formulaire avec les données soumises, y compris les fichiers uploadés
        if form.is_valid():
            doc = form.save(commit=False)#On crée l'objet Document sans encore l'enregistrer dans la base
            doc.auteur = request.user#On attribue à ce document l'utilisateur actuellement connecté comme auteur
            doc.save()
            messages.success(request, "Document ajouté avec succès")
            return redirect('documents')
        return render(request, 'ajouter_document.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class Edit_Document(View):
    def get(self, request, id):
        doc = get_object_or_404(Document, id=id)#On essaie de récupérer le document avec l'id donné.Si aucun document n'est trouvé, Django retourne automatiquement une erreur 404
        form = DocumentForm(instance=doc)
        return render(request, 'modifier_document.html', {'form': form})

    def post(self, request, id):
        doc = get_object_or_404(Document, id=id)
        form = DocumentForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            messages.success(request, "Document modifié avec succès")
            return redirect('documents')
        return render(request, 'modifier_document.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class Delete_Document(View):
    def post(self, request):
        id = request.POST.get('id')#Récupère l'identifiant du document à supprimer depuis le bouton de suppression
        doc = get_object_or_404(Document, id=id)#Recherche dans la base le document avec cet id
        doc.delete()
        messages.success(request, "Document supprimé avec succès")
        return redirect('documents')
    
class CustomLogoutView(LogoutView):
    def dispatch(self, request, *args, **kwargs):#dispatch() est une méthode de Django qui est appelée avant get() ou post(), peu importe la méthode HTTP
        messages.success(request, "Déconnexion réussie.")#Avant la déconnexion, on ajoute un message de succès dans le système de messages de Django
        return super().dispatch(request, *args, **kwargs)#Appelle la méthode dispatch() de la classe LogoutView pour continuer le traitement normal de la déconnexion
    
class AdminDashboardView(View):
    @method_decorator(staff_member_required)
    def get(self, request):
        utilisateurs = User.objects.all()
        
        # Récupération du terme de recherche
        search_query = request.GET.get('search', '')
        
        # Filtrage des documents si un terme de recherche est présent
        if search_query:
            documents = Document.objects.filter(titre__icontains=search_query)
        else:
            documents = Document.objects.all()
            
        return render(request, 'admin_dashboard.html', {
            'utilisateurs': utilisateurs,
            'documents': documents,
            'search_query': search_query
        })

@method_decorator(staff_member_required, name='dispatch')
class DeleteUser(View):
    """
    Vue pour supprimer un utilisateur.
    Accessible uniquement aux administrateurs.
    Les documents de l'utilisateur sont réassignés à l'admin.
    """
    def post(self, request):
        user_id = request.POST.get('user_id')#Récupère l'id de l'utilisateur à supprimer, transmis via le formulaire HTML 
        user = get_object_or_404(User, id=user_id)#Cherche l'utilisateur dans la base de données. Si l'utilisateur n'existe pas, affiche une erreur 404
        if not user.is_superuser:  # Empêcher la suppression des administrateurs
            # Supprimer les documents de l'utilisateur ou les réassigner à un admin
            Document.objects.filter(auteur=user).update(auteur=request.user)#Tous les documents créés par l'utilisateur supprimé sont réassignés à l'admin
            user.delete()#Supprime effectivement l'utilisateur de la base de données
            messages.success(request, "Utilisateur supprimé avec succès.")#Affiche un message de succès qui sera visible après la redirection
        else:
            messages.error(request, "Impossible de supprimer un administrateur.")#Si c'est un superutilisateur, on bloque la suppression et on montre un message d'erreur
        return redirect('admin_dashboard')#Redirige vers la page d'administration après l'opération

@method_decorator(staff_member_required, name='dispatch')
class CategorieListView(View):
    """
    Vue pour afficher la liste des catégories
    Accessible uniquement aux administrateurs
    """
    def get(self, request):
        categories = Categorie.objects.all()
        return render(request, 'categories/liste_categories.html', {
            'categories': categories
        })

@method_decorator(staff_member_required, name='dispatch')
class AddCategorie(View):
    """
    Vue pour ajouter une nouvelle catégorie.
    Accessible uniquement aux administrateurs.
    """
    def get(self, request):
        return render(request, 'categories/ajouter_categorie.html')

    def post(self, request):
        nom = request.POST.get('nom')
        if nom:#Vérifie que le champ n'est pas vide
            if not Categorie.objects.filter(nom=nom).exists():#On vérifie que cette catégorie n'existe pas déjà dans la base de données
                Categorie.objects.create(nom=nom)
                messages.success(request, "Catégorie ajoutée avec succès")
            else:
                messages.error(request, "Cette catégorie existe déjà")
        else:
            messages.error(request, "Le nom de la catégorie est requis")
        return redirect('liste_categories')

@method_decorator(staff_member_required, name='dispatch')
class DeleteCategorie(View):
    """
    Vue pour supprimer une catégorie.
    Accessible uniquement aux administrateurs.
    Vérifie si la catégorie contient des documents avant la suppression.
    """
    def post(self, request, id):
        categorie = get_object_or_404(Categorie, id=id)
        if Document.objects.filter(categorie=categorie).exists():#Vérifie si au moins un document est lié à cette catégorie.Cela empêche de supprimer une catégorie encore utilisée
            messages.error(request, "Impossible de supprimer cette catégorie car elle contient des documents")
        else:
            categorie.delete()
            messages.success(request, "Catégorie supprimée avec succès")
        return redirect('liste_categories')

@method_decorator(staff_member_required,name='dispatch')
class AddUser(View):
    def get(self,request):
        form=CustomUserCreationForm()
        return render(request, "ajouter_utilisateur.html", {'form': form}) 
    def post(self, request):
        form = CustomUserCreationForm(request.POST)#Le formulaire est rempli avec les données envoyées par l'utilisateur
        if form.is_valid():#Vérifie si les données du formulaire sont valides
            form.save()#Si les données sont valides, le formulaire est sauvegardé, ce qui crée un nouvel utilisateur dans la base de données
            messages.success(request, "Compte créé avec succès.")
        return render(request, 'ajouter_utilisateur.html', {'form': form})

@method_decorator(staff_member_required,name='dispatch')
class EditUser(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserEditForm(instance=user)
        return render(request, 'modifier_utilisateur.html', {
            'form': form,
            'user_to_edit': user
        })

    def post(self, request, id):
        user = get_object_or_404(User, id=id)
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Informations de l'utilisateur modifiées avec succès.")
            return redirect('admin_dashboard')
        return render(request, 'modifier_utilisateur.html', {
            'form': form,
            'user_to_edit': user
        })
    