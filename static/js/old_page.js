// $(".dropdown dt .mydropdown").on('click', function() {
//     $(".dropdown dd ul").slideToggle('fast');
// });
//
// $(".dropdown dd ul li a").on('click', function() {
//     $(".dropdown dd ul").hide();
// });
//

document.onreadystatechange = function() {
    if (document.readyState !== "complete") {
        document.querySelector("body").style.visibility = "hidden";
        document.querySelector("#change_background").style.visibility = "visible";
    } else {
        document.querySelector("#change_background").style.display = "none";
        document.querySelector("body").style.visibility = "visible";
    }
};
//
function getSelectedValue(id) {
    return $("#" + id).find("dt a span.value").html();
}
//
// $(document).bind('click', function(e) {
//     var $clicked = $(e.target);
//     if (!$clicked.parents().hasClass("dropdown")) $(".dropdown dd ul").hide();
// });
//
$('.mutliSelect input[type="checkbox"]').on('click', function() {
    var title = $(this).closest('.mutliSelect').find('input[type="checkbox"]').val(),
        title = $(this).val() + ",";
    if ($(this).is(':checked')) {
        var html = '<span title="' + title + '">' + title + '</span>';
        $('.multiSel').append(html);}
    else {
        $('span[title="' + title + '"]').remove();}
});
//
function disable()
{
    document.getElementById("accept").disabled=true;
    document.getElementById("status").disabled=true;
}
function enable()
{
    document.getElementById("accept").disabled=false;
    document.getElementById("status").disabled=false;
}