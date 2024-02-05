"""
Model Reader Service Class for Django Based Applications
"""
# To Access the Django Apps
from django.apps import apps
# To Access Django Settings
from django.conf import settings
# Import of Interface for Model Reader Service
from django_model_reader_x.interfaces.i_model_reader_service import \
    IModelReaderService


class DjangoModelReaderService(IModelReaderService):
    """
    Services for reading model details of Django Application
    """
    def __init__(self) -> None:
        """
        Initializing the Service with setting up all the required variables
        """        
        # self.INCLUDED_APPS = ["django.contrib.auth",] + settings.SRM_APPS
        self.INCLUDED_APPS = []
        self.lst_app_label_model_name=[]

        # Reading App Config
        self.apps_config = apps.get_app_configs()

        # Setting up the list of models with app names        
        self.set_all_lst_app_label_model_names()

    def get_model_by_name(self,app_name:str,model_name:str):
        """
        Get the Model Object by Name
        """
        for app_config in self.apps_config:
            if self.get_app_label_from_app_config(app_config=app_config)==app_name:
                models= app_config.get_models()
                for model in models:
                    if self.get_model_name(model)==model_name:
                        return model
        return None

    def get_app_full_name_from_app_config(self,app_config) -> str:
        """
        Get App full name from app config
        """
        return app_config.name
    
    def get_app_name_from_app_config(self,app_config) -> str:
        """
        Get App name from app config
        """
        return app_config.name

    def get_app_label_from_app_config(self,app_config) -> str:
        """
        Get App label from app config
        """
        return app_config.label

    def get_app_label_from_model(self,model) -> str:
        """
        Get app name of the model
        """
        return model._meta.app_label

    def get_app_full_name(self,model) -> str:
        """
        Get app full name of the model
        """
        app_full_name = model.__module__
        if ".models." in app_full_name:
            app_full_name = app_full_name.split(".models.")[0]
        
        return app_full_name

    def get_model_name(self,model) -> str:
        """
        Get model name
        """
        return model.__name__

    def get_model_doc_string(self,model) -> str:
        """
        Get model doc string
        """
        return model.__doc__

    def get_model_db_table_name(self,model) -> str:
        """
        get db table name of the model
        """
        return model._meta.db_table

    def set_all_lst_app_label_model_names(self):
        """
        Setting up the lst_app_label_model_name variable with list of app_label + model_name
        """
        for app_config in self.apps_config:
            app_label=self.get_app_label_from_app_config(app_config=app_config)
            models = app_config.get_models()
            for model in models:
                if not self.is_model_to_exclude(model):
                    model_name = self.get_model_name(model=model)
                    self.lst_app_label_model_name.append(app_label+"."+model_name)

    def get_model_column_names(self,model) -> list:
        """
        Get the list of fields of a Django model
        """
        return model._meta.get_fields()

    def is_model_to_exclude(self,model) -> bool:
        """
        Check if a model is part of exclusion model list
        """
        if ("user" not in str.lower(model.__name__)):
            # Check if the model's app is part of the Django core or a third-party package
            return model._meta.app_config.name.startswith('django.') or model._meta.app_config.name.startswith('third_party_package.')
        return False
    
    def is_app_to_include(self,app_config) -> bool:
        """
        Check if app is part of inclusion list
        """
        if len(self.INCLUDED_APPS)>0:
            if ((self.get_app_full_name_from_app_config(app_config=app_config) in self.INCLUDED_APPS) or
                (self.get_app_name_from_app_config(app_config=app_config) in self.INCLUDED_APPS) or
                (self.get_app_label_from_app_config(app_config=app_config) in self.INCLUDED_APPS)):
                return True
            return False
        else:
            return True

    def get_primary_key_fields(self,model) -> list:
        """
        Get list of primary key fields of a Django model.
        """
        lst_primary_fields = []
        for field in model._meta.get_fields():
            if hasattr(field,"primary_key"):
                if field.primary_key:
                    lst_primary_fields.append(field.name)

        return lst_primary_fields

    def get_field_name(self,field) -> str:
        """
        Get name of the field
        """
        field_name = field.name
        return field_name

    def get_db_column(self,field) -> str:
        """
        get DB name of the field if available else use field name
        """
        db_column_name = self.get_field_name(field)
        if hasattr(field,"db_column"):
            if field.db_column:
                db_column_name = field.db_column
        return db_column_name

    def get_datatype(self,field) -> str:
        """
        Get field Datatype
        """
        datatype = "NA"
        if field and hasattr(field, 'get_internal_type'):
            datatype = field.get_internal_type()
        return datatype

    def get_related_field_details(self,field) -> dict:
        """
        Get primary key fields of a Django model.
        """
        field_details = {}
        if field.is_relation and hasattr(field, 'remote_field') and field.remote_field is not None:
            # For ForeignKey fields

            related_app_full_name = self.get_app_full_name(field.related_model)
            related_app_label = self.get_app_label_from_model(field.related_model)
            related_model_name = self.get_model_name(field.related_model)
            related_db_table_name = self.get_model_db_table_name(field.related_model)

            related_name = getattr(field, 'related_name', None)

            if related_name:
                related_field_name=related_name
                related_db_column_name=related_name
            else:
                related_field_name = field.remote_field.name
                related_db_column_name = self.get_db_column(field.remote_field)

            field_details.update({"related_app_full_name": related_app_full_name})
            field_details.update({"related_app_label": related_app_label})
            field_details.update({"related_model_name":related_model_name})
            field_details.update({"related_db_table_name":related_db_table_name})
            field_details.update({"related_field_name":related_field_name})
            field_details.update({"related_db_column_name":related_db_column_name})
        return field_details

    def get_column_details(self,model) -> list:
        """
        Get columns with their data types and related tables/columns of a Django model.
        """

        lst_column_details = []

        for field in model._meta.get_fields():
            field_details = {}
            field_details.update({"field_name": self.get_field_name(field=field)})
            field_details.update({"db_column_name": self.get_db_column(field=field)})
            field_details.update({"datatype": self.get_datatype(field=field)})
            field_details.update({"model_name": self.get_model_name(model=model)})
            field_details.update({"app_label": self.get_app_label_from_model(model=model)})
            field_details.update({"app_full_name": self.get_app_full_name(model=model)})

            field_details.update(self.get_related_field_details(field=field))

            lst_column_details.append(field_details)

        return lst_column_details

    def prepare_joins_data(self,lst_column_details:list) -> list:
        """
        Preparing the Joins Data using column details list
        """
        lst_joins = []
        for column_details in lst_column_details:
            join_details = {}
            if column_details.get("datatype")=="ForeignKey":
                source_app_label = column_details.get("app_label")
                source_app_full_name = column_details.get("app_full_name")
                source_model_name = column_details.get("model_name")

                related_app_label = column_details.get("related_app_label")
                related_app_full_name = column_details.get("related_app_full_name")
                related_model_name = column_details.get("related_model_name")

                if related_app_label+"."+related_model_name in self.lst_app_label_model_name:
                    related_field_name = column_details.get("related_field_name")
                    inst_model = self.get_model_by_name(app_name=related_app_label,model_name=related_model_name)
                    if inst_model:
                        if related_field_name in self.get_model_column_names(model=inst_model):
                            join_details.update({"related_model_name":related_model_name})
                            join_details.update({"related_field":related_field_name})
                            join_details.update({"related_app_label":related_app_label})
                            join_details.update({"related_app_full_name":related_app_full_name})
                            join_details.update({'type': 'ForeignKey'})
                            join_details.update({"source_model_name":source_model_name})
                            join_details.update({"source_app_label":source_app_label})
                            join_details.update({"source_app_full_name":source_app_full_name})

                            lst_joins.append(join_details)
                        else:
                            lst_primary_fields = self.get_primary_key_fields(model=inst_model)
                            if len(lst_primary_fields)>0:
                                lst_primary_fields=lst_primary_fields[0]
                                join_details.update({"related_model_name":related_model_name})
                                join_details.update({"related_field":related_field_name})
                                join_details.update({"related_app_label":related_app_label})
                                join_details.update({"related_app_full_name":related_app_full_name})
                                join_details.update({'type': 'ForeignKey'})
                                join_details.update({"source_model_name":source_model_name})
                                join_details.update({"source_app_label":source_app_label})
                                join_details.update({"source_app_full_name":source_app_full_name})
                                lst_joins.append(join_details)
        return lst_joins

    def get_all_models_data(self) -> dict:
        """
        Get combined data of all models
        """
        lst_apps = []
        lst_models = []
        dct_data = {}

        # Iterate through all installed apps
        for app_config in self.apps_config:
            if self.is_app_to_include(app_config=app_config):
                lst_app_models = []
                app_label = self.get_app_label_from_app_config(app_config=app_config)
                app_full_name = self.get_app_full_name_from_app_config(app_config=app_config)
                dct_data.update({app_full_name:{}})

                # Get all models for the current app
                models = app_config.get_models()

                lst_apps.append(app_full_name)
                for model in models:
                    # Check if model is not part of exclusion list
                    if not self.is_model_to_exclude(model):
                        model_name = self.get_model_name(model=model)
                        model_doc_string = self.get_model_doc_string(model=model)
                        db_table_name = self.get_model_db_table_name(model=model)
                        lst_primary_fields = self.get_primary_key_fields(model=model)
                        lst_column_details = self.get_column_details(model=model)
                        lst_joins_details = self.prepare_joins_data(lst_column_details)

                        dct_data[app_full_name].update({model_name:{}})
                        model_details = {}
                        model_details.update({"app_full_name":app_full_name, "app_name":app_label,"model_name":model_name,"db_table_name":db_table_name,"model_doc_string":model_doc_string})
                        model_details.update({"lst_primary_fields":lst_primary_fields})
                        model_details.update({"lst_column_details":lst_column_details})
                        model_details.update({"lst_joins_details":lst_joins_details})

                        dct_data[app_full_name][model_name].update(model_details)
                        lst_models.append(model_name)
                        lst_app_models.append(model_name)
                dct_data[app_full_name].update({"lst_app_models":lst_app_models})

                if len(lst_app_models)==0:
                    del dct_data[app_full_name]
                    lst_apps.remove(app_full_name)

        return {"lst_apps":lst_apps,"dct_data":dct_data}
