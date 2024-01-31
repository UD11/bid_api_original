from django.db.models import Max
from django.http import HttpResponse
from django.shortcuts import render
from django.core.files.storage import default_storage

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from bidapp.serializers import UserSerializer, teamSerializer
from rest_framework.exceptions import AuthenticationFailed
from .models import User,team
import jwt,random,datetime
from storages.backends.s3boto3 import S3Boto3Storage
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

class signupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_image = request.FILES.get('user_image')
            if user_image:
                # Use the email as the filename
                user_image_name = f"{serializer.validated_data['email']}_{user_image.name}"

                s3 = S3Boto3Storage()
                user_image_path = f'user_images/{serializer.validated_data["email"]}/{user_image_name}'
                s3.save(user_image_path, user_image)

            print(serializer.validated_data)
            serializer.validated_data['user_image'] = user_image_path
            serializer.save()
            total_size = int(request.headers.get('Content-Length', 0))
            response_data = serializer.data
            response_data['total_size'] = total_size


            print('Total File Size:', total_size)

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#
# class signinView(APIView):
#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#
#         user = User.objects.filter(username=username, host = True).first()
#
#         if user is None:
#             raise AuthenticationFailed('USER NOT FOUND')
#
#         if not user.check_password(password):
#             raise AuthenticationFailed('INCORRECT PASSWORD')
#
#         payload = {
#             'id' : user.id,
#             'exp' : datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=60),
#             'iat' : datetime.datetime.now(tz=datetime.timezone.utc)
#         }
#
#         token = jwt.encode(payload,'secret',algorithm='HS256')
#
#         response = Response()
#         response.set_cookie(key='jwt',value=token, httponly=True, samesite='None')
#         response.data={
#             'jwt' : token,
#             # 'message' : 'Successfully logged in'
#         }
#
#         return response
#
# class getuserView(APIView):
#     def get(self, request):
#         token = request.COOKIES.get('jwt')
#         if not token:
#             raise AuthenticationFailed('unauthenticated user')
#         try:
#             data = jwt.decode(token,'secret',algorithms=['HS256'])
#         except:
#             raise jwt.ExpiredSignatureError('unauthenticated user')
#         id = data.get('id')
#         user = User.objects.get(id=id)
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

class getuserbyemailView(APIView):
    def get(self, request):
        email = request.query_params.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        file_path = f'{user.user_image.name}'
        s3_storage = default_storage

        with s3_storage.open(file_path) as image_file:
            response = HttpResponse(image_file.read(), content_type="image/jpeg")

        return response
#
# class signoutView(APIView):
#     def post(self, request):
#         response = Response({'message':'success'})
#         response.delete_cookie('jwt')
#
#         return response

class getallplayersView(APIView):
    def get(self, request):
        key = request.query_params.get('key', 'all')
        if key=='all':
            users = User.objects.filter(host = False, owner = False, coowner = False).exclude(player_position='NA')
        elif key=='sold':
            users  = User.objects.filter(host = False, owner =False, coowner = False,
                                         sold = True).exclude(player_position='NA')
        elif key =='unsold':
            users = User.objects.filter(host = False, owner =False, coowner = False,
                                        sold = False).exclude(player_position='NA')
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)


class getteamView(APIView):
    def get(self,request):
        team_id = request.query_params.get('team_id')
        curr_Team = team.objects.get(id = team_id)
        serializer = teamSerializer(curr_Team)
        return Response(serializer.data)


class getallteamView(APIView):
    def get(self,request):
        all_team = team.objects.all()
        serializer = teamSerializer(all_team,many=True)
        return Response(serializer.data)


class getnextplayerView(APIView):
    def get(self, request):
        role = request.query_params.get('role')
        players = User.objects.filter(player_position=role, sold=False,
                                      captain=False, vicecaptain=False, marquee=False)

        if players.exists():
            player = random.choice(players)
            serializer = UserSerializer(player)
            return Response(serializer.data)
        else:
            return Response({"message": "No available players for the specified role."}, status=404)

class TransferView(APIView):
    def post(self, request):
        print(request.data)
        try:
            with transaction.atomic():
                player_id = request.data.get('player_id')
                team_id = request.data.get('team_id')
                player_value = request.data.get('player_value')

                player = User.objects.get(id=player_id)
                selected_team = team.objects.get(id=team_id)

                if selected_team.pot - player_value < 0:
                    return Response({"message": "Team has not enough money"}, status=status.HTTP_400_BAD_REQUEST)

                selected_team.pot -= player_value
                player.sold = True
                player.player_value = player_value
                player.save()

                selected_team.players.add(player)
                selected_team.save()

                return Response({"message": "Player successfully transferred"})
        except ObjectDoesNotExist:
            return Response({"message": "User or Team not found"}, status=status.HTTP_404_NOT_FOUND)

class getPlayerByID(APIView):
    def get(self,request):
        player_id = request.query_params.get('player_id')
        player = User.objects.get(id=player_id)
        serializer = UserSerializer(player)
        return Response(serializer.data)


class records(APIView):
    def get(self, request):
        max_batsman = User.objects.filter(sold=True, player_position='Batsman').order_by('-player_value').first()
        max_bowler = User.objects.filter(sold=True, player_position='Bowler').order_by('-player_value').first()
        max_wk = User.objects.filter(sold=True, player_position='Wicketkeeper').order_by('-player_value').first()
        max_bla = User.objects.filter(sold=True, player_position='Bowling-All-Rounder').order_by('-player_value').first()
        max_bta = User.objects.filter(sold=True, player_position='Batting-All-Rounder').order_by('-player_value').first()

        data = {
            'max_batsman': UserSerializer(max_batsman).data if max_batsman else None,
            'max_bowler': UserSerializer(max_bowler).data if max_bowler else None,
            'max_wk': UserSerializer(max_wk).data if max_wk else None,
            'max_bla': UserSerializer(max_bla).data if max_bla else None,
            'max_bta': UserSerializer(max_bta).data if max_bta else None,
        }

        return Response(data)