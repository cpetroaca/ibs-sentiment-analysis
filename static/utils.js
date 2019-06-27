function buildSentimentDetails(postsList) {
  var html = "";
  for (i in postsList) 
  {
	  html = html.concat("<a class='detailsLink' href='" + postsList[i].link + "'>" + postsList[i].link + "</a><br>");
  }
  
  return html;
}