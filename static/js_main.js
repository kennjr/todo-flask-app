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
        console.log(response);
        return response.json();
   })
   .then(function(jsonresponse) {
        console.log(jsonresponse);
        // once we get a positive response we add the new item to the list
        const liItem= document.createElement('LI');
        liItem.innerHTML = jsonresponse['description'];
        document.getElementById('todos').appendChild(liItem);
        document.getElementById('error').classname='hidden';
   })
   .catch(function(error) {
         document.getElementById('error').classname='';
         document.getElementById('error').innerHTML = error.toString()
   })
}

let checkboxes = document.querySelectorAll('.check-completed');

for(let i = 0; i < checkboxes.length; i++){
    let checkbox = checkboxes[i];
    checkbox.onchange = function(event) {
        console.log(event)
        let checked_status = event.target.checked;
        let todo_id = event.target.dataset['id']
        // we're gonna update the value of the todo_item's completed col.
        fetch('http://localhost:5000/todos/' + todo_id + '/set-completed', {
            method: 'POST',
            body: JSON.stringify({ 'completed' :checked_status }),
            headers: { 'Content-Type': 'application/json' }
        }).then((response) => {
            return response;
        }).then((jsonresponse) => {
            console.log('js response', jsonresponse)
            document.getElementById('error').classname='hidden';
        }).catch((error) => {
            document.getElementById('error').classname='';
            document.getElementById('error').innerHTML = error.toString()
        })
    }
}

function delete_todo(pk){
    fetch('todos/' + pk + '/delete', {
        method: 'DELETE',
        body: JSON.stringify({'id': pk}),
        headers: { 'Content-Type': 'application/json' }
    }).then((response) => {
        return response;
    }).catch((error) => {
        console.log("An error occurred", error.toString())
    })
//    .then((jsonresponse) => {
//        let status = jsonresponse['status'];
//        if(status == true){
//            console.log("The mission was a success")
//        }
//    })

}