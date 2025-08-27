from rest_framework import serializers
from .models import Ad, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class AdSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, allow_null=True, required=False
    )
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Ad
        fields = (
            'id', 'title', 'description', 'price', 'is_active', 'created_at', 'owner', 'category', 'category_id',
            'status')

    def validate_title(self, v):
        if len(v) < 3:
            raise serializers.ValidationError("Заголовок должен быть длиной от 3 символов.")
        return v

    def validate_price(self, v):
        if v is not None and v < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return v
