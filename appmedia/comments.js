$(document).ready(function() {
     
     
     //Recaptcha.create("6LcrkQcAAAAAAF8BYL9QKiTO0x1Z-h0MIAQMRsSS", "recaptcha_div", {
     //       theme: "clean"       });

     
     
     
     $(':input:visible:enabled:first','#commentbox').focus();
     
     //intialize the form to go via ajax
      $('#commentform').ajaxForm({        
                    // dataType identifies the expected content type of the server response 
                    dataType:  'json',       
                    // success identifies the function to invoke when the server response 
                    // has been received
                     beforeSubmit:  handleSubmit , 
                    success: commentSubmission });
     
     
   
 });



function handleSubmit()
{
    //get the comment text
    var text = $("textarea[name=comment]").val();   
  
    //look for errors  
    if ($.trim(text).length  <= 0)
    {
        window.alert("Please enter the comment");
        return false;
    }
    
    //get the name
    var input_object = $("input[name=name123]");
    //username field is present
    if (input_object.length > 0) {        
            //look for errors  
            if ($.trim(input_object.val()).length  <= 0)
            {
                window.alert("Please enter the user name");
                return false;
            }    
    }
    
    
    //remove any previous errors which are beofre submit button
    if ($("#commenterror").length  > 0)
    {
        $("#commenterror").remove()
    }
    
    
    
    $("#submitbutton").before("<span id='ajaximage'> <img  src='/appmedia/topicmemes/images/ajax2.gif' alt='ajax image'/> &nbsp; Submitting........... &nbsp; </span>"); 
    $("#submitbutton").attr("disabled", "true");
    $("#submitbutton").removeAttr('disabled')
    
    return true;
}


function commentSubmission(data)
{    
        
    if (data['error_message'] === undefined) 
           {
             $("#ajaximage").remove();
             //add the text and content
             text = data['comment'];
             $('ul.commentlist').append(" <li> "+text+"</li>");
             $("#submitbutton").removeAttr('disabled')
             //clear form
             $('#commentform').clearForm();                                
           }
       else
       {
        $("#ajaximage").remove();
        $("#submitbutton").before("<span id='commenterror' class='red'>"+data['error_message']+" &nbsp; </span>"); 
        
       }
}
