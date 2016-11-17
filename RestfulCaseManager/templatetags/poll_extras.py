from django import template

register = template.Library()

@register.filter
def lower(value):
    return value.lower()

@register.filter("case_id")
def case_id(value):
    return str(value['_id'])

@register.filter("str_batch_id")
def str_batch_id(value):
    return str(value)

#@register.filter("role_id")
#def case_id(value):
#    return str(value['_id'])

@register.filter("result")
def result(value):
    return str(value['result'])