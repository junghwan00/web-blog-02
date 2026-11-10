from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from .models import Post
from .forms import PostForm
from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer
from .permissions import IsAuthorOrReadOnly


def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by('-published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def js_test(request):
    return render(request, 'blog/js_test.html', {})


# 공통평가 01 - #13 기타 편의기능: 검색/정렬/페이지네이션 + 본인 글 수정·삭제 권한
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'text']
    ordering_fields = ['published_date', 'created_date', 'title']
    ordering = ['-published_date']

    def perform_create(self, serializer):
        now = timezone.now()
        serializer.save(author=self.request.user, created_date=now, published_date=now)


# 로그인한 사용자 정보 확인용 (안드로이드 "서버 설정" 화면에서 로그인 성공 여부/아이디 표시에 사용)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def me(request):
    return Response({
        'id': request.user.id,
        'username': request.user.username,
    })


# 공통평가 02 - 편의기능#2: 감지 통계 대시보드
def stats(request):
    posts = Post.objects.all()
    total = posts.count()
    by_title = list(posts.values('title').annotate(count=Count('id')).order_by('-count'))
    max_count = by_title[0]['count'] if by_title else 0
    for row in by_title:
        row['percent'] = int(row['count'] * 100 / max_count) if max_count else 0
    recent = posts.order_by('-created_date')[:10]
    last_24h = posts.filter(created_date__gte=timezone.now() - timedelta(hours=24)).count()
    return render(request, 'blog/stats.html', {
        'total': total,
        'by_title': by_title,
        'recent': recent,
        'last_24h': last_24h,
    })
