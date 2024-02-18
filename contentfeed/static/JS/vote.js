async function upvote(item_id,session_id,csrf_t) 
{
  item = item_id
  session = session_id
  csrf = csrf_t
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