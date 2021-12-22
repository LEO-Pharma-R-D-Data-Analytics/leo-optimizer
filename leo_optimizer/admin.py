from django.contrib import admin

from django.db.models.fields.related import ForeignKey
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related import ManyToManyRel
from django.db.models.fields.related import ManyToOneRel
from django.db.models.fields.reverse_related import OneToOneRel


class QuickAdmin(admin.ModelAdmin):
    """
    Admin class, which can be used to quickly set up admin panel for a given model.
    This class solves N+1 problem for Django admin pages.
    """

    # Fields that need to be read-only
    READ_ONLY = []

    def __init__(self, *args, **kwargs):
        super(QuickAdmin, self).__init__(*args, **kwargs)

        # Data structure for 3 kinds of fields
        self.list_display = []
        self.select_related = []
        self.prefetch_related = []

        # Obtain model's fields
        self.get_model_fields()

        # Admin Page settings
        self.list_per_page = 20
        self.show_full_result_count = False
        self.list_select_related = True

        self.optimize_related_fields()

    def get_model_fields(self):
        """Method extract select_related, prefetch_related, and data fields on registered model."""
        for field in self.model._meta.get_fields():
            if isinstance(field, (ForeignKey, OneToOneRel)):
                self.select_related.append(field.name)
            elif isinstance(field, (ManyToManyField, ManyToOneRel, ManyToManyRel)):
                self.prefetch_related.append(field.name)
            else:
                not_id_field = field.name != 'id'
                if not_id_field:
                    self.list_display.append(field.name)

    def optimize_related_fields(self):
        """
        Method figures out what fields are select_related and optimized them.
        """
        self.list_select_related = self.select_related

    def get_queryset(self, request):
        """General django function. From docs: The get_queryset method is given
        the HttpRequest and is expected to return a queryset.
        """
        queryset = super(QuickAdmin, self).get_queryset(request)

        model_fields = [field.name for field in self.model._meta.get_fields()]
        if 'id' in model_fields:
            return queryset.order_by('id')

        return queryset

    def get_list_display(self, request):
        """General django function. From docs: The get_list_display method is given
        the HttpRequest and is expected to return a list or tuple of field
        names that will be displayed on the changelist view as described
        above in the ModelAdmin.list_display."""
        fields = self.select_related + self.list_display
        if fields.count('id'):
            return ['id'] + fields

        return fields

    def get_readonly_fields(self, request, obj):
        """General django function. From docs: The get_readonly_fields method is
        given the HttpRequest and the obj being edited (or None on an add form)
        and is expected to return a list or tuple of field names that will be
        displayed as read-only, as described above in the ModelAdmin.readonly_fields
        section."""
        return [field.name for field in self.model._meta.get_fields() if field.name in self.READ_ONLY]