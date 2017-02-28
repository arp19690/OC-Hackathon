var list = [];

var fields = [];

var required = document.querySelectorAll('.required');

$('.required').on('change',function(){

    if(fields.indexOf($(this).attr('name')) == -1){

        fields.push($(this).attr('name'));

        if($(this).val() !== ''){
            list.push(1);
        }
        else{
            list.pop();
        }
    }
    if($(this).val() !== '' && required.length == list.length){
        $('.submit').removeClass('disabled').attr('disabled',false);
    }
    else{
        $('.submit').addClass('disabled').attr('disabled',true);
    }
});

