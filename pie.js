let title = `Movie Rating in Apple TV Plus`
let title2 = `TV Ratings of TV Shows in Apple TV Plus`

var data = [{
    values: [16, 4, 13, 20, 11],
    labels: ['G',"PG", "PG-13", "R", "Unrated"],
    type: 'pie'
  }];
  
  var layout = {
    title: title,
    height: 400,
    width: 500
  };
  
  Plotly.newPlot('myPie', data, layout);


var data2 = [{
    values: [12, 2, 16, 11, 14, 51],
    labels: ['TV-Y','TV-Y7(Directed for older childern)', 'TV-G', 'TV-PG', 'TV-14', 'TV-MA'],
    type: 'pie'
  }];
  
  var layout2 = {
    title: title2,
    height: 400,
    width: 500
  };
  
  Plotly.newPlot('myPie2', data2, layout2);