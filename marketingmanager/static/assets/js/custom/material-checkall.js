var checked = [];


$('.panel-body').on('click','.parent-checkbox-single', function (e) {
    e.preventDefault();
    e.stopPropagation();

    var $this = $('.parent-checkbox-single');

    if ($this.hasClass('checked')) {
        checked = [];
        $this.removeClass('checked');
        $this.find('.checkbox-custom').removeClass('checked');
        $this.find('i').removeClass('checked');
        var $table = $('.dynamicTable');
        $table.find('tbody tr td .checkbox-single').each(function (i, el) {
            $(this).removeClass('checked');
            $(this).find('label').removeClass('checked');
            $(this).find('i').removeClass('checked');
            $(this).find('input').attr('value', '');
            $('.all_id').attr('value', '');
        });
        $('.approve').attr('disabled', true);
        $('.disapprove').attr('disabled', true);
        $('.request-pickup').attr('disabled', true);

        $('.btn-tooltip').parent().attr('data-toggle','tooltip');
        $('.btn-tooltip').parent().attr('data-original-title','Select product(s) for pickup.');
    }
    else {
        $this.addClass('checked');
        $this.find('.checkbox-custom').addClass('checked');
        $this.find('i').addClass('checked');
        var $table2 = $('.dynamicTable');
        $table2.find('tbody tr td .checkbox-single').each(function (i, el) {
            if (checked.indexOf($(this).attr('data-id')) == -1) {
                checked.push($(this).attr('data-id'));
            }
            $(this).addClass('checked');
            $(this).find('label').addClass('checked');
            $(this).find('i').addClass('checked');
            $(this).find('input').attr('value', $(this).attr('data-id'));
            $('.all_id').attr('value', checked);
        });

        $('.btn-tooltip').parent().removeAttr('data-toggle');
        $('.btn-tooltip').parent().removeAttr('data-original-title');

        $('.approve').attr('disabled', false);
        $('.disapprove').attr('disabled', false);
        $('.request-pickup').attr('disabled', false);
    }

});

$('.panel-body').on('click', '.checkbox-single', function (e) {

    e.preventDefault();
    e.stopPropagation();

    if (!$(this).hasClass('parent-checkbox-single')) {
        if ($(this).hasClass('checked')) {
            var index = checked.indexOf($(this).attr('data-id'));
            if (index > -1) {
                checked.splice(index, 1);
            }
            //checked.pop($(this).attr('data-id'));
            $(this).removeClass('checked');
            $(this).find('label').removeClass('checked');
            $(this).find('i').removeClass('checked');
            $(this).find('input').attr('value', '');
            $('.all_id').attr('value', '');

            $('.btn-tooltip').parent().attr('data-toggle','tooltip');
            $('.btn-tooltip').parent().attr('data-original-title','Select product(s) for pickup.');

        }
        else {
            checked.push($(this).attr('data-id'));
            $(this).addClass('checked');
            $(this).find('label').addClass('checked');
            $(this).find('i').addClass('checked');
            $(this).find('input').attr('value', $(this).attr('data-id'));
            $('.all_id').attr('value', checked);
            $('.btn-tooltip').parent().removeAttr('data-toggle');
            $('.btn-tooltip').parent().removeAttr('data-original-title');

        }
    }
    if ($('.checkbox.checked').length > 0) {
        $('.approve').attr('disabled', false);
        $('.disapprove').attr('disabled', false);
        $('.request-pickup').attr('disabled', false);
    }
    else {
        $('.approve').attr('disabled', true);
        $('.disapprove').attr('disabled', true);
        $('.request-pickup').attr('disabled', true);
    }
});

$(window).load(function () {
    $('.checkbox').find('.checkbox-material').remove();
});
