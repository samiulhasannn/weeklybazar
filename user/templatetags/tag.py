from django import template
from ..models import Item

register = template.Library()


@register.simple_tag
def delete_item(itemID, user):
    print(f"{user}, hi")
    print(f"{itemID}, hi")
    # user.cart.items.remove(Item.objects.get(itemID=itemID))
