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
        let formData = new FormData()
        let imageFile = $('#food-edit-upload')[0].files[0]
        let name = $('#name').val()
        let translation = $('#translation_id').val()
        let price = $('input[name="price"]').val()
        let category = $('#category').val()
        let description = $('#foodDescription').val()
        let availability = $('#is_availabe').is(':checked') ? 'available' : 'unavailable'
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

    $('#add-food-btn').click(function() {
        let formData = new FormData()
        let imageFile = $('#food-edit-upload')[0].files[0]
        let name = $('#name').val()
        let price = $('input[name="price"]').val()
        let category = $('#category').val()
        let description = $('#foodDescription').val()
        let availability = $('#is_availabe').is(':checked') ? 'available' : 'unavailable'

        if (imageFile) {
            formData.append('image', imageFile)
        }
        formData.append('name', name)
        formData.append('price', price)
        formData.append('category', category)
        formData.append('description', description)
        formData.append('is_available', availability)

        $.ajax({
            url: '/accounts/menu-add',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                // window.location.href = '/accounts/menu'
            },
            error: function(xhr, status, error) {
                console.error(xhr.responseText) // Log any errors to the console
                    // Handle error accordingly (e.g., display error message to the user)
            }
        })
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