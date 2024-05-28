var showFoodImage = 1;

$(document).ready(function() {
    $('#datepicker').datepicker({
        format: 'yyyy-mm-dd',
        defaultDate: new Date(),
        autoclose: true
    })

    // Function to delete a booking
    $('.deleteBooking').click(function() {
        let bookingId = $(this).attr('data-booking-id')
        $.ajax({
            url: '/delete-booking/' + bookingId, // Replace with your Django backend endpoint
            type: 'DELETE',
            success: function(response) {
                console.log(response) // Log the response from the server
                    // If deletion is successful, remove the corresponding row from the table
                $('#bookingRow_' + bookingId).remove()
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText) // Log any errors to the console
                    // Handle error accordingly (e.g., display error message to the user)
            }
        })
    })

    // Select category
    $('#categorySelect').on('change', function() {
        window.location.href = '/accounts/menu?cate=' + $(this).val()
    })

    // Preview image on file select
    $('#food-edit-upload').on('change', function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader()

            reader.onload = function(e) {
                $('#food-edit-image').attr('src', e.target.result)
                $('#food-edit-image').show()
            }

            reader.readAsDataURL(this.files[0])
        }
    })

    // Clicking edit-food-btn will send POST request to edit food with image, name, price
    $('#edit-food-btn').click(function() {
        $(this).prop('disabled', true);
        let formData = new FormData()
        let imageFile = $('#food-edit-upload')[0].files[0]
        let name = $('#name').val()
        let translation = $('#translation_id').val()
        let price = $('input[name="price"]').val()
        let category = $('#category').val()
        let description = $('#foodDescription').val()
        let availability = $('#is_availabe').is(':checked') ? 'available' : 'unavailable'
        let show_image =  $('#show_image').is(':checked') ? '1' : '0'
        let food_id = $('#food_id').val()

        if (imageFile) {
            formData.append('image', imageFile)
        }
        formData.append('food_id', food_id)
        formData.append('name', name)
        formData.append('price', price)
        formData.append('category', category)
        formData.append('translation_id', translation)
        formData.append('description', description)
        formData.append('availability', availability)
        formData.append('show_image', show_image)
        formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val())

        $.ajax({
            url: '/accounts/menu?food=' + food_id,
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                window.location.href = '/accounts/menu?food=' + food_id
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText) // Log any errors to the console
                    // Handle error accordingly (e.g., display error message to the user)
            }
        })
    })

    $('#add-food-btn').click(function(e) {
        $(this).prop('disabled', true);
        e.preventDefault();
        let formData = new FormData()
        let imageFile = $('#food-edit-upload')[0].files[0]
        let translation = $('#translation_id').val()
        let name = $('#name').val()
        let price = $('input[name="price"]').val()
        let category = $('#category').val()
        let description = $('#foodDescription').val()
        let availability = $('#is_availabe').is(':checked') ? 'available' : 'unavailable'
        let show_image =  $('#show_image').is(':checked') ? '1' : '0'

        if (imageFile) {
            formData.append('image', imageFile)
        }
        formData.append('name', name)
        formData.append('price', price)
        formData.append('category', category)
        formData.append('translation_id', translation)
        formData.append('description', description)
        formData.append('availability', availability)
        formData.append('show_image', show_image)
        formData.append('csrfmiddlewaretoken', $('[name=csrfmiddlewaretoken]').val())

        $.ajax({
            url: '/accounts/menu-add',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                window.location.href = '/accounts/menu'
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText) // Log any errors to the console
                    // Handle error accordingly (e.g., display error message to the user)
            }
        })
    })

    $('.cb-value').click(function() {
        var mainParent = $(this).parent('.toggle-btn');
        var toggleStatus = false;
        if ($(mainParent).find('input.cb-value').is(':checked')) {
            $(mainParent).addClass('active');
            toggleStatus = true;
        } else {
            $(mainParent).removeClass('active');
        }

        $.ajax({
            url: '/api/toggle-availability',
            method: 'POST',
            data: {
                status: toggleStatus,
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                console.log(response)
            }
        })
    })

    $('.food-cb-value').click(function() {
        var mainParent = $(this).parent('.toggle-btn');
        if ($(mainParent).find('input.food-cb-value').is(':checked')) {
            $(mainParent).addClass('active');
            showFoodImage = 1;
        } else {
            $(mainParent).removeClass('active');
            showFoodImage = 0;
        }
        $('.show_image').val(showFoodImage);
    })
})

$('#find-bookings').on('click', function() {
    var url = window.location.origin + '/accounts/profile?date=' + $('#datepicker').val()
    window.location.href = url
})

$('#booking_date_reload').on('change', function() {
    var url = window.location.origin + '/accounts/calendar?date=' + $(this).val()
    window.location.href = url
})

function mergeCells() {
    $('#booking-table tr').each(function() {
        var prevBookingId = null
        var colspan = 1

        $('td', this).each(function() {
            var bookingId = $(this).data('booking-id')

            if (bookingId === prevBookingId) {
                colspan++
                $(this)
                    .prevAll('[data-booking-id="' + bookingId + '"]')
                    .attr('colspan', colspan)
                    .addClass('merged-cell')
                $(this).remove()
            } else {
                prevBookingId = bookingId
                colspan = 1
            }
        })
    })
}

// Call the mergeCells function on page load
mergeCells()

function copyText() {
    // Get the text field
    var copyText = document.getElementById('myInput')

    // Select the text field
    copyText.select()
    copyText.setSelectionRange(0, 99999) // For mobile devices

    // Copy the text inside the text field
    navigator.clipboard.writeText(copyText.value)

    // Alert the copied text
    alert('Copied the text: ' + copyText.value)
}

$('.show-booking-detail').click(function() {
    var booking_id = $(this).data('booking-id')
    $.ajax({
        url: '/api/bookings?booking_id=' + booking_id,
        type: 'GET',
        success: function(response) {
            var tableDetail = $('#tableDetail')
            tableDetail.html('')
            var html = ''
            response.booking_details.forEach(function(detail) {
                html += '<tr>'
                html += '<td>' + detail.food_name + '</td>'
                html += '<td>' + detail.quantity + '</td>'
                html += '<td>' + detail.food_price + '</td>'
                html += '</tr>'
            })
            tableDetail.append(html)


            $('#customer-email').html(response.customer_email)
            $('#customer-phone').html(response.customer_phone)
            $('#customer-special-request').html(response.special_requests)

            $('#bookingModal').modal('show')
        }
    })
})

$('.booking-modal-detail').on('click', function() {
    var data_booking_id = $(this).data('booking-id');

    var table = '';
    $.ajax({
            url: '/api/bookings?booking_id=' + data_booking_id,
            type: 'GET',
            success: function(response) {
                var html = ''
                html += 'Booking <code>#' + response.id + '</code>'
                html += '<input type="hidden" name="booking-event-id" value="'+response.booking_event_id+'"/>'
                html += '<table class="table table-bordered">'
                html += '<tr><td>Number of people <i class="fa-solid fa-user-plus"></i></td><td><input class="form-control" type="number" name="booking-modal-total" value="' + response.total_people + '" disabled/></td></tr>'
                html += '<tr><td>Date</td><td><input class="form-control"  type="date" name="booking-modal-date" value="' + response.booking_date + '"/></td></tr>'
                html += '<tr><td>Time</td><td><input class="form-control"  type="time" name="booking-modal-time" value="' + response.booking_time + '" min="17:00" max="22:00" /></td></tr>'
                html += '<tr><td><i class="fa-regular fa-clock"></i> Duration (minute)</td><td><input class="form-control"  type="number" name="booking-modal-duration" value="' + response.duration + '" min="0" /></td></tr>'
                html += '<tr><td><i class="fa-regular fa-circle-user"></i> Customer</td><td><input class="form-control"  type="text" name="booking-modal-customer" value="' + response.customer_name + '" disabled/></td></tr>'
                html += '<tr><td><i class="fa-solid fa-phone"></i> Phone</td><td><input class="form-control"  type="text" name="booking-modal-customer-phone" value="' + response.customer_phone + '" disabled/></td></tr>'
                html += '<tr><td><i class="fa-regular fa-envelope"></i> Email</td><td><input class="form-control"  type="text" name="booking-modal-customer-email" value="' + response.customer_email + '" disabled/></td></tr>'
                html += '</table>'
                table += html

                $('.admin-booking-body').html(table);

                $('#adminBookingModal').modal('show');
            }
        });

    $('#admin-update-booking').on('click', function() {
        $(this).prop('disabled', true);
        $.ajax({
            url: '/api/book-table',
            method: 'POST',
            data: {
                data_booking_id: data_booking_id,
                is_updated: 1,
                booking_date: $('[name=booking-modal-date]').val(),
                booking_time: $('[name=booking-modal-time]').val(),
                booking_duration: $('[name=booking-modal-duration]').val(),
                total_customer: $('[name=booking-modal-total]').val(),
                fullname: $('[name=booking-modal-customer]').val(),
                phone: $('[name=booking-modal-customer-phone]').val(),
                email: $('[name=booking-modal-customer-email]').val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#adminBookingModal').modal('hide');
                window.location.reload();
            },
            error: function(xhr, status, error) {
                alert(xhr.responseText);
            }
        })
    })

    $('#admin-cancel-booking').on('click', function() {
        $(this).prop('disabled', true);
        var confirm = window.confirm("Are you sure you want to cancel this booking?")
        if (confirm == false) {
            return;
        }
        $.ajax({
            url: '/api/cancel-booking',
            method: 'POST',
            data: {
                data_booking_id: data_booking_id,
                booking_event: $('[name=booking-event-id]').val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#adminBookingModal').modal('hide');
                window.location.reload();;
            }
        })
    })
});

$('#add-booking-modal').on('click', function(e) {
     e.preventDefault();
     var html = ''
     html += '<table class="table table-bordered">'
     html += '<tr><td><i class="fa-solid fa-user-plus"></i> Number of people</td><td><input class="form-control" type="number" name="booking-modal-add-total" value=""/></td></tr>'
     html += '<tr><td>Date</td><td><input class="form-control"  type="date" name="booking-modal-add-date" value=""/></td></tr>'
     html += '<tr><td>Time</td><td><input class="form-control"  type="time" name="booking-modal-add-time" value="" min="17:00" max="22:00" /></td></tr>'
     html += '<tr><td><i class="fa-regular fa-circle-user"></i> Customer</td><td><input class="form-control"  type="text" name="booking-modal-add-customer" value=""/></td></tr>'
     html += '<tr><td><i class="fa-solid fa-phone"></i> Phone</td><td><input class="form-control"  type="text" name="booking-modal-add-customer-phone" value=""/></td></tr>'
     html += '<tr><td><i class="fa-regular fa-envelope"></i> Email</td><td><input class="form-control"  type="text" name="booking-modal-add-customer-email" value=""/></td></tr>'
     html += '</table>'

     $('.admin-booking-add-body').html(html);
     $('#adminAddBookingModal').modal('show');

    $('#admin-add-booking').on('click', function() {
        $(this).prop('disabled', true);
        $.ajax({
            url: '/api/book-table',
            method: 'POST',
            data: {
                booking_date: $('[name=booking-modal-add-date]').val(),
                booking_time: $('[name=booking-modal-add-time]').val(),
                total_customer: $('[name=booking-modal-add-total]').val(),
                fullname: $('[name=booking-modal-add-customer]').val(),
                phone: $('[name=booking-modal-add-customer-phone]').val(),
                email: $('[name=booking-modal-add-customer-email]').val(),
                csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#adminAddBookingModal').modal('hide');
                window.location.href = '/accounts/calendar?date='+ $('[name=booking-modal-add-date]').val();
            },
            error: function(xhr, status, error) {
                alert(xhr.responseText);
            }
        })
    })
});