$(document).ready(function () {
    $('#activeCheckbox').change(function () {
        $('#filterForm').submit(); // Submit form on checkbox change
    });
});
$(document).ready(function () {
    $('#mobActiveCheckbox').change(function () {
        $('#mobFilterForm').submit(); // Submit form on checkbox change
    });
});