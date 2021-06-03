from rest_framework.routers import DefaultRouter

from .views import PostViewSet, FollowViewSet, GroupViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('follow', FollowViewSet)
router.register('group', GroupViewSet)
# router.register(r'posts/(?P<post_id>\d+)/comments/', CommentViewSet, basename='Comment')
