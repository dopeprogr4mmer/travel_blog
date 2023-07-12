from django.db.models import Count, Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, get_object_or_404, reverse, redirect

from .models import Post, Author, PostView, Category

from newsletter.models import Signup

from .forms import CommentForm, PostForm

from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
# Create your views here.

from profiles.models import Profile

def handler404(request, *args, **kwargs):
    return render(request, '404.html', status = 404)

def handler500(request, *args, **kwargs):
    return render(request, '500.html', status = 500)

def data_deletion(request):
	return render(request, 'data_deletion.html', {})

def paginate(request, queryset):
	count = len(queryset)
	if count==0:
		context = {'count': count}
		return context

	paginator = Paginator(queryset[::-1], 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)

	
	context = {
		'count': count,
		'queryset' : paginated_queryset,
		'page_request_var' : page_request_var
	}
	return context
	
def search(request):
	category_count = get_category_count()
	#print(category_count)
	most_recent = Post.objects.order_by('-timestamp')[:3]
	all_posts = Post.objects.all()
	query = request.GET.get('q')
	if query:
		queryset = all_posts.filter(
			Q(title__icontains = query) |
			Q(overview__icontains = query) |
			Q(post_content__icontains = query)
		).distinct()

	most_recent = get_most_recent()
	category_count = get_category_count()
	context = paginate(request, queryset)
	count = context['count']
	if count==0:
		label = "It looks like there aren’t any great matches for your search."
	else:
		label = f"These are the results for your search. ({count})"
	context.update({'most_recent': most_recent,
					'category_count': category_count,
					'label': label
					})
	return render(request, 'blog.html', context)



def sort_by_category(request, category):
	queryset = Post.objects.filter(categories__title=category).order_by("-timestamp")
	#print(queryset)
	most_recent = get_most_recent()
	category_count = get_category_count()
	context = paginate(request, queryset)
	label = f"These are the posts in category '{category.upper()}'. ({context['count']})"
	context.update({'most_recent': most_recent,
					'category_count': category_count,
					'label': label
					})
	return render(request, 'blog.html', context)


def get_author(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None



def get_category_count():
	queryset = Post.objects.values('categories__title').annotate(Count('categories__title'))
	return queryset


def get_most_recent():
	queryset = Post.objects.order_by('-timestamp')[:3]
	return queryset


def index(request):
	featured = Post.objects.filter(featured = True)
	latest = Post.objects.order_by('-timestamp')[0:3]

	if request.method == 'POST':
		email = request.POST["email"]
		new_signup = Signup()
		new_signup.email = email
		new_signup.save()

	context = {
		'object_list' : featured,
		'latest' : latest
	}
	return render(request, 'index.html', context)

def blog(request):
	category_count = get_category_count()
	#print(category_count)
	most_recent = Post.objects.order_by('-timestamp')[:3]
	post_list = Post.objects.all()
	paginator = Paginator(post_list[::-1], 4)
	page_request_var = 'page'
	page = request.GET.get(page_request_var)

	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)
	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_pages)
	
	context = {
		'most_recent' : most_recent,
		'queryset' : paginated_queryset,
		'page_request_var' : page_request_var,
		'category_count' : category_count
	}
	return render(request, 'blog.html', context)

'''
def post_detail(request, id):
	most_recent = Post.objects.order_by('-timestamp')[:3]
	category_count = get_category_count()
	post =get_object_or_404(Post, id=id)

	if request.user.is_authenticated:	
		PostView.objects.get_or_create(user = request.user, post = post)

	commentform = CommentForm(request.POST or None)
	if request.method == 'POST':
		if commentform.is_valid():
			commentform.instance.user = request.user
			commentform.instance.post = post
			commentform.save()
			return redirect(reverse('myposts:post-detail', kwargs = {'id':post.pk }))

	context = {
		'commentform':commentform,
		'post':post,
		'most_recent' : most_recent,
		'category_count' : category_count
	}
	return render(request, 'post.html', context)



def post_create(request):
	if request.user.is_staff:
		title = 'Create'
		form = PostForm(request.POST or None, request.FILES or None)
		author = get_author(request.user)
		if request.method == 'POST': 
			if form.is_valid():
				form.instance.author = author
				form.save()
				return redirect(reverse('myposts:post-detail', kwargs = {'id':form.instance.id}))
		context = {
			'form':form,
			'title':title
	
				}
		return render(request, 'post_create.html', context)


def post_update(request, id):
	if request.user.is_staff:
		title = 'Update'
		post = get_object_or_404(Post, id=id)
		form = PostForm(
			request.POST or None,
			request.FILES or None, 
			instance = post)
		author = get_author(request.user)
		if request.method == 'POST': 
			if form.is_valid():
				form.instance.author = author
				form.save()
				return redirect(reverse('myposts:post-detail', kwargs = {'id':form.instance.id}))
		context = {
			'form':form,
			'title':title
			}
		return render(request, 'post_create.html', context)


def post_delete(request, id):
	if request.user.is_staff:
		post = get_object_or_404(Post, id=id)
		post.delete()
		return redirect(reverse('myposts:post-list'))


class PostUpdateView(UpdateView):
	template_name = "post_create.html" 	#overriding generic    
	form_class = PostForm
	queryset = Post.objects.all()			#<blog>/<modelname>_list.html
	#success_url = '/'

	def get_object(self):
		id_ = self.kwargs.get("id")
		return get_object_or_404(Post, id = id_)

	def form_valid(self, form):
		#print(form.cleaned_data)
		return super().form_valid(form)


def post_delete(request, id):
	if request.user.is_staff:
		post = get_object_or_404(Post, id=id)
		if request.method == "POST":
			post.delete()
			return redirect('blog/')
		context = {
			"post":post
		}
		return render(request,"post_delete.html", context)
'''
class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    form = CommentForm()

    def get_object(self):
        obj = super().get_object()
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(
                user=self.request.user,
                post=obj
            )
        return obj

    def get_context_data(self, **kwargs):
        category_count = get_category_count()
        most_recent = Post.objects.order_by('-timestamp')[:3]
        context = super().get_context_data(**kwargs)
        context['most_recent'] = most_recent
        context['page_request_var'] = "page"
        context['category_count'] = category_count
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            post = self.get_object()
            user = Profile.objects.get(user = request.user)
            form.instance.user = user
            form.instance.post = post
            form.save()
            return redirect(reverse("myposts:post-detail", kwargs={
                'pk': post.pk
            }))


"""
def post_detail(request, id):
    category_count = get_category_count()
    most_recent = Post.objects.order_by('-timestamp')[:3]
    post = get_object_or_404(Post, id=id)

    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=request.user, post=post)

    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.post = post
            form.save()
            return redirect(reverse("post-detail", kwargs={
                'id': post.pk
            }))
    context = {
        'post': post,
        'most_recent': most_recent,
        'category_count': category_count,
        'form': form
    }
    return render(request, 'post.html', context)
"""

class PostCreateView(CreateView):
	#if request.user.is_staff:
	model = Post
	template_name = 'post_create.html'
	form_class = PostForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Create'
		return context

	def form_valid(self, form):
		form.instance.author = get_author(self.request.user)
		form.save()
		return redirect(reverse("myposts:post-detail", kwargs={
		    'pk': form.instance.pk
		}))

"""
def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("myposts:post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)
"""

class PostUpdateView(UpdateView):
	#if request.user.is_staff:
	model = Post
	template_name = 'post_create.html'
	form_class = PostForm

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Update'
		return context

	def form_valid(self, form):
		form.instance.author = get_author(self.request.user)
		form.save()
		return redirect(reverse("myposts:post-detail", kwargs={
		    'pk': form.instance.pk
		}))

"""
def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Post, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("myposts:post-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)
"""

class PostDeleteView(DeleteView):
	#if request.user.is_staff:
	model = Post
	success_url = '/blog'
	template_name = 'post_delete.html'

"""
def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect(reverse("post-list"))
"""

