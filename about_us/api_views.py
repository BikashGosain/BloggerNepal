from rest_framework.generics import ListAPIView
from .models import AboutUs
from .serializers import AboutUsSerializer

class AboutUsListAPIView(ListAPIView):
    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
