/*************************************************************************/
//Javascript code for Naive Bayes gender prediction project.
//11 May 2015
//By Natalia Chetelat


//Grays out button whose function is to load the Naive Bayes model
function grayLoadNB(){
    $("#load_model").attr("disabled", "disabled")
}

//Activates (de-grays out) button whose function is to predict gender.
//This button is grayed out when page is first loaded, as prediction
//cannot happen until model is loaded.
function activatePredict(){
    $("#predict").removeAttr("disabled")
}

//Writes a message to the screen saying the model is loading when 
//the "load NB model" button is pressed.
function loadingMessage(){
    $("#loading").html("The model is loading...")
}

//Errases loading message from screen as soon as model is loaded onto memory.
function noLoadingMessage(){
    $("#loading").html("")
}


//Function that sends AJAX post request from pressing "Load NB Model" button.
//It sends a flag's setting as data and, if successful, grays out this
//button and activates the "guess gender" button.
$(document).ready(function(){
    $("#load_model").click(function(){
        loadingMessage();
        $.post("/loadnb",
        function(data){
            console.log(data); //Boolean, should be true. For debugging purposes
            noLoadingMessage();
            grayLoadNB();
            activatePredict();
        });
    return false});
});


//Function that sends AJAX post request from pressing "Guess Gender" button.
//It sends user's raw text as data and, if successful, prints the
//predicted gender of the text's author to the screen.
$(document).ready(function(){
    $("#predict").click(function(){
        $.post("/", {raw_text: $("#raw_text").val()},   
        function(data){
            console.log(data) //For debugging purposes
            var jsonObj = $.parseJSON(data);
            $("#gender").html(jsonObj[0].gender);
            $("#prob").html(jsonObj[0].prob + "%");
            });
        return false});
    });

