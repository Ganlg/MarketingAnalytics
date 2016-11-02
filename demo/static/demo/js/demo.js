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

var sentiment_chart = create_sentiment_chart();

$("#sentiment-text button").click(function(e){
  var url = $('input[name=url]').val()
  var token = $('input[name=csrfmiddlewaretoken]').val()
  var text = $('input[name=text]').val()
//  $('input[name=text]').val('')
  $.post(url, {
    'csrfmiddlewaretoken': token,
    'text': text
  }, function(data){
    sentiment_chart(data['sentiment'])
  })
})

function create_sentiment_chart(score=0){
  var margin = {top: 50, right: 10, bottom: 40, left: 10};
  var width = $('.container').width() - margin.left - margin.right;
  var height = 150 - margin.top - margin.bottom;

  console.log(width)
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
      .attr('x', x(new_score));

  }

  function get_color(score){
    if (score > 100/3*2){
      return '#50f442';
    }
    else if(score > 100/3){
      return '#07c7f2';
    }
    else {
      return '#f4210e'
    }
  }

}

