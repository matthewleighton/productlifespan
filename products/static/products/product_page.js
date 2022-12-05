function toggle_product_form() {
	if (product_form.style.display == "flex") {
		hide_product_form();
	} else {
		show_product_form();
	}
}

function show_product_form() {
	retirement_form.style.display ="none";
	product_detail_middle.style.display = "none";
	product_form.style.display = "flex";
	product_edit_button.innerHTML = "Details";
}

function hide_product_form() {
	product_detail_middle.style.display = "flex";
	product_form.style.display = "none";
	product_edit_button.innerHTML = product_edit_button_original_text;
}

function display_retirement_form() {
	retirement_form.style.display ="flex";
	product_detail_middle.style.display = "none";
	product_form.style.display = "none";
	product_edit_button.innerHTML = product_edit_button_original_text;
}

function hide_retirement_form() {
	retirement_form.style.display ="none";
	product_detail_middle.style.display = "flex";
	product_form.style.display = "none";
}


function undo_retirement() {
	retirement_date_field.value = '';
	retirement_form.submit();
}






var product_detail_middle = document.getElementById("product-detail-middle");
var product_form = document.getElementById("product-form");

var product_edit_button = document.getElementById("product-edit-toggle-button");
var product_edit_button_original_text = product_edit_button.innerHTML;

var retirement_form = document.getElementById('product-retirement-form');
var retirement_date_field = document.getElementsByName('retirement_date')[0]; 