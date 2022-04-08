jQuery(function($) {
    $('div.inline-group').sortable({
        /*containment: 'parent',
        zindex: 10, */
        items: 'tr.dynamic-item_set',
        handle: 'td',
    });
    $('div.tabular.inline-related tr').css('cursor', 'move');
    // $('tr.dynamic-item_set td').find('input[id$=order]').parent('td').hide();
    $('th.column-order').hide();
    $('td.field-order').hide();
    $('#menu_form').submit(function() {
        $('tr.dynamic-item_set').each(function(i) {
            if ($(this).find('input[id$=name]').val()) {
                $(this).find('input[id$=order]').val(i+1);
            }
        });
    });
});