# Create your views here.
from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView
from django.views.generic import TemplateView
from duelify_app.forms import RingForm, RegistrationForm, PunchForm,\
    ChooseCategoryForm, FeedbackForm, AjaxLoginForm
from duelify_app.models import Ring, DuelInvitation, Punch, Category
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import logout, authenticate, get_user_model, login, REDIRECT_FIELD_NAME
from django.contrib.auth.views import login as loginview
from duelify import settings
from django.shortcuts import render, get_object_or_404, resolve_url
from django.contrib import messages
from django.template.loader import get_template
from django.template.context import Context
from django.core.mail import send_mail
from django.core.paginator import Paginator, InvalidPage
from django.template.loader_tags import register
from django.utils import timezone
from django.utils.translation import ugettext as _, ungettext
from django.core.urlresolvers import reverse_lazy, reverse
from django.db.models.query_utils import Q
from django.utils.http import is_safe_url
from django.contrib.sites.models import get_current_site
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
import json
from django.template.response import TemplateResponse
from duelify_app.utils import get_user_location_details, get_user_browser
from django.db.models import Count


def handle_invitation(request, invitation, user):
    if invitation.ring.rule == 'personal':
        if invitation.ring.punch_set.all()[:1].get().side == 'red':
            invitation.ring.blue.add(user)
        else:
            invitation.ring.red.add(user)
            invitation.ring.save() # Delete the invitation from the database and session.
    invitation.delete()
    del request.session['invitation']

class RegisterSuccess(TemplateView):
    template_name='registration/register_success.html'
    def get_context_data(self, **kwargs):
        context = super(RegisterSuccess, self).get_context_data(**kwargs)
        return context

@register.inclusion_tag('tag_form_label_div_below_error.html')
def show_row_div_below_error(form_field, *args, **kwargs):
    return {'form_field': form_field }


@sensitive_post_parameters()
@csrf_protect
@never_cache
def Ajaxlogin(request, template_name='registration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AjaxLoginForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = authentication_form(data=request.POST)
        if form.is_valid():
            
            # Ensure the user-originating redirection url is safe.
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            
            # Okay, security check complete. Log the user in.
            login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
                
            response = {'success' : True, 'redirect_to':redirect_to}
        else:
            response = form.errors_as_json()
        return HttpResponse(json.dumps(response, ensure_ascii=False), mimetype='application/json')
            
    else:
        form = authentication_form(request)

    request.session.set_test_cookie()

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context, current_app=current_app)

def get_score_for_user(user):    
    score = Ring.objects.filter(punch__voters=user).count() * 2    
    score = score + (Punch.objects.filter(speaker=user).aggregate(voter_count=Count('voters')))['voter_count'] * 5        
    score = score + Ring.objects.filter(Q(red=user)|Q(blue=user)).count() * 20        
    return score


def side_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        result = Ajaxlogin(request, template_name='registration/side_login.html')
        if request.user.is_authenticated():
            request.user.score = get_score_for_user(request.user)
            request.user.save()            
        return result


def main_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        result = loginview(request)
        if request.user.is_authenticated():
            request.user.score = get_score_for_user(request.user)
            request.user.save()            
        return result


@login_required
def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')



def friends_accept(request, code):
    invitation = get_object_or_404(DuelInvitation, code__exact=code)
    request.session['invitation'] = invitation.id
    return HttpResponseRedirect('/register/')


def login_invited(request):
    if 'invitation' in request.session:
        invitation = DuelInvitation.objects.get(id=request.session['invitation'])  
        if invitation.ring.rule == 'personal':
            if invitation.email == request.user.email:
                if invitation.ring.punch_set.all()[:1].get().side == 'red':
                    invitation.ring.blue.add(request.user)
                else:
                    invitation.ring.red.add(request.user)
            else:
                messages.error(request, _(u'%(inviter) had send an invitation to the email address %(email), but you used an account with a different email address to login.') % {'inviter':invitation.sender, 'email' : invitation.email})
                messages.warning(request, _(u'Please logout and pick an account with the given email address: %(email)') % {'email' : invitation.email})
                return HttpResponseRedirect('/')
        # Delete the invitation from the database and session.
        punch_id = invitation.ring.pk
        invitation.delete()
        del request.session['invitation']                  
        return HttpResponseRedirect(reverse('discuss-topic', args=str(punch_id)))
    else:
        return HttpResponseRedirect('/')

      

def register_page(request):    
    if 'invitation' in request.session:
            invitation = DuelInvitation.objects.get(id=request.session['invitation'])  
            users = get_user_model().objects.filter(email=invitation.email)
            if users.count() > 0:
                user = users[0]
                punch_id = invitation.ring.pk
                handle_invitation(request, invitation, user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return HttpResponseRedirect(reverse('discuss-topic', args=str(punch_id)))
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        if 'invitation' in request.session:
            #invitation = DuelInvitation.objects.get(id=request.session['invitation'])                    
            form = RegistrationForm(request.POST, is_accept_invite = True, _email = invitation.email)
        else:
            form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_location = get_user_location_details(request)
            browser_type = get_user_browser(request)
            user.location = user_location.country
            user.browser = browser_type
            user.save()
            
            if 'invitation' in request.session:
                # Retrieve the invitation object.                
                handle_invitation(request, invitation, user)                
            
                
            user = authenticate(username=form.cleaned_data['email'], password=form.cleaned_data['password2'])            
            login(request, user)

            new_user_annoucement(user)
            return HttpResponseRedirect('/register/success/')
    else:
        if 'invitation' in request.session:
            invitation = DuelInvitation.objects.get(id=request.session['invitation'])                   
            form = RegistrationForm(is_accept_invite = True, _email = invitation.email)
        else:            
            form = RegistrationForm()    
    
    is_invited = False
    if 'invitation' in request.session:
        is_invited = True
        variables = {'form':form, 'is_invited': is_invited, 'invitee':invitation.email, 'inviter':invitation.sender.get_full_name(), 'topic':invitation.ring.topic }
    else:
        variables = {'form':form, 'is_invited': is_invited }
    return render(request, 'registration/register.html', variables)

def new_user_annoucement(user):
    template = get_template('registration/welcome.txt')
    context = Context({'first_name': user.first_name, 'email': user.email})
    message = template.render(context)    
    send_mail('Welcome to Duelify', message, settings.DEFAULT_FROM_EMAIL, [user.email])
    
    template = get_template('registration/new_signup.txt')            
    context = Context({'username': user})
    message = template.render(context)
    send_mail('New User Registration', message, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])


 
ITEMS_PER_PAGE = 9
def makePaginator(request, ITEMS_PER_PAGE, queryset):
    paginator = Paginator(queryset, ITEMS_PER_PAGE)
    try:
        page_number = int(request.GET['page'])
    except (KeyError, ValueError):
        page_number = 1
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        raise Http404
    objects = page.object_list
    return objects, paginator, page, page_number

def get_paginator_variables(paginator, page, page_number, custom_prefix):
    if custom_prefix:
        return {
                custom_prefix + 'show_paginator': paginator.num_pages > 1, 
                custom_prefix + 'has_prev': page.has_previous(), 
                custom_prefix + 'has_next': page.has_next(), 
                custom_prefix + 'page': page_number, 
                custom_prefix + 'pages': paginator.num_pages, 
                custom_prefix + 'next_page': page_number + 1, 
                custom_prefix + 'prev_page': page_number - 1                
                }
    else:
        return {
                'show_paginator': paginator.num_pages > 1, 
                'has_prev': page.has_previous(), 
                'has_next': page.has_next(), 
                'page': page_number, 
                'pages': paginator.num_pages, 
                'next_page': page_number + 1, 
                'prev_page': page_number - 1                
                }

def merge_with_additional_variables(request, paginator, page, page_number, variables):
    variables = dict(variables.items() + get_paginator_variables(paginator, page, page_number, None).items()) #+ get_localized_variables(request).items())
    return variables

@login_required()
def voteup_discussion(request, punch_id):
    punch = get_object_or_404(Punch.objects.all(), pk=punch_id)
    if punch.speaker != request.user:        
        if punch.voters.filter(pk=request.user.pk).count() == 0:
            punch.voters.add(request.user)
        else:
            punch.voters.remove(request.user)
        punch.save()
        request.user.score = get_score_for_user(request.user)
        request.user.save()            
    return HttpResponseRedirect(reverse('discuss-topic', args={str(punch.ring.pk), punch.ring.slug}))
    

@login_required()
def topics_discuss(request, ring_id, slug):
    ring = get_object_or_404(Ring.objects.all(), pk=ring_id)
    punch = Punch(ring = ring)
    punches = ring.punch_set.order_by('datetime')    
    is_vote_only = False
    template_title = _(u'View & Vote') 
    punch_form = None    
    is_continue = False
    if ring.red.filter(pk=request.user.pk).exists() or ring.blue.filter(pk=request.user.pk).exists():
        is_continue = True
    if ring.rule == 'public':
        template_title = _(u'Open Topic')
    elif is_continue:        
        template_title = _(u'Continue Discussion')                
    else:
        is_vote_only = True
    
    if request.method == 'POST':  
        punch_form = PunchForm(request.POST)
        if punch_form.is_valid():
            punch = punch_form.save(commit=False)
            punch.ring = ring         
            
            if punch.side == 'red' and not ring.red.filter(pk=request.user.pk).exists():
                ring.red.add(request.user)
            elif punch.side == 'blue' and not ring.blue.filter(pk=request.user.pk).exists():
                ring.blue.add(request.user)
            elif not punch.side and ring.red.filter(pk=request.user.pk).exists():
                punch.side = 'red'
            elif not punch.side and ring.blue.filter(pk=request.user.pk).exists():
                punch.side = 'blue'
                
            punch.speaker = request.user
            punch.datetime = timezone.now()
            punch.save()
            ring.save()
            request.user.score = get_score_for_user(request.user)
            request.user.save()            
            return HttpResponseRedirect(reverse_lazy('discuss-topic', args=str(punch.ring.pk)))
    else:
        #Is the user allowed to contribute to this topic?
        if not is_vote_only:            
            if ring.red.filter(pk=request.user.pk).exists():
                punch.side = 'red'
            if ring.blue.filter(pk=request.user.pk).exists():
                punch.side = 'blue'
            punch_form = PunchForm(instance=punch)
    
    is_without_opponent = False
    winner_sofar = _(u'Winner so far in this discussion:')    
    winner_color = ''
    if ring.red.filter(pk=request.user.pk).exists() or ring.blue.filter(pk=request.user.pk).exists():
        if ring.red.count() == 0 or ring.blue.count() == 0: 
            winner = _(u'You have started this discussion and no one is opposing your view yet.')
            winner_sofar = ''
            is_without_opponent = True
    else:
        if ring.rule == 'public':
            winner = _(u'No one is opposing this view yet. Can you do it?')
            winner_sofar = ''
            is_without_opponent = True
        else:
            winner = _(u'This is a personal duel between two authors. Please vote for who is right.')
            winner_sofar = ''
            is_without_opponent = True
    
    red_votes = blue_votes = 0 
    for punch in ring.punch_set.all():
        if punch.side == 'red':            
            red_votes = red_votes + punch.get_votes()
        else:            
            blue_votes = blue_votes + punch.get_votes()
    if blue_votes > red_votes:
        winner_color = 'blue'
        if ring.rule == 'public':
            winner = _(u'Blue side is winning! Majority of users see the statement to be true.')
        else:
            winner = ring.blue.all()[:1].get().get_full_name()
    elif blue_votes < red_votes:
        winner_color = 'red'
        if ring.rule == 'public':
            winner = _(u'Red side is winning! Majority of users see the statement to be untrue.')
        else:
            winner = ring.red.all()[:1].get().get_full_name()
    elif blue_votes == red_votes and not is_without_opponent:
        winner_color = ''
        winner = _(u'No winner can yet be concluded. The race is on.')
        winner_sofar = '' 
    #rings = Ring.objects.filter(Q(red.filter(pk=request.user.pk)|Q(blue.filter(pk=request.user.pk))))    
    variables = {'punch_form':punch_form, 'template_title': template_title, 'ring':ring, 'punches':punches, 'winner_sofar':winner_sofar,
                 'winner':winner, 'winner_color':winner_color, 'is_continue':is_continue}
    return render(request, 'discuss_topic.html', variables)


@login_required()
def discussion_add_edit(request, discussion_id=None):       
    if discussion_id is None:
        ring = Ring(category = Category.objects.get(pk=1), datetime=timezone.now())
        punch = Punch(ring=ring)
        template_title = _(u'Start a new topic')        
    else:        
        ring = get_object_or_404(Ring.objects.all(), pk=discussion_id)
        punch = punch(ring=ring)
        template_title = _(u'Edit existing topic')        
    if request.method == 'POST':        
        ring_form = RingForm(request.POST)        
        punch_form = PunchForm(request.POST)
        if ring_form.is_valid() and punch_form.is_valid():
            ring = ring_form.save(commit=False)
            punch = punch_form.save(commit=False)
            
            datetime = timezone.now()
            ring.datetime = datetime
            #pick_side = ring_form.cleaned_data["pick_side"]
            ring.save()
            if punch.side == 'red':
                ring.red.add(request.user)                   
            else:
                ring.blue.add(request.user)                
            ring.save()                        
            
            punch.ring = ring
            punch.speaker = request.user 
            punch.datetime = datetime
            punch.save()
                        
            request.user.score = get_score_for_user(request.user)
            request.user.save()                       
            if ring_form.cleaned_data['blue_invite']:
                invitation = DuelInvitation(                                    
                                        email=ring_form.cleaned_data['blue_invite'],
                                        code=get_user_model().objects.make_random_password(20),
                                        sender=request.user,
                                        ring=ring
                                        )
                invitation.save()
                try:
                    invitation.send()                
                    messages.warning(request, _(u'An invitation was sent to %(email)s.') % {'email' : invitation.email})
                except Exception:                
                    messages.error(request, _(u'An error happened when sending the invitation.'))    
            #log_contact(request, contact, 'contact_add_edit', secondary, profile, is_edit)
            else:
                messages.warning(request, _(u'Your open topic has been started. Lets wait and see if someone bites...'))            
            return HttpResponseRedirect('/')
    else:
        ring_form = RingForm(instance=ring)
        punch_form = PunchForm(instance=punch, is_new=True)
    variables = {'ring_form':ring_form, 'punch_form':punch_form, 'template_title': template_title }
    return render(request, 'discussion.html', variables)


class CategoryCreate(CreateView):
    template_name = 'category.html'
    model = Category
    
class CategoryUpdate(UpdateView):
    template_name = 'category.html'
    model = Category

class CategoryDelete(DeleteView):
    template_name = 'category.html'
    model = Category
    success_url = reverse_lazy('category-list')

def discussions(request):    
    rings = ''
    if not request.user.is_anonymous():
        rings = Ring.objects.filter(Q(red=request.user)|Q(blue=request.user))
    top3rings = Ring.objects.order_by('-datetime')[0:3]
    top3_6rings = Ring.objects.order_by('-datetime')[3:6]
    source = '/rings'
    variables = { 'top3rings' : top3rings, 'top3_6rings':top3_6rings, 'source' : source, 'rings':rings}    
    return render(request, 'top6_topics.html', variables)



def filter_discussions(request):
    rings_queryset = Ring.objects.all()
    if request.method == 'POST':
        form = ChooseCategoryForm(request.POST)
        if form.is_valid():
            show_open_topics = form.cleaned_data['show_open_topics']
            category = form.cleaned_data['category']            
            if show_open_topics:
                rings_queryset = Ring.objects.filter(category=category).filter(rule='public')
            else:
                rings_queryset = Ring.objects.filter(category=category)
    else:
        form = ChooseCategoryForm()
    rings, paginator, page, page_number = makePaginator(request, ITEMS_PER_PAGE, rings_queryset)
    variables = { 'form' : form , 'rings':rings}    
    variables = merge_with_additional_variables(request, paginator, page, page_number, variables)
    return render(request, 'category.html', variables)
    

#class TopicFilterDetail(DetailView):
#    model = Ring
#    def get_context_data(self, **kwargs):
#        # Call the base implementation first to get a context
#        context = super(TopicFilterDetail, self).get_context_data(**kwargs)
#        # Add in a QuerySet of all the books
#        context['book_list'] = Book.objects.all()
#        return context
#
#class PublisherBookList(ListView):
#    template_name = 'category.html'
#    def get_queryset(self):
#        self.category = get_object_or_404(Category, pk=self.args[0])
#        return Ring.objects.filter(category=self.category)

class ChooseCategoryView(FormView):
    template_name='category.html'
    form_class=ChooseCategoryForm
    success_url=reverse_lazy('topic-search')
    category = None
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ChooseCategoryView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['rings'] = Ring.objects.filter(category = self.category)
        return context
    
    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.        
        self.category = form.cleaned_data['category']
        #self.success_url = '/test/' + str(category.pk)
        return super(ChooseCategoryView, self).form_valid(form)


@login_required
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            send_mail('Feedback', form.cleaned_data['feedback'] + ' user: ' + request.user.get_full_name() + ' email: ' + request.user.email, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
            messages.info(request, _(u'Thank you for your feedback.'))
            return HttpResponseRedirect('/')
    else:
        form = FeedbackForm()
    rings = ''
    if not request.user.is_anonymous():
        rings = Ring.objects.filter(Q(red=request.user)|Q(blue=request.user))
    variables = {'form':form, 'rings':rings}    
    return render(request, 'feedback.html', variables)

#@login_required()
#class DiscussionAddEdit(CreateView):
#    form_class = RingForm
#    model = Ring
#    
#    def form_valid(self, form):
#        #form.instance.created_by = self.request.user
#        return super(DiscussionAddEdit, self).form_valid(form)
    