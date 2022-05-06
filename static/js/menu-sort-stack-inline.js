jQuery(function($) {
    $('div.inline-group').accordion({
        header: 'h3',
        active: false,
        collapsible: true,
    }).sortable({
        /*containment: 'parent',
        zindex: 10, */
        items: 'div.inline-related',
        handle: 'h3:first',
        connectWith: '.connected, .inline-group',
        placeholder: "ui-state-highlight",
        stop: function( event, ui ) {
          // IE doesn't register the blur when sorting
          // so trigger focusout handlers to remove .ui-state-focus
          ui.item.children( "h3" ).triggerHandler( "focusout" );

          // Refresh accordion to handle new order
          $( this ).accordion( "refresh" );
        },
        update: function() {

            $( this ).accordion( "refresh" );

            $(this).find('div.inline-related').each(function(i) {
                if ($(this).find('input[id$=name]').val()) {
                    $(this).find('input[id$=order]').val(i+1);
                    $(this).find('.sub-group').attr('data-order', (i+1));
                }
                var parent = $(this).parent().data('parent');
                if(parent === undefined) {
                    $(this).find('> fieldset.module select[id$=parent]').prop('selectedIndex', 0);
                } else {
                    $(this).find('select[id$=parent]').val(parent);
                }
            });
        }
    }).disableSelection();
    $('div.inline-related').each(function (){
        if($(this).find('input[type=hidden][id$=id]').val()) {
            if($(this).find('select[id$=parent]').val()) $(this).attr('data-root', $(this).find('select[id$=parent]').val());
            $(this).append(`<div class="sub-group connected" data-parent=${$(this).find('input[type=hidden][id$=id]').val()} data-order=${$(this).find('input[id$=order]').val()}></div>`);
        }
    });
    $('div.sub-group').sortable({
        items: 'div.inline-related',
        handle: 'h3:first',
        connectWith: '.connected, .inline-group',
        placeholder: "ui-state-highlight",
        update: function (){
            $(this).find('div.inline-related').each(function(i) {
                $(this).find('input[id$=order]').val($(this).parent().data('order') + '.'+(i+1));
                $(this).find('.sub-group').attr('data-order', $(this).find('input[id$=order]').val());
                var parent = $(this).parent().data('parent');
                if(parent) {
                    $(this).find('select[id$=parent]').val(parent);
                }
            });
        },
    }).disableSelection();
    $('div.inline-related h3').css('cursor', 'move');
    $('.field-order, .field-parent').hide();
    $('fieldset.module').css({'height': 'auto'});
    $('.inline-related').each(function (){
        $(this).appendTo($('.inline-group').find(`.sub-group[data-parent=${$(this).data('root')}]`));
    });
    $('.inline-related > h3 .delete').click(function (e){
        e.stopPropagation();
        if($(this).find('input[type=checkbox]').is(':checked')) {
            $(this).find('input[type=checkbox]').prop('checked', false);
        } else {
            $(this).find('input[type=checkbox]').prop('checked', true);
        }
    });
});