const DUMMY_DATA = [
	{'x': 0, 'y': 100/1, 'date': '1st January 2020'},
	{'x': 1, 'y': 100/2, 'date': '2nd January 2020'},
	{'x': 2, 'y': 100/3, 'date': '3d January 2020'},
	{'x': 3, 'y': 100/4, 'date': '4th January 2020'},

]

const DAYS_IN_MONTH = 365.25 / 12

// https://stackoverflow.com/a/563442/4897798
Date.prototype.addDays = function(days) {
	var date = new Date(this.valueOf());
	date.setDate(date.getDate() + days);
	return date;
}

function get_graph_data(day_increment) {
	var raw_graph_data = JSON.parse(document.getElementById('graph-data').textContent);

	var graph_data = []

	purchase_date   = new Date(raw_graph_data['purchase_date']);
	target_end_date = new Date(raw_graph_data['target_end_date']);
	price = raw_graph_data['price'];

	total_lifespan_days = (target_end_date - purchase_date) / (1000 * 3600 * 24);

	for (let d = 1; d <= total_lifespan_days; d+=day_increment) {
		daily_price = (price / d) * DAYS_IN_MONTH
		date = purchase_date.addDays(d-1);

		graph_data.push({
			'daily_price': daily_price,
			'date': date,
			'day_number': d
		});
	}

	return graph_data;
}

function get_current_age_in_days() {
	purchase_date = new Date(raw_graph_data['purchase_date']);
	today = new Date()

	return parseInt((today - purchase_date) / (1000 * 3600 * 24));
	// return 189;
}

const day_increment = 1;

const graph_data = get_graph_data(day_increment);

var container_height = 300;
// var container_width = document.getElementById('product-detail-graph').offsetWidth;


const raw_graph_data = JSON.parse(document.getElementById('graph-data').textContent);
const purchase_price = raw_graph_data['price'];

var current_age_in_days = get_current_age_in_days();
var x_start = get_current_age_in_days - 30*6
var x_end = current_age_in_days + 30*6

x_domain = [...Array(x_end).keys()];


const xScale = d3
	.scaleBand()
	// .domain(graph_data.map((dataPoint) => dataPoint.day_number))
	.domain(x_domain)
	.rangeRound([0, graph_data.length])
	.padding(0);

console.log(graph_data.length)




// TODO-NEXT: Figure out how to get the scalling correct.
// const yScale = d3.scaleSymlog().domain([0, purchase_price]).range([container_height, 0]);
const yScale = d3.scaleLinear().domain([0, purchase_price*DAYS_IN_MONTH]).range([container_height, 0]);

// const x_axis = d3.axisBottom().scale(xScale);
const y_axis = d3.axisLeft().scale(yScale);

const x_axis = d3.axisBottom()
				.scale(xScale)
				// .orient("top")
				.tickFormat((interval,i) => {
				  return i%30 !== 0 ? " ": interval;
				})
				// .innerTickSize(-container_height)
				// .outerTickSize(0)
				// .ticks(d3.time.month.utc, 1);



const svg = d3.select("#product-detail-graph")
	.classed('container', true)
	.style('border', '1px solid red')
	.style('height',  container_height +'px');

svg.selectAll('.bar')
	.data(graph_data)
	.enter()
	.append('rect')
	.classed('bar', true)
	.style('fill', 'blue')
	.attr('width', xScale.bandwidth())
	.attr('height', (data) => container_height - yScale(data.daily_price))
	.attr('x', data => xScale(data.day_number))
	.attr('y', data => yScale(data.daily_price));

// svg.append('path')
// 	.datum(graph_data)
// 	.attr('fill', 'none')
// 	.attr('stroke', 'steelblue')
// 	.attr('stroke-width', 2)
// 	.attr('d', d3.line()
// 		.x(d => xScale(d.day_number))
// 		.y(d => yScale(d.daily_price)));

// svg.append('g')
// 	.call(x_axis)
// 	.attr("transform", "translate(0, " + (container_height - 30) + ")");

// svg.append('g')
// 	.call(y_axis)
// 	.attr("transform", "translate(30, 0)");