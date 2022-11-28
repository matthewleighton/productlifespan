function toggle_product_form() {
	if (product_form.style.display == "flex") {
		hide_product_form();
	} else {
		show_product_form();
	}
}

function show_product_form() {
	product_detail_middle.style.display = "none";
	product_form.style.display = "flex";
	product_edit_button.innerHTML = "Details";
}

function hide_product_form() {
	product_detail_middle.style.display = "flex";
	product_form.style.display = "none";
	product_edit_button.innerHTML = product_edit_button_original_text;
}

var product_detail_middle = document.getElementById("product-detail-middle");
var product_form = document.getElementById("product-form");

var product_edit_button = document.getElementById("product-edit-toggle-button");
var product_edit_button_original_text = product_edit_button.innerHTML;