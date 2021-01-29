from .topic import Topic
from .message import Message
from .categories import Category, SubCategory

'''def annotate_posts(queryset, user):
    queryset = queryset.select_related('user')
    annotate_post_kwargs = {'likes': models.Count('postlike')}
    if user.is_authenticated:
        annotate_post_kwargs['is_user_liked'] = models.Count('postlike', filter=models.Q(postlike__user=user))
    annotated = queryset.annotate(**annotate_post_kwargs)
    return annotated.prefetch_related(
        models.Prefetch(
            'comment_set',
            queryset=Comment.objects.select_related('user').order_by('created'))
    )'''
