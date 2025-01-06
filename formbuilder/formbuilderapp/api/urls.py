from rest_framework.routers import DefaultRouter
from .views import FormViewSet, QuestionViewSet, ResponseViewSet, AnswerViewSet

router = DefaultRouter()
router.register(r'forms', FormViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'responses', ResponseViewSet)
router.register(r'answers', AnswerViewSet)

urlpatterns = router.urls
