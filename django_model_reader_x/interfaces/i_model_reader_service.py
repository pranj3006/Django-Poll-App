"""
Interface for Model Reader Service
"""
from abc import ABC, abstractmethod


class IModelReaderService(ABC):

    @abstractmethod
    def get_model_by_name(self,app_name:str,model_name:str):
        pass
    
    @abstractmethod
    def get_app_name_from_app_config(self,app_config) -> str:
        pass

    @abstractmethod
    def get_app_label_from_app_config(self,app_config) -> str:
        pass
    
    @abstractmethod
    def get_app_label_from_model(self,model) -> str:
        pass

    @abstractmethod
    def get_model_name(self,model) -> str:
        pass

    @abstractmethod
    def get_model_doc_string(self,model) -> str:
        pass
    
    @abstractmethod
    def get_model_db_table_name(self,model) -> str:
        pass
    
    @abstractmethod
    def set_all_lst_app_label_model_names(self):
        pass

    @abstractmethod
    def get_model_column_names(self,model) -> list:
        pass

    @abstractmethod
    def is_model_to_exclude(self,model) -> bool:
        pass
    
    @abstractmethod
    def is_app_to_include(self,app_config) -> bool:
        pass

    @abstractmethod
    def get_primary_key_fields(self,model) -> list:
        pass

    @abstractmethod
    def get_field_name(self,field) -> str:
        pass

    @abstractmethod
    def get_db_column(self,field) -> str:
        pass

    @abstractmethod
    def get_datatype(self,field) -> str:
        pass
    
    @abstractmethod
    def get_related_field_details(self,field) -> dict:
        pass
    
    @abstractmethod
    def get_column_details(self,model) -> list:
        pass
    
    @abstractmethod
    def prepare_joins_data(self,lst_column_details:list) -> list:
        pass
    
    @abstractmethod
    def get_all_models_data(self) -> dict:
        pass  

