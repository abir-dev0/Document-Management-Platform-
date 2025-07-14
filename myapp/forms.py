from django import forms
from .models import Document
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class DocumentForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification de documents.
    Inclut tous les champs nécessaires du modèle Document.
    """
    class Meta:
        model = Document
        fields = ['titre', 'description', 'fichier', 'categorie']
        widgets = {
            'titre': forms.TextInput(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Entrez le titre du document'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200',
                'placeholder': 'Décrivez le document',
                'rows': 4
            }),
            'fichier': forms.ClearableFileInput(attrs={
                'class': 'sr-only'
            }),
            'categorie': forms.Select(attrs={
                'class': 'block w-full pl-10 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200'
            }),
        }
        help_texts = {
            'titre': '',
            'description': '',
            'fichier': '',
            'categorie': ''
        }


class SearchDocForm(forms.Form):
    """
    Formulaire de recherche de documents.
    Permet de rechercher des documents par leur titre.
    """
    titre = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Rechercher un document...'
        })
    )

class CustomUserCreationForm(UserCreationForm):
    """
    Formulaire personnalisé pour la création d'utilisateur.
    Étend le formulaire de base de Django avec des champs supplémentaires.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Supprimer tous les messages d'aide
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''
        self.fields['username'].help_text = ''
        

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des labels
        self.fields['username'].label = "Nom d'utilisateur"
        self.fields['email'].label = "Adresse email"
        
        # Ajout des classes pour le style
        for field in self.fields.values():
            field.widget.attrs['class'] = 'block w-full pl-4 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors duration-200'
        