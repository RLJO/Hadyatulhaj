// Capture the form submit button$("#end_date_leave").change(function(){
 var errmsg = $('#error_msg');
 var end=new Date($(this).val());
 var start= new Date($("#start_date_leave").val());
 console.log(start);
 console.log(end);
 var noDays= $("#number_of_days_leave");
 var dif = (end.getTime()-start.getTime())/(1000 * 60 * 60 * 24);
console.log(end.getTime());
  console.log(start.getTime());

 noDays.val(dif);
 console.log(dif);
});