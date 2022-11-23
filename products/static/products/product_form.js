function target_end_date_changed(field) {
	value = field.value;
	console.log(value);
}

function target_age_changed(field) {
	target_age_years = field.value;
	target_age_days = 365.25 * target_age_years

	update_target_price(target_age_days)
	update_target_end_date(target_age_days)

}

function target_price_amount_changed(field) {

}

function target_price_period_changed(field) {

}


function update_lifespan_fields() {
	console.log('update_lifespan_fields')
}

function update_target_price(target_age_days) {

}

function update_target_end_date(target_age_days) {
	var buy_date = new Date(purchase_date_field.value);

	var new_target_end_date = new Date(buy_date);
	new_target_end_date.setDate(buy_date.getDate() + target_age_days);

	new_end_date_string = new_target_end_date.toISOString().split('T')[0];

	target_end_date_field.value = new_end_date_string;
}


var price_field = document.getElementsByName('price')[0];
var purchase_date_field = document.getElementsByName('purchase_date')[0];

var target_end_date_field = document.getElementsByName('target_end_date')[0];

price_field.addEventListener('change', update_lifespan_fields);
purchase_date_field.addEventListener('change', update_lifespan_fields);

