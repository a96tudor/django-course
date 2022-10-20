from django.core.paginator import Paginator


def get_paginator_for_dataset(dataset, request, per_page=3):

    paginator = Paginator(dataset, per_page=per_page)

    page = 1
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    if page > paginator.num_pages:
        page = paginator.num_pages

    objects_for_page = paginator.page(page)

    left_index = max(1, page - 4)
    right_index = min(page + 4, paginator.num_pages)

    return objects_for_page, paginator, range(left_index, right_index + 1)
