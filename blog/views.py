from django.shortcuts import render
from .models import POST, Comment
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import CommentForm

# Vista para mostrar todos los post

def post_list(request):
    posts = POST.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

# Vista para ver un detalle de un post 

def post_detail(request, pk):
    post = get_object_or_404(POST, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# Vista para crear un nuevo post

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# Vista para editar un post

@login_required
def post_edit(request, pk):
    post = get_object_or_404(POST, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# Vista para los borradores
@login_required
def post_draft_list(request):
    posts = POST.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

# Vista para publicar el borrador

@login_required
def post_publish(request, pk):
    post = get_object_or_404(POST, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

# Vista para eliminar una publicacion

@login_required
def post_remove(request, pk):
    post = get_object_or_404(POST, pk=pk)
    post.delete()
    return redirect('post_list')


# Vista para agregar comentarios

def add_comment_to_post(request, pk):
    post = get_object_or_404(POST, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

# Vistas para aprobar y eliminar comentarios

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)