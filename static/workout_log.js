document.addEventListener('DOMContentLoaded', function (){
    date = new Date()
    date_input = document.getElementById("date");
    date_input.value = date.getMonth() + 1 + "/" + date.getDate() + "/" + date.getFullYear();

    form_button = document.getElementById("open_form");
    form_button.addEventListener("click", openForm);
    close_button = document.getElementById("close_form");
    close_button.addEventListener("click", closeForm);

    exercises = document.querySelectorAll(".form_popup form button")
    // add workout from popup
    var id = 0;
    for (let i = 0; i < exercises.length; i++) {
        exercises[i].addEventListener("click", function(){
            type = exercises[i].dataset.type;
            workout = exercises[i].id;
            muscle = exercises[i].dataset.muscle;
            var ajax = new XMLHttpRequest();

            ajax.onreadystatechange = function(){
                if (ajax.readyState == 4 && ajax.status == 200){
                    document.getElementById('infodiv').outerHTML = this.responseText;
                    canvas = document.querySelectorAll("#canvas"+(id-1));
                    for (var i = 0; i < canvas.length; i++){
                      draw_graph(canvas[i]);
                    }
                }
            }
            //try using server to return modified html
            
            ajax.open("GET", "/wTemplate?workout="+workout+"&type="+type+ "&id="+id+"&muscle="+ muscle, true);
            id++;
            ajax.send();
            closeForm();
        })
    }

})
function openForm() {
    document.getElementById("form_popup").style.visibility = "visible";
    document.getElementById("form_popup").style.opacity = 1;
}
function closeForm() {
    document.getElementById("form_popup").style.visibility = "hidden";
}

function deleteWorkout(id){
    document.getElementById(id).remove()
}

function addSet(element){
    var ajax = new XMLHttpRequest();
    id = element.dataset.id;
    type = element.dataset.type;
    workout = element.dataset.workout;

    Counter = document.querySelector(".workout_holder #"+id+" .set_info input#counter");
    next = parseInt(Counter.value);
    next += 1;
    ajax.onreadystatechange = function(){
        if (ajax.readyState == 4 && ajax.status == 200){
            Counter.value = next;
            document.querySelector("#"+id+" #set_placeholder").outerHTML = ajax.responseText;
        }
    }

    ajax.open("GET", "/sTemplate?type="+type+"&workout="+workout+"&muscle="+muscle+"&number="+next+"&id="+id, true);
    ajax.send();
}

function deleteSet(id, exerciseId){
    Counter = document.querySelector(".workout_holder #"+exerciseId+" .set_info input#counter")
    number_id = Counter.value;
    number_id--;
    Counter.value = number_id
    
    setHolder = document.querySelector("#"+exerciseId+" .set_info .set_holder")

    set = setHolder.querySelector(":scope > #set"+id);
    set.remove();
    id++;
    set = setHolder.querySelector(":scope > #set"+id);
    while(set){
        text = set.querySelector("p");
        text.innerHTML = id - 1
        let set_id = id-1;
        set.id = "set"+set_id;
        set.querySelector("button").setAttribute("data-id", id - 1);
        id++;
        set = setHolder.querySelector(":scope > #set"+id);
    }

}
function parseData(string){
  let clean = string.slice(1, string.length-1);
  return clean.split(",")
}

function parseData(string){
  let clean = string.slice(1, string.length-1);
  return clean.split(",")
}


function draw_graph(canvas) {
//REFACTOR: change based on duration
  //FOR some reason passed in as string
  var x_input = canvas.dataset.x;
  var y_input = canvas.dataset.y;
  
  var y_to_time = false;

  if (canvas.dataset.type == "Duration"){
    y_to_time = true;
  }
  

  const title = canvas.dataset.title;

  xValues = parseData(x_input);
  yValues = parseData(y_input);

  if(y_to_time){
    new Chart(canvas, {
      type: 'line',
      data: {
        labels: xValues,
        datasets: [{
          label: 'your progress over time',
          data: yValues,
          borderColor: 'red'
        }]
      },
      options: {
        plugins: {
            title: {
                display: true,
                text: title,
            }
        },
         scales: {
            y: {
                ticks: {
                    // Include a dollar sign in the ticks
                    callback: function(value, index, ticks) {
                      var hours = Math.floor(value / 3600);
                      value = value % 3600;
                      var minutes = Math.floor(value / 60);
                      var value = value % 60;
                      return String(hours) + ":" + String(minutes) + ":" + String(value);
                    }
                }
            }
          }
      }
    });
  }
  else{
    new Chart(canvas, {
      type: 'line',
      data: {
        labels: xValues,
        datasets: [{
          label: 'your progress over time',
          data: yValues,
          borderColor: 'red'
        }]
      },
      options: {
        plugins: {
            title: {
                display: true,
                text: title,
            }
        },
      }
    });
  }
  
 
}
