from django.template import RequestContext
from django.shortcuts import  get_object_or_404, render_to_response
from blog.models import Post


def index(request):
    context = RequestContext(request)
    # get the blog posts that are published
    posts = Post.objects.filter(published=True)
    # now return the rendered template
    return render_to_response( 'blog/index.html', {'posts': posts},context)

def post(request, slug):
    context = RequestContext(request)
    # get the Post object
    post = get_object_or_404(Post, slug=slug)
    # now return the rendered template	
    return render_to_response('blog/post.html', {'post': post},context)


