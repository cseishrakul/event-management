from django import forms
from events.models import Event,Participant,Category

class StyledFormMixin:
    ''' Using mixin widget '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()

    default_classes = 'border-2 border-gray-300 w-full p-3 rounded-lg shadow-sm focus:outline-none focus:border-rose-500 focus:ring-rose-500'

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            # print(field_name, field.widget.attrs)
            label = field.label if field.label else field_name.replace("_", " ").title()
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.EmailInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': 'Enter your email',
                    'type': 'email'
                })
            elif isinstance(field.widget, forms.PasswordInput):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': 'Enter your password',
                    'type': 'password'
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f"{self.default_classes} resize-none",
                    'placeholder': f'Enter {field.label.lower()}',
                    'rows': 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    'class': 'space-y-2',
                    'placeholder': f'Enter {field.label.lower()}'
                })
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': self.default_classes,
                    'placeholder': f'Select {label.lower()}'
                })



class CategoryForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'}),
            'description': forms.Textarea(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg resize-none'}),
        }
        
   
        
class EventForm(StyledFormMixin, forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=Participant.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'}),
        required=False
    )

    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category','image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'category': forms.Select(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        if self.instance.pk:
            self.fields['participants'].initial = self.instance.participants.all()

    def save(self, commit=True):
        event = super().save(commit=False)
        if commit:
            event.save()
        if event.pk:
            event.participants.set(self.cleaned_data['participants'])
        return event

        
class ParticipantForm(StyledFormMixin,forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['name', 'email', 'events']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'}),
            'email': forms.EmailInput(attrs={'class': 'border-2 border-gray-300 w-full p-3 rounded-lg'}),
            'events': forms.CheckboxSelectMultiple(attrs={'class': 'space-y-2'}),
        }

    