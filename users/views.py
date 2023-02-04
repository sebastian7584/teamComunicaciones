from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from azureControl.azureControl import Azure_db
from .models import User
import jwt, datetime
import json

db = Azure_db()

# Create your views here.
class RegisterView(APIView):

    def post(self, request):
        serializer = UserSerializer(data =request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        try:
            user = db.read_item('usuarios', email)
        except Exception as e:
            user = None

        if user is None:
            raise AuthenticationFailed('Usuario no encontrado')
        
        if password != user['password']:
            raise AuthenticationFailed('Clave incorrecta')
        
        
        payload = {
            'id' : user['serial'],
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes= 60),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt':token
        }
        
        return response

class UserView(APIView):

    def post(self, request):
        response = Response()
        response.set_cookie(key='jwts', value='hhh', httponly=True)
        data = request.body
        token = json.loads(data)
        token = token['jwt']
        print(token)
        if not token:
            raise AuthenticationFailed('Debes estar logueado')

        try:
            payload = jwt.decode(token, 'secret', algorithms='HS256')
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Debes estar logueado')
     
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        

        return Response({"detail":'d'})
    


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response