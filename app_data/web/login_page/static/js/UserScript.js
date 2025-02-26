

    //https://www.freecodecamp.org/news/how-to-send-http-requests-using-javascript/
    async function Send_Data_(data, url) {
        try {
            const response = await fetch(url, {
                method: "POST",
                body: data,
                headers: {
                    "Content-Type": "application/json; charset=UTF-8",  //Ensures JSON encoding
                },
            });
    
            if (!response.ok) {
                throw new Error(`Network error: ${response.status} - ${response.statusText}`);
            }
    
            // Ensure the response is JSON
            const responseData = await response.json().catch(() => null);
            if (!responseData) throw new Error("Invalid JSON response from server");
    
            return responseData;
    
        } catch (error) {

            return null;  // Always return null instead of crashing
        }
    }
    

    


    async function GetURL(saved_url){
        Start_Loading_js();
        let endpoint = `${window.location.origin}/api/ScanURL/`; //Api endpoint
       
        let message_body = JSON.stringify({ url: saved_url }); 
        
        const response = await Send_Data_(message_body, endpoint);

        //!change response to the correct variable name
        if (response && response.result) {  
            document.getElementById("Resualt-par").innerHTML = "";//clear the previous result
            document.getElementById("Resualt-par").innerHTML = saved_url + "<br>" + "URLScan Malicious: " + response.result.urlscan + "<br>" + "VirusTotal Safe: " + response.result.virustotal;
            Stop_Loading_js();

        } else {
            console.error("Error:", response.Error);
            //console.error("Failed to retrieve 2FA key.");
            Stop_Loading_js();
        }
    }
    
    
    


let Loading_parameter = undefined;

function Start_Loading_js() {
    Loading_parameter = Metro.activity.open({
        type: 'square',
        overlayColor: '#fff',
        overlayAlpha: 1,
        text: '<div class="loader"></div>', // Injects custom CSS loader
    });
}

function Stop_Loading_js() {
    Metro.activity.close(Loading_parameter);
}


                    /* HTML: <div class="loader"></div> */
