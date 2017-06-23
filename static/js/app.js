/**
 * Created by Kevin on 2017-06-12.
 */


/**
 * Showing multi/single layer options depending on checkbox click
 */
$('#multi-layer-checkbox').change(function () {
    if (this.checked) {
        $('#multi-layer-options').show();
        $('#single-layer-options').hide();
    } else {
        $('#multi-layer-options').hide();
        $('#single-layer-options').show();
    }
});

/**
 * Checking sure we have an image uploaded and show overlay
 */

$('#heatmap-generate-form').on('submit', function (e) {

    has_demo_img_selected = $('#demo-img-checkboxes').find('input[type=checkbox]:checked').length;
    has_uploaded_img = $('#upload-file').val();

    if (has_demo_img_selected || has_uploaded_img) {
        $('#no-image-selected-alert').hide();
        $('#overlay').css('visibility', 'visible');
        $('body').css('overflow', 'hidden');
    } else {
        e.preventDefault(e);
        $('#no-image-selected-alert').fadeIn();
    }
});
