// Capture the form submit button
$("#submit_button_id").click(function(event){
  event.preventDefault();
  // Get form data
  var form_data = $("#contactForm1").serialize();
  var errmsg = $('#error_msg');
   var form = this.form;
        // prepare data
        var mydata = new FormData(form);
  var post_url = window.location.href;
  console.log(form_data);
  console.log(post_url);
  // Sending a POST request to Moyasar API using AJAX
  $.ajax({
  url: post_url,

  type: "post",
  data: mydata,
              processData: false,
              contentType: false,

//  dataType: "json",
})
// uses `.done` callback to handle a successful AJAX request
.done(function(data) {
// Here we will handle JSON response and do step3 & step4
var payment_id = data.id;
// Redirect the user to transaction_url
var str=$("#course_type").val;
 console.log(str);
if (['internal', 'external'].indexOf(str) >= 0)
 {
// errmsg.text('Your Request has been Sent Successfully');
 alert('Your Request has been Sent Successfully');
}
else
    {
//    errmsg.text('تم ارسال طلبكم بنجاح');
    alert('تم ارسال طلبكم بنجاح');
    }
})
.fail(function (data) {
                    console.log('An error occurred.');
                console.log(data);
                errmsg.text(' Wrong With your Request ');
                });
});

$("#add_custody_button").click(function(event){
   event.preventDefault();
   var form_data = $("#FormCustodyLine").serialize();
   var form = this.form;
   var my_data = new FormData(form);
  var post_url = window.location.href;
  $.ajax({
  url: post_url,
  type: "post",
  data: my_data,
  processData: false,
  contentType: false,
})
.done(function(data) {
var amount = document.getElementById("amount").value;
var remain_amount = document.getElementById("remain_amount").value;
//var custody_attachment = document.getElementById("custody_attachment").value;
//console.log(">>>>>>>>>>>>::::::::::::"+custody_attachment)
//if(typeof custody_attachment == 'undefined' || custody_attachment == null || custody_attachment == '') {
//alert('من فضلك ارفق الملفات');
//}
if (amount > remain_amount){
    alert(' المبلغ يجب ان يكون اقل من او يساوي'+' '+remain_amount);
}
else{
    var payment_id = data.id;
    alert('تم ارسال طلبكم بنجاح');
    parent.window.location.href='my/custody/in_progress'
    }
})
});

$("#course_type").change(function(){
 var errmsg = $('#error_msg');
   if($(this).val()=="private" || $(this).val()==  "خاصة")
   {
       $("div#start_date").show();
       $("div#end_date").show();
         errmsg.text('');

   }
    else
    {
     errmsg.text('');
        $("div#start_date").hide();
        $("div#end_date").hide();

    }
});

$("#end_date_private").change(function(){
 var errmsg = $('#error_msg');
 var end=new Date($(this).val());
 var start= new Date($("#start_date_private").val());
 console.log(start);
 console.log(end);
 var noDays= $("#number_of_days");
 var dif = (end.getTime()-start.getTime())/(1000 * 60 * 60 * 24);
console.log(end.getTime());
  console.log(start.getTime());

 noDays.val(dif);
 console.log(dif);
});
