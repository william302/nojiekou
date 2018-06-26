def get_model():
    from blog.models import MPTTComment
    return MPTTComment


def get_form():
    from blog.forms import MPTTCommentForm
    return MPTTCommentForm

