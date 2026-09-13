from django import forms

from tasks.models import Task


class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["project", "title", "description", "due_date", "assigned_to"]

        widgets = {
            "project": forms.Select(
                attrs={
                    "class": (
                        "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 "
                        "text-sm text-gray-900 shadow-sm outline-none "
                        "transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
                    )
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": (
                        "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 "
                        "text-sm text-gray-900 shadow-sm outline-none "
                        "placeholder:text-gray-400 "
                        "transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
                    ),
                    "placeholder": "Enter task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": (
                        "w-full rounded-lg border border-gray-300 bg-white px-4 py-2.5 "
                        "text-sm text-gray-900 shadow-sm outline-none "
                        "placeholder:text-gray-400 resize-none "
                        "transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
                    ),
                    "rows": 5,
                    "placeholder": "Describe the task...",
                }
            ),
            "due_date": forms.SelectDateWidget(
                attrs={
                    "class": (
                        "rounded-lg border border-gray-300 bg-white px-3 py-2.5 "
                        "text-sm text-gray-900 shadow-sm outline-none "
                        "transition focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
                    )
                }
            ),
            "assigned_to": forms.CheckboxSelectMultiple(
                attrs={
                    "class": "space-y-2",
                }
            ),
        }
