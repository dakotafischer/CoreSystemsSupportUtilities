from django.shortcuts import render
from django.views import generic
from .models import LoggedApp, AuditLog
from django.core.paginator import Paginator
from .forms import AuditLogForm

class AuditLogsView(generic.ListView):
    form_class = AuditLogForm
    initial = {'key': 'value'}
    model = AuditLog
    template_name = 'logs/generic-list.html'
    context_object_name = 'query_set'
    paginate_by = 20
    #form_holder = None

    def get_queryset(self, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)
        return q_set

    def get(self, request, *args, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)

        #adding the paginator
        paginator = Paginator(q_set, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        form = self.form_class(request.GET)
        if form.is_valid() and form.cleaned_data['entity_id'] is not None:
            entity_id = form.cleaned_data['entity_id']
            q_set = AuditLog.objects.filter(environment=environment, entity_id__icontains=entity_id)
            return render(request, self.template_name, {'form': form, 'query_set': page_obj})
        else:
            form = self.form_class(initial=self.initial)
            return render(request, self.template_name, {'form': form, 'query_set': page_obj})
        '''
        Idk about this part or lines 159 or 122 .. You have to pass the query results around somehow but i'm to tired to get this to work right meow
        elif self.form_holder:
            entity_id = self.form_holder.cleaned_data['entity_id']
            q_set = AuditLog.objects.filter(environment=environment, entity_id__icontains=entity_id)
            paginator = Paginator(q_set, 25)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, self.template_name, {'form': form, 'query_set': page_obj})
        '''


    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        #self.form_holder = form
        environment = self.kwargs['env']
        if form.is_valid():
            entity_id = form.cleaned_data['entity_id']
            q_set = AuditLog.objects.filter(environment=environment, entity_id__icontains=entity_id)

            # adding the paginator
            paginator = Paginator(q_set, 25)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, self.template_name, {'form': form, 'query_set': page_obj})

    def filter_from_form(self, environment, entity_id, saml_subject, date):
        q_set = AuditLog.objects.filter(environment=environment)
        if entity_id is not None:
            q_set = q_set.filter(entity_id__icontains=entity_id)
        if saml_subject is not None:
            q_set = q_set.filter(saml_subject__icontains=saml_subject)
        if date is not None:
            pass
        return q_set

class HomeView(generic.ListView):       # this needs to return a dict to build the env table with. tables = { application = {name = pf, env = prod, log_types = [audit, transaction, server,]}
    model = AuditLog
    template_name = 'logs/generic-list.html'

    def get_app_environments(self):
        app_environments = dict()
        for app in Application.objects.all().distinct():
            app_environments[str(app)] = ApplicationEnvironment.objects.filter(application=app)
        return app_environments

    def get_log_types(self):
        application_log_types = dict()
        for app in Application.objects.all().distinct():
            application_log_types[str(app)] = LogType.objects.filter(application=app)
        return application_log_types

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['now'] = timezone.now()
        context['applications'] = Application.objects.all()
        context['application_log_types'] = self.get_log_types()
        context['app_environments'] = self.get_app_environments()
        return context

class LoggedAppsView(generic.ListView):
    ''' note: to pass a class based view the url parameters you just access them via a functions kwargs.
    # for example in get_queryset(self, **kwargs): you can get a url param via self.kwargs['name-of-arg']'''
    model = LoggedApp
    #template_name = 'logs/generic-list.html'
    template_name = 'logs/generic-list.html'
    #context_object_name = 'query_set'
    context_object_name = 'app_tables'

    def get_queryset(self, **kwargs):
        q_set = self.get_app_tables()
        return q_set

    def get_app_tables(self):
        app_tables = {
            'Ping Federate Logs' : ['PROD', 'TEST', 'QA', 'DEV',],
            'Event Manager Logs' : ['PROD', 'TEST', 'QA', 'DEV',],
            }
        return app_tables


    def filter_by_app(self, application):
        q_set = LoggedApp.objects.filter(application__startswith=self.kwargs['application'])
        if len(q_set) > 0:
            return q_set
        else:
            return ['No Application found that starts with :' + str(self.kwargs['application'])]

    def filter_by_env(self, q_set, environment):
        q = q_set.filter(environment__iexact=environment)
        if len(q) > 0:
            return q
        else:
            q.insert('No Environment found for :' + str(environment))
            return q

class ServerLogsView(generic.ListView):
    model = AuditLog
    template_name = 'logs/generic-list.html'
    context_object_name = 'query_set'

    def get_queryset(self, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)
        return q_set

class TransactionLogsView(generic.ListView):
    model = AuditLog
    template_name = 'logs/generic-list.html'
    context_object_name = 'query_set'

    def get_queryset(self, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)
        return q_set



class RequestLogsView(generic.ListView):
    model = AuditLog
    template_name = 'logs/generic-list.html'
    context_object_name = 'query_set'

    def get_queryset(self, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)
        return q_set

class AdminLogsView(generic.ListView):
    model = AuditLog
    template_name = 'logs/generic-list.html'
    context_object_name = 'query_set'

    def get_queryset(self, **kwargs):
        environment = self.kwargs['env']
        q_set = AuditLog.objects.filter(environment=environment)
        return q_set
