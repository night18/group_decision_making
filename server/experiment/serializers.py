from rest_framework import serializers
from .models import Defendant

class DefendantModelSerializer(serializers.HyperlinkedModelSerializer):
	instance_id = serializers.SerializerMethodField('get_instance_id')
	class Meta:
		model = Defendant
		fields = ('instance_id', 'race', 'sex', 'age', 'prior', 'felony', 'misdemeanor', 'charge_degree', 'charge_reason', 'charge_explain', 'model_suggestion', 'ground_truth', 'condition')

	def get_instance_id(self, obj):
		return obj._id

class DefendantWOTruthModelSerializer(serializers.HyperlinkedModelSerializer):
	instance_id = serializers.SerializerMethodField('get_instance_id')
	class Meta:
		model = Defendant
		fields = ('instance_id', 'race', 'sex', 'age', 'prior', 'felony', 'misdemeanor', 'charge_degree', 'charge_reason', 'charge_explain', 'model_suggestion', 'condition')

	def get_instance_id(self, obj):
		return obj._id


class DefendantTruthModelSerializer(serializers.HyperlinkedModelSerializer):
	instance_id = serializers.SerializerMethodField('get_instance_id')

	class Meta:
		model = Defendant
		fields = ('instance_id', 'ground_truth')	

	def get_instance_id(self, obj):
		return obj._id	