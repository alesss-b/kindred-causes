from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput, DateInput, Textarea, Select, NumberInput

class TailwindInput(TextInput):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'input'

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())
        input_html = super().render(name, value, attrs, renderer)
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {input_html}
        </fieldset>
        '''
        return mark_safe(html)


class TailwindDateInput(DateInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input', 'type': 'date'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())
        input_html = super().render(name, value, attrs, renderer)
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {input_html}
        </fieldset>
        '''
        return mark_safe(html)


class TailwindEmailInput(TextInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input', 'type': 'email'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())
        input_html = super().render(name, value, attrs, renderer)
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {input_html}
        </fieldset>
        '''
        return mark_safe(html)


class TailwindTextarea(Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'textarea h-24'

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())
        input_html = super().render(name, value, attrs, renderer)
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {input_html}
        </fieldset>
        '''
        return mark_safe(html)


class TailwindSelect(Select):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'select'

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())
        placeholder = attrs.get("placeholder", "Select an option")

        options_html = f'<option disabled selected>{placeholder}</option>'
        for option_value, option_label in self.choices:
            selected = "selected" if str(value) == str(option_value) else ""
            options_html += f'<option value="{option_value}" {selected}>{option_label}</option>'

        select_html = f'<select name="{name}" class="select">{options_html}</select>'
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {select_html}
        </fieldset>
        '''
        return mark_safe(html)
    


class TailwindRating(NumberInput):
    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'rating'

        verbose_name = attrs.get("verbose_name", name.replace("_", " ").title())

        ratings_html = ''
        for rating_number in range(5):
            ratings_html += f'<input type="radio" name="{name}" value="{rating_number + 1}" class="mask mask-star" aria-label="{rating_number} star" />'

        rating_html = f'<div class="rating">{ratings_html}</div>'
        
        html = f'''
        <fieldset class="fieldset">
            <legend class="fieldset-legend">{verbose_name}</legend>
            {rating_html}
        </fieldset>
        '''
        return mark_safe(html)