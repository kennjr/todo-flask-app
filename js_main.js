document.getElementById('form').onsubmit = function (e) {
   // the line below prevents the form from being submitted automatically and the form fields getting cleared
   e.preventDefault();
   // we're setting up the fetch that we'll use to send the data to the server, it takes in 2 args: the url(endpoint) and the body
   fetch('http://localhost:5000/todos/create', {
      method: 'POST',
      // we're using JSON.stringify to convert the json data that is added into a str version of itself
      body: JSON.stringify({'description':document.getElementById('description').value
           }),
      // the headers is mandatory,  we use it to tell the server that we're sending json data to it
      headers: {
            'Content-Type': 'application/json'
      }
   })
   .then(function(response) {
         return response.json();
   })
   .then(function(jsonresponse) {
        // once we get a positive response we add the new item to the list
        const liItem= document.createElement('LI');
        liItem.innerHTML = jsonResponse['description'];
        document.getElementById('todo_list').appendChild(liItem);
        document.getElementById('error').classname='hidden';
   })
   .catch(function(error) {
         document.getElementById('error').classname='';
         document.getElementById('error').innerHTML = error.toString()
   }
}