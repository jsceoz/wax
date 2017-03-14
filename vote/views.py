from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, authentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from .models import Activity, Group, Item, Vote
from user.models import Student, Staff
from news_management.views import get_ip
import datetime
import django_filters.rest_framework


class StaffPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        try:
            student = Student.objects.filter(user=request.user)
            staff = Staff.objects.filter(student=student)
        except:
            return False
        return True


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ('id', 'name', 'content', 'starting_time', 'end_time', 'least_vote_num', 'most_vote_num')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields =  ('id', 'activity', 'id_in_activity', 'name')


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'group', 'name', 'cover', 'content', 'id_in_group', 'id_in_activity', 'vote_num')


class ActivitySet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('id',)


class GroupSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('id', 'activity')


class ItemSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [StaffPermission]
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter
    )
    filter_fields = ('id', 'group')


class ListAndCreateVote(APIView):
    authentication_classes = (authentication.TokenAuthentication,)

    def check_vote_num(self, user, item):
        """
        check has voted today and whether exceed limit
        :param user:
        :param item:
        :return:
        """
        vote_set = Vote.objects.filter(date=datetime.date.today(), item__group=item.group)
        group = item.group

        group_most_vote_num = group.most_vote_num

        if len(vote_set) >= group_most_vote_num:
            return False
        for vote in vote_set:
            if vote.item == item:
                return False
        return True

    def post(self, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        user = request.user
        item = request.data['item']
        item_instance = Item.objects.get(pk=item)

        if self.check_vote_num(request.user, item_instance):
            vote = Vote(
                item=item_instance,
                ip=ip,
                user=Student.objects.get(user=user),
            )
            vote.save()
            return Response(status=status.HTTP_201_CREATED, data={'msg': 'success'})
        else:
            return Response(status=status.HTTP_200_OK, data={'msg': 'exceed limit'})


















































