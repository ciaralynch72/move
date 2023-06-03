from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect, HttpResponse
from .models import Post, Comment, Category
from .forms import CommentForm, ContactForm, PostForm, EditForm
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.urls import reverse_lazy


# Create your views here.

class PostList(generic.ListView):

    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(
        self,
        request,
        slug,
        *args,
        **kwargs
        ):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = \
            post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(request, 'post_detail.html', {
            'post': post,
            'comments': comments,
            'commented': False,
            'liked': liked,
            'comment_form': CommentForm(),
            })

    def post(
        self,
        request,
        slug,
        *args,
        **kwargs
        ):

        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = \
            post.comments.filter(approved=True).order_by('-created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(request, 'post_detail.html', {
            'post': post,
            'comments': comments,
            'commented': True,
            'comment_form': comment_form,
            'liked': liked,
            })


class PostLike(View):

    def post(
        self,
        request,
        slug,
        *args,
        **kwargs
        ):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


class CatListView(generic.ListView):

    template_name = 'category.html'
    context_object_name = 'catlist'

    def get_queryset(self):
        content = {'cat': self.kwargs['category'],
                   'posts': Post.objects.filter(category__name=self.kwargs
                   ['category'
                   ]).filter(status=1)}
        return content


def category_list(request):
    category_list = Category.objects.exclude(name='default')
    context = {'category_list': category_list}
    return context


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = 'Website Inquiry'
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
                }
            message = '\n'.join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com',
                          ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
                messages.success(request, "Message sent.")
            return redirect('home')
            messages.error(request, "Error. Message not sent.")

    form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def about(request):
    return render(request, 'about.html')


class AddPostView(generic.CreateView):

    model = Post
    form_class = PostForm
    template_name = 'add_blog_post.html'


class EditPostView(generic.UpdateView):

    model = Post
    form_class = EditForm
    template_name = 'edit_post.html'


class DeletePostView(generic.DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')