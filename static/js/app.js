/**
 * Created by Kevin on 2017-06-12.
 */

$('#generate-heatmap-btn').on('click', function () {
    $('#overlay').css('visibility', 'visible');
    $('body').css('overflow', 'hidden');
});

$('#multi-layer-checkbox').change(function () {
    if (this.checked) {
        $('#multi-layer-options').show();
        $('#single-layer-options').hide();
    } else {
        $('#multi-layer-options').hide();
        $('#single-layer-options').show();
    }
});