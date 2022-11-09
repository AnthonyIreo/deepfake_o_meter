document.getElementById("accept").onclick = function() { 
    // waiting page after clicking the submit
    // content = "<div class='preloader'><img src='{{ url_for('static', filename='images/favicon.png') }}'><h3>please wait...</h3></div>";
    // document.getElementById('submit_preloader').innerHTML = content;
  
    // react
    function Preload(){
        return (
            <div class="preloader">
                <div class="sk-spinner sk-spinner-rotating-plane"></div>
                <br/>
                <br/>
                <h2>Please wait...</h2>
            </div>
        );
    }

    // reactDOM
    ReactDOM.render(<Preload />, submit_preloader);

}
