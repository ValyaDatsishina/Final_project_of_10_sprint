from rest_framework.routers import DefaultRouter

from .views import PostViewSet, FollowViewSet, GroupViewSet, UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('posts', PostViewSet)
router.register('follow', FollowViewSet)
router.register('group', GroupViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments/', CommentViewSet, basename='Comment')
