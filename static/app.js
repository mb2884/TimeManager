var debug = false;

document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");

  var calendar = new FullCalendar.Calendar(calendarEl, {
    // Calendar configuration options
    headerToolbar: {
      left: "prev,next today",
      center: "title",
      right: "dayGridMonth,timeGridWeek,timeGridDay",
    },
    timeZone: "America/New_York",
    navLinks: true,
    selectable: true,
    selectMirror: true,
    selectOverlap: true,
    eventConstraint: {
      start: "00:00",
      end: "24:00",
    },
    eventOverlap: true,

    eventClick: function (arg) {
      if (confirm("Are you sure you want to delete this event?")) {
        // Send an AJAX request to delete the event from the database
        $.ajax({
          type: "POST",
          url: "/delete-event",
          contentType: "application/json",
          data: JSON.stringify({
            event_id: arg.event._def.publicId,
          }), // Pass the event ID to the server
          success: function (response) {
            console.log(response); // Log success message
            arg.event.remove(); // Remove the event from the calendar UI
            refreshCalendar(); // Refresh the calendar after deleting the event
          },
          error: function (_xhr, _status, error) {
            console.error(error); // Log error message
            refreshCalendar();
            // Handle errors and provide feedback to the user
          },
        });
      }
    },
    editable: true,
    dayMaxEvents: true,
    select: function (arg) {
      var title = prompt("Event Title:");

      if (title) {
        let requestData = {
          type: "POST",
          url: "/add-event",
          contentType: "application/json",
          data: JSON.stringify({
            username: username,
            title: title,
            start: arg.start.toISOString(),
            end: arg.end.toISOString(),
            allDay: arg.allDay,
            recurring: null, // Add recurring option to the data
          }),
          success: function (response) {
            console.assert(response.id, "Response ID is not defined");
            if (response.id) {
              calendar.addEvent({
                title: title,
                start: arg.start,
                end: arg.end,
                allDay: arg.allDay,
                id: response.id,
                color: response.color,
              });
              refreshCalendar(); // Refresh the calendar after adding the event
            }
          },
          error: function (_xhr, _status, error) {
            alert(
              "There was an error processing your request. Please try again."
            );
            console.error(error);
            refreshCalendar();
          },
        };
        $.ajax(requestData);
      }
      calendar.unselect();
    },
    eventDrop: function (arg) {
      // When an event is dropped/moved, send an AJAX request to update the event on the server
      $.ajax({
        type: "POST",
        url: "/update-event",
        contentType: "application/json",
        data: JSON.stringify({
          event_id: arg.event._def.publicId,
          start: arg.event.start.toISOString(),
          end: arg.event.end ? arg.event.end.toISOString() : null, 
          allDay: arg.event.allDay,
          title: arg.event.title,
        }),
        success: function (response) {
          console.log(response); // Log success message
        },
        error: function (_xhr, _status, error) {
          refreshCalendar();
          console.error(error); // Log error message
        },
      });
    },
    eventResize: function (arg) {
      // When an event is resized, send an AJAX request to update the event duration on the server
      $.ajax({
        type: "POST",
        url: "/update-event",
        contentType: "application/json",
        data: JSON.stringify({
          event_id: arg.event._def.publicId,
          start: arg.event.start.toISOString(),
          end: arg.event.end ? arg.event.end.toISOString() : null, // Check if the event has an end time
          allDay: arg.event.allDay,
          title: arg.event.title,
        }),
        success: function (response) {
          console.log(response); 
        },
        error: function (_xhr, _status, error) {
          refreshCalendar();
          console.error(error); 
        },
      });
    },
    eventDrop: function (arg) {
      // When an event is dropped/moved, send an AJAX request to update the event on the server
      $.ajax({
        type: "POST",
        url: "/update-event",
        contentType: "application/json",
        data: JSON.stringify({
          event_id: arg.event._def.publicId,
          start: arg.event.start.toISOString(),
          end: arg.event.end
            ? arg.event.end.toISOString()
            : arg.event._instance.range.end.toISOString(), 
          allDay: arg.event.allDay,
          title: arg.event.title,
        }),
        success: function (response) {
          //refreshCalendar();
          console.log(response); // Log success message
        },
        error: function (_xhr, _status, error) {
          refreshCalendar();
          console.error(error); // Log error message
          // Handle errors and provide feedback to the user
        },
      });
    },
  });

  calendar.render();
  calendar.today();

  // Get events from the server
  $.ajax({
    type: "GET",
    url: "/get-events",
    success: function (response) {
      // Add events to the calendar
      console.assert(response, "Response is not defined");
      calendar.addEventSource(response);
      calendar.render();
      refreshCalendar();
    },
    error: function (_xhr, _status, error) {
      console.error(error);
      refreshCalendar();
      // Handle errors and provide feedback to the user
    },
  });

  // Define refreshCalendar function
  function refreshCalendar() {
    // Get events from the server
    $.ajax({
      type: "GET",
      url: "/get-events",
      success: function (events) {
        // Clear the calendar
        calendar.removeAllEvents();
        // Add events to the calendar
        calendar.addEventSource(events);
        calendar.render();
      },
      error: function (_xhr, _status, error) {
        console.error(error);
        // Handle errors and provide feedback to the user
      },
    });
  }

  function validateTaskFields() {
    var title = $("#taskName").val();
    var duration = parseInt($("#duration").val());
    var startDate = $("#startDate").val();
    var startTime = $("#startTime").val();
    var dueDate = $("#dueDate").val();
    var dueTime = $("#dueTime").val();

    // Check if any field is empty
    if (
      title.trim() === "" ||
      isNaN(duration) ||
      duration <= 0 ||
      startDate === "" ||
      startTime === "" ||
      dueDate === "" ||
      dueTime === ""
    ) {
      $("#durationError").text("Please fill out all fields.");
      return false;
    }

    if (isNaN(duration) || duration <= 0) {
      $("#durationError").text("Duration must be a positive number.");
      return false;
    }

    // Check if due date is after start date
    var startDateTime = new Date(startDate + " " + startTime);
    var endDateTime = new Date(dueDate + " " + dueTime);
    if (endDateTime <= startDateTime) {
      $("#durationError").text("Due date must be after start date.");
      return false;
    }

    // Check to see if the task is longer than the time between the start and end date
    var timeDifference = endDateTime - startDateTime;
    var hoursDifference = timeDifference / (1000 * 3600);
    if (hoursDifference < duration) {
      $("#durationError").text(
        "Task duration is longer than the time between start and end date."
      );
      return false;
    }
    // Check if the title is too long
    if (title.length > 45) {
      $("#durationError").text(
        "Task name must be under 45 characters."
      );
      return false;
    }

    // Clear the error message if all fields are valid
    $("#durationError").text("");
    return true;
  }

  // Function to add task
  function addTask() {
    // Validate all task fields
    console.assert(validateTaskFields(), "Task fields are not valid");


    let title = $("#taskName").val();
    let duration = Math.round(parseFloat($("#duration").val()));
    let startDate = $("#startDate").val();
    let startTime = $("#startTime").val();
    let dueDate = $("#dueDate").val();
    let dueTime = $("#dueTime").val();

    let startDateTime = new Date(
      Date.parse(startDate + " " + startTime)
    );
    startDateTime.toLocaleString("en-US", {
      timeZone: "America/New_York",
    });

    let endDateTime = new Date(Date.parse(dueDate + " " + dueTime));
    endDateTime.toLocaleString("en-US", {
      timeZone: "America/New_York",
    });

    // Send task details to the server
    $.ajax({
      type: "POST",
      url: "/add-task",
      contentType: "application/json",
      data: JSON.stringify({
        username: username,
        title: title,
        start: startDateTime.toISOString(),
        end: endDateTime.toISOString(),
        length: duration, // Include task-specific field
        events: calendar.getEvents(),
      }),
      success: function (response) {
        // Handle success response if needed
        console.log(response);

        refreshCalendar();

        fetchAndDisplayTasks();

        // Clear the input fields
        if (!debug) {
          $("#taskName").val("");
          $("#duration").val("");
          $("#startDate").val("");
          $("#startTime").val("");
          $("#dueDate").val("");
          $("#dueTime").val("");
        }
      },
      error: function (xhr, _status, error) {
        // Handle error response if needed
        console.error("Error adding task:", error);
        fetchAndDisplayTasks();
        alert(JSON.parse(xhr.responseText).error);
        refreshCalendar();
      },
    });
  }

  function validateEventFields() {
    var title = $("#eventName").val();
    var startDate = $("#firstDate").val();
    var startTime = $("#firstTime").val();
    var endDate = $("#endDate").val();
    var endTime = $("#endTime").val();
    var color = $("#color").val();
    var startDateTime = new Date(startDate + " " + startTime);
    var endDateTime = new Date(endDate + " " + endTime);
    var monday = $("#monday").is(":checked");
    var tuesday = $("#tuesday").is(":checked");
    var wednesday = $("#wednesday").is(":checked");
    var thursday = $("#thursday").is(":checked");
    var friday = $("#friday").is(":checked");
    var saturday = $("#saturday").is(":checked");
    var sunday = $("#sunday").is(":checked");
    var recurEndDate = $("#recurEndDate").val();
    // Check if any field is empty
    if (
      title.trim() === "" ||
      startDate === "" ||
      startTime === "" ||
      endDate === "" ||
      endTime === ""
    ) {
      $("#TimeError").text("Please fill out all fields."); // Welll, it's not really alll fields is it?
      return false;
    }
    if (endDateTime <= startDateTime) {
      $("#TimeError").text("End date must be after start date.");
      return false;
    }
    if (title.length > 45) {
      $("#TimeError").text("Event name must be under 45 characters.");
      return false;
    }

    // Check if checkboxes any checkboxes are checked while the end date is empty
    if (
      (monday ||
        tuesday ||
        wednesday ||
        thursday ||
        friday ||
        saturday ||
        sunday) &&
      recurEndDate === ""
    ) {
      $("#TimeError").text(
        "Please enter an end date for recurring events."
      );
      return false;
    }

    // Check to see if end date is full but no checkboxes are checked
    if (
      !(
        monday ||
        tuesday ||
        wednesday ||
        thursday ||
        friday ||
        saturday ||
        sunday
      ) &&
      recurEndDate !== ""
    ) {
      $("#TimeError").text(
        "Please select at least one day of the week for recurring events."
      );
      return false;
    }

    // Clear the error message if all fields are valid
    $("#TimeError").text("");
    return true;
  }

  function addEvent() {
    // Validate all event fields
    console.assert(validateEventFields(), "Event fields are not valid");

    var title = $("#eventName").val();
    var startDate = $("#firstDate").val();
    var startTime = $("#firstTime").val();

    var endDate = $("#endDate").val();
    var endTime = $("#endTime").val();

    var start = new Date(Date.parse(startDate + " " + startTime));
    start = start.toLocaleString("en-US", {
      timeZone: "America/New_York",
    });

    var end = new Date(Date.parse(endDate + " " + endTime));
    end = end.toLocaleString("en-US", {
      timeZone: "America/New_York",
    });

    var color = $("#color").val();

    var recurEndDate = $("#recurEndDate").val();
    if (recurEndDate !== "" && recurEndDate !== null) {
      var date = new Date(recurEndDate);
      date.setDate(date.getDate() + 1);
      recurEndDate = date.toISOString().split("T")[0];
    }

    var sunday = $("#sunday").is(":checked");
    var monday = $("#monday").is(":checked");
    var tuesday = $("#tuesday").is(":checked");
    var wednesday = $("#wednesday").is(":checked");
    var thursday = $("#thursday").is(":checked");
    var friday = $("#friday").is(":checked");
    var saturday = $("#saturday").is(":checked");
    // Construct an array of days of the week
    var daysOfWeek = [];
    if (sunday) daysOfWeek.push(0);
    if (monday) daysOfWeek.push(1);
    if (tuesday) daysOfWeek.push(2);
    if (wednesday) daysOfWeek.push(3);
    if (thursday) daysOfWeek.push(4);
    if (friday) daysOfWeek.push(5);
    if (saturday) daysOfWeek.push(6);
    // Send event details to the server

    let requestData = {
      type: "POST",
      url: "/add-event",
      contentType: "application/json",
      data: JSON.stringify({
        username: username,
        title: title,
        start: start,
        end: end,
        allDay: false,
        daysOfWeek: daysOfWeek,
        color: color,
        startRecur: start,
        endRecur: recurEndDate,
      }),
      success: function (response) {
        console.assert(response.id, "Response ID is not defined");
        if (response.id) {
          calendar.addEvent({
            title: response.title,
            start: response.start,
            end: response.end,
            allDay: false,
            id: response.id,
            color: response.color,
            daysOfWeek: response.daysOfWeek,
            startTime: response.startTime,
            endTime: response.endTime,
            startRecur: response.startRecur,
            endRecur: response.endRecur,
          });
          refreshCalendar(); // Refresh the calendar after adding the event

          if (!debug) {
            // clear the input fields
            $("#eventName").val("");
            $("#firstDate").val("");
            $("#firstTime").val("");
            $("#endDate").val("");
            $("#endTime").val("");
            $("color").val("");
            // Clear the checkbox fields for the days of the week
            $("#sunday").prop("checked", false);
            $("#monday").prop("checked", false);
            $("#tuesday").prop("checked", false);
            $("#wednesday").prop("checked", false);
            $("#thursday").prop("checked", false);
            $("#friday").prop("checked", false);
            $("#saturday").prop("checked", false);
            $("#recurEndDate").val("");
          }
        }
      },
      error: function (_xhr, _status, error) {
        alert(
          "There was an error processing your request. Please try again."
        );
        console.error(error);
        refreshCalendar();
      },
    };
    $.ajax(requestData);
  }

  // Event listener for add task button click
  $("#addTaskButton").click(function () {
    // Validate all fields before adding task
    if (validateTaskFields()) {
      addTask();
      // After adding the task, fetch and display tasks again
      fetchAndDisplayTasks();
    }
  });

  $("#addEventButton").click(function () {
    // Validate all fields before adding task
    if (validateEventFields()) {
      addEvent();
      // After adding the task, fetch and display tasks again
      refreshCalendar();
    }
  });

  // On page load, fetch and display tasks
  fetchAndDisplayTasks();

  // Check if the tutorial has been completed before
  var tutorialCompleted = localStorage.getItem("tutorialCompleted");

  // If the tutorial has been completed before, hide it and return
  if (tutorialCompleted === "true") {
    document.getElementById("tutorial").style.display = "none";
    document.getElementById("runTutorialLink").style.display = "block";
  } else {
    // Show the tutorial
    document.getElementById("tutorial").style.display = "block";
    document.getElementById("runTutorialLink").style.display = "none";
  }

  // Tutorial steps
  var steps = document.querySelectorAll(".tutorial-step");
  var currentStepIndex = 0;

  // Function to show a specific step
  function showStep(index) {
    steps.forEach(function (step, i) {
      step.style.display = i === index ? "block" : "none";
      switch (index) {
        case 1:
          $(".fc-button-primary").addClass("attention-element");
          calendar.changeView("dayGridMonth");
          break;
        case 2:
          $(".fc-button-primary").removeClass("attention-element");
          calendar.changeView("timeGridWeek");
          calendar.today();
          break;
        case 4:
          $("#addTaskButton").addClass("attention-element");
          break;

        case 5:
          $("#addTaskButton").removeClass("attention-element");
          $("#eventAdder").addClass("attention-element");
          break;
        case 6:
          $("#eventAdder").removeClass("attention-element");
          $("#taskTitle").addClass("attention-element");
          break;
      }
    });
  }

  // Show the first step initially
  showStep(currentStepIndex);

  // Add event listener for the Enter key to advance the tutorial steps
  document.addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      currentStepIndex++;
      if (currentStepIndex < steps.length) {
        showStep(currentStepIndex);
      } else {
        // If there are no more steps, hide the tutorial and mark it as completed
        $("#taskTitle").removeClass("attention-element");
        document.getElementById("tutorial").style.display = "none";
        localStorage.setItem("tutorialCompleted", "true");
        // show the run tutorial link
        document.getElementById("runTutorialLink").style.display =
          "block";
      }
    }
  });
  // Function to run the tutorial
  function runTutorial() {
    // Show the tutorial container
    document.getElementById("tutorial").style.display = "block";
    // Reset tutorial steps to the beginning
    currentStepIndex = 0;
    showStep(currentStepIndex);
    // Hide the "Run Tutorial" link after starting the tutorial
    document.getElementById("runTutorialLink").style.display = "none";
  }

  // Event listener for the "Run Tutorial" link
  document
    .getElementById("runTutorialLink")
    .addEventListener("click", function () {
      runTutorial();
    });

  $(document).on("click", ".delete-task", function () {
    var taskId = $(this).data("id");
    var listItem = $(this).closest("li"); // Get the parent <li> element

    // Send an AJAX request to delete the task from the server
    $.ajax({
      type: "POST",
      url: "/delete-task",
      contentType: "application/json",
      data: JSON.stringify({ task_id: taskId }), // Pass the task ID to the server
      success: function (response) {
        console.log(response); // Log success message
        // Remove the task from the task list
        listItem.remove(); // Remove the parent <li> element
        refreshCalendar();
      },
      error: function (_xhr, _status, error) {
        console.error(error); // Log error message
        refreshCalendar();
        // Handle errors and provide feedback to the user
      },
    });
  });

  // Function to fetch tasks from the server and display them in the task list
  function fetchAndDisplayTasks() {
    // Fetch tasks from the server
    $.ajax({
      type: "GET",
      url: "/get-tasks",
      success: function (tasks) {
        // Clear the task list
        $("#taskList").empty();

        // Iterate over each task and create a list item for it
        tasks.forEach(function (task) {
          // Create list item HTML
          var listItemHtml =
            "<li>" +
            task.title +
            '<a href="#" class="delete-task" data-id="' +
            task.id +
            '">❌</a></li>';

          // Append the list item to the task list
          $("#taskList").append(listItemHtml);
          refreshCalendar();
        });
      },
      error: function (_xhr, _status, error) {
        console.error(error);
        refreshCalendar();
        // Handle errors and provide feedback to the user
      },
    });
  }
  // On page load, fetch and display tasks
  fetchAndDisplayTasks();
});

// Define getRandomColor function
function getRandomColor() {
  var minBrightness = 128; // Minimum brightness threshold

  // Generate random values for red, green, and blue components
  var r = Math.floor(Math.random() * 256);
  var g = Math.floor(Math.random() * 256);
  var b = Math.floor(Math.random() * 256);

  // Calculate the brightness of the color using the YIQ formula
  var brightness = (r * 299 + g * 587 + b * 114) / 1000;

  // If the brightness is below the threshold, adjust the color
  if (brightness < minBrightness) {
    // Increase brightness by adding a fixed value to each component
    var brightnessDifference = minBrightness - brightness;
    var adjustmentFactor = brightnessDifference / brightness;
    r = Math.min(255, Math.floor(r + adjustmentFactor * r));
    g = Math.min(255, Math.floor(g + adjustmentFactor * g));
    b = Math.min(255, Math.floor(b + adjustmentFactor * b));
  }

  // Convert RGB components to hexadecimal string representation
  var hexColor =
    "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);

  return hexColor;
}

document.addEventListener("DOMContentLoaded", function () {
  var phrases = [
    "You got this",
    "You're awesome",
    "Believe in yourself",
    "Stay positive",
    "Keep going",
    "Dream big",
    "Make it happen",
    "You're amazing",
    "You can do it",
    "Never give up",
    "Almost Friday",
    "Work hard play hard",
    "Grades are a social construct",
    "We out here",
    "So back",
    "Academic weapon",
    "Just rip it",
    "F it we ball",
    "Here we go",
    "You're so up right now",
    "Keep going!",
    "Don't forget to rest!",
  ];

  var index = 0;
  var dynamicText = document.getElementById("dynamicText");

  function updateText() {
    var phrase = phrases[index];
    var words = phrase.split(" "); // Split the phrase into words

    dynamicText.textContent = ""; // Clear the text content initially

    // Apply the random color to the text element
    dynamicText.style.color = getRandomColor();

    // Display each word sequentially with a delay
    words.forEach(function (word, wordIndex) {
      setTimeout(function () {
        dynamicText.textContent += word + " "; // Append the word with a space
        // If it's the last word, append a newline character
        if (wordIndex === words.length - 1) {
          dynamicText.textContent += "\n";
        }
      }, wordIndex * 500); // Delay each word by 500 milliseconds
    });

    index = (index + 1) % phrases.length;
  }

  // Initial text update
  updateText();

  // Update text every 3 seconds
  setInterval(updateText, 3000);
});

function openSettings() {
  var settings = document.getElementById("settingsMenu");
  if (
    settings.style.display === "none" ||
    settings.style.display === ""
  ) {
    $("#settings").addClass("red");
    settings.style.display = "block";
    $("#settingsMenu").removeClass("slideRight");
    $("#settingsMenu").addClass("slideLeft");
    $("#dynamicText").addClass("slideDown");
    $("#dynamicText").removeClass("slideUp");
  } else {
    $("#settings").removeClass("red");
    $("#settingsMenu").removeClass("slideLeft");
    $("#settingsMenu").addClass("slideRight");
    $("#dynamicText").removeClass("slideDown");
    $("#dynamicText").addClass("slideUp");
    settings.addEventListener(
      "transitionend",
      () => {
        settings.style.display = "none";
      },
      { once: true }
    );
    setTimeout(() => {
      settings.style.display = "none";
    }, 400); // Adjust timeout to match transition duration
  }
}

function validateSettings() {
  var earliestTime = $("#earliestTime").val();
  var latestTime = $("#latestTime").val();
  var idealChunkSize = $("#idealChunkSize").val();
  var eventPadding = $("#eventPadding").val();
  if (
    earliestTime === "" ||
    latestTime === "" ||
    idealChunkSize === "" ||
    eventPadding === ""
  ) {
    $("#settingsError").text("Please fill out all fields.");
    return false;
  }
  if (earliestTime >= latestTime) {
    $("#settingsError").text(
      "Earliest time must be before latest time."
    );
    return false;
  }
  if (idealChunkSize <= 0) {
    $("#settingsError").text(
      "Ideal chunk size must be a positive number."
    );
    return false;
  }
  if (eventPadding < 0) {
    $("#settingsError").text(
      "Event padding must be a non-negative number."
    );
    return false;
  }

  $("#settingsError").text("");
  return true;
}

function saveSettings() {
  console.assert(validateSettings(), "Settings are not valid");
  var earliestTime = $("#earliestTime").val();
  var latestTime = $("#latestTime").val();
  var idealChunkSize = $("#idealChunkSize").val();
  var eventPadding = $("#eventPadding").val();

  var requestData = {
    type: "POST",
    url: "/save-settings",
    contentType: "application/json",
    data: JSON.stringify({
      username: username,
      earliestTime: earliestTime,
      latestTime: latestTime,
      idealChunkSize: idealChunkSize,
      eventPadding: eventPadding,
    }),
    success: function (response) {
      console.log(response); // Log success message
    },
    error: function (_xhr, _status, error) {
      alert("Could not save settings. Please try again.");
      console.error(error);
    },
  };

  $.ajax(requestData);
}

function logout() {
  // Call the logout route when the button is clicked
  $.ajax({
    type: "GET",
    url: "/logoutapp",
    success: function (response) {
      console.log(response); // success message
      window.location.href = "/landing"; // Redirect to the landing page
    },
    error: function (_xhr, _status, error) {
      console.error(error); // Log error message
    },
  });
}

function toggleSidebar(type) {
  if (type === "task") {
    document.getElementById("taskSidebar").style.display = "block";
    document.getElementById("eventSidebar").style.display = "none";
    document.getElementById("eventAdder").style.display = "block";
    document.getElementById("taskAdder").style.display = "none";
  } else if (type === "event") {
    document.getElementById("taskSidebar").style.display = "none";
    document.getElementById("eventSidebar").style.display = "block";
    document.getElementById("eventAdder").style.display = "nonee";
    document.getElementById("taskAdder").style.display = "block";
  }
}

$(document).on("click", "#taskAdder", function () {
  toggleSidebar("task");
});

$(document).on("click", "#eventAdder", function () {
  toggleSidebar("event");
});
