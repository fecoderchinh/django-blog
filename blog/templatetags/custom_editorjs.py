import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

register = template.Library()


def generate_paragraph(data):
    text = data.get('text').replace('&nbsp;', ' ')
    return f'<p>{text}</p>'


def generate_list(data):
    list_li = ''.join([f'<li>{item}</li>' for item in data.get('items')])
    tag = 'ol' if data.get('style') == 'ordered' else 'ul'
    return f'<{tag}>{list_li}</{tag}>'


def generate_header(data):
    text = data.get('text').replace('&nbsp;', ' ')
    level = data.get('level')
    return f'<h{level}>{text}</h{level}>'


def generate_image(data):
    url = data.get('file', {}).get('url')
    caption = data.get('caption')
    classes = []

    if data.get('stretched'):
        classes.append('stretched')
    if data.get('withBorder'):
        classes.append('withBorder')
    if data.get('withBackground'):
        classes.append('withBackground')

    classes = ' '.join(classes)

    return f'<img src="{url}" alt="{caption}" class="{classes}" />'


def generate_delimiter():
    return '<div class="delimiter"></div>'


def generate_table(data):
    rows = data.get('content', [])
    table = ''

    for row in rows:
        table += '<tr>'
        for cell in row:
            table += f'<td>{cell}</td>'
        table += '</tr>'

    return f'<table>{table}</table>'


def generate_warning(data):
    title, message = data.get('title'), data.get('message')

    if title:
        title = f'<div class="alert__title">{title}</div>'
    if message:
        message = f'<div class="alert__message">{message}</div>'

    return f'<div class="alert">{title}{message}</div>'


def generate_quote(data):
    alignment = data.get('alignment')
    caption = data.get('caption')
    text = data.get('text')

    if caption:
        caption = f'<cite>{caption}</cite>'

    classes = f'align-{alignment}' if alignment else None

    return f'<blockquote class="{classes}">{text}{caption}</blockquote>'


def generate_code(data):
    code = data.get('code')
    return f'<code class="code">{code}</code>'


def generate_raw(data):
    return data.get('html')


def generate_embed(data):
    service = data.get('service')
    caption = data.get('caption')
    embed = data.get('embed')
    iframe = f'<iframe src="{embed}" allow="autoplay" allowfullscreen="allowfullscreen"></iframe>'

    return f'<div class="embed {service}">{iframe}{caption}</div>'


def generate_link(data):
    link, meta = data.get('link'), data.get('meta')

    if not link or not meta:
        return ''

    title = meta.get('title')
    description = meta.get('description')
    image = meta.get('image')

    wrapper = f'<div class="link-block"><a href="{link}" target="_blank" rel="nofollow noopener noreferrer">'

    if image.get('url'):
        image_url = image.get('url')
        wrapper += f'<div class="link-block__image" style="background-image: url(\'{image_url}\');"></div>'

    if title:
        wrapper += f'<p class="link-block__title">{title}</p>'

    if description:
        wrapper += f'<p class="link-block__description">{description}</p>'

    wrapper += f'<p class="link-block__link">{link}</p>'
    wrapper += '</a></div>'
    return wrapper


def columns(i):
    switcher = {
        1: '',
        2: 'col-md-6',
        3: 'col-md-4',
        4: 'col-md-3',
        5: 'col-md-1-5 col-lg-1-5',
    }
    return switcher.get(i, "")


def generate_carousel(data, block_id):
    rows = data
    items = ''

    _columns = columns(int(rows['countItemEachRow']))

    if rows['config'] == 'carousel':
        items += f'<div class=row>'
        items += f'<div class="col-12">'
        items += f'<article class="gallery text-center swiper">'
        items += f'<div class="swiper-wrapper pb-3">'
        for row in rows['items']:
            items += '<figure class="swiper-slide">'
            items += '<img class="img-fluid mb-3" src=' + row['url'] + '/>'
            items += '<figurecaption>' + row['caption'] + '</figurecaption>'
            items += '</figure>'
        items += f'</div>'
        items += f'<div class="swiper-pagination"></div>'
        items += f'<div class="swiper-button-prev"></div>'
        items += f'<div class="swiper-button-next"></div>'
        # items += f'<div class="swiper-scrollbar"></div>'
        items += f'</article>'
        items += f'</div>'
        items += f'</div>'
    elif rows['config'] == 'masonry':
        items += f'<div class=row>'
        items += f'<div class=col-12>'
        items += f'<div id=data-' + block_id + '>'
        for row in rows['items']:
            items += '<figure><img class=img-fluid src=' + row[
                'url'] + '/><figurecaption>' + row['caption'] + '</figurecaption></figure>'
        items += f'</div>'
        items += f'</div>'
        items += f'</div>'
    else:
        items += f'<div class=row>'
        for row in rows['items']:
            items += f'<div class="col-6 col-sm-6 ' + _columns + '">'
            items += '<figure><img class=img-fluid src=' + row[
                'url'] + '/><figurecaption>' + row['caption'] + '</figurecaption></figure>'
            items += f'</div>'
        items += f'</div>'

    return items


def include_macy_js(data):
    rows = data
    items = ''
    if rows['config'] == 'masonry':
        items += f'<script src="https://cdn.jsdelivr.net/npm/macy@2"></script>'
    return items


def include_macy_config_js(data, element_id):
    rows = data
    items = ''
    if rows['config'] == 'masonry':
        items += """
            <script>
                let _itemsNumber = %s;
                var masonry = new Macy({
                    container: '%s',
                    trueOrder: false,
                    waitForImages: false,
                    useOwnImageLoader: false,
                    debug: true,
                    mobileFirst: true,
                    columns: 1,
                    margin: 15,
                    breakAt: {
                        1024: _itemsNumber,
                        768: _itemsNumber > 1 ? 3 : 1,
                        320: _itemsNumber > 1 ? 2 : 1,
                    },
                });
            </script>
        """ % (rows['countItemEachRow'], '#data-' + element_id)
    return items


def include_carousel_scripts(data):
    rows = data
    items = ''
    if rows['config'] == 'carousel':
        items += """
            <script type="module">
                import Swiper from 'https://unpkg.com/swiper@8/swiper-bundle.esm.browser.min.js'
                const _itemsNumber = %s;
                const swiper = new Swiper('.swiper', {
                  // Optional parameters
                  direction: 'horizontal',
                  loop: true,
                  slidesPerView: 1,
                  spaceBetween: 10,
                  breakpoints: {
                    // when window width is >= 640px
                    640: {
                      slidesPerView: _itemsNumber >= 2 ? 2 : 1,
                    },
                    // when window width is >= 768px
                    768: {
                      slidesPerView: _itemsNumber >= 3 ? 3 : 1,
                    },
                    // when window width is >= 1024px
                    1024: {
                      slidesPerView: _itemsNumber > 1 ? _itemsNumber : 1,
                    },
                  },
                
                  // If we need pagination
                  pagination: {
                    el: '.swiper-pagination',
                    clickable: true,
                  },
                
                  // Navigation arrows
                  navigation: {
                    nextEl: '.swiper-button-next',
                    prevEl: '.swiper-button-prev',
                  },
                
                  // And if we need scrollbar
                  scrollbar: {
                    el: '.swiper-scrollbar',
                    hide: true,
                  },
                });
            </script>
        """ % (rows['countItemEachRow'])
    return items


def include_carousel_stylesheets(data):
    rows = data
    items = ''
    if rows['config'] == 'carousel':
        items += f'<link rel="stylesheet" href="https://unpkg.com/swiper@8/swiper-bundle.min.css"/>'
    return items


@register.filter(is_safe=True)
def editorjs(value):
    if not value or value == 'null':
        return ""

    if not isinstance(value, dict):
        try:
            value = json.loads(value)
        except ValueError:
            return value
        except TypeError:
            return value

    html_list = []
    for item in value['blocks']:

        type, data, id = item.get('type'), item.get('data'), item.get('id')
        type = type.lower()

        if type == 'paragraph':
            html_list.append(generate_paragraph(data))
        elif type == 'header':
            html_list.append(generate_header(data))
        elif type == 'list':
            html_list.append(generate_list(data))
        elif type == 'image':
            html_list.append(generate_image(data))
        elif type == 'delimiter':
            html_list.append(generate_delimiter())
        elif type == 'warning':
            html_list.append(generate_warning(data))
        elif type == 'table':
            html_list.append(generate_table(data))
        elif type == 'code':
            html_list.append(generate_code(data))
        elif type == 'raw':
            html_list.append(generate_raw(data))
        elif type == 'embed':
            html_list.append(generate_embed(data))
        elif type == 'quote':
            html_list.append(generate_quote(data))
        elif type == 'linktool':
            html_list.append(generate_link(data))
        elif type == 'carousel':
            html_list.append(generate_carousel(data, id))

    return mark_safe(''.join(html_list))


@register.filter(is_safe=True)
def include_js(value):
    if not value or value == 'null':
        return ""

    if not isinstance(value, dict):
        try:
            value = json.loads(value)
        except ValueError:
            return value
        except TypeError:
            return value

    html_list = []
    flag = False

    for item in value['blocks']:

        type, data, id = item.get('type'), item.get('data'), item.get('id')
        type = type.lower()

        if type == 'carousel':
            html_list.append(include_carousel_scripts(data))
            if flag is False:
                html_list.append(include_macy_js(data))
                flag = True
            html_list.append(include_macy_config_js(data, id))

    return mark_safe(''.join(html_list))


@register.filter(is_safe=True)
def include_css(value):
    if not value or value == 'null':
        return ""

    if not isinstance(value, dict):
        try:
            value = json.loads(value)
        except ValueError:
            return value
        except TypeError:
            return value

    html_list = []
    for item in value['blocks']:

        type, data = item.get('type'), item.get('data')
        type = type.lower()

        if type == 'carousel':
            html_list.append(include_carousel_stylesheets(data))

    return mark_safe(''.join(html_list))


@register.simple_tag
def check_category(value):
    if str(value) == 'blog.Category.None':
        return _('Uncategorized')
    else:
        return False
