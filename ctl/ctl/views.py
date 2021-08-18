from django.shortcuts import render

def homepage(request):
    response = render(request, 'homepage.html')
    return response


style_to_outfits = None
data_path = '../data_outfits_generated'


def init():
    global style_to_outfits
    if style_to_outfits is None:
        import json
        with open(data_path + '/top_k_reults.json') as f: # json path with outfits
            style_to_outfits = json.load(f)
    return style_to_outfits


def anchor_categories(request):
    style_to_outfits_dict = init()
    anchor_cat = set()
    for style in style_to_outfits_dict.keys():
        for category in style_to_outfits_dict[style].keys():
            anchor_cat.add(category)

    context = {
        'categories': anchor_cat
    }

    response = render(request, 'categories.html', context)
    return response


def anchor_items(request):
    cat = request.GET.get('cat', '')
    style_to_outfits_dict = init()
    anchor_items = set()
    for style in style_to_outfits_dict.keys():
        if cat in style_to_outfits_dict[style]:
            for anchor_item in style_to_outfits_dict[style][cat]:
                anchor_items.add(anchor_item)

    context = {
        'anchor_items': anchor_items,
        'cat': cat
    }

    response = render(request, 'anchoritems.html', context)
    return response


def outfits(request):
    cat = request.GET.get('cat', '')
    item = request.GET.get('item', '')
    style_to_outfits_dict = init()
    resp_outfits = {}
    for style in style_to_outfits_dict.keys():
        if cat in style_to_outfits_dict[style] and item in style_to_outfits_dict[style][cat]:
            resp_outfits[style] = style_to_outfits_dict[style][cat][item]
            resp_outfits[style]['size'] = range(len(resp_outfits[style]['outfits'][0]['outfit']))
            master_template = resp_outfits[style]['masterTemplate']
            resp_outfits[style]['template'] = [master_template['parentcat']]
            resp_outfits[style]['template'].extend(master_template['impcat'][0])
            resp_outfits[style]['template'].extend(master_template['optionalcat'])

    context = {
        'cat': cat,
        'anchor': item,
        'outfits': resp_outfits
    }

    response = render(request, 'outfit.html', context)
    return response
