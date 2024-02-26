async function upvote(item_id,session_id,csrf_t) 
{
  var item = item_id;
  var session = session_id;
  var csrf = csrf_t;

  const addCSS = s => document.head.appendChild(document.createElement("style")).innerHTML = s;
  addCSS("#id-"+item+" { background-Color: #FADF33 !important; }");
  addCSS("#id-"+item+" { Color: #353238 !important; }");
  addCSS("#id-"+item+" { border: 1px solid #FADF33 !important; }");
  addCSS("#id-"+item+"::after { content:\x22d!\x22 }");
  
  const vote = new Request(
    "/vote/"+item+"/"+session+"/",
    {
        method: 'POST',
        headers: {'X-CSRFToken': csrf},
        mode: 'same-origin' // Do not send CSRF token to another domain.
    }
  )
  fetch(vote)
}