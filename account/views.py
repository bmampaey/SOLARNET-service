from django.views.generic import TemplateView
from django.core.urlresolvers import reverse


from scenario_editor.models import Scenario, Telecommand

class UserHistoryView(TemplateView):
	http_method_names = [u'get']
	template_name = 'account/user_history.html'
	
	def get_context_data(self, **kwargs):
		'''Add history objects to the context'''
		context = super(UserHistoryView, self).get_context_data(**kwargs)
		context['scenario_history'] = list()
		#import pdb; pdb.set_trace()
		for record in Scenario.history.filter(history_user=self.request.user).order_by('id', '-history_date').distinct('id'):
			record.url = reverse('scenario_editor:scenario_detail', kwargs={'pk':record.id})
			context['scenario_history'].append(record)
		for record in Telecommand.history.filter(history_user=self.request.user).order_by('id', '-history_date').distinct('id'):
			record.url = reverse('scenario_editor:telecommand_detail',  kwargs={'pk':record.id})
			context['scenario_history'].append(record)
		return context

