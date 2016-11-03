//var csrftoken = $.cookie('csrftoken');
//function csrfSafeMethod(method) {
//  // these HTTP methods do not require CSRF protection
//  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));  
//} 
//
//$.ajaxSetup({
//  beforeSend: function(xhr, settings) {
//    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {        
//      xhr.setRequestHeader("X-CSRFToken", csrftoken);      
//    }    }
//});

var get_color = d3.scaleLinear().domain([0, 100])
      .interpolate(d3.interpolateHcl)
      .range([d3.rgb("#db1c0a"), d3.rgb('#33cc33')]);

var sentiment_chart = create_sentiment_chart();

$('#sentiment-text input').keydown(function (event) {
  var keyCode = (event.keyCode ? event.keyCode : event.which);
  if(keyCode == 13)  // the enter key code
  {
    $('#sentiment-text button').trigger('click');
    return false;  
  }
});


$("#sentiment-text button").click(function(e){
  var url = $('input[name=url]').val()
  var token = $('input[name=csrfmiddlewaretoken]').val()
  var text = $('input[name=text]').val()
  $('input[name=text]').val('')
  $.post(url, {
    'csrfmiddlewaretoken': token,
    'text': text
  }, function(data){
//    sentiment_chart(data['sentiment'])
//    console.log(data)
    sentiment_chart(Math.round(data[data.length-1]['score']));
    $('#graph g').remove()
    create_sentiment_graph(data)
  })
})

function create_sentiment_chart(score=0){
  var margin = {top: 50, right: 10, bottom: 40, left: 10};
  var width = $('.container').width() - margin.left - margin.right;
  var height = 150 - margin.top - margin.bottom;

  var x = d3.scaleLinear()
    .range([0, width])
    .domain([0, 100]);

  var xAxis = d3.axisBottom()
    .scale(x);

  var svg = d3.select("#chart")
  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + "," + margin.top +")");

  g.append('g')
    .attr('transform', 'translate(0,' + (height + 2) +')')
    .call(xAxis)
  
  var text_container = g.append('g')
    .attr("transform", "translate(0," + (height + margin.bottom/2) +")")
  
  text_container.append('text')
    .attr("transform", "translate("+ width/2 +",0)")
    .attr("dy", "1em")
    .attr("text-anchor", "middle")
    .text("Neutral")
  
  text_container.append('text')
    .attr("transform", "translate("+ width +",0)")
    .attr("dy", "1em")
    .attr("text-anchor", "end")
    .text("Positive")
  text_container.append('text')
    .attr("dy", "1em")
    .attr("text-anchor", "begin")
    .text("Negative")
  

  var container = g.selectAll(".bar")
    .data([score]).enter()
    .append("g")
    .attr("class", "bar")

  bar = container.append("rect")

  var text = container.append('text')
    .attr("x", 0)
    .attr("y", height/2)
    .attr("text-anchor", "begin")

  bar.attr("x", 0)
    .attr("y", 0)
    .attr("height", height)
    .attr('width', 0)

  return function(new_score){
    bar.data([score]).transition()
      .duration(500)
      .attr("width", x(new_score))
      .attr("fill", get_color(new_score));
    text.text(new_score)
      .transition()
      .duration(500)
      .attr('x', x(new_score))
      .attr('fill', get_color(new_score))

  }

}

function create_sentiment_graph(data){
  var margin = {top: 50, right: 10, bottom: 40, left: 60};
  var width = $('.container').width() - margin.left - margin.right;
  var height = 400 - margin.top - margin.bottom;
  
  
  var y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, 100]);
  
  var x = d3.scaleBand().rangeRound([0, width]).padding(0.1)
    .domain(d3.range(data.length));
  
  var yAxis = d3.axisLeft(y);
  
  var xAxis = d3.axisBottom(x)
    .tickFormat(function(d){return data[d]['text']});
  
  var svg = d3.select("#graph")
  var g = svg.append('g')
    .attr('transform', 'translate(' + margin.left + "," + margin.top +")");
  
  g.append('g')
    .attr("class", "axis axis--y")
    .call(yAxis)
  
  g.append('text')
    .attr("transform", "translate("+ (-margin.left/2) + "," + height/2 +")rotate(-90)")
    .attr('text-anchor', 'middle')
    .text("Sentiment");
  
  g.append('g')
    .attr("class", "axis axis--x")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis);
  
  g.selectAll(".bar")
    .data(data)
    .enter().append("circle")
    .attr("class", "dot")
    .attr("cx", function(d, i){ return x(i) + x.bandwidth() /2;})
    .attr("cy", function(d){ return y(d['score']);})
    .attr("r", Math.min(5, x.bandwidth()))
    .attr("fill", function(d){ return get_color(d['score'])});
  
  var line = d3.line()
    .x(function(d, i){return x(i) + x.bandwidth()/2})
    .y(function(d){return y(d['score'])});
  
  g.append("path")
    .datum(data)
    .attr('class', 'line')
    .attr("d", line)
    .attr('stroke', get_color(data[data.length-1]['score']))
//  console.log(data)
  
}

//function get_color(score){
//  if (score >= 80){
//    return '#33cc33';
//  }
//  else if (score >= 60) {
//    return '#1ac6ff';
//  }
//  else if (score >= 40){
//    return '#b3ecff';
//  }
//  else if(score >=20){
//    return '#faa59e';
//  }
//  else {
//    return '#db1c0a';
//  }
//}



