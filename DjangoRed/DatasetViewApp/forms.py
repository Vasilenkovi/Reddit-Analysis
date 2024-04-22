from django import forms
from django.http import HttpRequest

class Dataset_operation_form(forms.Form):
    def __init__(self, request: HttpRequest) -> None:
        super().__init__()
        self.fields["ids"] = [k for k in request.POST.keys() if k not in ("csrfmiddlewaretoken", "view", "statistic", "cluster", "name-for-added-datasets")]

    def clean(self) -> bool:
        if not self.fields["ids"]:
            return False

        common_prefix = self.fields["ids"][0][0:4] # Take first 4 characters of a first job_id

        for i in self.fields["ids"]:
            if i[0:4] != common_prefix:
                return False

        self.fields["common_job"] = common_prefix
        return True
    
    def is_valid(self) -> bool:
        return self.clean()

    def get_ids_as_list(self) -> list:
        return self.fields["ids"]