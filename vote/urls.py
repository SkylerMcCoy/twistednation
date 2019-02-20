from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vote.views.home', name='home'),
    # url(r'^vote/', include('vote.foo.urls')),

    url(r'^public/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    #Cutom
    url(r'^$', 'members.views.login_member'),
    url(r'^login/$', 'members.views.login_member'),
    url(r'^register/$', 'members.views.register'),
    url(r'^logout/$', 'members.views.logout_member',  name="homepage_logout"),
    url(r'^profile/edit/$', 'members.views.profile_edit'),  
    url(r'^profile/$', 'members.views.profile_view', {'profile_id':''}),
    url(r'^profile/(?P<profile_id>.*)/$', 'members.views.profile_view'),
    url(r'^search/$', 'members.views.search_members'),
    url(r'^friend/add/$', 'members.views.friend_add'),
    url(r'^friend/accept/$', 'members.views.friend_accept'),
    url(r'^friend/delete/$', 'members.views.friend_delete'),
    url(r'^notifications/$', 'members.views.notifications'),
    url(r'^posts/$', 'posts.views.test_view'),
    url(r'^pinned-posts/$', 'pins.views.post_pins_view'),
    url(r'^pin/(?P<post_id>.*?)/pin/$', 'pins.views.post_pin'),
    url(r'^post/(?P<post_id>.*?)/action/$', 'posts.views.post_vote'),
    url(r'^comments/(?P<type>.+?)/(?P<id>.+?)/view/$', 'comments.views.comment_view'),
    url(r'^comments/(?P<type>.+?)/(?P<id>.+?)/add/$', 'comments.views.comment_add'),

    url(r'^home/$', 'history.views.home'),
    url(r'^friends/$', 'members.views.friends'),
    url(r'^messages/$', 'messages.views.message_view'),
    url(r'^messages/(?P<username>.+?)/send.+?$', 'messages.views.message_send'),
    url(r'^messages/(?P<username>.+?)/check.+?$', 'messages.views.message_check'),
    url(r'^messages/(?P<username>.+?)/$', 'messages.views.message_individual_view'),
    url(r'^templates/$', 'posts.views.templates'),
    url(r'^blog/$','blog.views.blog_view_all' ),
    url(r'^blog/create/$','blog.views.blog_edit' ),
    url(r'^blog/(?P<blog_id>.+?)/edit/$','blog.views.blog_edit' ),
    url(r'^blog/(?P<blog_id>.+?)/$','blog.views.blog_view' ),
    url(r'^realtime/$','realtime.views.notifications' ),
    url(r'^polls/search/$','polls.views.poll_search' ),
    url(r'^polls/trending/$','polls.views.poll_trending' ),
    url(r'^polls/$','polls.views.poll_create' ),
    url(r'^polls/(?P<poll_id>.+?)/$','polls.views.poll_view' ),
    url(r'^poll/(?P<poll_id>.+?)/(?P<choice_id>.+?)/select/$','polls.views.choice_select' ),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'%s(?P<path>.*)' % settings.MEDIA_URL[1:], 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
    
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^public/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.SITE_ROOT+'/templates/static'}),
    )
"""
urlpatterns += patterns('',
    url(r'^petitions/$', 'petitions.views.index'),
    url(r'^petitions/(?P<pet_id>\d+)/?$','petitions.views.viewpet'),
    url(r'^petitions/(?P<pet_id>\d+)/signed/?$','petitions.views.signed'),
    url(r'^petitions/listall/?$','petitions.views.listall'),
    url(r'^petitions/(?P<pet_id>\d+)/delete/?$','petitions.views.delpet'),
)
"""
urlpatterns += patterns('',
    #url(r'^petitions/$', 'petitions.views.index'),
    url(r'^petitions/?$','petitionsnew.views.pet_view_all'),
    url(r'^petitions/create/?$','petitionsnew.views.create_petition'),
    url(r'^petitions/(?P<pet_id>\d+?)/add-decision-maker/?$','petitionsnew.views.dm_add'),
    url(r'^petitions/(?P<pet_id>\d+?)/sign/?$','petitionsnew.views.pet_sign'),
    url(r'^petitions/(?P<pet_id>\d+?)/?$','petitionsnew.views.view_pet'),
    url(r'^petitions/(?P<pet_id>\d+?)/cover-letter/?$','petitionsnew.views.pet_cover'),
    url(r'^petitions/(?P<pet_id>\d+?)/audio-message/?$','petitionsnew.views.pet_audio_msg'),
    url(r'^petitions/(?P<pet_id>\d+?)/delete/?$','petitionsnew.views.pet_del'),
    #url(r'^petitions/(?P<pet_id>\d+)/signed/?$','petitions.views.signed'),
    #url(r'^petitions/listall/?$','petitions.views.listall'),
    #url(r'^petitions/(?P<pet_id>\d+)/delete/?$','petitions.views.delpet'),
)

urlpatterns += patterns('',
    url(r'^debate/done/$','debate.views.index'),
    url(r'^debate/step2/$','debate.views.steptwo'),
    url(r'^debate/$','debate.views.stepthree'),
    url(r'^debate/(?P<deb_id>\d+)/?$','debate.views.viewdeb'),
    url(r'^debate/participate/(?P<deb_id>\d+)/$','debate.views.participate'),
    url(r'^debate/invite/(?P<deb_id>\d+)/$','debate.views.invite'),
    url(r'^debate/(?P<deb_id>\d+)/start/$','debate.views.start'),
)

urlpatterns += patterns('',
    url(r'^upload/$','upload.views.upload_image'),
    url(r'^albumlist/$','upload.views.index'),
    url(r'^albumlist/(?P<album_id>\d+)/?$','upload.views.viewalbum'),
    url(r'^albumedit/(?P<album_id>\d+)/?$','upload.views.editalbum'),    
    url(r'^viewpic/(?P<pic_id>\d+)/?$','upload.views.viewpic'),
    url(r'^deletepic/(?P<pic_id>\d+)/?$','upload.views.deletepic'),
)

urlpatterns += patterns('',
    url(r'^history/$','history.views.histry'),
)

urlpatterns += patterns('',
    url(r'^video/$','video.views.upload'),
    url(r'^video/(?P<vid_id>\d+)/?$','video.views.viewvid'),
)
urlpatterns += patterns('',
    (r'^grappelli/', include('grappelli.urls')),
)
urlpatterns += patterns('',
    (r'^tinymce/', include('tinymce.urls')),
)


