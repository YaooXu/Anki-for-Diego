$(init);

function init() {
    $('#add_from_text_bt').click(function () {
        var $textArea = $('#words-area'),
            words = $textArea.val();
        var cmd = 'add_from_text' + ':' + words;
        return pycmd(cmd)
    });

    $('#add_from_file_bt').click(function () {
        return pycmd('add_form_file')
    });
}