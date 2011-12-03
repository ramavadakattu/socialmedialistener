$(document).ready(function() {    
  
   

   window.setInterval('fetchData()',5000);
    
    
    
    
 });


function fetchData()
{
    
   
    
   serverurl ="/ebaylistener/totalshares/"
   //Get the answer
   $.get(serverurl,
            {},
            afterSubmit,
            "json"
           );

}


function afterSubmit(data)
{
    if (data['error_message'] === undefined) 
           {
            
            
            previouscount =  $('#sharecountspan').html();
            intpreviouscount = parseInt(previouscount)
            currentcount =  data['totalentries']
            

        if (currentcount > intpreviouscount )
           {
            
              $('#sharecountspan').html(data['totalentries']);
              $('#sharecountbox').animate({backgroundColor : "#FFFF00"}, 600);
               $('#sharecountbox').animate({backgroundColor : "#FFFACD"}, 600);
                $('#sharecountbox').animate({backgroundColor : "#FFFFFF"}, 600);
                
           }
                
                
                
              
              
              }
            
    
}