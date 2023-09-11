//solução para model do listSemana, para conseguir passar o dado dele para o model sem muito trabalho.
$(function() {
    $('.fa-circle-exclamation').click(function(){
        var my_id = $(this).data('id')
        console.log(my_id)
        $('#semana_hidden').val(my_id);
    });
});