from django.shortcuts import render, get_object_or_404
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .models import Pet
from .serializers import PetBaseSerializer
from rest_framework.response import Response
from rest_framework import status


class PetBaseListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, APIView):
    """
    Просмотр списка питомцев и добавление нового питомца.
    Доступ только для администратора.
    """
    serializer_class = PetBaseSerializer
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        # Вызываем метод для получения списка питомцев
        queryset = self.get_queryset()
        pets = queryset.all()
        # Рендерим HTML-шаблон с данными о питомцах
        return render(request, 'pet_base/pet_base.html', {'pets': pets})

    def post(self, request, *args, **kwargs):
        # Cоздание нового питомца
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        # Фильтруем список питомцев по кличке
        queryset = Pet.objects.all()
        name = self.request.GET.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset


class PetBaseRetrieveUpdateDestroyView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                                       mixins.DestroyModelMixin, APIView):
    """
    Просмотр, обновление и удаление записи о питомце.
    """
    serializer_class = PetBaseSerializer
    queryset = Pet.objects.all()

    def get(self, request, pk, *args, **kwargs):
        pet = self.get_object(pk)
        return render(request, 'pet_base/pet_detail.html', {'pet': pet})

    def put(self, request, pk, *args, **kwargs):
        pet = self.get_object(pk)
        # Обновляем питомца
        serializer = self.serializer_class(pet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        pet = self.get_object(pk)
        pet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        return get_object_or_404(Pet, pk=pk)
