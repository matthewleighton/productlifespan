// Hide/show the retired products in the Product Table.
function toggle_retired_products() {
	if (document.getElementsByClassName('show-retired-products-checkbox')[0].checked) {
		display_style = 'table-row'
	} else {
		display_style = 'none'
	}

	elements = document.getElementsByClassName('retired');

	for (var i=0;i<elements.length;i+=1){

		if (elements[i].tagName == 'TR') {
			elements[i].style.display = display_style;
		}
	}
}

toggle_retired_products();