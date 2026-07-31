from django import forms
from .models import Complaint, ComplaintComment
from departments.models import Department

class ComplaintForm(forms.ModelForm):
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label="Auto-Detect (AI)",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Complaint
        fields = ['title', 'description', 'image', 'contact_number', 'department', 'address', 'city', 'state', 'pincode', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brief title of the complaint'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Detailed description...'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Street Address / Landmark'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'pincode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Pincode'}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ComplaintStatusForm, self).__init__(*args, **kwargs)
        # Limit choices to in_progress and resolved for manual updates
        # Ideally we'd filter choices, but for now we trust the widget or validation
        self.fields['status'].choices = [
            ('in_progress', 'In Progress'),
            ('resolved', 'Resolved'),
        ]


class ComplaintCommentForm(forms.ModelForm):
    class Meta:
        model = ComplaintComment
        fields = ['comment_text', 'image']
        widgets = {
            'comment_text': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 2, 
                'placeholder': 'Write a message or update...'
            }),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
