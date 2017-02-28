
$( window ).load(function(){

	$('.checkbox').find('.checkbox-material').remove();

	$('.panel-ctrls-center>div').removeClass('form-group');

	$('.dataTables_length>.panel-ctrls-center').text().replace(' records per page','');

	$('.panel-ctrls>.col-md-12 + i').remove();

	// $('#product-grid_filter').next().remove();

	// $('#product-grid_filter').remove();

});