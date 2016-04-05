$(function() {
  var windowWidth, wrapperWidth, svgWidth, svgHeight, responseData;
  var margin = {top: 60, right: 75, bottom: 75, left: 75};
  var selectedMonth = 'January'; // make this the current month

  d3.json('/data', function(data) {
    responseData = data;
    makeGraph();
  });

  $(window).resize(function() {
    makeGraph();
  });

  $('button').on('click', function() {
    selectedMonth = $(this).text();
    $('.month').empty();
    makeGraph()
  })

  function makeGraph() {
    $('svg').empty();
    setSizes();
    var height = svgHeight - margin.top - margin.bottom;
    var width = svgWidth - margin.left - margin.right;
    var monthData = responseData[selectedMonth]
    var dataRanges = getDataRanges(monthData);
    var dataScales = getDataScales(dataRanges, width, height)    
    
    var svgSelection = d3.select('svg')
      .attr('height', svgHeight)
      .attr('width', svgWidth)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

    var dataPoints = svgSelection
      .selectAll('circle')
      .data(monthData)
      .enter()
      .append('circle');

    var dataAttributes = dataPoints
      .attr('cx', function (d) { return dataScales.year(getYear(d.date)); })
      .attr('cy', function(d) { return dataScales.temp(d.temp); })
      .attr('r', 10)
      .attr('fill', 'limegreen');

    var text = svgSelection
      .selectAll('text')
      .data(monthData)
      .enter()
      .append('text');

    var dataLabels = text
      .attr('x', function(d) { return dataScales.year(getYear(d.date)) + 10; })
      .attr('y', function(d) { return dataScales.temp(d.temp) - 10; })
      .text( function (d) { return getDayMonth(d.date) + ', ' + d.temp + '°F'; })
      .attr('font-family', 'helvetica')
      .attr('font-size', '16px')
      .attr('fill', function(d) { return d.color });

    var yearAxis = d3.svg.axis()
      .scale(dataScales.year)
      .orient('bottom')
      .ticks(8)
      .tickFormat(d3.format('d'));

    var tempAxis = d3.svg.axis()
      .scale(dataScales.temp)
      .orient('left')
      .ticks(5);

    svgSelection.append('g')
      .attr('class', 'axis')
      .attr('transform', 'translate(0, ' + height + ')')
      .call(yearAxis);

    svgSelection.append('g')
      .attr('class', 'axis')
      .call(tempAxis);

    svgSelection.append('text') // Add year-axis label, similar to title
      .attr('class', 'label')
      .attr('x', (width/2))
      .attr('y', height + margin.bottom/2)
      .attr('dy', '16')
      .attr('text-anchor', 'middle')  
      .style('font-size', '16px') 
      .text(selectedMonth + ' Meetings');

    svgSelection.append('text') // Add temp-axis label, similar to above, but with transform
      .attr('class', 'label')
      .attr('transform', 'rotate(-90)')
      .attr('y', 0 - margin.left/2)
      .attr('x', 0 - height/2)
      .attr('dy', '-8')
      .attr('text-anchor', 'middle')  
      .style('font-size', '16px') 
      .text('Temperatures');

    // svgSelection.append('text') // Graph title
    //   .attr('class', 'month')
    //   .attr('x', (width/2))
    //   .attr('y', 0 - (margin.top/2))
    //   .attr('text-anchor', 'middle')
    //   .text(selectedMonth);
  }

  function getDataScales(dataRanges, width, height) {
    var tempScale = d3.scale.linear() 
      .domain([dataRanges.minTemp, dataRanges.maxTemp]) // Define the temp domain by the max and min temp values
      .range([height, 0]);
    var yearScale = d3.scale.linear()
      .domain([dataRanges.minYear, dataRanges.maxYear]) // Define the year domain by the max and min year values
      .range([0, width]);
    return { temp: tempScale, year: yearScale };
  }

  function getDataRanges(monthData) {
    var maxTemp = d3.max(monthData, function(d) { return parseInt(d.temp); });
    var minTemp = d3.min(monthData, function(d) { return parseInt(d.temp); });
    var maxYear = d3.max(monthData, function(d) { return getYear(d.date); });
    var minYear = d3.min(monthData, function(d) { return getYear(d.date); });
    return { maxTemp: maxTemp, minTemp: minTemp, maxYear: maxYear, minYear: minYear };
  }

  function getYear(date) {
    return parseInt(date.slice(-4));
  }

  function getDayMonth(date) {
    return date.slice(0, 5);
  }

  function setSizes() {
    // windowWidth = $(window).width();
    wrapperWidth = $('.wrapper').width();
    svgWidth = wrapperWidth;
    svgHeight = svgWidth * 5/8;
  }
});