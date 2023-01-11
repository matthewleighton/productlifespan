function target_end_date_changed() {
	target_end_date = new Date(target_end_date_field.value);
	purchase_date = new Date(purchase_date_field.value);

	time_delta = target_end_date - purchase_date;
	target_age_days = Math.ceil(time_delta / (1000 * 60 * 60 * 24));

	update_target_price_amount(target_age_days);
	update_target_age(target_age_days);

	last_edited_lifespan_field = 'target_end_date';
}

function target_age_changed() {
	target_age_years = target_age_field.value;
	target_age_days = 365.25 * target_age_years

	update_target_price_amount(target_age_days)
	update_target_end_date(target_age_days)

	last_edited_lifespan_field = 'target_age'
}

function target_price_amount_changed() {
	target_price_amount = target_price_amount_field.value;

	buy_price = buy_price_field.value;
	time_units = buy_price / target_price_amount;

	target_price_period_days = target_price_period_field.value;

	target_age_days = time_units * target_price_period_days;

	update_target_end_date(target_age_days);
	update_target_age(target_age_days);

	last_edited_lifespan_field = 'target_price_amount';
}

function target_price_period_changed() {
	target_price_amount_changed();
}


function update_lifespan_fields() {
	switch(last_edited_lifespan_field) {
		case 'target_end_date':
			target_end_date_changed(target_end_date_field);
			break
		case 'target_age':
			target_age_changed(target_age_field);
			break;
		case 'target_price_amount':
			target_price_amount_changed(target_price_amount_field);
			break
	}
}

function update_target_price_amount(target_age_days) {
	target_price_period_days = target_price_period_field.value;
	divisor = target_age_days / target_price_period_days;

	buy_price = buy_price_field.value;
	new_target_price_amount = (buy_price / divisor).toFixed(2);

	target_price_amount_field.value = new_target_price_amount;
}


function update_target_age(target_age_days) {
	target_age_years = (target_age_days / 365.25).toFixed(2);

	target_age_field.value = target_age_years;
}


function update_target_end_date(target_age_days) {
	var buy_date = new Date(purchase_date_field.value);

	var new_target_end_date = new Date(buy_date);
	new_target_end_date.setDate(buy_date.getDate() + target_age_days);

	new_end_date_string = new_target_end_date.toISOString().split('T')[0];

	target_end_date_field.value = new_end_date_string;
}

function initialize_fields() {
	target_end_date_changed();
}





var buy_price_field = document.getElementsByName('price')[0];
var purchase_date_field = document.getElementsByName('purchase_date')[0];

var target_end_date_field = document.getElementsByName('target_end_date')[0];
var target_age_field = document.getElementsByName('target_age')[0];
var target_price_amount_field = document.getElementsByName('target_price_amount')[0];
var target_price_period_field = document.getElementsByName('target_price_period')[0];


buy_price_field.addEventListener('change', update_lifespan_fields);
purchase_date_field.addEventListener('change', update_lifespan_fields);

// We keep track of which lifespan field was last edited.
// This is so that, when either the product price or purchase date is edited,
// the last_edited_lifespan_field will be held as a constant, since we assume it's the
// one which the user actually cares about - the other fields will change to fit
// with the new price/purchase date.
var last_edited_lifespan_field = 'target_end_date';


var delete_confirmation = function(e) {
	if (!confirm('Are you sure you want to delete this product?')) e.preventDefault();
}
document.getElementById('product-delete-button').addEventListener('click', delete_confirmation, false);



initialize_fields();