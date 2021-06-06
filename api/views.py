# TODO:  Напишите свой вариант
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .models import Post, Comment, User, Follow, Group
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, FollowSerializer, GroupSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group = self.request.query_params.get('group', None)
        if group is not None:
            #  через ORM отфильтровать объекты модели User
            #  по значению параметра username, полученнго в запросе
            queryset = queryset.filter(group=group)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly, ]

    def list(self, request, pk, pk_comment=None):
        post = get_object_or_404(Post, id=pk)
        if pk_comment:
            comment = get_object_or_404(self.queryset, id=pk_comment, post=pk)
            serializer = self.serializer_class(comment)
            return Response(serializer.data)
        comments = post.comments
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)

    def create(self, request, pk):
        post = get_object_or_404(Post, id=pk)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=self.request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk, pk_comment):
        post = get_object_or_404(Post, id=pk)
        comment = get_object_or_404(self.queryset, id=pk_comment, post=pk)
        serializer = self.serializer_class(comment, data=request.data)
        if request.user == comment.author:
            if serializer.is_valid():
                serializer.save(author=self.request.user, post=post)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk, pk_comment):
        comment = get_object_or_404(self.queryset, id=pk_comment, post=pk)
        if request.user == comment.author:
            comment.delete()
            return Response('Comment delete', status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=following__username', '=user__username']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def list(self, request):
    #     user = get_object_or_404(self.queryset, username=self.request.user)
    #     following = user.follower
    #     serializer = self.serializer_class(following, many=True)
    #     return Response(serializer.data)

    # def follow(self, request):
    #     user = Follow.objects.get(user=self.request.user)
    #     serializer = self.serializer_class(user, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=self.request.user)
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
