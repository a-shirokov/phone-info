from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import FormView

from .forms import PhoneNumberForm


class PhoneInfoView(FormView):
    title = 'Информация о номере телефона'
    form_class = PhoneNumberForm
    template_name = 'phone_info.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.title
        return context

    def form_valid(self, form):
        phone_info = form.get_phone_info()

        context = self.get_context_data(
            form=self.get_form_class()(
                initial=self.get_initial(),
                prefix=self.get_prefix(),
            ),
            phone=form.cleaned_data['phone'],
            phone_info=phone_info,
        )
        context['phone_info'] = phone_info

        print(context)

        return self.render_to_response(context)

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
