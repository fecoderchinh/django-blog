jQuery(function($) {
    $('.gallery-item a').each(function(ele) {
        // $(this).attr('data-change', $(this).attr('href'))
        $(this).attr('href', 'javascript:void(0)');
    })

    $('.addlink').attr('href', 'javascript:void(0)');
    $('.addlink ').click(function () {

    $header = $(this);
    //getting the next element
    $content = $('.gallery-accordion');
    //open up the content needed - toggle the slide- if visible, slide up, if not slidedown.
    $content.slideToggle(500, function () {
        //execute this after slideToggle is done
        //change text of header based on visibility of content div
        // $header.text(function () {
        //     //change text based on condition
        //     return $content.is(":visible") ? "Collapse" : "Expand";
        // });
    });

});

    $('.result_list--body').find('.gallery-item input[type=checkbox][name=_selected_action]').each(function (){
        if($(this).prop('checked')) {
            $(this).parent('.gallery-item').addClass('selected')
        }
    })

    $('#action-toggle, .column-image_tag').click(function (e){
        e.stopPropagation();
        if($('.result_list--body').find('.gallery-item input[type=checkbox][name=_selected_action]').is(':checked')) {
            $('#action-toggle').prop('checked', false);
            $('.result_list--body').find('.gallery-item input[type=checkbox][name=_selected_action]').prop('checked', false);
            $('.result_list--body').find('.gallery-item').removeClass('selected');
        } else {
            $('#action-toggle').prop('checked', true);
            $('.result_list--body').find('.gallery-item input[type=checkbox][name=_selected_action]').prop('checked', true);
            $('.result_list--body').find('.gallery-item').addClass('selected');
        }
    });

    $('.gallery-item').click(function (e) {
        e.stopPropagation();
        $(this).toggleClass('selected')
        $(this).find('input[name=_selected_action]').prop('checked', !!$(this).hasClass('selected'))
    })

});