function toggle_retired_products() {
	if (document.getElementsByClassName('show-retired-products-checkbox')[0].checked) {
		display_style = 'table-row'
	} else {
		display_style = 'none'
	}

	retired_products = document.getElementsByClassName('retired');

	for (var i=0;i<retired_products.length;i+=1){
		retired_products[i].style.display = display_style;
	}
}