from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .routers import router
# from .views import CommentList
from .views import CommentViewSet, FollowViewSet

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/<int:pk>/comments/', CommentViewSet.as_view({'get': 'list',
                                                             'post': 'create'})),
    path('posts/<int:pk>/comments/<int:pk_comment>/', CommentViewSet.as_view({'get': 'list',
                                                                              'put': 'update',
                                                                              'patch': 'update',
                                                                              'delete': 'destroy'})),
    # path('follow/', FollowViewSet.as_view({'get': 'list',
    #                                        'post': 'follow'})),
    path('', include(router.urls)),
    # path('posts/<int:pk>/comments/', CommentList.as_view())
]
