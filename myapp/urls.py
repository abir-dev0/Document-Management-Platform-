from django.urls import path
from .views import (
    Documents, AddDoc, Delete_Document, Edit_Document,
    LoginView, RegisterView, AdminDashboardView, DeleteUser,
    CategorieListView, AddCategorie, DeleteCategorie, CustomLogoutView,
    AddUser, EditUser
)

urlpatterns = [
    # URLs d'authentification
    path('login/', LoginView.as_view(), name='login'),  # Page de connexion
    path('register/', RegisterView.as_view(), name='register'),  # Page d'inscription
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Déconnexion

    # URLs de gestion des documents
    path('', Documents.as_view(), name='documents'),  # Page d'accueil/liste des documents
    path('ajouter/', AddDoc.as_view(), name='ajouter_document'),  # Ajout de document
    path('modifier/<int:id>/', Edit_Document.as_view(), name='modifier_document'),  # Modification de document
    path('supprimer/', Delete_Document.as_view(), name='supprimer_document'),  # Suppression de document

    # URLs d'administration
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),  # Tableau de bord admin
    path('supprimer-utilisateur/', DeleteUser.as_view(), name='supprimer_utilisateur'),  # Suppression d'utilisateur
    path('ajouter-utilisateur/', AddUser.as_view(), name='ajouter_utilisateur'),  # Ajout d'utilisateur
    path('modifier-utilisateur/<int:id>/', EditUser.as_view(), name='modifier_utilisateur'),  # Modification d'utilisateur

    # URLs de gestion des catégories
    path('categories/', CategorieListView.as_view(), name='liste_categories'),  # Liste des catégories
    path('categories/ajouter/', AddCategorie.as_view(), name='ajouter_categorie'),  # Ajout de catégorie
    path('categories/supprimer/<int:id>/', DeleteCategorie.as_view(), name='supprimer_categorie'),  # Suppression de catégorie
]
