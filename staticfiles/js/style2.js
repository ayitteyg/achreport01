console.log("mystyle.js is loaded!");

$(document).ready(function() {

    // Add a preloader
    setTimeout(() => {
        $('#preloader').fadeOut();
    }, 1000);

    // Initialize AOS
    AOS.init();

    // Smooth scrolling
    $('a[href*="#"]').click(function(event) {
        event.preventDefault();
        $('html, body').animate({
            scrollTop: $($(this).attr('href')).offset().top
        }, 500);
    });

    // Back to top
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn();
        } else {
            $('.back-to-top').fadeOut();
        }
    });

}); // ← this was missing




$(document).ready(function() {
    $("#department-select").select2({
        placeholder: "Start typing a department...",
        allowClear: true,
        minimumInputLength: 1, // Start searching after typing 1 character
        ajax: {
            url: "{% url 'get_departments' %}", // URL of our API endpoint
            dataType: "json",
            delay: 250,
            data: function(params) {
                return { q: params.term }; // Pass the search term to the API
            },
            processResults: function(data) {
                return {
                    results: $.map(data, function(item) {
                        return { id: item, text: item };
                    })
                };
            }
        }
    });
});



function confirmFormSubmission(formId, message) {
    document.getElementById(formId).addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent default form submission

        Swal.fire({
            title: "Confirm Submission",
            text: message, // Custom message
            icon: "warning",
            showCancelButton: true,
            confirmButtonText: "Yes, Submit",
            cancelButtonText: "No",
            customClass: {
                title: 'swal-title',
                content: 'swal-content',
                confirmButton: 'swal-confirm-button',
                cancelButton: 'swal-cancel-button'
            }
        }).then((result) => {
            if (result.isConfirmed) {
                // Show loading alert
                Swal.fire({
                    // title: "Submitting...",
                    text: "Submitting report...",
                    icon: "info",
                    allowOutsideClick: false,
                    showConfirmButton: false,
                    didOpen: () => {
                        Swal.showLoading(); // Show loading animation
                    }
                });

                let formData = new FormData(this);

                fetch(this.action, {
                        method: "POST",
                        body: formData,
                        headers: { "X-Requested-With": "XMLHttpRequest" }
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Hide loading alert and show success message
                        Swal.fire({
                            title: "Success!",
                            text: data.message,
                            icon: "success",
                            confirmButtonText: "OK",
                            timer: 10000,
                            timerProgressBar: true
                        }).then(() => {
                            location.reload(); // Reload page after alert
                        });
                    })
                    .catch(error => {
                        // Hide loading alert and show error message
                        Swal.fire({
                            title: "Error!",
                            text: "Something went wrong. Please try again.",
                            icon: "error",
                            confirmButtonText: "OK"
                        });
                    });
            }
        });
    });
}


// Usage Example: Call this function for any form dynamically
confirmFormSubmission("activity-form-id", "Do you want to submit this data?");
confirmFormSubmission("baptism-form-id", "Do you want to submit this data?");
confirmFormSubmission("transfer-form-id", "Do you want to submit this data?");
confirmFormSubmission("attendance-form-id", "Do you want to submit this data?");
confirmFormSubmission("visitor-form-id", "Do you want to submit this data?");
confirmFormSubmission("dedication-form-id", "Do you want to submit this data?");
confirmFormSubmission("event-form-id", "Do you want to submit this data?");
confirmFormSubmission("treasury-form-id", "Do you want to submit this data?");




function OnFormSubmissionSuccess(formId) {
    document.addEventListener("DOMContentLoaded", function() {
        let form = document.querySelector(`#${formId}`);
        if (form) {
            form.addEventListener("submit", function(event) {
                event.preventDefault(); // Prevent normal form submission

                let formData = new FormData(this);

                fetch(this.action, {
                        method: "POST",
                        body: formData,
                        headers: { "X-Requested-With": "XMLHttpRequest" }
                    })
                    .then(response => response.json())
                    .then(data => {
                        alert(data.message); // Show success alert
                        location.reload(); // Reload page to reflect changes (optional)
                    })
                    .catch(error => console.error("Error:", error));
            });
        }
    });
}

// Call the function with the form ID
document.addEventListener("DOMContentLoaded", function() {
    OnsubmissionSuccess("activity-form-id"); // Replace with any form ID
});


function changeBreadCrumbTitle(id) {
    console.log("clicked: ", id)
        // Update breadcrumb title
    const title = document.getElementById(id).innerText;
    document.getElementById("breadcrumb-title").innerText = title;
}





function tableRowClicked(yearId) {
    console.log("Clicked on row with year ID:", yearId);
    // Now you can use the yearId to identify the row
    const row = document.getElementById(yearId);
    console.log(row)
    if (row) {
        // Do something with the row, e.g., change its background color
        row.classList.add('table-info')
    }
}