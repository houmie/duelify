from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from duelify_app.views import logout_page, discussions,\
    discussion_add_edit, register_page, RegisterSuccess, ChooseCategoryView, CategoryCreate, CategoryUpdate, CategoryDelete,\
    filter_discussions, friends_accept, topics_discuss, voteup_discussion,\
    feedback, side_login, main_login, new_users_invited, login_invited
from django.views.generic.list import ListView
from duelify_app.models import Ring, Category
from django.views.generic.base import TemplateView


js_info_dict = {
     'packages': ('duelify_app',),
}

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'duelify.views.home', name='home'),
    # url(r'^duelify/', include('duelify.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'', include('social_auth.urls')),
    (r'^admin/', include(admin.site.urls)),
    url(r'^post$', TemplateView.as_view(template_name="post.html")),
    #url(r'^error$', TemplateView.as_view(template_name="error.html")),
    (r'^side_login/$', side_login),
    (r'^login/$', main_login),
    (r'^logout/$', logout_page),
    (r'^register/$', register_page),
    (r'^register/success/$', RegisterSuccess.as_view(template_name='registration/register_success.html')),
    (r'^i18n/$', include('django.conf.urls.i18n')),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),
    
    (r'^password_reset/$','django.contrib.auth.views.password_reset'),
    (r'^password_reset_done/$','django.contrib.auth.views.password_reset_done'),
    (r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$','django.contrib.auth.views.password_reset_confirm'),
    (r'^password_reset_complete/$','django.contrib.auth.views.password_reset_complete'),
    
    (r'^$', discussions),
    (r'^feedback/$', feedback),
    #(r'^discussion/(?P<discussion_id>\d+)/$', discussion_display),
    #(r'^discussion/delete/(?P<discussion_id>\d+)/$', discussion_delete),
    #(r'^discussion/edit/(?P<discussion_id>\d+)/$', discussion_add_edit),
    #(r'^discussion/add/', DiscussionAddEdit.as_view()),
    (r'^topics/add/$', discussion_add_edit),
    url(r'^topics/discuss/(?P<ring_id>\d+)/$', topics_discuss, name='discuss-topic'),
    (r'^vote-up/discussion/(?P<punch_id>\d+)/$', voteup_discussion),
    
    #(r'^topics/search/', discussion_search),
#    url(r'^topics/search/$', ListView.as_view(
#                                           queryset=Ring.objects.order_by('-datetime'), 
#                                           context_object_name='ring_list', 
#                                           template_name='discussions.html'), name='topic-search'),
    #url(r'^topics/search/$', ChooseCategoryView.as_view(), name='topic-search'),
    url(r'^topics/search/$', filter_discussions, name='topic-search'),    
    url(r'^topics/filter/$', ChooseCategoryView.as_view(), name='topic-filter'),    
    url(r'^categories/$', ListView.as_view(model=Category, context_object_name='categories', template_name='categories.html'), name='category-list'),
#    url(r'^category/add/$', CategoryCreate.as_view(), name='author-add'),
#    url(r'^category/edit/(?P<pk>\d+)/$', CategoryUpdate.as_view(), name='author-edit'),
#    url(r'^category/delete/(?P<pk>\d+)/$', CategoryDelete.as_view(), name='author-delete'),
    #(r'^duel/invite/$', duel_invite),
    (r'^duel/accept/(\w+)/$', friends_accept),
    #url(r'^register-invite/$', register_invite, name='register-invite'),
    url(r'^new-users-invited/$', new_users_invited, name='new-users-invited'),
    url(r'^login-invited/$', login_invited, name='login-invited'),    
    url(r'^signup-error/$', TemplateView.as_view(template_name="error.html"), name='signup-error'),
        
)
urlpatterns += staticfiles_urlpatterns()
