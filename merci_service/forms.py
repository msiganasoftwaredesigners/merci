from django import forms

from .models import MerciInquiry

INPUT_CLASS = "merci-input"


class MerciInquiryForm(forms.ModelForm):
    # Honeypot: hidden from people with CSS, bots tend to fill it in.
    website = forms.CharField(required=False)

    class Meta:
        model = MerciInquiry
        fields = [
            "full_name", "organization", "email", "phone", "service",
            "language", "timeline", "budget", "project_description",
        ]
        widgets = {
            "project_description": forms.Textarea(attrs={"rows": 5}),
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "organization": forms.TextInput(attrs={"autocomplete": "organization"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
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
        for name in ("service", "language", "timeline"):
            self.fields[name].choices = [("", "Select an option")] + list(self.fields[name].choices)[1:]
            