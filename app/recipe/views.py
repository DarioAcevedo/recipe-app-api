from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


from core.models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer

# Create your views here.

class BaseRecipeAtrrViewSet(viewsets.GenericViewSet,
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin):
    """Base model viewset for user owned recipe attributes"""
    authentication_classes= (TokenAuthentication, )
    permission_classes= (IsAuthenticated, )
    
    def get_queryset(self):
        """Return objects for current user"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        
        serializer.save(user=self.request.user)


class TagViewSet(BaseRecipeAtrrViewSet):
    """Manage tags in the database"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(BaseRecipeAtrrViewSet):
    """Manage the Ingredients"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Manage recipes in database"""
    serializer_class= RecipeSerializer
    queryset= Recipe.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes= (IsAuthenticated,)

    def get_queryset(self):
        
        return self.queryset.filter(user=self.request.user)

    