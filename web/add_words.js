$(init);

function init() {
    $('#add_from_text_bt').click(function () {
        var $textArea = $('#words-area'),
            words = $textArea.val();
        var cmd = 'add_from_text' + ':' + words;
        return pycmd(cmd)
    });

    $('#add_from_file_bt').click(function () {
        return pycmd('add_from_file')
    });

    $('#import_model').click(function () {
        return pycmd('import_model')
    });

    $('#smart_add').click(function () {
        return pycmd('smart_add')
    });

    $('#choose_model').change(function () {
        return pycmd('change_model:' + $(this).val())
    });
}