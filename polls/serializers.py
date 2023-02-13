from polls.models import SampleData, SampleDataMptt
from rest_framework import serializers


class RecursiveField(serializers.Serializer):
    def to_native(self, value):
        return self.parent.to_native(value)


class SampleDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = SampleData
        fields = '__all__'


class SampleDataMpttSerializers(serializers.ModelSerializer):
    children = RecursiveField(many=True, required=False)
    parent = SampleDataSerializers(source='datarow')

    class Meta:
        model = SampleDataMptt
        fields = '__all__'


class SampleTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()
    parent = SampleDataSerializers(source='datarow')

    class Meta:
        model = SampleDataMptt
        fields = ['id', 'parent', 'children']

    def get_children(self, obj):
        serializer = self.__class__(
            obj.get_children(), many=True, context=self.context
        )
        return serializer.data
