from django.utils.safestring import mark_safe
from django.forms.widgets import TextInput, DateInput, Textarea, Select, NumberInput, PasswordInput

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
    

class TailwindPassword(PasswordInput):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'input', 'type': 'password'}
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




#     <fieldset class="fieldset w-full">
#     <legend class="fieldset-legend ">Password</legend>
#     <label class="input w-full validator">
#         <svg class="h-[1em] opacity-50" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
#             <g stroke-linejoin="round" stroke-linecap="round" stroke-width="2.5" fill="none" stroke="currentColor">
#                 <path
#                     d="M2.586 17.414A2 2 0 0 0 2 18.828V21a1 1 0 0 0 1 1h3a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h1a1 1 0 0 0 1-1v-1a1 1 0 0 1 1-1h.172a2 2 0 0 0 1.414-.586l.814-.814a6.5 6.5 0 1 0-4-4z">
#                 </path>
#                 <circle cx="16.5" cy="7.5" r=".5" fill="currentColor"></circle>
#             </g>
#         </svg>
#         <input type="password" required placeholder="Password" minlength="8" pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}"
#             title="Must be more than 8 characters, including number, lowercase letter, uppercase letter" />
#     </label>
#     <div class="validator-hint hidden">Inncorect Password</div>
# </fieldset>