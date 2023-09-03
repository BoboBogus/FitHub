document.addEventListener('DOMContentLoaded', function (){
let date = new Date();
let year = date.getFullYear();
let month = date.getMonth();
 
const day = document.querySelector(".calendar-dates");
 
const currdate = document
    .querySelector(".calendar-current-date");
 
const prenexIcons = document
    .querySelectorAll(".calendar-navigation span");
 
// Array of month names
const months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
];
 
// Function to generate the calendar
const manipulate = () => {
 
    // Get the first day of the month
    let dayone = new Date(year, month, 1).getDay();
 
    // Get the last date of the month
    let lastdate = new Date(year, month + 1, 0).getDate();
 
    // Get the day of the last date of the month
    let dayend = new Date(year, month, lastdate).getDay();
 
    // Get the last date of the previous month
    let monthlastdate = new Date(year, month, 0).getDate();
 
    // Variable to store the generated calendar HTML
    let lit = "";
 
    // Loop to add the last dates of the previous month
    for (let i = dayone; i > 0; i--) {
        lit +=
            `<li class="inactive">${monthlastdate - i + 1}</li>`;
    }
 
    // Loop to add the dates of the current month
    for (let i = 1; i <= lastdate; i++) {
 
        // Check if the current date is today
        let isToday = i === date.getDate()
            && month === new Date().getMonth()
            && year === new Date().getFullYear()
            ? "active"
            : "";
        lit += `<li class="${isToday}">${i}</li>`;
    }
 
    // Loop to add the first dates of the next month
    for (let i = dayend; i < 6; i++) {
        lit += `<li class="inactive">${i - dayend + 1}</li>`
    }
 
    // Update the text of the current date element
    // with the formatted current month and year
    currdate.innerText = `${months[month]} ${year}`;
 
    // update the HTML of the dates element
    // with the generated calendar
    day.innerHTML = lit;
}
 
manipulate();
 
// Attach a click event listener to each icon
prenexIcons.forEach(icon => {
 
    // When an icon is clicked
    icon.addEventListener("click", () => {
 
        // Check if the icon is "calendar-prev"
        // or "calendar-next"
        month = icon.id === "calendar-prev" ? month - 1 : month + 1;
 
        // Check if the month is out of range
        if (month < 0 || month > 11) {
 
            // Set the date to the first day of the
            // month with the new year
            date = new Date(year, month, new Date().getDate());
 
            // Set the year to the new year
            year = date.getFullYear();
 
            // Set the month to the new month
            month = date.getMonth();
        }
 
        else {
 
            // Set the date to the current date
            date = new Date();
        }
 
        // Call the manipulate function to
        // update the calendar display
        manipulate();
    });
});
// TUTORIAL USED TO CREATE THE CALENDAR: https://www.geeksforgeeks.org/how-to-design-a-simple-calendar-using-javascript/#


    //locate every canvas and create workout graph
    canvas = document.querySelectorAll('#workout-canvas');
    for (var i = 0; i < canvas.length; i++) {
        draw_graph(canvas[i]);
    }

    radar = document.getElementById("radar-canvas");
    if (radar){
      draw_radar_graph(radar);

    }

})

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
                        },
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
function draw_radar_graph(canvas){

  const labels = ["Abdominals","Abductors","Adductors","Biceps","Calves","Cardio","Chest","Forearms","Fullbody","Glutes","Hamstrings","Lats","Lower Back","Quadriceps","Shoulders","Traps","Triceps","Upper Back"];
  data = canvas.dataset.data
  data = parseData(data)
  new Chart(canvas, {
    type: 'radar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Fitness Level',
        data: data,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'red',
        borderWidth: 2,
        pointBackgroundColor: 'rgba(54, 162, 235, 1)',
        pointBorderColor: '#fff',
        pointHoverBackgroundColor: '#fff',
        pointHoverBorderColor: 'rgba(54, 162, 235, 1)',
      }]
    },
    options: {
      scale: {
        angleLines: {
          display: true
        },
        r:{
          min: 0
        },
        ticks: {
          beginAtZero: true
        }
      }
    }
  });

}