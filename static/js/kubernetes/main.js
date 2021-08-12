$('.desc-pods').click(function(){
    let podname;
    let clustername;
    let namespace;
    podname = $(this).attr("data-podname");
    clustername = $(this).attr("data-clustername");
    namespace = $(this).attr("data-namespace");
    $.ajax(
    {
        type:"GET",
        url: "/kubernetes/describe/" + clustername + "/" + namespace + "/"+ podname + "/",
        data:{},
        success: function( data ) 
        {
            console.log(data);
        }
     })
});