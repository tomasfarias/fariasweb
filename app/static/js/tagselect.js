$(document).ready(function() {
    $('#tags').select2({
        allowClear:true,
        placeholder: 'Tag post...',
        tags: true,
        tokenSeparators: [',', ' ']
    });
});