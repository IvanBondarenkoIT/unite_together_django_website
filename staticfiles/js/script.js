$(document).ready(function () {
    $('#activeCheckbox').change(function () {
        $('#filterForm').submit(); // Submit form on checkbox change
    });
});