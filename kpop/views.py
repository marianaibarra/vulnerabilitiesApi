
from rest_framework.views import APIView
from kpop.models import Album, EntertainmentCompany, Fan, Idol, IdolGroup, Song
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q, F

class KpopList(APIView):
    def get(self, request, format=None):
        try:
            """
            1. ¿Cuáles son las 3 compañías con más grupos bajo su gestión?
                Hint: Usa annotate(), Count() y ordena los resultados.
            """
            
            most_groups = EntertainmentCompany.objects.values('id', 'name').annotate(num_groups=Count("groups")).order_by("-num_groups")[:3]
            
            most_groups_nicer = {item['name']: item['num_groups'] for item in most_groups}
            
            """
            🔹 2. Encuentra todos los idols que sean líderes de sus grupos.
                Su position debe contener "Leader".
                La consulta debe devolver el stage_name y el grupo.
                Hint: Usa filter(Q(...)).
            """
            
            # Version 1
            # leaders = Idol.objects.filter(Q(position__contains='Leader'))
            
            # Version 2, reduce llamadas a la db
            leaders = Idol.objects.select_related('company', 'group').filter(Q(position__contains='Leader'))
            
            leaders_nicer = [{'company': idol.company.name, 'stage_name': idol.stage_name, 'group': idol.group.name if idol.group else None} for idol in leaders]
            
            """
            🔹 3. ¿Cuáles son los idols con la mayor diferencia entre altura y peso?
                Ordena los resultados mostrando stage_name, height_cm - weight_kg.
                Hint: Usa F() y annotate().
            
            """
            
            return Response(leaders_nicer)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
