from django import forms

from .models import MerciInquiry

INPUT_CLASS = "m-input"

# Shown inside the collapsed "Add more details" section of the form.
OPTIONAL_FIELDS = ("organization", "email", "language", "timeline", "budget")


class MerciInquiryForm(forms.ModelForm):
    # Honeypot: hidden from people with CSS, bots tend to fill it in.
    website = forms.CharField(required=False)

    class Meta:
        model = MerciInquiry
        fields = [
            "full_name", "phone", "service", "project_description",
            "organization", "email", "language", "timeline", "budget",
        ]
        labels = {
            "full_name": "Your name",
            "phone": "Phone or WhatsApp",
            "service": "What do you need?",
            "project_description": "Tell us about your project",
            "language": "Production language",
            "timeline": "When do you need it?",
            "budget": "Budget (optional)",
        }
        widgets = {
            "project_description": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "A few lines is enough: what it is for, who will watch it, and any dates that matter.",
            }),
            "full_name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Full name"}),
            "organization": forms.TextInput(attrs={"autocomplete": "organization", "placeholder": "Company, NGO or brand"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel", "inputmode": "tel", "placeholder": "+251 9XX XXX XXX"}),
            "budget": forms.TextInput(attrs={"placeholder": "e.g. ETB 150,000 or a range"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "website":
                continue
            field.widget.attrs["class"] = INPUT_CLASS
            if field.required:
                field.widget.attrs["required"] = "required"
        # Replace Django's "---------" with friendlier first options.
        empty_labels = {"service": "Choose a service", "language": "Not sure yet", "timeline": "Not sure yet"}
        for name, label in empty_labels.items():
            self.fields[name].choices = [("", label)] + [c for c in self.fields[name].choices if c[0] != ""]

    @property
    def optional_has_errors(self):
        return any(name in self.errors for name in OPTIONAL_FIELDS)
